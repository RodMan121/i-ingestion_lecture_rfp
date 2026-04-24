# Bibliothèque de Prompts — Gouvernance I-Ingestion

Ce dossier contient les actifs immatériels critiques pour l'analyse des RFP. Chaque prompt est versionné pour garantir l'auditabilité des résultats.

## 📋 Index des Prompts

| Code | Version | Nom | Usage |
|:---|:---|:---|:---|
| **ABB-02** | 1.2 | Extraction Exigences | Extraction atomique et fidèle des obligations. |
| **ABB-02-T**| 1.0 | User Template | Template de message pour fournir les fichiers au LLM. |
| **F1** | - | Compliance Check | (À venir) Vérification de l'adéquation solution. |
| **F3** | - | Murder Boarding | (À venir) Simulation de soutenance. |

## ⚖️ Règles de Versionnage
1. Ne jamais modifier un fichier existant (`-v1.2.md`).
2. Créer une nouvelle version pour toute amélioration suite à un débriefing de comité.
3. Tracer l'utilisation de la version dans le `Governance Log` du projet.

## 🛠 Mode d'emploi
1. Charger le **System Prompt** (ex: `ABB-02-extraction-exigences-v1.2.md`).
2. Utiliser le **User Template** pour joindre les fichiers `rfp-with-confidence.md` et les CSV de `tables/`.
