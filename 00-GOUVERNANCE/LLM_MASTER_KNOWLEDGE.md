---
version: 1.1.0
date: 2026-04-24
compatible_avec: ABB-02 >= 1.0
statut: PRODUCTION_READY
---

# 🧠 LLM MASTER KNOWLEDGE : Pipeline d'Ingestion RFP (ABB-01)

Ce document est la source de vérité pour comprendre l'architecture, l'historique et l'utilisation du Hub d'Ingestion RFP.

## 1. GENÈSE ET OBJECTIF (Le "Pourquoi")
**Problème :** L'analyse d'un appel d'offres (RFP) commence par des heures de copier-coller (2-4h).
**Solution :** Un pipeline industriel qui transforme le "vrac" documentaire en données certifiées en moins de 30 minutes.
**Objectif final :** Produire un Markdown structuré et des CSV qui servent de "Carburant Fiable" pour l'IA (ABB-02).

## 2. MODES OPÉRATOIRES (SBB)

### SBB-01A : Lecture Manuelle (Fallback)
*Protocole à activer si le PDF est un scan de mauvaise qualité ou délai < 2j.*
1. **Passe 1 (Cartographie)** : Identifier les sections et tableaux sans écrire. Repérer les zones denses.
2. **Passe 2 (Extraction)** : Isoler uniquement les obligations (*shall/must/doit*) dans `REQUIREMENTS.md`.
3. **Passe 3 (Audit)** : Recopie binaire des tableaux contractuels les plus engageants.

### SBB-01B : Pipeline Docling (Automatisé)
*Moteur IA de parsing structuré couplé à une réconciliation binaire.*
- **Classification** : Basée sur mots-clés (CCTP, CCAP, RC, BPU).
- **Flexibilité** : Possibilité de forcer un rôle si le nom du fichier est ambigu.
- **Connectivité** : S'appuie sur `DOCLING_SERVE_URL` (défaut : port 5001).

## 3. MÉTRIQUES DE FIABILITÉ (Seuils de Confiance)

Le pipeline marque chaque bloc de texte selon son score de confiance OCR :
- **✅ FIABLE (> 0.90)** : Confiance totale dans l'extraction.
- **⚠️ VIGILANCE (0.70 - 0.90)** : Risque de caractères mal reconnus. Vérification ciblée requise.
- **🔴 CRITIQUE (< 0.70)** : Texte probablement corrompu. Validation humaine obligatoire avant usage.

## 4. SCHÉMA DU MANIFESTE (`MANIFEST.json`)
C'est l'index unique de la session de travail pour les agents IA avals.
```json
{
  "source": "/chemin/vers/pdf",
  "date": "2026-04-24T18:00:00",
  "statut_global": "FIABLE | VÉRIFICATION_REQUISE",
  "details": [
    {
      "fichier": "nom_original.pdf",
      "role": "CCTP",
      "sha256": "empreinte_unique",
      "markdown_file": "rfp-structured.md",
      "confiance_globale": 0.94
    }
  ]
}
```

## 5. GESTION DES CAS D'ERREUR
- **Serveur Docling inaccessible** : Le script s'arrête proprement après vérification du `/health`.
- **Fichier Protégé/Corrompu** : Log d'erreur dans les métadonnées et poursuite du lot.
- **Document "Image Pure"** : Déclenchement automatique de la capture HD de page si < 5 blocs texte détectés.

## 6. CONSIGNES POUR LE LLM CONSOMMATEUR
*Si tu es un LLM et que tu lis ce document :*
1. **Hiérarchie** : Le CCTP est ta source absolue. Le CCAP définit les règles juridiques.
2. **Intégrité** : Vérifie toujours que le SHA256 n'a pas changé entre deux analyses d'un même document.
3. **Prudence** : Si tu extrais une donnée d'un bloc marqué 🔴 ou ⚠️, tu DOIS le mentionner dans ton output.
4. **Localisation** : Cite toujours le fichier CSV ou la page Markdown d'origine pour chaque affirmation.

---
*Master Knowledge v1.1.0 — Prêt pour injection IA.*
