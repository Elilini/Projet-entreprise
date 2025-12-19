import requests
from duckduckgo_search import DDGS
import ollama

def recherche_web_secours(siren):
    """Recherche des informations sur une entreprise via DuckDuckGo si absente du CSV."""
    print(f"🌐 Recherche Web pour le SIREN : {siren}...")
    try:
        with DDGS() as ddgs:
            # On cherche spécifiquement le nom de l'entreprise lié au SIREN
            requete = f"entreprise SIREN {siren} société"
            resultats = list(ddgs.text(requete, max_results=3))
            
            if resultats:
                # On extrait le titre du premier résultat (souvent le nom de la boîte)
                premier_resultat = resultats[0]
                nom_estime = premier_resultat['title'].split("-")[0].split(":")[0].strip()
                
                print(f"✅ Trouvé sur le Web : {nom_estime}")
                return {
                    "nom": nom_estime,
                    "description": premier_resultat['body'],
                    "siren": siren,
                    "url": premier_resultat['href']
                }
    except Exception as e:
        print(f"❌ Erreur DuckDuckGo : {e}")
    
    return None

def get_news(nom_entreprise):
    """Récupère les dernières actualités."""
    try:
        with DDGS() as ddgs:
            resultats = list(ddgs.text(f"actualité {nom_entreprise}", max_results=5))
            return [r['title'] for r in resultats]
    except:
        return ["Aucune actualité récente trouvée."]

def ollama_analyse_et_diagnostic(nom, contexte, news):
    news_formatted = "\n".join([f"- {n}" for n in news]) if news else "Aucune actualité trouvée."

    # AJOUT DE L'INSTRUCTION DE LANGUE
    prompt = f"""
    RÉDIGE TON RAPPORT EXCLUSIVEMENT EN FRANÇAIS.

    Tu es un Senior Strategist chez Goldman Sachs. Ton objectif est de fournir un audit de santé et une projection 2050 pour l'entreprise {nom}.

    DONNÉES DISPONIBLES :
    - Fiche Entreprise : {contexte}
    - Actualités brûlantes : {news_formatted}

    CONSIGNES DE RÉDACTION (STRICTES) :
    - LANGUE : RÉDIGE TOUT EN FRANÇAIS (Vocabulaire soutenu et professionnel).
    - Longueur : Rédige un rapport très détaillé (minimum 600-800 mots).
    - Croisement d'infos : Analyse comment les news récentes impactent directement le secteur de {nom}. 
    - Secteur : Identifie le secteur d'activité et discute des enjeux (ex: IA, régulations européennes, transition énergétique).

    STRUCTURE DU RAPPORT :
    1. 🔍 ANALYSE DE SANTÉ ET POSITIONNEMENT : Décortique le score de 85/100.
    2. 📰 DÉCRYPTAGE DE L'ACTUALITÉ & IMPACT SECTORIEL : Analyse les news citées.
    3. 🚀 PERSPECTIVES STRATÉGIQUES 2050 : Comment l'entreprise doit-elle pivoter ?
    4. ⚠️ RISQUES CRITIQUES : Cite 3 menaces majeures.

    IMPORTANT : TOUT LE RAPPORT DOIT ÊTRE EN LANGUE FRANÇAISE.
    """

    import requests
    try:
        response = requests.post('http://localhost:11434/api/generate', 
                                 json={
                                     "model": "mistral", 
                                     "prompt": prompt, 
                                     "stream": False,
                                     "options": {
                                         "num_predict": 2048,
                                         "temperature": 0.7
                                     }
                                 }, timeout=600) 
        return response.json().get('response', "Erreur : Rapport non généré.")
    except Exception as e:
        return f"Erreur de connexion à l'IA : {str(e)}"