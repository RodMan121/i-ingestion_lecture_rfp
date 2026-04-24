import httpx
import json
from pathlib import Path
import sys

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:7b" # Passage au modèle de production 7B

def extract_with_ollama(md_path: str, prompt_path: str, output_json: str):
    """
    Appelle Ollama pour extraire les exigences
    """
    print(f"🚀 Lancement de l'extraction IA (Modèle: {MODEL_NAME})...")
    
    md_content = Path(md_path).read_text(encoding='utf-8')
    prompt_template = Path(prompt_path).read_text(encoding='utf-8')
    
    full_prompt = f"{prompt_template}\n\n{md_content}"
    
    payload = {
        "model": MODEL_NAME,
        "prompt": full_prompt,
        "stream": False,
        "format": "json"
    }
    
    try:
        response = httpx.post(OLLAMA_URL, json=payload, timeout=600)
        response.raise_for_status()
        
        result = response.json()
        raw_response = result.get("response", "{}")
        
        # Sauvegarde du JSON brut
        Path(output_json).write_text(raw_response, encoding='utf-8')
        print(f"✅ JSON extrait sauvegardé : {output_json}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'appel à Ollama : {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python extract-requirements.py <md_in> <prompt_in> <json_out>")
        sys.exit(1)
    
    extract_with_ollama(sys.argv[1], sys.argv[2], sys.argv[3])
