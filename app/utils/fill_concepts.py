import requests
import json
import os
import dotenv
from sqlalchemy import create_engine

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("/app", "")
dotenv.load_dotenv(os.path.join(BASE_DIR, '.env'))
KEY_WS = os.environ["KEY_WS"]
URL_ROOT  = os.environ["URL_ROOT"]
SUPPORT  = os.environ["SUPPORT"]
REFERENTIELS  = os.environ["REFERENTIELS"]
COULEUR  = os.environ["COULEUR"]
GENERALITE_ARCHITECTURE  = os.environ["GENERALITE_ARCHITECTURE"]
MOT_CLE  = os.environ["MOT_CLE"]
ENTITE  = os.environ["ENTITE"]
MH = os.environ["CLASSEMENT_MH"]

# vider les tables existantes
SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
db_path = SQLALCHEMY_DATABASE_URI.replace("///", "///"+BASE_DIR+ "/app/")
engine = create_engine(db_path)
try:
    engine.execute("delete from concept_text")
    engine.execute("delete from concept")
    engine.execute("delete from referentiel_text")
    engine.execute("delete from referentiel")
except:
    pass


# créer les référentiels
referentiels  = json.loads(REFERENTIELS)
for ref in referentiels:
    print(ref)
    post_headers = {"ws-key": KEY_WS}
    r = requests.post(URL_ROOT + "/insert_referentiel", data=json.dumps(ref), headers=post_headers)
    print(r.status_code)

# insertion des couleurs 
couleurs  = json.loads(COULEUR)
for couleur in couleurs:
    print(couleur)
    post_headers = {"ws-key": KEY_WS}
    r = requests.post(URL_ROOT + "/insert_concept", data=json.dumps(couleur), headers=post_headers)
    print(r.status_code)

# insertion des mh 
mhs  = json.loads(MH)
for mh in mhs:
    print(mh)
    post_headers = {"ws-key": KEY_WS}
    r = requests.post(URL_ROOT + "/insert_concept", data=json.dumps(mh), headers=post_headers)
    print(r.status_code)

# insertion des supports 
supports  = json.loads(SUPPORT)
for support in supports:
    print(support)
    post_headers = {"ws-key": KEY_WS}
    r = requests.post(URL_ROOT + "/insert_concept", data=json.dumps(support), headers=post_headers)
    print(r.status_code)

# insertion des generalites 
generalites  = json.loads(GENERALITE_ARCHITECTURE)
for gen in generalites:
    print(gen)
    post_headers = {"ws-key": KEY_WS}
    r = requests.post(URL_ROOT + "/insert_concept", data=json.dumps(gen), headers=post_headers)
    print(r.status_code)

# insertion des entités 
entites  = json.loads(ENTITE)
for entite in entites:
    print(entite)
    post_headers = {"ws-key": KEY_WS}
    r = requests.post(URL_ROOT + "/insert_concept", data=json.dumps(entite), headers=post_headers)
    print(r.status_code)

#insertion des mots clés
mots  = json.loads(MOT_CLE)
for mot in mots:
    print(mot)
    post_headers = {"ws-key": KEY_WS}
    r = requests.post(URL_ROOT + "/insert_concept", data=json.dumps(mot), headers=post_headers)
    print(r.status_code)