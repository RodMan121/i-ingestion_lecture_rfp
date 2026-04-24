# Ingestion de Bibliothèque RFP — Pipeline Docling (Standard ABB-01)

## 🌟 Points Forts (Version Consolidée)
- **Filtre Intelligent Anti-Logo** : Ignore automatiquement les petites images (logos, icônes) pour ne garder que les schémas et photos techniques (> 3000 pts²).
- **Capture HD de Secours** : Utilise PyMuPDF pour "photographier" les pages des documents purement visuels (ex: schémas Visio vectoriels) quand l'IA ne détecte pas d'objet image.
- **Support Multi-Formats** : PDF, DOCX, XLSX, PPTX, HTML.
- **Orchestration IA** : MANIFEST.json complet pour piloter l'étape d'analyse suivante.

## 🛠 Installation
```bash
uv pip install httpx docling-core pandas pymupdf Pillow
```

## 📂 Structure des Artifacts
```
A-ingestion/
  ├── MANIFEST.json           # Index global
  └── [Nom_du_Document]/      
       ├── rfp-structured.md      # Markdown propre (structuré pour IA)
       ├── rapport-parsing.json   # Métadonnées, stats et SHA256
       ├── rapport-reconciliation.json # Audit de fidélité vs PDF binaire
       └── images/                # Uniquement les schémas et captures utiles
```

---
*Standard ABB-01 — Qualité de donnée industrielle.*
