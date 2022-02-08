from flask import redirect, url_for, request
from ..app import app, db
from ..constantes import KEY_WS, URL_ROOT, SQLALCHEMY_DATABASE_URI_ABSOLUTE
from ..utils.service_identifiant import IdentifierService
from ..utils.service_numero_inventaire import InventoryNumberService
import requests
import json
import re
import sqlite3
import os
import pandas as pd
from datetime import datetime

@app.route("/to_excel", methods=['POST'])
def to_excel():
    json_retour = {}
    headers = request.headers
    ws_key = headers.get("ws-key")
    data = request.get_json(force=True)
    if KEY_WS == ws_key:
        json_retour["status"]  =  "ok"
        filepath = data["filepath"]
        limit = data["limit"]
        os.system("rm " + filepath)
        conn = sqlite3.connect(SQLALCHEMY_DATABASE_URI_ABSOLUTE)
        # la requête sera la sortie
        query = conn.execute("""
            with cte as(select ac.instanceid, ad.code, rank() over(partition by ac.instanceid order by ad.code) as rang
            from instance_concept ac
            left join concept ad on ad.conceptid = ac.conceptid 
            where ac.relationtype = 'Mot clé')
                select c.identifiervalue as N_inventaire, d.rue as Rue, d.numero as N_rue, d.arrondissement as Arrondissement, d.ville as Ville, d.departement as Departement,
                e.latitude as Latitude, e.longitude as Longitude, g.code as Support, i.code as Couleur, k.code as Taille, m.datedebut as Date_prise_vue, o.textvalue as Photographe,
                null as Droits, q.textvalue as Mention_don, s.textvalue as Mention_collection, u.datedebut as Date_construction, w.textvalue as Architecte, y.code as Classement_MH,
                z.textvalue as Legende, ab.code as Generalite_architecture, ae.code as Mot_cle1, af.code as Mot_cle2, ag.code as Mot_cle3, ah.code as Mot_cle4, ai.code as Mot_cle5, 
                aj.code as Mot_cle6, ak.textvalue as Autre_adresse, al.textvalue as Notes, am.identifiervalue as Cote_base, an.identifiervalue as Cote_classement, 
                ap.activitedate as Date_inventaire, aq.textvalue as Auteur
                from instance a
                inner join concept b on a.instancetype = b.conceptid and b.code = 'PHOTO'
                left join instance_identifier c on c.instanceid = a.instanceid and c.identifiertype = 'Numéro d''inventaire'
                left join adresse d on d.instanceid = a.instanceid and d.adressetype  = 'Principale' left join geolocalisation e on e.instanceid = a.instanceid
                left join instance_concept f on f.instanceid = a.instanceid and f.relationtype = 'Support' left join concept g on g.conceptid = f.conceptid 
                left join instance_concept h on h.instanceid = a.instanceid and h.relationtype = 'Couleur' left join concept i on i.conceptid = h.conceptid 
                left join instance_concept j on j.instanceid = a.instanceid and j.relationtype = 'Taille' left join concept k on k.conceptid = j.conceptid 
                left join instance_evenement l on l.instanceid = a.instanceid and l.relationtype = 'Prise de vue' left join evenement m on m.evenementid = l.evenementid
                left join instance_agent n on n.instanceid = a.instanceid and n.relationtype = 'Photographe' left join agent_text o on o.agentid = n.agentid and o.texttype = 'Identité civile'
                left join instance_agent p on p.instanceid = a.instanceid and p.relationtype = 'Donateur' left join agent_text q on q.agentid = p.agentid and q.texttype = 'Identité civile'
                left join instance_instance r on r.sourceinstanceid = a.instanceid  left join instance_text s on s.instanceid = r.targetinstanceid and s.texttype = 'Label'
                left join instance_evenement t on t.instanceid = a.instanceid and t.relationtype = 'Construction' left join evenement u on u.evenementid = t.evenementid
                left join instance_agent v on v.instanceid = a.instanceid and v.relationtype = 'Architecte' left join agent_text w on w.agentid = v.agentid and w.texttype = 'Identité civile'
                left join instance_concept x on x.instanceid = a.instanceid and x.relationtype = 'Classement MH' left join concept y on y.conceptid = x.conceptid 
                left join instance_text z on z.instanceid = a.instanceid and z.texttype = 'Légende'
                left join instance_concept aa on aa.instanceid = a.instanceid and aa.relationtype = 'Généralité d''architecture' left join concept ab on ab.conceptid = aa.conceptid 
                left join cte ae on ae.instanceid = a.instanceid and ae.rang = 1
                left join cte af on af.instanceid = a.instanceid and af.rang = 2
                left join cte ag on ag.instanceid = a.instanceid and ag.rang = 3
                left join cte ah on ah.instanceid = a.instanceid and ah.rang = 4
                left join cte ai on ai.instanceid = a.instanceid and ai.rang = 5
                left join cte aj on aj.instanceid = a.instanceid and aj.rang = 6
                left join instance_text ak on ak.instanceid = a.instanceid and ak.texttype = 'Autre adresse'
                left join instance_text al on al.instanceid = a.instanceid and al.texttype = 'Note'
                left join instance_identifier am on am.instanceid = a.instanceid and am.identifiertype = 'Cote de la base de numérisations'
                left join instance_identifier an on an.instanceid = a.instanceid and an.identifiertype = 'Cote physique'
                left join instance_activite ao on ao.instanceid = a.instanceid and ao.relationtype = 'Inventaire' left join activite ap on ap.activiteid = ao.activiteid
                left join agent_text aq on aq.agentid = ap.agentid and aq.texttype = 'Code inventaire'
                limit """ + str(limit))

        results= pd.DataFrame.from_records(data = query.fetchall(), columns = [column[0] for column in query.description])
        results.to_excel(filepath, sheet_name="Inventaire", index=False)
        json_retour["filepath"] = filepath
    else:
        json_retour["status"]  =  "not allowed"
    return json_retour


