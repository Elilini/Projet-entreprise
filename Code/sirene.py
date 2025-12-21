import csv
import os

SIRENE_DATA = {}
CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "sirene.csv")

def load_sirene_data():
    global SIRENE_DATA
    if not os.path.exists(CSV_PATH):
        print(f"❌ Fichier CSV introuvable : {CSV_PATH}")
        return

    try:
        # On utilise utf-8-sig pour tenter de supprimer le \ufeff automatiquement
        with open(CSV_PATH, newline="", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            
            # --- CORRECTION CRUCIALE ICI ---
            # On nettoie manuellement chaque nom de colonne pour enlever le \ufeff restant
            reader.fieldnames = [name.replace('\ufeff', '').strip() for name in reader.fieldnames]
            
            print(f"📋 Colonnes nettoyées : {reader.fieldnames[:3]}")

            for row in reader:
                # Maintenant on peut chercher 'SIREN' sans le bug
                raw_siren = row.get("SIREN")
                if raw_siren:
                    siren_clean = "".join(filter(str.isdigit, str(raw_siren)))
                    SIRENE_DATA[siren_clean] = row
                    
        print(f"✅ {len(SIRENE_DATA)} entreprises chargées avec succès !")
    except Exception as e:
        print(f"❌ Erreur lors du chargement : {e}")

load_sirene_data()

def get_company_info(siren: str):
    siren_nettoye = "".join(filter(str.isdigit, str(siren)))
    entreprise = SIRENE_DATA.get(siren_nettoye)
    if not entreprise:
        return {"error": "non_trouve"}
    
    return {
        "nom": entreprise.get("Nom ou raison sociale de l'entreprise") or "Inconnu",
        "activite": entreprise.get("Activité principale de l'établissement") or "N/A"
    }