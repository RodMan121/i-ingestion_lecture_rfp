# 🚀 Hub d'Intelligence RFP (Standard ABB-01 & ABB-02)

Ce dispositif industriel transforme le "vrac" documentaire d'un appel d'offres en une base de données d'exigences certifiée, prête pour l'aide au chiffrage et à la conception.

## 🏗 Les 2 Étapes Clés

### Étape 1 : ABB-01 — Ingestion & Certification
**Objectif** : Nettoyer, structurer et auditer la donnée source (PDF, Word, Excel).
- **Moteur** : IA Docling (Parsing structuré).
- **Sortie** : Markdown enrichi avec scores de confiance et CSV de tableaux.

### Étape 2 : ABB-02 — Extraction & Qualification
**Objectif** : Isoler les obligations contractuelles et les classifier.
- **Moteur** : LLM Local (Mistral/Llama3 via Ollama).
- **Sortie** : `REQUIREMENTS.md` (Le référentiel central du projet).

## 🛠 Installation Rapide

```bash
# 1. Environnement
python -m venv venv-avant-vente
source venv-avant-vente/bin/activate

# 2. Dépendances
pip install docling pandas httpx pymupdf Pillow

# 3. Moteur IA Local (Docker Ollama requis)
curl http://localhost:11434/api/tags # Vérifie Ollama
```

## 🚀 Utilisation (Cycle Complet)

```bash
# A. Ingestion (ABB-01)
python 00-GOUVERNANCE/scripts/parse-rfp.py <source> <destination>

# B. Extraction IA (ABB-02)
python 00-GOUVERNANCE/scripts/extract-requirements.py <md_in> <prompt_in> <json_out>

# C. Génération Référentiel
python 00-GOUVERNANCE/scripts/json-to-requirements.py <json_in> <md_out> <client> <objet>
```

## 📂 Structure du Dépôt
- `00-GOUVERNANCE/` : Scripts, Guides, Dossier d'Architecture.
- `01-REFERENCE/` : Templates (Fiche de réception, Prompt IA).
- `03-PROJETS/` : (Exclu de Git) Zone de travail confidentielle.

---
*Standard Industriel — Fiabilité Absolue, Zéro Hallucination.*
