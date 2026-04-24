---
version: 1.2.0
date: 2026-04-24
type: Dossier d'Architecture GenAI (DAG)
target_audience: AI Agents, Solution Architects, Prompt Engineers
---

# 🧠 DOSSIER D'ARCHITECTURE : Hub d'Ingestion RFP (ABB-01)

## 1. VISION STRATÉGIQUE GENAI
L'objectif de ce hub n'est pas la simple conversion de format, mais la **certification de la donnée source** pour les systèmes RAG (Retrieval Augmented Generation). 

Dans un contexte de réponse à appel d'offres (RFP), une erreur de lecture sur un SLA ou un prix peut invalider toute une offre. Ce pipeline agit comme un "pare-feu de qualité" avant l'injection dans les agents d'analyse (ABB-02).

## 2. MODÈLE DE DONNÉES POUR L'IA (The "Context Window")

L'IA ne doit pas seulement lire le texte, elle doit comprendre sa **fiabilité intrinsèque**. Le pipeline décompose chaque document en trois couches de contexte :

| Couche | Format | Rôle pour l'IA |
|:--- |:--- |:--- |
| **Sémantique** | `.md` | Structure hiérarchique pour le chunking et la navigation. |
| **Tabulaire** | `.csv` | Données de précision (prix, matrices) extraites hors-flux pour éviter les erreurs de parsing Markdown. |
| **Confiance** | `.json` | Métadonnées de certitude (SHA256, Confidence Score) pour pondérer le raisonnement. |

## 3. LOGIQUE D'INGESTION ET RAISONNEMENT (Chain of Thought)

### 3.1 Classification et Routage
Le pipeline utilise une logique de classification pour attribuer un **Rôle Contractuel**. Ce rôle définit le "Poids Juridique" d'une information :
- **CCTP** : Source de vérité technique absolue.
- **CCAP** : Source de vérité juridique (règles et pénalités).
- **BPU/DPGF** : Source de vérité financière (bordereau des prix).

### 3.2 Les 3 Dimensions de la Fiabilité
1. **Fidélité Textuelle** : Comparaison entre l'IA Docling et l'extraction binaire PyMuPDF.
2. **Intégrité Structurelle** : Maintien de l'arbre de décision (Titre > Sous-titre > Exigence).
3. **Complétude** : Garantie qu'aucun tableau n'a été tronqué par une erreur de mise en page.

## 4. MÉTRIQUES DE CONFIANCE (Quantified Quality)

Le LLM consommateur doit adapter son comportement selon les seuils suivants intégrés dans le Markdown :

- **✅ [CONFIANCE > 0.90]** : Traitement automatique autorisé.
- **⚠️ [CONFIANCE 0.70 - 0.90]** : "Hallucination probable". L'IA doit ajouter une note de bas de page demandant vérification.
- **🔴 [CONFIANCE < 0.70]** : "Donnée corrompue". L'IA doit refuser de traiter ce bloc et signaler une "rupture de chaîne de confiance".

## 5. PROTOCOLES DE REPLI (Resilience)

### SBB-01A : Protocole Manuel
Si `confiance_globale < 0.60`, le système impose une lecture humaine en 3 passes :
1. **Cartographie** (Structure)
2. **Extraction** (Obligations uniquement)
3. **Audit** (Recopie des tableaux critiques)

### SBB-01B : "Fallback Image"
Si Docling détecte moins de 5 blocs de texte (ex: schéma pur), le pipeline bascule en **Capture HD**. L'IA reçoit alors un bloc de texte descriptif pointant vers l'image extraite.

## 6. SCHÉMA D'INTEROPÉRABILITÉ (`MANIFEST.json`)
Ce fichier permet à un orchestrateur d'agents de piloter le lot de documents :
```json
{
  "statut_global": "FIABLE | VÉRIFICATION_REQUISE",
  "ordre_priorite": ["CCTP", "CCAP", "RC", "ANNEXES"],
  "index": {
    "sha256_id": {
      "role": "CCTP",
      "markdown": "A-ingestion/doc/rfp-structured.md",
      "csv": ["table-01.csv", "table-02.csv"],
      "quality_score": 0.94
    }
  }
}
```

## 7. CONSIGNES DE RAISONNEMENT POUR L'IA (System Prompting)
*Instructions pour l'agent ABB-02 utilisant ces données :*
1. **Ancre de Vérité** : Ne jamais inventer une exigence non présente dans le `.md`.
2. **Gestion de l'Incertitude** : Cite systématiquement le score de confiance si `< 0.90`.
3. **Audit de Version** : Avant toute analyse, compare le `sha256` actuel avec celui de tes archives.
4. **Référence Tabulaire** : Pour tout chiffre financier, le `.csv` prime sur le `.md`.

---
*Master Knowledge v1.2.0 — Architecture certifiée pour GenAI industrielle.*
