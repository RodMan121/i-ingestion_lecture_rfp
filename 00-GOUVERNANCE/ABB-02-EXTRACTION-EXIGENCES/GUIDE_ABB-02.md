# 📖 Guide Opérationnel : ABB-02 — EXTRACTION DES EXIGENCES

## Objectif
Qualifier les exigences contractuelles et produire le référentiel maître du projet.

## Scripts Dédiés
1. **Extraction IA** : `00-GOUVERNANCE/ABB-02-EXTRACTION/scripts/extract-multimodal.py`
2. **Formatage Référentiel** : `00-GOUVERNANCE/ABB-02-EXTRACTION/scripts/json-to-requirements.py`

## Commande (Cycle complet)
```bash
# 1. Analyse par le LLM (Ollama)
python 00-GOUVERNANCE/ABB-02-EXTRACTION/scripts/extract-multimodal.py \
  "dossier_artefacts" \
  "01-REFERENCE/ABB-02-EXTRACTION/prompt-extraction-exigences.md" \
  "raw_exigences.json"

# 2. Génération du REQUIREMENTS.md
python 00-GOUVERNANCE/ABB-02-EXTRACTION/scripts/json-to-requirements.py \
  "raw_exigences.json" \
  "REQUIREMENTS.md" "Client" "Projet"
```

---
*Standard ABB-02 — Qualification de l'exigence métier.*
