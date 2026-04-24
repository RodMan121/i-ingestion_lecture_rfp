# 📖 Guide Opérationnel : ABB-01 — INGESTION DU BESOIN

## Objectif
Transformer les documents bruts (PDF, XLSX, DOCX) en données certifiées et structurées (Markdown, CSV).

## Script Dédié
- **Chemin** : `00-GOUVERNANCE/ABB-01-INGESTION/scripts/parse-rfp.py`
- **Commande** :
  ```bash
  python 00-GOUVERNANCE/ABB-01-INGESTION/scripts/parse-rfp.py <source_brute> <destination_artefacts>
  ```

## Étapes de Validation
1. Remplir la **Fiche de Réception** (`01-REFERENCE/ABB-01-INGESTION/fiche-reception.md`).
2. Exécuter le script de parsing.
3. Vérifier le `rapport-parsing.json` pour détecter les blocs 🔴 (incertitudes).

---
*Standard ABB-01 — Certification de la donnée source.*
