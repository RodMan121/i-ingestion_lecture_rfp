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
MAX_CHARS_PER_CHUNK = int(os.getenv("BATCH_MAX_CHARS", "25000")) # Réduit pour laisser place aux tables

def compute_global_hash(doc_dir: Path) -> str:
    """Hash combiné de tous les artefacts (MD + CSV) pour traçabilité totale"""
    sha256 = hashlib.sha256()
    files = sorted(list(doc_dir.glob("rfp-structured.md")) + list(doc_dir.glob("tables/*.csv")))
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

def load_all_data(doc_dir: Path):
    md_file = doc_dir / "rfp-structured.md"
    text_content = md_file.read_text(encoding='utf-8') if md_file.exists() else ""
    
    tables = []
    tab_dir = doc_dir / "tables"
    if tab_dir.exists():
        for csv_file in sorted(tab_dir.glob("*.csv")):
            tables.append(f"--- TABLEAU: {csv_file.name} ---\n{csv_file.read_text(encoding='utf-8')}")
    
    return text_content, "\n\n".join(tables)

def call_ollama_safe(system_prompt, user_content):
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
            raw_text = resp.json().get("message", {}).get("content", "{}")
            return json.loads(raw_text)
        except Exception as e:
            print(f"\n  ❌ Erreur critique bloc : {e}")
            return None

def extract_multimodal(doc_dir_str, prompt_path_str, output_json_str):
    doc_dir = Path(doc_dir_str)
    prompt_path = Path(prompt_path_str)
    output_path = Path(output_json_str)
    
    if not doc_dir.exists():
        print(f"❌ Dossier introuvable : {doc_dir}")
        return

    text, tables = load_all_data(doc_dir)
    if not text and not tables:
        print("❌ Aucune donnée à traiter (MD et CSV vides).")
        return

    prompt_template = prompt_path.read_text(encoding='utf-8')
    chunks = [text[i:i+MAX_CHARS_PER_CHUNK] for i in range(0, len(text), MAX_CHARS_PER_CHUNK)]
    if not chunks: chunks = [""]
    
    # Stockage avec dédoublonnage par Ref
    requirements_map = {} 
    contradictions = []
    critical_refs = set()
    
    total_chunks = len(chunks)
    start_time = time.time()
    
    for i, chunk_text in enumerate(chunks):
        print_progress(i, total_chunks)
        user_input = f"{chunk_text}\n\n{tables}"
        
        res = call_ollama_safe(prompt_template, user_input)
        if res:
            # Fusion intelligente : la dernière extraction d'une Ref écrase la précédente (souvent plus complète)
            for ex in res.get("exigences", []):
                ref = ex.get("ref", f"UNKNOWN-{time.time()}")
                requirements_map[ref] = ex
            
            contradictions.extend(res.get("contradictions_md_vs_csv", []))
            critical_refs.update(res.get("exigences_critiques", []))
        
        print_progress(i+1, total_chunks)

    final_package = {
        "meta": {
            "version": "2.2.0",
            "timestamp": datetime.now().isoformat(),
            "model": OLLAMA_MODEL,
            "source_hash": compute_global_hash(doc_dir),
            "batch_chunks": total_chunks
        },
        "extraction": {
            "exigences": list(requirements_map.values()),
            "exigences_critiques": list(critical_refs),
            "contradictions": contradictions
        }
    }
    
    output_path.write_text(json.dumps(final_package, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"✨ Extraction terminée. {len(requirements_map)} exigences uniques trouvées.")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python extract-multimodal.py <doc_dir> <prompt_path> <output_json>")
        sys.exit(1)
    extract_multimodal(sys.argv[1], sys.argv[2], sys.argv[3])
