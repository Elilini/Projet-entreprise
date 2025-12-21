import csv
import os

# Chemin vers le CSV
CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "sirene.csv")

# Dictionnaire pour stocker les données
SIRENE_DATA = {}

def load_sirene_data():
    global SIRENE_DATA

    if not os.path.exists(CSV_PATH):
        print("❌ Fichier CSV SIRENE introuvable :", CSV_PATH)
        return

    with open(CSV_PATH, newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        print("Colonnes détectées :", reader.fieldnames)
        for row in reader:
            siren = row.get('SIREN') or row.get('\ufeffSIREN')
            if siren:
                siren = siren.strip()
                SIRENE_DATA[siren] = row

    print(f"✅ {len(SIRENE_DATA)} entreprises chargées depuis le CSV SIRENE")

def get_company_info(siren: str):
    siren = siren.strip()
    if not siren.isdigit() or len(siren) != 9:
        return {"error": "SIREN invalide (9 chiffres requis)"}

    entreprise = SIRENE_DATA.get(siren)
    if not entreprise:
        return {"error": "Entreprise introuvable dans la base SIRENE"}

    return {
        "nom": entreprise.get("Nom ou raison sociale de l'entreprise", "Non défini"),
        "activite": entreprise.get("Activité principale de l'entreprise", "Non défini"),
        "etat": entreprise.get("Nature juridique de l'entreprise", "Inconnu"),
        "date_creation": entreprise.get("Année et mois de création de l'entreprise", "Non définie"),
        "categorie": entreprise.get("Catégorie d'entreprise", "Non définie"),
        "effectifs": entreprise.get("Tranche d'effectif salarié de l'entreprise", "Non défini")
    }

# Chargement des données
load_sirene_data()

# Boucle interactive
while True:
    siren_input = input("\nTape un SIREN (9 chiffres) ou 'exit' pour quitter : ")
    if siren_input.lower() == 'exit':
        break
    info = get_company_info(siren_input)
    print(info)
