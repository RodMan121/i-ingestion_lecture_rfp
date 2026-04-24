# 🧠 MANIFESTE PROJET : Hub d'Intelligence RFP (ABB-01/02)

> **Destinataire :** Intelligence Artificielle (Claude/GPT) ou Humain en phase de reprise.
> **Objectif :** Fournir une compréhension immédiate de l'architecture, de la logique de confiance et des procédures opérationnelles.

---

## 1. VISION ET INTENTION
Ce projet est un pipeline industriel de traitement d'Appels d'Offres (RFP). Sa raison d'être est de résoudre le problème du "Garbage In, Garbage Out".
- **Souveraineté** : Tout tourne en local (Docker/Ollama). Aucune donnée ne sort.
- **Fiabilité Absolue** : On ne croit pas l'IA sur parole. On vérifie chaque bloc par réconciliation binaire et par croisement multimodal (Texte vs Tableaux).

---

## 2. ARCHITECTURE DES COMPOSANTS (ABB)

Le projet suit la nomenclature **ABB (Architecture Building Block)** :

### 🔹 ABB-01 — INGESTION DU BESOIN
*Dossier : `00-GOUVERNANCE/ABB-01-INGESTION-BESOIN/`*
- **Rôle** : Certification de la donnée source.
- **Moteur** : **Docling** (IA Document Analysis).
- **Philosophie** : On transforme le PDF/XLSX en **Dossier d'ARTEFACTS** (.md sémantique, .csv tabulaire, .json d'audit).
- **Script clé** : `scripts/parse-rfp.py`.

### 🔸 ABB-02 — EXTRACTION DES EXIGENCES
*Dossier : `00-GOUVERNANCE/ABB-02-EXTRACTION-EXIGENCES/`*
- **Rôle** : Qualification de l'exigence métier.
- **Moteur** : **Ollama (Qwen2.5-Coder:7b)**.
- **Philosophie** : **Multimodalité**. Le script lit le texte ET les tableaux CSV simultanément. Si un chiffre diffère, le CSV fait foi.
- **Scripts clés** : `scripts/extract-multimodal.py` (IA) et `scripts/json-to-requirements.py` (Formatage).

---

## 3. LOGIQUE DE CONFIANCE (The 3 Pillars)
1. **Fidélité Textuelle** : Comparaison Docling vs PyMuPDF (ratio de similarité).
2. **Intégrité Structurelle** : Arbre hiérarchique préservé pour le chunking.
3. **Précision Tabulaire** : Les CSV isolent les données chiffrées (SLA/Prix) souvent corrompues par le Markdown.

---

## 4. GUIDE DE DÉMARRAGE RAPIDE (Pour reprise)

### A. Préparer le terrain
```bash
docker start ollama docling-serve
llmfit recommend --limit 5  # Vérifie que la RAM est ok
```

### B. Traiter un document
1. **Ingérer** : `python 00-GOUVERNANCE/ABB-01-INGESTION-BESOIN/scripts/parse-rfp.py "source" "destination"`
2. **Extraire** : `python 00-GOUVERNANCE/ABB-02-EXTRACTION-EXIGENCES/scripts/extract-multimodal.py "artefacts" "prompt" "out.json"`
3. **Produire** : `python 00-GOUVERNANCE/ABB-02-EXTRACTION-EXIGENCES/scripts/json-to-requirements.py "out.json" "REQUIREMENTS.md" "Client" "Objet"`

---

## 5. PIÈGES ÉVITÉS ET SOLUTIONS IMPLÉMENTÉES
- **Saturation Contexte** : Implémentation du **Batch Processing** (découpage du document par blocs de 30k chars).
- **Perte de Symboles** : Encodage `UTF-8` strict avec `ensure_ascii=False`.
- **Ordre CSV** : Tri alphabétique déterministe pour garantir la reproductibilité de l'extraction.
- **Sécurité** : `.gitignore` et purge de l'historique Git pour protéger les secrets personnels.

---
*Fichier généré le 24/04/2026 — Gardien de la connaissance du projet.*
