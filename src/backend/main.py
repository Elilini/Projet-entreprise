from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests

# 1. IMPORTS DES FONCTIONS LOCALES
from sirene import get_company_info
from analyse import get_news, ollama_analyse_et_diagnostic, recherche_web_secours

app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/diagnostic/{siren}")
async def generer_diagnostic(siren: str):
    print(f"--- 🔍 Analyse en cours pour le SIREN : {siren} ---")
    
    try:
        # 1. IDENTIFICATION DE L'ENTREPRISE
        infos = get_company_info(siren)
        if isinstance(infos, dict) and "error" not in infos:
            source = "Base de données interne"
            nom = infos.get("nom")
        else:
            print("Recherche web de secours active...")
            web_res = recherche_web_secours(siren)
            source = "Recherche Web (Live)"
            nom = web_res.get("nom", f"Entreprise {siren}")
            infos = web_res

        # 2. COLLECTE DES ACTUALITÉS
        news = get_news(nom)
        
        # 3. GÉNÉRATION DU RAPPORT EXPERT 
        # On enrichit le contexte pour forcer l'IA à croiser les infos
        contexte_expert = f"Entreprise: {nom}. Données Sirene: {str(infos)}. Note de santé: 85/100. Croissance moyenne: 3.5%."
        
        print("Génération du rapport stratégique (Ollama)...")
        rapport_ia_texte = ollama_analyse_et_diagnostic(nom, contexte_expert, news)

        # 4. PRÉPARATION DES DONNÉES GRAPHIQUES (Projection 2050)
        annees = [str(a) for a in range(2022, 2051)]
        historique_reel = [100, 105, 115] # 2022, 2023, 2024
        
        last_val = historique_reel[-1]
        previsions_final = [None] * (len(historique_reel) - 1)
        
        # Simulation mathématique de croissance jusqu'en 2050
        for i in range(0, len(annees) - len(historique_reel) + 1):
            val = last_val * (1.035 ** i)
            previsions_final.append(round(val, 2))

        # 5. ENVOI DES DONNÉES AU FRONTEND
        return {
            "entreprise": nom,
            "source": source,
            "news_titres": news if news else ["Aucune actualité sectorielle récente trouvée."],
            "rapport_ia": {"texte": rapport_ia_texte},
            "graph": {
                "labels": annees,
                "historique": historique_reel + [None] * (len(annees) - len(historique_reel)),
                "prevision": previsions_final,
                "score": 85,
                "co2_labels": ["2024", "2030", "2040", "2050"],
                "co2_data": [100, 75, 40, 5]
            }
        }
        
    except Exception as e:
        print(f"❌ ERREUR SERVEUR : {str(e)}")
        return {"erreur": "Une erreur interne est survenue lors de l'analyse."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)