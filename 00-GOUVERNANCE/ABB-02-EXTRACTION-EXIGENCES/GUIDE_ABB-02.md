# 🟧 ABB-02 — EXTRACTION DES EXIGENCES (Qualification)

L'ABB-02 transforme les données certifiées en un référentiel métier exploitable par les équipes techniques et commerciales.

## 🏗 Architecture de l'Étape
1. **Entrée** : Dossier d'ARTEFACTS issu de l'ABB-01 (Markdown + CSV).
2. **Traitement** : Analyse multimodale croisée par LLM Local (Ollama/Qwen2.5).
3. **Sortie** : Fichier `REQUIREMENTS.md` normalisé.

## 🛠 Scripts Dédiés

### 1. Extraction IA (Analyse croisée texte/tableaux)
- **Chemin** : `00-GOUVERNANCE/ABB-02-EXTRACTION-EXIGENCES/scripts/extract-multimodal.py`
- **Usage** :
  ```bash
  python 00-GOUVERNANCE/ABB-02-EXTRACTION-EXIGENCES/scripts/extract-multimodal.py <dossier_artefacts_doc> <prompt_md> <resultat_json>
  ```

### 2. Génération du Référentiel (Formatage)
- **Chemin** : `00-GOUVERNANCE/ABB-02-EXTRACTION-EXIGENCES/scripts/json-to-requirements.py`
- **Usage** :
  ```bash
  python 00-GOUVERNANCE/ABB-02-EXTRACTION-EXIGENCES/scripts/json-to-requirements.py <resultat_json> <nom_fichier_md> <client> <objet>
  ```

## 📋 Protocole Opérationnel
1. **Sizing** : Lancer `llmfit recommend` pour valider la RAM disponible.
2. **Extraction** : Lancer `extract-multimodal.py` sur le dossier d'un document (ex: CCTP).
3. **Formatage** : Convertir le JSON brut en `REQUIREMENTS.md` tabulaire.
4. **Qualification** : L'architecte valide manuellement les flags 🔴 et ⚠️ dans le fichier final.

---
*Fiabilité ABB-02 : Le croisement Markdown + CSV garantit la précision des chiffres.*
