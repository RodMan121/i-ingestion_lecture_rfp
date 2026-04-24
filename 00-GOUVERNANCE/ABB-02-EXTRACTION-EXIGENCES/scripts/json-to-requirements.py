import json
from pathlib import Path
from datetime import datetime
import sys

def safe_markdown(text):
    """Échappe les caractères brisant les tableaux Markdown (|)"""
    if not text: return "N/A"
    return str(text).replace("|", "/").replace("\n", " ").strip()

def json_to_requirements(json_path: str, output_path: str, client: str, objet: str):
    """
    Transforme le JSON robuste (Format v2.3.0) en REQUIREMENTS.md
    Supporte les exigences critiques sous forme de liste de strings.
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            full_data = json.load(f)
            data = full_data.get("extraction", {})
            meta = full_data.get("meta", {})
    except Exception as e:
        print(f"❌ Erreur lecture JSON : {e}")
        return

    lines = []
    lines.append(f"# REQUIREMENTS — {safe_markdown(client)} — {safe_markdown(objet)} — v1.0\n\n")
    lines.append(f"## Métadonnées d'extraction IA\n")
    lines.append(f"- Date traitement : {meta.get('timestamp', 'N/A')}\n")
    lines.append(f"- Modèle utilisé : {meta.get('model', 'Inconnu')}\n")
    lines.append(f"- Statut global : EXT (Extrait)\n")
    lines.append(f"- Source Hash Global : `{meta.get('source_hash', 'N/A')}`\n\n")
    
    exigences = data.get("exigences", [])
    critiques = data.get("exigences_critiques", []) # Liste de strings (Refs)

    lines.append(f"**Indicateurs :** {len(exigences)} exigences détectées, dont {len(critiques)} signalées comme critiques 🔥.\n\n")

    lines.append("## Référentiel des exigences\n\n")
    lines.append("| Ref | Intitulé | Type | BDAT | Prio | Statut | Origine | Flag |\n")
    lines.append("|-----|----------|------|------|------|--------|---------|------|\n")
    
    flag_emoji = {
        "BLOQUANT": "🔴",
        "ATTENTION": "🟡", 
        "STANDARD": "⚪"
    }
    
    # Tri alphabétique par Ref pour la lisibilité
    sorted_ex = sorted(exigences, key=lambda x: str(x.get("ref", "")))

    for ex in sorted_ex:
        ref = str(ex.get('ref', 'N/A'))
        display_ref = safe_markdown(ref)
        
        # Ajout du badge critique si la Ref est dans la liste
        if ref in critiques:
            display_ref = f"**{display_ref}** 🔥"
            
        flag = flag_emoji.get(ex.get("flag", "STANDARD"), "⚪")
        
        lines.append(
            f"| {display_ref} | {safe_markdown(ex.get('intitule'))} | "
            f"{safe_markdown(ex.get('type'))} | {safe_markdown(ex.get('bdat'))} | "
            f"{safe_markdown(ex.get('priorite'))} | EXT | "
            f"{safe_markdown(ex.get('source_origine'))} | {flag} |\n"
        )
    
    if data.get("contradictions"):
        lines.append("\n## Contradictions / Ambiguïtés détectées\n\n")
        for c in data["contradictions"]:
            refs = c.get("refs", [])
            ref_str = " vs ".join(refs) if isinstance(refs, list) else str(refs)
            lines.append(f"- **{safe_markdown(ref_str)}** : {safe_markdown(c.get('description'))}\n")
    
    Path(output_path).write_text("".join(lines), encoding="utf-8")
    print(f"✅ REQUIREMENTS.md généré : {len(exigences)} exigences (dont {len(critiques)} critiques).")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python json-to-requirements.py <json_in> <md_out> <client> <objet>")
    else:
        json_to_requirements(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
