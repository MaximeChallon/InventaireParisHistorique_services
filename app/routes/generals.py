from flask import redirect, url_for, request
from ..app import app, db
from ..constantes import KEY_WS, URL_ROOT
from ..utils.service_identifiant import IdentifierService
import requests
import json
import re


@app.route("/select/<int:num_inventaire>", methods=['POST'])
def select(num_inventaire):
    json_retour = {}
    headers = request.headers
    ws_key = headers.get("ws-key")
    if KEY_WS == ws_key:
        json_retour["status"]  =  "ok"
    else:
        json_retour["status"]  =  "not allowed"
    return json_retour

@app.route("/insert/<int:num_inventaire>", methods=['POST'])
def insert(num_inventaire):
    json_retour = {}
    headers = request.headers
    ws_key = headers.get("ws-key")
    data = request.get_json(force=True)
    if KEY_WS == ws_key:
        json_retour["status"]  =  "ok"

        # delete de l'existant
        try:
            ancieninstance = db.engine.execute("select instanceid from instance where code = '"+str(num_inventaire)+"'").fetchall()[0][0]
            db.engine.execute("delete from instance_identifier where instanceid = '"+str(ancieninstance)+"'")
            db.engine.execute("delete from adresse where instanceid = '"+str(ancieninstance)+"'")
            db.engine.execute("delete from geolocalisation where instanceid = '"+str(ancieninstance)+"'")
            db.engine.execute("delete from instance_concept where instanceid = '"+str(ancieninstance)+"'")
            db.engine.execute("delete from instance_agent where instanceid = '"+str(ancieninstance)+"'")
            db.engine.execute("delete from instance_text where instanceid = '"+str(ancieninstance)+"'")
            db.engine.execute("delete from instance_instance where sourceinstanceid = '"+str(ancieninstance)+"' or targetinstanceid = '"+str(ancieninstance)+"'")
            db.engine.execute("delete from instance where instanceid = '"+str(ancieninstance)+"'")

            events = str([event[0]  for event in db.engine.execute("select evenementid from instance_evenement where instanceid = '"+str(ancieninstance)+"'").fetchall()]).replace("\"", "'").replace("[", "(").replace("]", ")")
            db.engine.execute("delete from instance_evenement where instanceid = '"+str(ancieninstance)+"'")
            db.engine.execute("delete from evenement where evenementid in "+str(events))

            activites = str([activite[0]  for activite in db.engine.execute("select activiteid from instance_activite where instanceid = '"+str(ancieninstance)+"'").fetchall()]).replace("\"", "'").replace("[", "(").replace("]", ")")
            db.engine.execute("delete from instance_activite where instanceid = '"+str(ancieninstance)+"'")
            db.engine.execute("delete from activite where activiteid in "+str(activites))
        except Exception as e:
            if str(e) != "list index out of range":
                print(e)

        # création de l'instance
        instanceid  = IdentifierService.create("instance", str(num_inventaire))
        instancetype = (db.engine.execute("select conceptid from concept where code = '"+data["type"]+"'")).fetchall()[0][0] 
        db.engine.execute("INSERT into instance (instanceid, instancetype, code) values ('"+instanceid+"','"+ instancetype +"', '"+str(num_inventaire)+"')")

        #identifier
        identifierid = IdentifierService.create("identifier", str(num_inventaire))
        db.engine.execute("insert into instance_identifier(instanceid, identifierid, identifiertype, identifiervalue) values ('"+instanceid+"','"+identifierid+"','Numéro d''inventaire','"+str(num_inventaire)+"')")

        #adresse
        if "Rue" in data or "N_rue" in data:
            adresseid = IdentifierService.create("adresse", str(data["Rue"] if "Rue" in data else "") + (data["N_rue"] if "N_rue" in data else "") + str(num_inventaire))
            requete = ("insert into adresse(instanceid,adresseid, rue,adressetype "+
                (",numero" if "N_rue" in data else "") +
                (",arrondissement" if "Arrondissement" in data else "") +
                (",ville" if "Ville" in data else "") +
                (",departement" if "Departement" in data else "") +
            ") values (" +
                "'" + instanceid + "'" +
                ",'" + adresseid + "'" +
                ",'" + (data["Rue"].replace("'", "''") if "Rue" in data else "") + "'" +
                ",'Principale'" +
                (",'"+ data["N_rue"] +"'" if "N_rue" in data else "") +
                ("," + str(data["Arrondissement"]) if "Arrondissement" in data else "") +
                (",'" + str(data["Ville"]) + "'"  if "Ville" in data else "") +
                ("," + str(data["Departement"])  if "Departement" in data else "") +
            ")")
            db.engine.execute(requete)
        
        #TODO: sites

        # geoloc
        if "Latitude" in data and "Longitude" in data:
            geolocalisationid = IdentifierService.create("geolocalisation", str(data["Latitude"]) + str(data["Longitude"]) + str(num_inventaire))
            db.engine.execute("insert into geolocalisation(instanceid, geolocalisationid, latitude, longitude) values ('"+instanceid+"','"+geolocalisationid+"',"+str(data["Latitude"])+","+str(data["Longitude"])+")")
        
        # support 
        if "Support" in data:
            conceptid_support = db.engine.execute("select conceptid from concept where code = '"+data["Support"]+"'").fetchall()[0][0]
            db.engine.execute("insert into instance_concept(instanceid, conceptid, relationtype) values ('"+instanceid+"', '"+conceptid_support+"', 'Support')")
        
        # couleur 
        if "Couleur" in data:
            conceptid_couleur = db.engine.execute("select conceptid from concept where code = '"+data["Couleur"]+"'").fetchall()[0][0]
            db.engine.execute("insert into instance_concept(instanceid, conceptid, relationtype) values ('"+instanceid+"', '"+conceptid_couleur+"', 'Couleur')")
        
        #tailles: créer le concept s'il n'existe pas
        if "Taille" in data:
            try:
                conceptid_taille = db.engine.execute("select conceptid from concept where code = '"+data["Taille"].replace(" ", "")+"'").fetchall()[0][0]
            except: 
                # créer concept
                post_headers = {"ws-key": KEY_WS}
                envoi_json = {"Referentiel":"TAILLE"}
                envoi_json["Code"] = data["Taille"].replace(" ", "")
                envoi_json["Textes"] = [{"texttype": "Label", "textlang":"fre", "textvalue": data["Taille"].replace(" ", "")}]
                r = requests.post(URL_ROOT + "/insert_concept", data=json.dumps(envoi_json), headers=post_headers)
                conceptid_taille = json.loads((r.text))["conceptid"]
            db.engine.execute("insert into instance_concept(instanceid, conceptid, relationtype) values ('"+instanceid+"', '"+conceptid_taille+"', 'Taille')")

        # evenement: prise de vue
        if "Prise_vue" in data:
            eventid = IdentifierService.create("evenement", "prise de vue" + str(data["Prise_vue"]) + str(num_inventaire))
            db.engine.execute("insert into evenement(evenementid, datedebut, datefin, evenementtype) values ('"+eventid+"', '"+data["Prise_vue"]+"','"+data["Prise_vue"]+"', 'Prise de vue')")
            db.engine.execute("insert into instance_evenement(instanceid, evenementid, relationtype) values ('"+instanceid+"','"+eventid+"','Prise de vue')")

        #photographe: créer l'agent s'il n'existe pas
        if "Photographe" in data:
            try:
                agentid_photographe = db.engine.execute("select agentid from agent_text where textvalue = '"+data["Photographe"]+"'").fetchall()[0][0]
            except: 
                # créer agent
                post_headers = {"ws-key": KEY_WS}
                envoi_json = {"Type":"PP"}
                envoi_json["Textes"] = [{"texttype": "Identité civile", "textlang":"fre", "textvalue": data["Photographe"]}]
                r = requests.post(URL_ROOT + "/insert_agent", data=json.dumps(envoi_json), headers=post_headers)
                agentid_photographe = json.loads((r.text))["agentid"]
            db.engine.execute("insert into instance_agent(instanceid, agentid, relationtype) values ('"+instanceid+"', '"+agentid_photographe+"', 'Photographe')")

        #TODO: droits

        #dons: créer l'agent s'il n'existe pas
        if "Don" in data:
            try:
                agentid_don = db.engine.execute("select agentid from agent_text where textvalue = '"+data["Don"]+"'").fetchall()[0][0]
            except: 
                # créer agent
                post_headers = {"ws-key": KEY_WS}
                envoi_json = {"Type":"PP"}
                envoi_json["Textes"] = [{"texttype": "Identité civile", "textlang":"fre", "textvalue": data["Don"]}]
                r = requests.post(URL_ROOT + "/insert_agent", data=json.dumps(envoi_json), headers=post_headers)
                agentid_don = json.loads((r.text))["agentid"]
            db.engine.execute("insert into instance_agent(instanceid, agentid, relationtype) values ('"+instanceid+"', '"+agentid_don+"', 'Donateur')")

        # collection: créer l'instance si elle n'existe pas
        if "Collection" in data:
            try:
                instanceid_collection = db.engine.execute("select instanceid from instance_text where textvalue = '"+data["Collection"]+"' and texttype = 'Label'").fetchall()[0][0]
            except: 
                # créer instance
                post_headers = {"ws-key": KEY_WS}
                # récup conceptid du type COLLECTION
                conceptid_collection = db.engine.execute("select conceptid from concept where code = 'COLLECTION'").fetchall()[0][0]
                # insréer l'instance puis son texte
                instanceid_collection = IdentifierService.create("instance", str(data["Collection"]))
                db.engine.execute("insert into instance(instanceid, instancetype) values ('"+instanceid_collection+"', '"+conceptid_collection+"')")
                db.engine.execute("insert into instance_text(instanceid, textid, texttype, textlang, textvalue) values ('"+instanceid_collection+"', '"+IdentifierService.create("text", str(data["Collection"]) + "label")+"', 'Label', 'fre', '"+data["Collection"]+"')")
            db.engine.execute("insert into instance_instance(sourceinstanceid, targetinstanceid, relationtype) values ('"+instanceid+"', '"+instanceid_collection+"', 'Fait partie de')")
        
        # evenement: construction
        if "Construction" in data:
            eventid = IdentifierService.create("evenement", "construction" + str(data["Construction"]) + str(num_inventaire))
            try:
                db.engine.execute("insert into evenement(evenementid, datedebut, datefin, evenementtype) values ('"+eventid+"', '"+data["Construction"]+"','"+data["Construction"]+"', 'Construction')")
                db.engine.execute("insert into instance_evenement(instanceid, evenementid, relationtype) values ('"+instanceid+"','"+eventid+"','Construction')")
            except Exception as e:
                print(e)
        
        #architecte: créer l'agent s'il n'existe pas
        if "Architecte" in data:
            try:
                agentid_archi = db.engine.execute("select agentid from agent_text where textvalue = '"+data["Architecte"]+"'").fetchall()[0][0]
            except: 
                # créer agent
                post_headers = {"ws-key": KEY_WS}
                envoi_json = {"Type":"PP"}
                envoi_json["Textes"] = [{"texttype": "Identité civile", "textlang":"fre", "textvalue": data["Architecte"]}]
                r = requests.post(URL_ROOT + "/insert_agent", data=json.dumps(envoi_json), headers=post_headers)
                agentid_archi = json.loads((r.text))["agentid"]
            db.engine.execute("insert into instance_agent(instanceid, agentid, relationtype) values ('"+instanceid+"', '"+agentid_archi+"', 'Architecte')")

        # classement mh 
        if "MH" in data:
            conceptid_mh = db.engine.execute("select conceptid from concept inner join referentiel on referentiel.referentielid = concept.referentielid and referentiel.code = 'MH' where concept.code = '"+data["MH"]+"'").fetchall()[0][0]
            db.engine.execute("insert into instance_concept(instanceid, conceptid, relationtype) values ('"+instanceid+"', '"+conceptid_mh+"', 'Classement MH')")

        # légende
        if "Legende" in data:
            value_legende = (re.compile(r'[\n\r\t]').sub(" ", data["Legende"])).replace("'", "''")
            db.engine.execute("insert into instance_text (instanceid, textid, texttype, textlang, textvalue) values ('"+instanceid+"','"+IdentifierService.create("text", value_legende + "legende" + str(num_inventaire))+"','Légende','fre','"+value_legende+"')")
        
        # generalite
        if "Generalite" in data:
            conceptid_gen = db.engine.execute("select conceptid from concept inner join referentiel on referentiel.referentielid = concept.referentielid and referentiel.code = 'GENERALITE_ARCHITECTURE' where concept.code = '"+data["Generalite"]+"'").fetchall()[0][0]
            db.engine.execute("insert into instance_concept(instanceid, conceptid, relationtype) values ('"+instanceid+"', '"+conceptid_gen+"', 'Généralité d''architecture')")

        #mots clés
        if "Mots_cles" in data:
            for mot in data["Mots_cles"].replace("[", "").replace("]", "").split(","):
                try:
                    conceptid_mot = db.engine.execute("select conceptid from concept inner join referentiel on referentiel.referentielid = concept.referentielid and referentiel.code = 'MOT_CLE' where concept.code = "+mot+"").fetchall()[0][0]
                    db.engine.execute("insert into instance_concept(instanceid, conceptid, relationtype) values ('"+instanceid+"', '"+conceptid_mot+"', 'Mot clé')")
                except Exception as e:
                    print(mot + " : " + str(e))
        
        # autre adresse
        if "Autre_adresse" in data:
            value_aa= (re.compile(r'[\n\r\t]').sub(" ", data["Autre_adresse"])).replace("'", "''")
            db.engine.execute("insert into instance_text (instanceid, textid, texttype, textlang, textvalue) values ('"+instanceid+"','"+IdentifierService.create("text", value_aa + "autre_adresse" + str(num_inventaire))+"','Autre adresse','fre','"+value_aa+"')")

        # note
        if "Note" in data:
            value_note= (re.compile(r'[\n\r\t]').sub(" ", data["Note"])).replace("'", "''")
            db.engine.execute("insert into instance_text (instanceid, textid, texttype, textlang, textvalue) values ('"+instanceid+"','"+IdentifierService.create("text", value_note + "note" + str(num_inventaire))+"','Note','fre','"+value_note+"')")

        # cote base: identifiant d'instance
        if "Cote_base" in data:
            db.engine.execute("insert into instance_identifier(instanceid, identifierid, identifiertype, identifiervalue) values ('"+ instanceid +"', '"+IdentifierService.create("identifier", str(data["Cote_base"]))+"', 'Cote de la base de numérisations', '"+str(data["Cote_base"])+"')")
        
        # cote physique: identifiant d'instance
        if "Cote" in data:
            db.engine.execute("insert into instance_identifier(instanceid, identifierid, identifiertype, identifiervalue) values ('"+ instanceid +"', '"+IdentifierService.create("identifier", str(data["Cote"]) + "Cote" + str(num_inventaire))+"', 'Cote physique', '"+str(data["Cote"])+"')")

        # activité d'inventaire
        if "Auteur" in data and "Date_inventaire" in data:
            # chercher l'agent sinon le créer
            try:
                agentid_auteur = db.engine.execute("select agentid from agent_text where textvalue like '"+data["Auteur"]+"%'").fetchall()[0][0]
            except: 
                # créer agent
                post_headers = {"ws-key": KEY_WS}
                envoi_json = {"Type":"PP"}
                envoi_json["Textes"] = [{"texttype": "Code inventaire", "textlang":"fre", "textvalue": data["Auteur"]}]
                r = requests.post(URL_ROOT + "/insert_agent", data=json.dumps(envoi_json), headers=post_headers)
                agentid_auteur = json.loads((r.text))["agentid"]
            # créer l'activité
            activiteid = IdentifierService.create("activite", str(data["Date_inventaire"]) + str(data["Auteur"])+"inventaire" + str(num_inventaire))
            db.engine.execute("insert into activite(activiteid, agentid, activitetype, activitedate) values ('"+activiteid+"','"+agentid_auteur+"','Inventaire','"+str(data["Date_inventaire"])+"')")
            db.engine.execute("insert into instance_activite(instanceid,activiteid,relationtype) values ('"+instanceid+"', '"+activiteid+"', 'Inventaire')")

        json_retour["instanceid"] = instanceid
    else:
        json_retour["status"]  =  "not allowed"
    return json_retour


