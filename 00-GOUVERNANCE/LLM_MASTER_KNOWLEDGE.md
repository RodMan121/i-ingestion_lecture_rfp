---
version: 1.4.0
date: 2026-04-24
type: Dossier d'Architecture GenAI (DAG)
target_audience: AI Agents, Solution Architects, Prompt Engineers
---

# 🧠 DOSSIER D'ARCHITECTURE : Hub d'Ingestion & Extraction RFP

## 1. VISION STRATÉGIQUE : "De la donnée brute à l'exigence qualifiée"
L'architecture se décompose en deux blocs majeurs :
- **ABB-01 (Ingestion)** : Certification de la donnée source (Docling).
- **ABB-02 (Extraction)** : Isolation des obligations contractuelles (Ollama/LLM).

```mermaid
graph LR
    subgraph ABB-01 : Ingestion
        RAW[RFP Brut] --> DOC[Docling]
        DOC --> CERT[Donnée Certifiée .md]
    end
    subgraph ABB-02 : Extraction
        CERT --> OLL[Ollama / Local LLM]
        OLL --> REQ[REQUIREMENTS.md]
    end
```

---

## 2. MODÈLE D'EXTRACTION IA (ABB-02)
L'IA (Mistral/Llama3 via Ollama) opère une transformation de la **Couche Sémantique** vers un **Référentiel d'Exigences** structuré.

### 2.1 Invariant de Sortie : `REQUIREMENTS.md`
C'est le fichier central du projet. Sa structure est immuable pour garantir la compatibilité avec les outils de chiffrage (BPU) et de cadrage (D1).

### 2.2 Taxonomie d'Analyse
Chaque exigence extraite par l'IA doit être tagguée :
- **Type** : Fonctionnel (F), Technique (T), Organisationnel (O), Contractuel (C).
- **BDAT** : Business, Data, Application, Technology.
- **Priorité** : OBL (Obligatoire), SOH (Souhaitable).

---

## 3. LOGIQUE DE CONFIANCE ET ESCALADE
L'ABB-02 hérite des scores de confiance de l'ABB-01.

```mermaid
flowchart TD
    MD[Lecture rfp-structured.md] --> CONF{Score > 0.90?}
    CONF -->|OUI| EXT[Extraction Directe]
    CONF -->|NON ⚠️| WARN[Extraction avec Flag ATTENTION]
    CONF -->|NON 🔴| MANUAL[Escalade SBB-01A : Lecture Humaine]
    
    EXT & WARN --> JSON[Sortie JSON Extraction]
    JSON --> REQ_MD[Génération REQUIREMENTS.md]
```

---

## 2. ARCHITECTURE DES COUCHES DE DONNÉES
Pour maximiser la précision, nous séparons le document en **3 couches indépendantes** mais reliées. Cela permet à l'IA de choisir le meilleur format selon la question posée.

```mermaid
graph TD
    DOC[Document Ingesté] --> C1[Couche SÉMANTIQUE .md]
    DOC --> C2[Couche TABULAIRE .csv]
    DOC --> C3[Couche CONFIANCE .json]

    C1 --> |Rôle| HIAR[Navigation & Titres]
    C2 --> |Rôle| DATA[Précision Chiffrée]
    C3 --> |Rôle| AUDIT[Scores de certitude]
```

- **Sémantique** : Arbre hiérarchique pour le chunking et la navigation.
- **Tabulaire** : Extraction brute des cellules pour éviter la corruption du Markdown.
- **Confiance** : Audit de chaque mot (OCR Confidence Score).

---

## 3. LE CYCLE DE FIABILITÉ (The 3-Pillars)
Nous ne faisons pas confiance aveuglément à l'IA de parsing. Le pipeline vérifie l'extraction via trois dimensions :

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

## 4. MÉTRIQUES DE CONFIANCE OPÉRATIONNELLES
L'IA doit adapter son raisonnement en fonction des marqueurs visuels insérés dans le texte :

| Icône | Seuil Confiance | Comportement IA Attendu |
|:--- |:--- |:--- |
| ✅ | **> 0.90** | **Affirmation directe**. La donnée est contractuelle. |
| ⚠️ | **0.70 - 0.90** | **Prudence**. L'IA doit dire : "Sous réserve de vérification..." |
| 🔴 | **< 0.70** | **Refus**. L'IA doit dire : "Donnée illisible, intervention humaine requise." |

---

## 5. ORCHESTRATION PAR LE MANIFESTE
Le `MANIFEST.json` sert de "Table de Routage" pour les agents IA. Il permet de traiter un lot de documents comme une seule entité cohérente.

```mermaid
sequenceDiagram
    participant Agent as Agent IA (ABB-02)
    participant Manifest as MANIFEST.json
    participant Files as Fichiers Ingestés

    Agent->>Manifest: Quels sont les documents prioritaires ?
    Manifest-->>Agent: 1. CCTP (Certifié), 2. BPU (Certifié)
    Agent->>Files: Lit CCTP (rfp-structured.md)
    Agent->>Files: Croise avec BPU (tables/table-01.csv)
    Agent-->>Agent: Raisonnement croisé
```

---

## 6. CONSIGNES DE RAISONNEMENT (Prompting)
*Instructions fondamentales pour tout LLM consommant cette architecture :*

1. **Hiérarchie Contractuelle** : En cas de conflit, le **CCTP** (Technique) prime sur tout, sauf sur le **CCAP** pour les aspects juridiques/financiers.
2. **Audit SHA256** : Avant de répondre, valide que l'ID du document (sha256) est identique à celui de ta session précédente.
3. **Zéro-Invention** : Si une information est absente des 3 couches, réponds : "Donnée non trouvée dans le référentiel certifié".

---
*Master Knowledge v1.3.0 — Architecture Pédagogique pour GenAI.*
