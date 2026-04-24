import httpx          # Pour envoyer les documents au serveur Docling (requêtes HTTP)
from pathlib import Path  # Pour manipuler les dossiers et fichiers de manière moderne
import pandas as pd      # Pour transformer les tableaux extraits en fichiers Excel/CSV
import json             # Pour lire et écrire les rapports techniques (JSON)
import sys              # Pour interagir avec l'ordinateur (quitter en cas d'erreur)
import base64           # Pour transformer le texte des images (Base64) en vraies photos PNG
import hashlib          # Pour créer une "empreinte digitale" (SHA256) unique du fichier
import time             # Pour gérer les temps de pause et les essais
import io               # Pour manipuler des données en mémoire sans créer de fichiers temporaires
from datetime import datetime # Pour horodater précisément chaque traitement
from docling_core.types.doc import DoclingDocument, PictureItem, TextItem # Types de données Docling
from PIL import Image    # La bibliothèque "Pillow" pour découper et sauvegarder les images

# --- AGENTS DE SÉCURITÉ ---
# On essaie d'importer PyMuPDF (outil de lecture binaire de PDF). 
# S'il n'est pas installé, on désactive simplement la "réconciliation" (double vérification).
try:
    import pymupdf
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

# --- CONFIGURATION DES RÈGLES MÉTIER ---
# Ces réglages permettent de calibrer la "sensibilité" de l'intelligence artificielle.

DOCLING_SERVE_URL = "http://localhost:5001/v1/convert/file" # Adresse du cerveau de parsing
SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".pptx", ".xlsx", ".html"} # Formats acceptés

# Seuil pour distinguer un LOGO d'un SCHÉMA TECHNIQUE.
# Un logo fait généralement moins de 3000 unités de surface.
MIN_IMAGE_AREA_LOGO = 3000 

# Seuils de confiance OCR (Reconnaissance de caractères)
CONFIDENCE_THRESHOLD_CRITICAL = 0.70  # En dessous de 70%, on met un 🔴 (Alerte rouge)
CONFIDENCE_THRESHOLD_WARNING = 0.90   # En dessous de 90%, on met un ⚠️ (Vigilance)

# Seuil de réconciliation : si Docling et PyMuPDF divergent de plus de 15%, on alerte.
RECONCILIATION_RATIO_THRESHOLD = 0.85

# Seuil de détection de schéma : si un document a moins de 5 blocs de texte, c'est un dessin.
SCHEMA_DETECTION_TEXT_LIMIT = 5

# --- NOMS DES FICHIERS DE SORTIE ---
MARKDOWN_ENRICHED_NAME = "rfp-structured.md"
BLOCKS_TO_VERIFY_NAME = "blocks-to-verify.json"
RECONCILIATION_REPORT_NAME = "rapport-reconciliation.json"
METADATA_NAME = "rapport-parsing.json"

# --- CLASSIFICATION AUTOMATIQUE ---
# On devine le rôle contractuel d'un document selon les mots trouvés dans son nom.
FILENAME_TO_ROLE = {
    "cctp": "CCTP", "technique": "CCTP", "rc": "RC", 
    "ccap": "CCAP", "bpu": "BPU", "dpgf": "DPGF", "annexe": "ANNEXE"
}

# Pour chaque rôle, on définit quel "cerveau" (Prompt) l'IA utilisera à l'étape ABB-02.
ROLE_TO_PROMPT = {
    "CCTP": "ABB-02-extraction-exigences.md", 
    "CCAP": "ABB-03-analyse-contractuelle.md", 
    "RC": "ABB-02-extraction-criteres-selection.md", 
    "ANNEXE": "ABB-02-extraction-contexte-as-is.md", 
    "UNKNOWN": "ABB-02-extraction-exigences.md"
}

# Priorité de traitement : on veut toujours analyser le CCTP en premier.
ROLE_PRIORITY = {"CCTP": 1, "CCAP": 2, "RC": 3, "ANNEXE": 4, "BPU": 5, "DPGF": 6, "UNKNOWN": 99}

# Conversion des types de texte Docling vers la mise en forme Markdown (lisible par l'homme).
LABEL_TO_MARKDOWN = {
    "heading_1": "# ", "heading_2": "## ", "heading_3": "### ", 
    "heading_4": "#### ", "heading_5": "##### ", 
    "caption": "> ", "footnote": "*Note : ", "list_item": "- "
}

# --- OUTILS DE VÉRIFICATION ---

