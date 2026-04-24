import json
from pathlib import Path
from datetime import date
import sys

def json_to_requirements(json_path: str, output_path: str, client: str, objet: str):
    """
    Transforme le JSON produit par le LLM en REQUIREMENTS.md
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Erreur lecture JSON : {e}")
        # Tentative de nettoyage si Ollama a mis du texte avant/après
        content = Path(json_path).read_text(encoding='utf-8')
        if "{" in content:
            data = json.loads(content[content.find("{"):content.rfind("}")+1])
        else:
            raise e

    lines = []
    lines.append(f"# REQUIREMENTS — {client} — {objet} — v1.0\n\n")
    lines.append(f"## Métadonnées\n")
    lines.append(f"- Date création : {date.today()}\n")
    lines.append(f"- Statut global : EXT (Extrait)\n\n")
    
    lines.append("## Référentiel des exigences\n\n")
    lines.append("| Ref | Intitulé | Type | BDAT | Prio | Statut | Section | Flag |\n")
    lines.append("|-----|----------|------|------|------|--------|---------|------|\n")
    
    flag_emoji = {
        "BLOQUANT": "🔴",
        "ATTENTION": "🟡", 
        "STANDARD": "⚪"
    }
    
    for ex in data.get("exigences", []):
        flag = flag_emoji.get(ex.get("flag", "STANDARD"), "⚪")
        lines.append(
            f"| {ex['ref']} | {ex['intitule']} | "
            f"{ex['type']} | {ex['bdat']} | {ex['priorite']} | "
            f"EXT | {ex.get('source_section', '')} | {flag} |\n"
        )
    
    if data.get("contradictions"):
        lines.append("\n## Contradictions identifiées\n\n")
        for c in data["contradictions"]:
            refs = " vs ".join(c.get("refs", []))
            lines.append(f"- **{refs}** : {c.get('description', '')}\n")
    
    if data.get("exigences_implicites_suggerees"):
        lines.append("\n## Exigences implicites suggérées par l'IA\n")
        lines.append("*(à valider par l'architecte)*\n\n")
        for ei in data["exigences_implicites_suggerees"]:
            lines.append(f"- [ ] {ei}\n")
    
    Path(output_path).write_text("".join(lines), encoding="utf-8")
    print(f"✅ REQUIREMENTS.md généré : {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python json-to-requirements.py <json_in> <md_out> <client> <objet>")
    else:
        json_to_requirements(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
