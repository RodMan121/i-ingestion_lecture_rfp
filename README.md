# 🚀 Hub d'Intelligence RFP (Standard ABB-01 & ABB-02)

Ce dispositif industriel est segmenté en deux blocs autonomes, chacun piloté par ses propres scripts.

---

## 🏗 Étape 1 : ABB-01 — L'Ingestion (Certification)
**Script unique** : `00-GOUVERNANCE/scripts/parse-rfp.py`

- **Objectif** : Transformer le "vrac" (PDF, XLSX) en données structurées.
- **Entrée** : Dossier contenant les documents originaux du client.
- **Sortie** : Dossier d'ARTEFACTS (Markdown, Tables CSV, Audit JSON).
- **Action** :
  ```bash
  python 00-GOUVERNANCE/scripts/parse-rfp.py "03-PROJETS/RFP-BRUT" "03-PROJETS/ARTIFACTS"
  ```

---

## 🏗 Étape 2 : ABB-02 — L'Extraction (Qualification)
**Scripts dédiés** : `extract-multimodal.py` et `json-to-requirements.py`

- **Objectif** : Isoler les obligations contractuelles à partir des ARTEFACTS.
- **Entrée** : Le dossier d'artefacts généré par l'ABB-01.
- **Sortie** : Le fichier `REQUIREMENTS.md` (Pivot de la réponse).
- **Action (en 2 temps)** :
  1. **Extraction IA** :
     ```bash
     python 00-GOUVERNANCE/scripts/extract-multimodal.py "path/to/artifacts" "prompt.md" "raw.json"
     ```
  2. **Génération du Référentiel** :
     ```bash
     python 00-GOUVERNANCE/scripts/json-to-requirements.py "raw.json" "REQUIREMENTS.md" "Client" "Objet"
     ```

---

## 📂 Structure du Dépôt
- `00-GOUVERNANCE/scripts/` : Le coffre-fort des scripts ABB-01 et ABB-02.
- `00-GOUVERNANCE/` : Guides et Dossier d'Architecture.
- `01-REFERENCE/` : Templates (Fiche de réception, Prompt IA).

---
*Fiabilité Absolue — 1 ABB = 1 Script Dédié.*
