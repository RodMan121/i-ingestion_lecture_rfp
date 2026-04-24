import os
import json
import httpx
import time
import hashlib
from pathlib import Path
from datetime import datetime
import sys

# Configuration par variables d'environnement (Standards GenAI)
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")
MAX_CHARS_PER_CHUNK = int(os.getenv("BATCH_MAX_CHARS", "30000"))

def compute_file_hash(path: Path) -> str:
    """Calcul l'empreinte pour la traçabilité des données"""
    if not path.exists(): return "absent"
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def print_progress(current, total, prefix='Extraction IA', length=30):
    """Barre de progression console déterministe"""
    percent = ("{0:.1f}").format(100 * (current / float(total)))
    filled_length = int(length * current // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% ({current}/{total})')
    sys.stdout.flush()
    if current == total: print()

def load_all_data(doc_dir: Path):
    """Charge et sécurise les sources d'artefacts"""
    md_file = doc_dir / "rfp-structured.md"
    if not md_file.exists():
        print(f"  ⚠️  ATTENTION : Fichier source absent : {md_file}")
        text_content = ""
    else:
        text_content = md_file.read_text(encoding='utf-8')

    # Chargement déterministe des tables CSV
    tables = []
    tab_dir = doc_dir / "tables"
    if tab_dir.exists():
        for csv_file in sorted(tab_dir.glob("*.csv")):
            tables.append(f"--- TABLEAU: {csv_file.name} ---\n{csv_file.read_text(encoding='utf-8')}")
    
    return text_content, "\n\n".join(tables)

def call_ollama_safe(system_prompt, user_content):
    """Appel robuste à Ollama avec validation JSON et retry policy"""
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
            
            # Validation structurelle de la réponse
            raw_text = resp.json().get("message", {}).get("content", "{}")
            return json.loads(raw_text)
            
        except (json.JSONDecodeError, httpx.HTTPError) as e:
            print(f"\n  ❌ Erreur de réponse (Modèle ou Réseau) : {e}")
            return None

def extract_multimodal(doc_dir_str, prompt_path_str, output_json_str):
    doc_dir = Path(doc_dir_str)
    prompt_path = Path(prompt_path_str)
    output_path = Path(output_json_str)
    
    print(f"🚀 Extraction Multimodale (Production Grade)")
    print(f"  → Modèle : {OLLAMA_MODEL}")
    
    text, tables = load_all_data(doc_dir)
    prompt_template = prompt_path.read_text(encoding='utf-8')
    
    # Stratégie de Batching par découpage de caractères
    chunks = [text[i:i+MAX_CHARS_PER_CHUNK] for i in range(0, len(text), MAX_CHARS_PER_CHUNK)]
    if not chunks: chunks = [""]
    
    all_requirements = []
    all_contradictions = []
    total_chunks = len(chunks)
    start_time = time.time()
    
    for i, chunk_text in enumerate(chunks):
        print_progress(i, total_chunks)
        
        # Fusion des sources pour le contexte du bloc
        user_input = f"{chunk_text}\n\n{tables}"
        
        res = call_ollama_safe(prompt_template, user_input)
        if res:
            all_requirements.extend(res.get("exigences", []))
            all_contradictions.extend(res.get("contradictions_md_vs_csv", []))
        
        print_progress(i+1, total_chunks)

    # Paquet final avec Métadonnées de traçabilité
    final_package = {
        "meta": {
            "version": "2.1.0",
            "timestamp": datetime.now().isoformat(),
            "model": OLLAMA_MODEL,
            "source_dir": str(doc_dir.absolute()),
            "source_hash": compute_file_hash(doc_dir / "rfp-structured.md"),
            "prompt_hash": compute_file_hash(prompt_path),
            "batch_chunks": total_chunks
        },
        "extraction": {
            "exigences": all_requirements,
            "contradictions": all_contradictions
        }
    }
    
    # Écriture propre et sécurisée
    output_path.write_text(json.dumps(final_package, ensure_ascii=False, indent=2), encoding='utf-8')
    
    duration = int(time.time() - start_time)
    print(f"✨ Extraction terminée en {duration}s. Fichier : {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python extract-multimodal.py <doc_dir> <prompt_path> <output_json>")
        sys.exit(1)
    extract_multimodal(sys.argv[1], sys.argv[2], sys.argv[3])