@app.route("/insert_referentiel", methods=["POST"])
def insert_referentiel():
    json_retour = {}
    headers = request.headers
    ws_key = headers.get("ws-key")
    data = request.get_json(force=True)
    if KEY_WS == ws_key:
        json_retour["status"]  =  "ok"
        referentielid = IdentifierService.create("referentiel", str(data["Code"]))
        if data["Code"]:
            db.engine.execute("INSERT INTO referentiel(referentielid, code) VALUES ('" + referentielid+ "','" + data["Code"] + "')")
        if data["Textes"]:
            textes = list(data["Textes"])
            for texte in textes:
                text = dict(texte)
                textid = IdentifierService.create("text", str(text["textvalue"]) + str(text["texttype"] + str(text["textlang"])))
                if text["texttype"] and text["textlang"] and  text["textvalue"] :
                    db.engine.execute("INSERT INTO referentiel_text(referentielid, textid, texttype, textlang, textvalue) VALUES ('" + referentielid+ "','" + textid + "','" + text["texttype"] + "','" + text["textlang"] + "','" + text["textvalue"].replace("'", "''") + "')")
        json_retour["referentielid"] = referentielid
    else:
        json_retour["status"]  =  "not allowed"
    return json_retour


@app.route("/insert_concept", methods=["POST"])
def insert_concept():
    json_retour = {}
    headers = request.headers
    ws_key = headers.get("ws-key")
    data = request.get_json(force=True)
    if KEY_WS == ws_key:
        json_retour["status"]  =  "ok"
        conceptid = IdentifierService.create("concept", str(data["Code"]))
        # récupérer le référentielid
        referentielid = db.engine.execute("select referentielid from referentiel where code = '" + data["Referentiel"] + "'").fetchall()[0][0]
        if data["Code"]:
            db.engine.execute("INSERT INTO concept(conceptid, code, referentielid) VALUES ('" + conceptid+ "','" + data["Code"] + "','"+referentielid+"')")
        if data["Textes"]:
            textes = list(data["Textes"])
            for texte in textes:
                text = dict(texte)
                textid = IdentifierService.create("text", str(text["textvalue"]) + str(text["texttype"] + str(text["textlang"])))
                if text["texttype"] and text["textlang"] and  text["textvalue"] :
                    db.engine.execute("INSERT INTO concept_text(conceptid, textid, texttype, textlang, textvalue) VALUES ('" + conceptid+ "','" + textid + "','" + text["texttype"] + "','" + text["textlang"] + "','" + text["textvalue"].replace("'", "''") + "')")
        json_retour["conceptid"] = conceptid
    else:
        json_retour["status"]  =  "not allowed"
    return json_retour

@app.route("/insert_agent", methods=["POST"])
def insert_agent():
    json_retour = {}
    headers = request.headers
    ws_key = headers.get("ws-key")
    data = request.get_json(force=True)
    if KEY_WS == ws_key:
        json_retour["status"]  =  "ok"
        agentid = IdentifierService.create("agent", str(data["Textes"][0]["textvalue"]))
        db.engine.execute("INSERT into agent(agentid, agenttype) values ('"+agentid+"', '"+str(data["Type"])+"')")
        if data["Textes"]:
            textes = list(data["Textes"])
            for texte in textes:
                text = dict(texte)
                textid = IdentifierService.create("text", str(text["textvalue"]) + str(text["texttype"] + str(text["textlang"])))
                if text["texttype"] and text["textlang"] and  text["textvalue"] :
                    db.engine.execute("INSERT INTO agent_text(agentid, textid, texttype, textlang, textvalue) VALUES ('" + agentid+ "','" + textid + "','" + text["texttype"] + "','" + text["textlang"] + "','" + text["textvalue"].replace("'", "''") + "')")
        json_retour["agentid"] = agentid
    else:
        json_retour["status"]  =  "not allowed"
    return json_retour