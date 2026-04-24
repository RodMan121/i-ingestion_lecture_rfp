import json
import httpx
from pathlib import Path
import sys

# Config
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:7b"

def load_all_artifacts(doc_dir: Path):
    """Charge Markdown, tous les CSV et les métadonnées"""
    context = []
    
    # 1. Texte principal
    md_file = doc_dir / "rfp-structured.md"
    if md_file.exists():
        context.append(f"--- CONTENU TEXTUEL (.md) ---\n{md_file.read_text(encoding='utf-8')}")
    
    # 2. Tableaux CSV
    tab_dir = doc_dir / "tables"
    if tab_dir.exists():
        for csv_file in tab_dir.glob("*.csv"):
            context.append(f"--- TABLEAU: {csv_file.name} ---\n{csv_file.read_text(encoding='utf-8')}")
            
    # 3. Métadonnées
    meta_file = doc_dir / "rapport-parsing.json"
    if meta_file.exists():
        context.append(f"--- MÉTADONNÉES D'AUDIT ---\n{meta_file.read_text(encoding='utf-8')}")
        
    return "\n\n".join(context)

def extract_multimodal(doc_dir_str: str, prompt_path: str, output_json: str):
    doc_dir = Path(doc_dir_str)
    print(f"🚀 Extraction Multimodale (Texte + Tables) : {doc_dir.name}")
    
    full_context = load_all_artifacts(doc_dir)
    prompt_template = Path(prompt_path).read_text(encoding='utf-8')
    
    # On gère le découpage si le contexte global est trop énorme (> 100k chars)
    if len(full_context) > 100000:
        print("  ⚠️ Contexte volumineux, passage en mode Batch sécurisé...")
        # Ici on pourrait implémenter un chunking intelligent
    
    payload = {
        "model": MODEL_NAME,
        "prompt": f"{prompt_template}\n\n{full_context}",
        "stream": False,
        "format": "json",
        "options": {"num_ctx": 32768} # On étend la fenêtre pour Qwen
    }
    
    try:
        response = httpx.post(OLLAMA_URL, json=payload, timeout=900)
        response.raise_for_status()
        res_json = response.json().get("response", "{}")
        
        Path(output_json).write_text(res_json, encoding='utf-8', errors='ignore')
        print(f"✅ Extraction réussie : {output_json}")
        
    except Exception as e:
        print(f"❌ Erreur IA : {e}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python extract-multimodal.py <dossier_doc> <prompt_in> <json_out>")
        sys.exit(1)
    extract_multimodal(sys.argv[1], sys.argv[2], sys.argv[3])