def check_server_health(base_url, retries=3, delay=5):
    """Vérifie si le moteur Docker Docling est allumé et prêt à travailler."""
    url = base_url.replace("/v1/convert/file", "/health")
    for i in range(retries):
        try:
            r = httpx.get(url, timeout=5)
            if r.status_code == 200:
                print("✅ Serveur Docling opérationnel")
                return True
        except httpx.ConnectError:
            print(f"⏳ Serveur non joignable ({i+1}/{retries})... Vérifiez Docker.")
        except httpx.TimeoutException:
            print(f"⏳ Le serveur sature ({i+1}/{retries})... On attend un peu.")
        except Exception as e:
            print(f"❌ Erreur fatale : {type(e).__name__}")
            return False 
        if i < retries - 1: time.sleep(delay)
    return False

def detect_ocr_needed(path):
    """
    Décide si on doit activer l'OCR (lecture pixel par pixel).
    On prend un échantillon de pages (début, milieu, fin) pour ne pas être trompé
    par une page de garde qui contient souvent très peu de texte.
    """
    if path.suffix.lower() != ".pdf" or not PYMUPDF_AVAILABLE: return False
    try:
        doc = pymupdf.open(path)
        total = len(doc)
        if total <= 4: sample = list(range(total))
        else: sample = [total // 4, total // 2, (3 * total) // 4, total - 1]
        
        txt_found = sum(1 for i in sample if len(doc[i].get_text().strip()) > 100)
        # Si moins de 60% des pages testées ont du texte, c'est probablement un scan.
        needs_ocr = (txt_found / len(sample)) < 0.6
        if needs_ocr:
            print(f"  → OCR activé ({txt_found}/{len(sample)} pages avec texte)")
        return needs_ocr
    except: return True

def compute_sha256(file_path):
    """Calcule l'empreinte unique du fichier pour garantir son intégrité (Preuve d'Audit)."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""): sha256.update(chunk)
    return sha256.hexdigest()

# --- COEUR DU TRAITEMENT (Le coeur de la machine) ---

def process_single_file(file_path: Path, base_output_dir: Path):
    """Transforme un document brut en une Source de Vérité structurée et certifiée."""
    
    # 1. PRÉPARATION DE L'ENVIRONNEMENT
    # On crée un dossier dédié par document pour ne pas mélanger les tableaux et les images.
    doc_stem = file_path.stem
    out_path = base_output_dir / doc_stem
    img_path, tab_path = out_path / "images", out_path / "tables"
    for d in [out_path, img_path, tab_path]: d.mkdir(parents=True, exist_ok=True)

    role = next((r for k, r in FILENAME_TO_ROLE.items() if k in doc_stem.lower()), "UNKNOWN")
    print(f"\n📄 {file_path.name} [Rôle détecté : {role}]")
    needs_ocr = detect_ocr_needed(file_path)

    try:
        # 2. APPEL À L'IA DE PARSING (DOCLING)
        with open(file_path, "rb") as f:
            resp = httpx.post(
                DOCLING_SERVE_URL, 
                files={"files": (file_path.name, f)}, 
                data={
                    "to_formats": "json", 
                    "do_ocr": str(needs_ocr).lower(), 
                    "include_pictures": "true", 
                    "include_page_images": "true" # On demande les images de page au cas où
                }, 
                timeout=600
            )
            resp.raise_for_status()
        
        # On valide le format du résultat reçu
        data = resp.json()
        doc = DoclingDocument.model_validate(data["document"]["json_content"])
        # On stocke la preuve brute (JSON) : c'est notre Source de Vérité technique.
        (out_path / "SOURCE-OF-TRUTH.json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

        # 3. CHARGEMENT DES IMAGES DE PAGES (Backup pour les schémas vectoriels type Visio)
        page_imgs = {}
        for pi in data.get("document", {}).get("page_images", []):
            if pi.get("uri", "").startswith("data:image/"):
                img_data = base64.b64decode(pi["uri"].split(",", 1)[1])
                page_imgs[pi["page_no"]] = Image.open(io.BytesIO(img_data))

        # 4. EXTRACTION INTELLIGENTE DES IMAGES (IA + CROP + FILTRE ANTI-LOGO)
        extracted_imgs, img_idx = {}, 0
        for pic in doc.pictures:
            if not pic.prov: continue
            bbox = pic.prov[0].bbox
            # FILTRE : Si l'image est trop petite (Area), c'est un logo. On l'ignore.
            if abs(bbox.r - bbox.l) * abs(bbox.t - bbox.b) < MIN_IMAGE_AREA_LOGO:
                continue
            
            img_idx += 1
            fname = f"picture-{img_idx:02d}.png"
            saved = False
            
            # Méthode A : L'IA a réussi à extraire directement le bitmap (pixels).
            if pic.image and str(pic.image.uri).startswith("data:image/"):
                (img_path / fname).write_bytes(base64.b64decode(str(pic.image.uri).split(",", 1)[1]))
                saved = True
            # Méthode B : C'est un schéma vectoriel (Visio). On le découpe dans l'image de la page.
            elif pic.prov[0].page_no in page_imgs:
                p_img, w, h = page_imgs[pic.prov[0].page_no], *page_imgs[pic.prov[0].page_no].size
                l, t, r, b = bbox.l, h - bbox.t, bbox.r, h - bbox.b # Conversion coordonnées points -> pixels
                try:
                    p_img.crop((l, t, r, b)).save(img_path / fname)
                    saved = True
                except: pass
            
            if saved: extracted_imgs[pic.self_ref] = f"images/{fname}"

        # 5. CONSTRUCTION DU MARKDOWN ENRICHI (Carburant pour l'IA ABB-02)
        lines, low_conf, p_texts = [], [], {}
        for item, _ in doc.iterate_items():
            if isinstance(item, TextItem):
                text, label = item.text.strip(), item.label
                if not text: continue
                # On indexe le texte par page pour la réconciliation finale
                for p in item.prov: p_texts.setdefault(p.page_no, []).append(text)
                
                # On récupère le score de confiance OCR (fiabilité du texte)
                conf = [getattr(p, "confidence", None) for p in item.prov if getattr(p, "confidence", None) is not None]
                avg = sum(conf)/len(conf) if conf else None
                
                # Mise en forme selon la hiérarchie (Titres, Listes...)
                if label in LABEL_TO_MARKDOWN:
                    lines.append(f"\n{LABEL_TO_MARKDOWN[label]}{text}\n")
                elif label != "table_of_contents":
                    # Ajout des drapeaux de vigilance pour le LLM en aval
                    flag = ""
                    if avg is not None:
                        if avg < CONFIDENCE_THRESHOLD_CRITICAL:
                            flag = "🔴"; low_conf.append({"text": text[:50], "conf": avg, "page": item.prov[0].page_no})
                        elif avg < CONFIDENCE_THRESHOLD_WARNING: flag = "⚠️"
                        lines.append(f"[CONF: {avg:.2f}] {flag} {text}\n")
                    else:
                        lines.append(f"{text}\n")
            
            # Insertion des images à leur place exacte dans le texte
            elif isinstance(item, PictureItem) and item.self_ref in extracted_imgs:
                lines.append(f"\n![Illustration]({extracted_imgs[item.self_ref]})\n")

        # 6. MODE SECOURS : CAPTURE HD PYMUPDF (Pour les documents purement graphiques)
        if not lines and not extracted_imgs and file_path.suffix.lower() == ".pdf" and PYMUPDF_AVAILABLE:
            print("    → Mode Schéma Pur détecté : Capture HD des pages activée.")
            mu = pymupdf.open(file_path)
            for i, page in enumerate(mu):
                pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2)) # Zoom 2x pour la qualité
                fname = f"page-capture-{i+1:02d}.png"
                pix.save(img_path / fname)
                extracted_imgs[f"page_{i+1}"] = f"images/{fname}"
                lines.append(f"\n![Schéma]({extracted_imgs[f'page_{i+1}']})\n")
            mu.close()

        # Écriture du Markdown final avec en-têtes de contexte cachés
        role_hdr = f"<!-- DOCUMENT_ROLE: {role} -->\n<!-- SOURCE: {file_path.name} -->\n<!-- OCR_USED: {needs_ocr} -->\n\n"
        (out_path / MARKDOWN_ENRICHED_NAME).write_text(role_hdr + "\n".join(lines), encoding="utf-8")
        if low_conf:
            (out_path / BLOCKS_TO_VERIFY_NAME).write_text(json.dumps(low_conf, indent=2), encoding="utf-8")

        # 7. EXTRACTION DES TABLEAUX (Fichiers CSV exploitables par Excel/Pandas)
        tables_failed = []
        for i, t in enumerate(doc.tables):
            try:
                # On passe 'doc=doc' pour que Docling puisse résoudre les cellules fusionnées
                t.export_to_dataframe(doc=doc).to_csv(tab_path / f"table-{i+1:02d}.csv", index=False)
            except Exception as e:
                tables_failed.append({"index": i+1, "erreur": str(e)})

        # 8. RÉCONCILIATION (Double vérification binaire/IA pour détecter les oublis)
        divergences = []
        if file_path.suffix.lower() == ".pdf" and PYMUPDF_AVAILABLE:
            mu_doc = pymupdf.open(file_path)
            for n in range(1, len(mu_doc) + 1):
                t1 = mu_doc[n-1].get_text().replace(" ","") # Texte binaire
                t2 = "".join(p_texts.get(n, [])).replace(" ","") # Texte IA Docling
                l1, l2 = len(t1), len(t2)
                # Si l'écart de longueur est trop important, on flague la page.
                if max(l1, l2) > 0 and min(l1, l2)/max(l1, l2) < RECONCILIATION_RATIO_THRESHOLD:
                    divergences.append({"page": n, "ratio": round(min(l1, l2)/max(l1, l2), 2)})
            (out_path / RECONCILIATION_REPORT_NAME).write_text(json.dumps(divergences, indent=2), encoding="utf-8")

        # 9. GÉNÉRATION DES MÉTADONNÉES ET STATUT FINAL
        statut = "BRUT_A_VERIFIER" if (divergences or low_conf or tables_failed) else "FIABLE"
        meta = {
            "sha256":             compute_sha256(file_path),
            "role":               role,
            "prompt_abb02":       ROLE_TO_PROMPT.get(role),
            "statut":             statut,
            "date":               datetime.now().isoformat(),
            "stats": {
                "pages":           len(doc.pages),
                "tables":          len(doc.tables),
                "images_utiles":   len(extracted_imgs),
                "incertitudes_ocr": len(low_conf),
                "tables_failed":   len(tables_failed)
            },
            "tables_failed_detail": tables_failed
        }
        (out_path / METADATA_NAME).write_text(json.dumps(meta, indent=2), encoding="utf-8")
        print(f"  → Terminé : {statut} ({len(extracted_imgs)} images extraites)")
        
        # Résumé pour le MANIFEST global
        return {
            "fichier": file_path.name, 
            "role": role, 
            "statut": statut, 
            "markdown_file": str((out_path / MARKDOWN_ENRICHED_NAME).relative_to(base_output_dir.parent)),
            "tables_dir": str(tab_path.relative_to(base_output_dir.parent))
        }
    except Exception as e:
        print(f"  ❌ ÉCHEC CRITIQUE : {e}")
        return {"fichier": file_path.name, "statut": "ERREUR"}

# --- ORCHESTRATION DU LOT (Batch) ---

def main(input_path, output_dir):
    """Fonction de lancement : gère le dossier source et crée le Manifeste final."""
    if not check_server_health(DOCLING_SERVE_URL):
        sys.exit(1)
    
    src, out = Path(input_path), Path(output_dir)
    files, seen = [], set()
    
    # On identifie tous les fichiers valides dans le dossier (en ignorant les doublons et fichiers Windows)
    if src.is_file():
        files = [src]
    else:
        for ext in SUPPORTED_EXTENSIONS:
            for f in list(src.rglob(f"*{ext}")) + list(src.rglob(f"*{ext.upper()}")):
                if ":" not in f.name and f.resolve() not in seen:
                    seen.add(f.resolve())
                    files.append(f)
    
    if not files:
        print("Aucun document trouvé."); return
    
    print(f"🚀 Lancement Batch Ingestion ABB-01 : {len(files)} document(s).")
    
    # On traite chaque fichier un par un
    results = [process_single_file(f, out) for f in sorted(files)]
    
    # On crée le MANIFEST.json : c'est la feuille de route pour l'IA ABB-02
    sorted_res = sorted(results, key=lambda r: ROLE_PRIORITY.get(r.get("role", "UNKNOWN"), 99))
    manifest = {
        "source": str(src.absolute()), 
        "date": datetime.now().isoformat(), 
        "statut_global": "VÉRIFICATION_REQUISE" if any(r.get("statut") != "FIABLE" for r in sorted_res) else "FIABLE", 
        "ordre_traitement_abb02": [r["markdown_file"] for r in sorted_res if r.get("statut") != "ERREUR" and r.get("role") not in ("BPU", "DPGF")], 
        "documents_chiffrage": [r["tables_dir"] for r in sorted_res if r.get("role") in ("BPU", "DPGF")], 
        "details": sorted_res
    }
    (out / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n✅ MANIFEST.json généré. Votre bibliothèque est prête pour l'IA.")

if __name__ == "__main__":
    # Point d'entrée du script : python parse-rfp.py <source> <destination>
    if len(sys.argv) < 3:
        print("Usage : python parse-rfp.py <dossier_source> <dossier_sortie>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
