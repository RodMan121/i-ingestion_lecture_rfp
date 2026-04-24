# 📖 Manuel Opérationnel par Script

Ce guide définit la responsabilité de chaque script dans le pipeline.

---

## 🔵 ABB-01 : Script `parse-rfp.py`
**Responsabilité** : Garantir la fidélité de la donnée source.

1. **Usage** : `python 00-GOUVERNANCE/scripts/parse-rfp.py "source" "destination"`
2. **Audit** : Vérifier le `rapport-parsing.json` généré.
3. **Point d'arrêt** : Si des blocs sont marqués 🔴, corriger le `rfp-structured.md` avant de passer au script suivant.

---

## 🟡 ABB-02 : Script `extract-multimodal.py`
**Responsabilité** : Raisonner sur les artefacts pour isoler les obligations.

1. **Usage** : `python 00-GOUVERNANCE/scripts/extract-multimodal.py "path/to/artifacts" "prompt" "out.json"`
2. **Intelligence** : Ce script charge le texte (.md) + les tableaux (.csv) pour une analyse croisée.
3. **Moteur** : Nécessite Ollama en local avec `qwen2.5-coder:7b`.

---

## 🔴 ABB-02 : Script `json-to-requirements.py`
**Responsabilité** : Formater le résultat IA en document métier utilisable.

1. **Usage** : `python 00-GOUVERNANCE/scripts/json-to-requirements.py "out.json" "REQUIREMENTS.md" "Client" "Projet"`
2. **Résultat** : Un tableau Markdown propre, classé par type et priorité (OBL/SOH).

---
*Standard v2.2 — 1 Étape = 1 Script.*
