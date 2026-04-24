# 🟦 ABB-01 — INGESTION DU BESOIN (Certification)

L'ABB-01 est la fondation de la chaîne de confiance. Son but est de transformer des documents hétérogènes en données structurées et auditées.

## 🏗 Architecture de l'Étape
1. **Entrée** : PDF natifs ou scannés, fichiers XLSX, DOCX.
2. **Traitement** : Analyse structurelle par IA (Docling).
3. **Sortie** : Un dossier d'**ARTEFACTS** (.md, .csv, .json).

## 🛠 Script Dédié
- **Chemin** : `00-GOUVERNANCE/ABB-01-INGESTION-BESOIN/scripts/parse-rfp.py`
- **Usage** :
  ```bash
  python 00-GOUVERNANCE/ABB-01-INGESTION-BESOIN/scripts/parse-rfp.py <dossier_source_brut> <dossier_destination_artefacts>
  ```

## 📋 Protocole Opérationnel
1. **Initialisation** : Remplir `01-REFERENCE/ABB-01-INGESTION-BESOIN/templates/fiche-reception.md`.
2. **Exécution** : Lancer le script sur le dossier contenant les documents du client.
3. **Certification (Critique)** : 
   - Ouvrir `rapport-parsing.json`.
   - Si `ocr_utilise` est True ou si des blocs sont marqués 🔴 dans le Markdown, une correction manuelle est impérative avant l'ABB-02.

---
*Fiabilité ABB-01 : Une donnée mal ingérée produit une exigence fausse.*
