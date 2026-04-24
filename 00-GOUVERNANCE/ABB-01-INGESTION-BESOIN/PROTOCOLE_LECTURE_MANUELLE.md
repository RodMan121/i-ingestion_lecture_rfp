# SBB-01A — Lecture Manuelle Structurée

**Condition d'activation :** Niveau 0 / PDF scanné / délai < 2j

## Protocole Opérationnel

### ÉTAPE 1 — Lecture en 2 passes
*Ne pas écrire pendant la première passe.*

**PASSE 1 — Lecture rapide (20-30 min)**
- Objectif : cartographier le document.
- Identifier les sections principales.
- Repérer les tableaux d'exigences.
- Marquer les zones denses (surlignage jaune).
- Marquer les contradictions ou ambiguïtés (surlignage rouge).

**PASSE 2 — Extraction structurée (60-90 min)**
- Objectif : alimenter `REQUIREMENTS.md`.
- Parcourir section par section.
- Extraire uniquement les *shall / doit / obligatoire / must*.
- Ignorer les éléments descriptifs sans obligation.
- Numéroter séquentiellement : EX-001, EX-002…

### ÉTAPE 2 — Structuration dans REQUIREMENTS.md
Pour chaque exigence extraite :
- **Référence** (EX-XXX)
- **Intitulé** (reformulation concise)
- **Page source**
- **Type** : F/T/O/C/R
- **Domaine BDAT** : B/D/A/T
- **Priorité** : Obligatoire / Souhaitable / Éliminatoire

### ÉTAPE 3 — Vérification des tableaux
- Recopier la structure complète des tableaux du CCTP.
- Vérifier que chaque ligne est bien reportée dans `REQUIREMENTS.md`.

## ⚠️ Signal d'alerte
**STOP** si vous commencez à :
- Interpréter une exigence (→ ABB-02).
- Chercher une réponse (→ D1).
- Évaluer la faisabilité (→ B1).

*ABB-01 est une tâche d'extraction pure.*
