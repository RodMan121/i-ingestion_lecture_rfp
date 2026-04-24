import os
import json
import httpx
import time
import hashlib
from pathlib import Path
from datetime import datetime
import sys

# Configuration
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")
MAX_CHARS_PER_CHUNK = int(os.getenv("BATCH_MAX_CHARS", "30000"))

def compute_global_hash(doc_dir: Path) -> str:
    """Hash combiné de tous les artefacts pour une traçabilité sans faille"""
    sha256 = hashlib.sha256()
    # On prend le MD et tous les CSV du dossier tables
    files = sorted(list(doc_dir.glob("*.md")) + list(doc_dir.glob("tables/*.csv")))
    for path in files:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
    return sha256.hexdigest()

def print_progress(current, total, prefix='Extraction IA', length=30):
    percent = ("{0:.1f}").format(100 * (current / float(total)))
    filled_length = int(length * current // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% ({current}/{total})')
    sys.stdout.flush()
    if current == total: print()

def load_data(doc_dir: Path):
    md_file = doc_dir / "rfp-structured.md"
    text = md_file.read_text(encoding='utf-8') if md_file.exists() else ""
    
    tables = []
    tab_dir = doc_dir / "tables"
    if tab_dir.exists():
        for csv in sorted(tab_dir.glob("*.csv")):
            tables.append(f"--- TABLEAU CSV: {csv.name} ---\n{csv.read_text(encoding='utf-8')}")
    
    return text, "\n\n".join(tables)

def call_ollama(system_prompt, user_content):
    transport = httpx.HTTPTransport(retries=3)
    with httpx.Client(transport=transport, timeout=900) as client:
        payload = {
            "model": OLLAMA_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "stream": False,
            "format": "json",
            "options": {"num_ctx": 32768}
        }
        try:
            resp = client.post(OLLAMA_URL, json=payload)
            resp.raise_for_status()
            raw = resp.json().get("message", {}).get("content", "{}")
            return json.loads(raw)
        except Exception as e:
            print(f"\n❌ Erreur bloc : {e}")
            return None

def extract_multimodal(doc_dir_str, prompt_path_str, output_json_str):
    doc_dir = Path(doc_dir_str)
    prompt_path = Path(prompt_path_str)
    output_path = Path(output_json_str)
    
    text, tables = load_data(doc_dir)
    prompt_base = prompt_path.read_text(encoding='utf-8')
    
    # P1 : On injecte les tables dans le CONTEXTE SYSTÈME (permanent)
    system_prompt = f"{prompt_base}\n\nVOICI LES TABLEAUX CONTRACTUELS DE RÉFÉRENCE :\n{tables}"
    
    chunks = [text[i:i+MAX_CHARS_PER_CHUNK] for i in range(0, len(text), MAX_CHARS_PER_CHUNK)]
    if not chunks: chunks = [""]
    
    req_map = {}
    all_contradictions = []
    critical_refs = set()
    total = len(chunks)
    start_time = time.time()
    
    for i, chunk in enumerate(chunks):
        if not chunk.strip() and total > 1: continue # P2 : Skip empty
        
        print_progress(i, total)
        res = call_ollama(system_prompt, f"FLUX TEXTUEL À ANALYSER :\n{chunk}")
        
        if res:
            # Dédoublonnage et fusion par Ref
            for ex in res.get("exigences", []):
                ref = ex.get("ref", f"NEW-{time.time()}")
                req_map[ref] = ex
            
            # P0 : Collecte des critiques et contradictions
            all_contradictions.extend(res.get("contradictions_md_vs_csv", []))
            critical_refs.update(res.get("exigences_critiques", []))
            
        print_progress(i+1, total)

    final = {
        "meta": {
            "version": "2.3.0",
            "timestamp": datetime.now().isoformat(),
            "model": OLLAMA_MODEL,
            "source_hash": compute_global_hash(doc_dir), # Hash complet
            "batch_chunks": total
        },
        "extraction": {
            "exigences": list(req_map.values()),
            "exigences_critiques": list(critical_refs),
            "contradictions": all_contradictions
        }
    }
    
    output_path.write_text(json.dumps(final, ensure_ascii=False, indent=2), encoding='utf-8')
    duration = int(time.time() - start_time)
    print(f"✨ Terminé en {duration}s. {len(req_map)} exigences uniques certifiées.")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python extract-multimodal.py <dir> <prompt> <out>")
        sys.exit(1)
    extract_multimodal(sys.argv[1], sys.argv[2], sys.argv[3])
