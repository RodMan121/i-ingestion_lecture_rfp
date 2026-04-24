# CONTEXTE POUR LLM - SOURCE DE VÉRITÉ (ABB-01)
-----------------------------------------------
Ce document définit comment tu dois interpréter les fichiers issus du pipeline d'ingestion.

## 1. INTÉGRITÉ ET TRAÇABILITÉ (SHA256)
Le fichier `rapport-parsing.json` contient une empreinte **SHA256** du PDF source. 
- Si tu analyses plusieurs versions d'un même document, vérifie toujours si le SHA256 a changé.
- Toute divergence de SHA256 impose une re-validation des exigences extraites.

## 2. PONDÉRATION DE LA FIABILITÉ (SCORING OCR)
Le fichier `rfp-structured.md` contient des scores de confiance pour les blocs issus de documents scannés ou mixtes.
- **[CONFIANCE > 0.90]** : Traite l'information comme une certitude contractuelle.
- **[CONFIANCE 0.70 - 0.90] ⚠️** : L'exigence peut contenir des fautes de frappe ou des chiffres erronés. Flague-la comme "À vérifier".
- **[CONFIANCE < 0.70] 🔴** : Ne pas extraire d'exigence sans validation humaine préalable. Le texte est probablement corrompu.

## 3. RÉCONCILIATION ET COMPLÉTUDE
Consulte le fichier `rapport-reconciliation.json`.
- Si le taux de confiance global est < 85%, signale-le à l'utilisateur. 
- Une page avec un ratio de similarité faible indique souvent un tableau complexe que tu dois analyser avec prudence via les fichiers `.csv` dédiés.

## 4. RÔLES ET PRIORITÉS DES DOCUMENTS
- **CCTP** (Priorité 1) : Cahier des Clauses Techniques Particulières. Source absolue des exigences techniques.
- **CCAP** (Priorité 2) : Cahier des Clauses Administratives Particulières. Définit le cadre juridique, les pénalités et la durée.
- **RC** (Priorité 3) : Règlement de Consultation. Détaille les critères de notation de l'offre.
- **ANNEXES** : Compléments techniques (Architecture, SLA détaillés, Cyber-sécurité).

## 5. CONSIGNES POUR L'ANALYSE IA
- **Croisement** : Toujours croiser les références textuelles du `.md` avec les données structurées des `.csv`.
- **Conflits** : En cas de divergence entre deux documents, les dispositions du **CCTP** prévalent, sauf mention contraire dans le **CCAP**.
- **Unités d'Œuvre (UO)** : Porter une attention particulière à la définition des UO (ex: 'Machines virtuelles à la demande') qui sont les briques de base du chiffrage.
- **Invariants** : Tu trouveras toujours les métadonnées dans `rapport-parsing.json` et le texte structuré dans `rfp-structured.md`.
