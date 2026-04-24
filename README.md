# 🚀 Hub d'Intelligence RFP

Dispositif industriel segmenté selon le standard d'ingénierie ABB.

---

## 🔹 ABB-01 — INGESTION DU BESOIN
**Rôle** : Certification de la donnée source.
- **Dossier** : `00-GOUVERNANCE/ABB-01-INGESTION-BESOIN/`
- **Script principal** : `scripts/parse-rfp.py`
- **Lancement** : Voir `GUIDE_ABB-01.md`

---

## 🔸 ABB-02 — EXTRACTION DES EXIGENCES
**Rôle** : Production du référentiel d'exigences (`REQUIREMENTS.md`).
- **Dossier** : `00-GOUVERNANCE/ABB-02-EXTRACTION-EXIGENCES/`
- **Scripts** : `scripts/extract-multimodal.py`, `scripts/json-to-requirements.py`
- **Lancement** : Voir `GUIDE_ABB-02.md`

---

## 📁 Architecture du Dépôt
- `00-GOUVERNANCE/` : Cerveau méthodologique et scripts par bloc ABB.
- `01-REFERENCE/` : Templates (Fiches, Prompts, Requirements) par bloc ABB.
- `03-PROJETS/` : Zone de travail confidentielle (Exclue de Git).

---
*Standard v3.1 — Structuration par ABB Complète.*
