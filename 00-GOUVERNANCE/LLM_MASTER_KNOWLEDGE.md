---
version: 2.4.0
date: 2026-04-24
type: Dossier d'Architecture GenAI (DAG)
target_audience: AI Agents, Solution Architects, Prompt Engineers
---

# 🧠 DOSSIER D'ARCHITECTURE : Organisation par ABB

## 1. VISION STRATÉGIQUE : La segmentation ABB
L'architecture est scindée en deux blocs autonomes pour garantir la séparation des responsabilités.

```mermaid
graph TD
    subgraph ABB-01 : INGESTION DU BESOIN [Dossier ABB-01-INGESTION-BESOIN/]
        RAW[RFP Brut] --> P1[scripts/parse-rfp.py]
        P1 --> ARTEFACTS[Dossier Artefacts]
    end
    
    subgraph ABB-02 : EXTRACTION DES EXIGENCES [Dossier ABB-02-EXTRACTION-EXIGENCES/]
        ARTEFACTS --> P2[scripts/extract-multimodal.py]
        P2 --> P3[scripts/json-to-requirements.py]
        P3 --> REQ[REQUIREMENTS.md]
    end
```

---

## 2. MODÈLE DE DONNÉES PAR ÉTAPE

### Étape 01 (Certification)
- **Input** : Binaire (.pdf, .xlsx).
- **Output** : Artefacts normalisés. On ne parle pas encore d'exigences, mais de "données structurées".

### Étape 02 (Qualification)
- **Input** : Artefacts (.md + .csv).
- **Output** : Référentiel métier. C'est ici que l'intelligence métier intervient via le LLM.

---

## 3. LOGIQUE DE FIABILITÉ (Passage de relais)
L'ABB-02 ne peut être lancé que si l'ABB-01 a validé le **Score de Confiance**.
- Si `parse-rfp.py` génère un score < 0.70 sur une section, l'opérateur doit corriger le Markdown avant de lancer `extract-multimodal.py`.

---
*Master Knowledge v2.2.0 — Segmenté par Scripts.*
