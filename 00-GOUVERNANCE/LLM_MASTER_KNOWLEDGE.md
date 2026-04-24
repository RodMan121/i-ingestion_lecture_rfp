---
version: 1.6.0
date: 2026-04-24
type: Dossier d'Architecture GenAI (DAG)
target_audience: AI Agents, Solution Architects, Prompt Engineers
---

# 🧠 DOSSIER D'ARCHITECTURE : Hub d'Ingestion & Extraction RFP

## 1. VISION STRATÉGIQUE GENAI
Transformer des documents non structurés en **Contexte Actionnable** pour LLM en garantissant la fidélité binaire et sémantique.

```mermaid
graph LR
    subgraph ABB-01 : Ingestion
        RAW[RFP Brut] --> DOC[Docling]
        DOC --> CERT[Donnée Certifiée .md]
    end
    subgraph ABB-02 : Extraction
        CERT --> FIT[Hardware Sizing llmfit]
        FIT --> OLL[Ollama qwen2.5-coder:7b]
        OLL --> REQ[REQUIREMENTS.md]
    end
    RAW -. Audit .-> REQ
```

---

## 2. MODÈLE DE DONNÉES EN COUCHES
L'IA opère sur trois couches pour minimiser les hallucinations :

1. **Couche Sémantique (.md)** : Structure hiérarchique (Arbre de sections).
2. **Couche Tabulaire (.csv)** : Données de précision (Matrices SLA/Prix).
3. **Couche Confiance (.json)** : Métadonnées d'audit (Score OCR, SHA256).

---

## 3. DIMENSIONNEMENT MATÉRIEL ET IA (ABB-02)
L'étape d'extraction s'appuie sur une infrastructure 100% locale pour des raisons de confidentialité de données :
- **Outil de sizing** : `llmfit` évalue la RAM et le CPU disponibles pour s'assurer que le modèle tournera sans out-of-memory.
- **Modèle recommandé** : `qwen2.5-coder:7b`. Ce modèle de 7 milliards de paramètres, quantifié en Q4_K_M ou supérieur, offre le meilleur compromis Vitesse/Logique pour la tâche ardue de l'extraction d'exigences contractuelles.

---

## 4. LOGIQUE DE FIABILITÉ (The 3-Pillars)

```mermaid
flowchart TD
    D1[Fidélité Textuelle] --> V1{Ratio > 0.85?}
    D2[Intégrité Structurelle] --> V2{Sections OK?}
    D3[Complétude] --> V3{Lignes OK?}

    V1 -->|Échec| VERIF[VÉRIFICATION REQUISE]
    V2 -->|Échec| VERIF
    V3 -->|Échec| VERIF

    V1 -->|Succès| OK[Audit Validé]
    V2 -->|Succès| OK
    V3 -->|Succès| OK
    
    OK --> FIABLE[Statut FIABLE]
```

---

## 4. SCHÉMA D'INTEROPÉRABILITÉ (`MANIFEST.json`)
Sert de table de routage pour les orchestrateurs d'agents :
```json
{
  "session_id": "ISO-DATE-UID",
  "statut_global": "FIABLE | VÉRIFICATION_REQUISE",
  "documents": [
    {
      "role": "CCTP",
      "sha256": "hash",
      "artefacts": { "markdown": "...", "tables": [] },
      "confiance_globale": 0.94
    }
  ]
}
```

---

## 5. CONSIGNES DE RAISONNEMENT POUR L'IA (System Prompt)
*Si tu es un agent IA utilisant ce référentiel :*
1. **Poids Contractuel** : CCTP > Annexes.
2. **Gestion 🔴/⚠️** : Interdiction d'extraire des faits contractuels depuis des blocs < 0.70 de confiance sans le mentionner.
3. **Traçabilité** : Toujours citer le SHA256 source et la page Markdown.

---
*Master Knowledge v1.5.0 — Certifié pour Ingestion GenAI.*
