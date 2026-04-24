import json
from pathlib import Path
from datetime import date
import sys

def json_to_requirements(json_path: str, output_path: str, client: str, objet: str):
    """
    Transforme le JSON produit par le LLM (Format v2.1.0) en REQUIREMENTS.md
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            full_data = json.load(f)
            # Support du nouveau format avec 'meta' et 'extraction'
            data = full_data.get("extraction", full_data)
            meta = full_data.get("meta", {})
    except Exception as e:
        print(f"❌ Erreur lecture JSON : {e}")
        return

    lines = []
    lines.append(f"# REQUIREMENTS — {client} — {objet} — v1.0\n\n")
    lines.append(f"## Métadonnées d'extraction IA\n")
    lines.append(f"- Date traitement : {meta.get('timestamp', date.today())}\n")
    lines.append(f"- Modèle utilisé : {meta.get('model', 'Inconnu')}\n")
    lines.append(f"- Statut global : EXT (Extrait)\n")
    lines.append(f"- Source Hash : `{meta.get('source_hash', 'N/A')}`\n\n")
    
    lines.append("## Référentiel des exigences\n\n")
    lines.append("| Ref | Intitulé | Type | BDAT | Prio | Statut | Origine | Flag |\n")
    lines.append("|-----|----------|------|------|------|--------|---------|------|\n")
    
    flag_emoji = {
        "BLOQUANT": "🔴",
        "ATTENTION": "🟡", 
        "STANDARD": "⚪"
    }
    
    for ex in data.get("exigences", []):
        flag = flag_emoji.get(ex.get("flag", "STANDARD"), "⚪")
        lines.append(
            f"| {ex.get('ref', 'N/A')} | {ex.get('intitule', 'N/A')} | "
            f"{ex.get('type', 'N/A')} | {ex.get('bdat', 'N/A')} | {ex.get('priorite', 'N/A')} | "
            f"EXT | {ex.get('source_origine', 'N/A')} | {flag} |\n"
        )
    
    if data.get("contradictions"):
        lines.append("\n## Contradictions / Ambiguïtés détectées\n\n")
        for c in data["contradictions"]:
            # Gestion du cas où 'refs' est une liste ou une string
            refs = c.get("refs", [])
            ref_str = " vs ".join(refs) if isinstance(refs, list) else str(refs)
            lines.append(f"- **{ref_str}** : {c.get('description', 'Conflit non décrit')}\n")
    
    Path(output_path).write_text("".join(lines), encoding="utf-8")
    print(f"✅ REQUIREMENTS.md généré avec succès : {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python json-to-requirements.py <json_in> <md_out> <client> <objet>")
    else:
        json_to_requirements(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