@app.route("/select/<int:num_inventaire>", methods=['POST'])
def select(num_inventaire):
    json_retour = {}
    headers = request.headers
    ws_key = headers.get("ws-key")
    data = request.get_json(force=True)
    if KEY_WS == ws_key:
        json_retour["status"]  =  "ok"
        try:
            instanceid = db.engine.execute("select instanceid from instance_identifier where identifiertype = '"+str(data["type"])+"' and identifiervalue = '"+str(num_inventaire)+"'").fetchall()[0][0]
            json_retour["instanceid"] = instanceid
            json_retour["num_inv"] = db.engine.execute("select identifiervalue from instance_identifier where instanceid = '"+instanceid+"' and identifiertype = 'Numéro d''inventaire'").fetchall()[0][0]
        except:
            pass
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
            db.engine.execute("delete from instance_identifier where instanceid = '"+str(ancieninstance)+"' and identifiertype != 'Numéro d''inventaire' and identifiertype != 'Cote physique'")
            db.engine.execute("delete from adresse where instanceid = '"+str(ancieninstance)+"'")
            db.engine.execute("delete from geolocalisation where instanceid = '"+str(ancieninstance)+"'")
            db.engine.execute("delete from instance_concept where instanceid = '"+str(ancieninstance)+"'")
            db.engine.execute("delete from instance_agent where instanceid = '"+str(ancieninstance)+"'")
            db.engine.execute("delete from instance_text where instanceid = '"+str(ancieninstance)+"'")
            db.engine.execute("delete from instance_instance where sourceinstanceid = '"+str(ancieninstance)+"' or targetinstanceid = '"+str(ancieninstance)+"'")
            #db.engine.execute("delete from instance where instanceid = '"+str(ancieninstance)+"'")

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
        db.engine.execute("INSERT or ignore into instance (instanceid, instancetype, code) values ('"+instanceid+"','"+ instancetype +"', '"+str(num_inventaire)+"') ")

        #identifier
        identifierid = IdentifierService.create("identifier", str(num_inventaire))
        db.engine.execute("insert or ignore into instance_identifier(instanceid, identifierid, identifiertype, identifiervalue) values ('"+instanceid+"','"+identifierid+"','Numéro d''inventaire','"+str(num_inventaire)+"')")

        #identifiant métier
        if "Id_metier" in data:
            identifierid_metier = IdentifierService.create("identifier", str(data["Id_metier"] + "idmetier" + data["Id_metier_type"]))
            db.engine.execute("insert or ignore into instance_identifier(instanceid, identifierid, identifiertype, identifiervalue) values ('"+instanceid+"','"+identifierid_metier+"','"+data["Id_metier_type"]+"','"+str(data["Id_metier"])+"')")

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
                (",'" + str(data["Ville"]).replace("'", "''") + "'"  if "Ville" in data else "") +
                ("," + str(data["Departement"])  if "Departement" in data else "") +
            ")")
            db.engine.execute(requete)
        
        #Site
        if "Site" in data:
            value = (re.compile(r'[\n\r\t]').sub(" ", data["Site"])).replace("'", "''")
            db.engine.execute("insert into instance_text (instanceid, textid, texttype, textlang, textvalue) values ('"+instanceid+"','"+IdentifierService.create("text", value + "site" + str(num_inventaire))+"','Site','fre','"+value+"')")

        # geoloc
        if "Latitude" in data and "Longitude" in data:
            geolocalisationid = IdentifierService.create("geolocalisation", str(data["Latitude"]) + str(data["Longitude"]) + str(num_inventaire))
            db.engine.execute("insert into geolocalisation(instanceid, geolocalisationid, latitude, longitude) values ('"+instanceid+"','"+geolocalisationid+"',"+str(data["Latitude"])+","+str(data["Longitude"])+")")
        
        # support 
        if "Support" in data:
            try:
                support = data["Support"]
                if support == "TRANSPARENT":
                    support = "NEGATIF"
                if support == "PHOTOCOPIE":
                    support = "TIRAGE PAPIER"
                conceptid_support = db.engine.execute("select conceptid from concept where code = '"+data["Support"]+"'").fetchall()[0][0]
                db.engine.execute("insert into instance_concept(instanceid, conceptid, relationtype) values ('"+instanceid+"', '"+conceptid_support+"', 'Support')")
            except:
                pass
        
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
                agentid_photographe = db.engine.execute("select agentid from agent_text where textvalue = '"+data["Photographe"].replace("'", "''")+"'").fetchall()[0][0]
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
                agentid_don = db.engine.execute("select agentid from agent_text where textvalue = '"+data["Don"].replace("'", "''")+"'").fetchall()[0][0]
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
                agentid_archi = db.engine.execute("select agentid from agent_text where textvalue = '"+data["Architecte"].replace("'", "''")+"'").fetchall()[0][0]
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
            try:
                conceptid_mh = db.engine.execute("select conceptid from concept inner join referentiel on referentiel.referentielid = concept.referentielid and referentiel.code = 'MH' where concept.code = '"+data["MH"].upper()+"'").fetchall()[0][0]
                db.engine.execute("insert into instance_concept(instanceid, conceptid, relationtype) values ('"+instanceid+"', '"+conceptid_mh+"', 'Classement MH')")
            except:
                pass

        # légende
        if "Legende" in data:
            value_legende = (re.compile(r'[\n\r\t]').sub(" ", data["Legende"])).replace("'", "''")
            db.engine.execute("insert into instance_text (instanceid, textid, texttype, textlang, textvalue) values ('"+instanceid+"','"+IdentifierService.create("text", value_legende + "legende" + str(num_inventaire))+"','Légende','fre','"+value_legende+"')")
        
        # generalite
        if "Generalite" in data:
            mot_cle = data["Generalite"]
            if mot_cle == "HOTEL PARTICULIER" or mot_cle == "HÔTEL PARTICULIER":
                mot_cle = "HÔTEL_PARTICULIER"
            try:
                conceptid_gen = db.engine.execute("select conceptid from concept inner join referentiel on referentiel.referentielid = concept.referentielid and referentiel.code = 'GENERALITE_ARCHITECTURE' where concept.code like '%"+mot_cle+"%'").fetchall()[0][0]
                db.engine.execute("insert into instance_concept(instanceid, conceptid, relationtype) values ('"+instanceid+"', '"+conceptid_gen+"', 'Généralité d''architecture')")
            except:
                pass

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
        
        if "Note2" in data:
            value_note2= (re.compile(r'[\n\r\t]').sub(" ", data["Note2"])).replace("'", "''")
            db.engine.execute("insert into instance_text (instanceid, textid, texttype, textlang, textvalue) values ('"+instanceid+"','"+IdentifierService.create("text", value_note2 + "note" + str(num_inventaire))+"','Note','fre','"+value_note2+"')")

        # cote base: identifiant d'instance
        if "Cote_base" in data:
            db.engine.execute("insert into instance_identifier(instanceid, identifierid, identifiertype, identifiervalue) values ('"+ instanceid +"', '"+IdentifierService.create("identifier", str(data["Cote_base"] + datetime.now().strftime("%d/%m/%Y %H:%M:%S")))+"', 'Cote de la base de numérisations', '"+str(data["Cote_base"])+"')")
        
        # cote physique: identifiant d'instance
        if "Cote" in data:
            db.engine.execute("insert into instance_identifier(instanceid, identifierid, identifiertype, identifiervalue) values ('"+ instanceid +"', '"+IdentifierService.create("identifier",  "Cote physique" + str(num_inventaire))+"', 'Cote physique', '"+str(data["Cote"])+"') on conflict (identifierid) do update set identifiervalue = '"+str(data["Cote"])+"' ")

        #activité entrée base numérisation
        if "Entree_base_num" in data:
            try:
                agentid = db.engine.execute("select agentid from agent_text where textvalue like 'INCONNU'").fetchall()[0][0]
            except: 
                # créer agent
                post_headers = {"ws-key": KEY_WS}
                envoi_json = {"Type":"PP"}
                envoi_json["Textes"] = [{"texttype": "Code inventaire", "textlang":"fre", "textvalue": "INCONNU"}]
                r = requests.post(URL_ROOT + "/insert_agent", data=json.dumps(envoi_json), headers=post_headers)
                agentid = json.loads((r.text))["agentid"]
            activiteid = IdentifierService.create("activite", str(data["Entree_base_num"] + "entree base num")+"inventaire" + str(num_inventaire))
            db.engine.execute("insert into activite(activiteid,  activitetype, activitedate, agentid) values ('"+activiteid+"','Inventaire','"+str(data["Entree_base_num"])+"','"+agentid+"')")
            db.engine.execute("insert into instance_activite(instanceid,activiteid,relationtype) values ('"+instanceid+"', '"+activiteid+"', 'Entrée en base de numérisation')")
        
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

@app.route("/create_inventory_number/<cote_physique>", methods=["POST"])
def create_inventory_number(cote_physique):
    return InventoryNumberService.create(cote_physique)

@app.route("/get_identifiant/<type_entite>/<cle>", methods=["GET"])
def get_identifiant(type_entite, cle):
    return IdentifierService.create(type_entite, cle)