# 🚀 Hub d'Ingestion RFP (Standard ABB-01)

Ce dépôt contient le pipeline industriel permettant de transformer des documents d'appels d'offres (RFP) bruts en une bibliothèque de données structurée et certifiée pour l'analyse par IA.

## 📋 Prérequis

1. **Serveur Docling** : Le pipeline s'appuie sur une instance Docling Serve active.
   - URL par défaut : `http://localhost:5001`
   - Vérification : `curl http://localhost:5001/health`

2. **Python 3.10+** (Testé en 3.13)

## 🛠 Installation

```bash
# 1. Création de l'environnement virtuel
python -m venv venv-avant-vente
source venv-avant-vente/bin/activate  # Linux/Mac

# 2. Installation des dépendances
pip install docling pandas httpx pymupdf Pillow
```

## 🚀 Utilisation

Le script `parse-rfp.py` automatise l'ingestion de tout un dossier (PDF, DOCX, XLSX).

```bash
# Syntaxe : python 00-GOUVERNANCE/scripts/parse-rfp.py <dossier_source> <dossier_destination>

python 00-GOUVERNANCE/scripts/parse-rfp.py \
  "03-PROJETS/2025-01-CLIENT/01-rfp-source" \
  "03-PROJETS/2025-01-CLIENT/artifacts/A-ingestion"
```

## 💎 Fiabilité et Sorties

Le pipeline génère pour chaque document un "coffre-fort" d'artefacts dans le dossier destination :

- **`rfp-structured.md`** : Texte intégral avec scores de confiance OCR par bloc (🔴/⚠️).
- **`tables/*.csv`** : Extraction haute fidélité de tous les tableaux (SLA, Prix, Exigences).
- **`rapport-parsing.json`** : Métadonnées, SHA256 (audit d'intégrité) et stats.
- **`rapport-reconciliation.json`** : Audit de complétude (Docling vs PyMuPDF).
- **`MANIFEST.json`** : Index global pilotant l'analyse IA (ABB-02).

## 📂 Structure du Dépôt

- `00-GOUVERNANCE/` : Scripts de parsing, prompts IA et guides méthodologiques.
- `01-REFERENCE/` : Templates (Fiche de réception RFP).
- `03-PROJETS/` : (Exclu de Git) Dossier de travail local pour les données confidentielles.

---
*Standard ABB-01 — Transformer le vrac documentaire en gisement de données fiables.*
