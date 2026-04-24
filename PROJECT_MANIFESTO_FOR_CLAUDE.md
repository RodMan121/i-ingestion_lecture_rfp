# 🧠 MANIFESTE PROJET : Hub d'Intelligence RFP (v3.2)

> **Destinataire :** Intelligence Artificielle (Claude/GPT) ou Humain en phase de reprise.
> **Objectif :** Fournir une compréhension immédiate de l'architecture "Production-Grade" et des procédures opérationnelles.

---

## 1. VISION ET FILTRE DE QUALITÉ
Ce projet résout le problème du **"Garbage In, Garbage Out"**. Aucune donnée n'est injectée dans l'IA d'analyse (ABB-02) sans avoir été certifiée par l'IA d'ingestion (ABB-01).
- **Hachage 360°** : Markdown + Tableaux CSV sont hashés ensemble pour garantir la traçabilité.
- **Multimodalité Locale** : Utilisation de Qwen2.5-Coder:7b via Ollama (100% On-Premise).

---

## 2. ARCHITECTURE DES COMPOSANTS (ABB)

### 🔹 ABB-01 — INGESTION DU BESOIN (Certification)
*Dossier : `00-GOUVERNANCE/ABB-01-INGESTION-BESOIN/`*
- **Rôle** : Produire les **ARTEFACTS** (.md, .csv, .json).
- **Scripts** : `scripts/parse-rfp.py`.
- **Preuve** : Le fichier `rapport-parsing.json` définit si la donnée est exploitable par l'IA.

### 🔸 ABB-02 — EXTRACTION DES EXIGENCES (Qualification)
*Dossier : `00-GOUVERNANCE/ABB-02-EXTRACTION-EXIGENCES/`*
- **Rôle** : Produire le **Référentiel métier** (`REQUIREMENTS.md`).
- **Scripts** : `scripts/extract-multimodal.py` (IA) et `scripts/json-to-requirements.py` (Formatage).
- **Intelligence** : Croisement du texte et des tables CSV. Les exigences critiques sont marquées 🔥.

---

## 3. LOGIQUE DE CONFIANCE ET RÈGLES D'OR
1. **Primauté Tabulaire** : En cas de conflit Texte vs CSV, le **CSV gagne**.
2. **Héritage de Confiance** : Si ABB-01 flague un bloc en 🔴 ou ⚠️, l'ABB-02 l'indique dans le `REQUIREMENTS.md`.
3. **Zéro Corruption** : Les tableaux Markdown sont protégés par un échappement des caractères spéciaux.

---

## 4. GUIDE DE REPRISE RAPIDE

```bash
# 1. Ingestion
python 00-GOUVERNANCE/ABB-01-INGESTION-BESOIN/scripts/parse-rfp.py "source" "artefacts"

# 2. Extraction IA Multimodale
python 00-GOUVERNANCE/ABB-02-EXTRACTION-EXIGENCES/scripts/extract-multimodal.py "artefacts" "prompt_v3.md" "raw.json"

# 3. Formatage Référentiel
python 00-GOUVERNANCE/ABB-02-EXTRACTION-EXIGENCES/scripts/json-to-requirements.py "raw.json" "REQUIREMENTS.md" "Client" "Projet"
```

---
*Fichier généré le 24/04/2026 — Gardien de l'intelligence du Hub.*
