# 📖 Manuel Opérationnel : Du PDF au Référentiel d'Exigences

Ce guide explique pas à pas comment utiliser le Hub pour traiter un nouvel appel d'offres.

---

## 🟢 ÉTAPE 0 : Réception & Audit
Avant de lancer l'IA, remplir la **Fiche de Réception** (`01-REFERENCE/templates/artifacts/fiche-reception.md`).
- Objectif : Identifier la complétude du dossier client.

---

## 🔵 ÉTAPE 1 : Ingestion (ABB-01)
Transformation du PDF en Markdown "Propre".

**Action :**
```bash
python 00-GOUVERNANCE/scripts/parse-rfp.py "source" "destination"
```

**Pourquoi c'est important ?**
Docling nettoie les logos, extrait les tableaux en CSV et calcule un **Score de Confiance**.
*Consigne :* Si le rapport indique des blocs 🔴, une correction manuelle du Markdown est obligatoire avant l'étape 2.

---

## 🟡 ÉTAPE 2 : Extraction IA (ABB-02)
Utilisation du LLM Local pour isoler les obligations.

**Action :**
```bash
python 00-GOUVERNANCE/scripts/extract-requirements.py \
  "path/to/rfp-structured.md" \
  "01-REFERENCE/templates/artifacts/prompt-extraction-exigences.md" \
  "output/exigences.json"
```

**Que fait l'IA ?**
Elle scanne le texte, cherche les mots-clés de l'obligation (*doit, shall...*) et produit un JSON structuré. Elle détecte aussi les **contradictions** entre clauses.

---

## 🔴 ÉTAPE 3 : Production du Référentiel
Génération du fichier maître du projet.

**Action :**
```bash
python 00-GOUVERNANCE/scripts/json-to-requirements.py "in.json" "REQUIREMENTS.md" "Client" "Objet"
```

**Le résultat final :**
Un fichier `REQUIREMENTS.md` tabulaire, classé par domaine (BDAT) et priorité. C'est ce fichier qui sera utilisé par l'équipe pour répondre au client.

---

## 🛠 Cas Particulier : Le mode Manuel (SBB-01A)
Si l'IA échoue (scan illisible), suivre le protocole en 3 passes :
1. **Cartographie** (Sections)
2. **Extraction** (Shall/Must)
3. **Audit** (Tables)

---
*Fin du Guide Opérationnel v2.0*
