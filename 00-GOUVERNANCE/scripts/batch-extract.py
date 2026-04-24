import json
from pathlib import Path
import sys
import httpx

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:7b"
CHUNK_SIZE = 400  # Nombre de lignes par bloc

def extract_chunk(text, prompt_template):
    """Extrait les exigences pour un bloc spécifique"""
    payload = {
        "model": MODEL_NAME,
        "prompt": f"{prompt_template}\n\n{text}",
        "stream": False,
        "format": "json"
    }
    try:
        response = httpx.post(OLLAMA_URL, json=payload, timeout=600)
        response.raise_for_status()
        return json.loads(response.json().get("response", "{}"))
    except Exception as e:
        print(f"  ⚠️ Erreur sur un bloc : {e}")
        return None

def batch_process(md_path, prompt_path, output_json):
    """Orchestre le découpage et la fusion"""
    print(f"🚀 Lancement du Batch Processing : {md_path}")
    
    md_lines = Path(md_path).read_text(encoding='utf-8').splitlines()
    prompt_template = Path(prompt_path).read_text(encoding='utf-8')
    
    total_chunks = (len(md_lines) // CHUNK_SIZE) + 1
    all_results = {
        "exigences": [],
        "exigences_critiques": [],
        "contradictions": [],
        "exigences_implicites_suggerees": []
    }

    for i in range(total_chunks):
        start = i * CHUNK_SIZE
        end = start + CHUNK_SIZE
        chunk_text = "\n".join(md_lines[start:end])
        
        if not chunk_text.strip():
            continue
            
        print(f"  → Traitement bloc {i+1}/{total_chunks}...")
        res = extract_chunk(chunk_text, prompt_template)
        
        if res:
            all_results["exigences"].extend(res.get("exigences", []))
            all_results["exigences_critiques"].extend(res.get("exigences_critiques", []))
            all_results["contradictions"].extend(res.get("contradictions", []))
            all_results["exigences_implicites_suggerees"].extend(res.get("exigences_implicites_suggerees", []))

    # Sauvegarde finale
    Path(output_json).write_text(json.dumps(all_results, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"✅ Batch terminé. {len(all_results['exigences'])} exigences extraites au total.")
    print(f"💾 Résultat sauvegardé dans : {output_json}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python batch-extract.py <md_in> <prompt_in> <json_out>")
        sys.exit(1)
    batch_process(sys.argv[1], sys.argv[2], sys.argv[3])
