# 🚀 Hub d'Intelligence RFP (ABB-01 & ABB-02)

Dispositif industriel certifié pour transformer des documents d'appels d'offres en référentiels d'exigences fiables.

---

## 🏗 Architecture "1 Étape = 1 Dossier Dédié"

### 🔹 ABB-01 — INGESTION DU BESOIN (Certification)
**Rôle** : Transformer le vrac (PDF, XLSX) en données structurées et auditées.
- **Dossier** : `00-GOUVERNANCE/ABB-01-INGESTION-BESOIN/`
- **Script principal** : `scripts/parse-rfp.py` (IA Docling)
- **Lancement** : Voir `GUIDE_ABB-01.md`

### 🔸 ABB-02 — EXTRACTION DES EXIGENCES (Qualification)
**Rôle** : Analyse multimodale pour produire le `REQUIREMENTS.md`.
- **Dossier** : `00-GOUVERNANCE/ABB-02-EXTRACTION-EXIGENCES/`
- **Scripts** : `scripts/extract-multimodal.py` (Ollama), `scripts/json-to-requirements.py`
- **Lancement** : Voir `GUIDE_ABB-02.md`

---

## 🛠 Installation & Prérequis

1. **Environnement Python 3.13** :
   ```bash
   python -m venv venv-avant-vente
   source venv-avant-vente/bin/activate
   pip install docling pandas httpx pymupdf Pillow
   ```
2. **Outils IA** :
   - Docker **Ollama** (Modèle `qwen2.5-coder:7b`)
   - Outil de sizing : `llmfit` (`curl -fsSL https://llmfit.axjns.dev/install.sh | sh`)

## 📂 Structure du Dépôt
- `00-GOUVERNANCE/` : Cerveau méthodologique, scripts et prompts par bloc ABB.
- `01-REFERENCE/` : Templates (Fiches, Requirements) par bloc ABB.
- `03-PROJETS/` : Zone de travail locale (Exclue de Git).

---
*Standard v3.2 — Fiabilité Industrielle & Multimodalité.*
