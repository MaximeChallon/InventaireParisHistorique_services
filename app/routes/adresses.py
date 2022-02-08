from flask import redirect, url_for, request
from ..app import app, db
from ..constantes import KEY_WS, URL_ROOT, SQLALCHEMY_DATABASE_URI_ABSOLUTE, OSM_TAGS_KEPT, PARIS_PBF_FILE
from ..utils.service_identifiant import IdentifierService
import requests
import json
import re
import sqlite3
import os
import urllib
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from googletrans import Translator, constants
import unidecode

def translate(chaine, from_, to_):
    translator = Translator()
    translation = translator.translate(str(chaine),src=from_, dest=to_)
    return unidecode.unidecode(re.sub(r'^(une? )(.*)$', r'\2',str(translation.text)).upper())

def tags_to_descriptive_data(tags):
    data = {"mots_cles":[]}
    for k in tags.keys():
        if k in OSM_TAGS_KEPT:
            if k.startswith("addr"):
                data["num_rue"] = tags["addr:streetnumber"] if "addr:streetnumber" in tags else None
                data["rue"] = tags["addr:street"] if "addr:street" in tags else None
                data["ville"] = tags["addr:city"] if "addr:city" in tags else None
                data["code_postal"] = tags["addr:postcode"] if "addr:postcode" in tags else None
            elif k == "name":
                data["nom_site"] = tags["name"] 
            elif k == "wikidata" or k=="wikipedia":
                data[k] = tags[k]
            elif tags[k] == "yes" or tags[k] == "no":
                # alors k est un mot clé concept posé sur la gemoetry que si yes
                if tags[k] == "yes":
                    data["mots_cles"].append(translate(k,"en", "fr").upper())
            elif k in [  "building",   "amenity",  "bridge",  "man_made",  "shop"]:
                #alors la valeur de tags[k] est le mot clé concept
                data["mots_cles"].append(translate("a " +tags[k],"en", "fr").upper())
            else:
                # TODO: pour le reste, ça devient des textes
                pass
    return data

@app.route("/get_around_objects/<int:around>/<latitude>/<longitude>", methods=["GET"])
def get_around_objects( around, latitude, longitude):
    request = """
    [out:json];
    way
    (around:"""+str(around)+""", """+str(latitude)+""","""+str(longitude)+""");
    out  tags body;
    """
    requete = requests.get("https://overpass-api.de/api/interpreter?data="+urllib.parse.quote(request))
    try:
        r = json.dumps(requete.json())
    except Exception as e:
        print(e)
        print(requete.content)
        r = {"elements":[""]}
    return str(r)

@app.route("/get_nodes/<type>/<osmid>", methods=["GET"])
def get_nodes( type, osmid):
    request = """
    [out:json];
    """+str(type)+"""
    ("""+str(osmid)+""");
    out  tags body;
    """
    requete = requests.get("https://overpass-api.de/api/interpreter?data="+urllib.parse.quote(request))
    try:
        r = json.dumps(requete.json())
    except Exception as e:
        print(e)
        print(requete.content)
        r = {"elements":[""]}
    return str(r)

@app.route("/get_ways/<type>/<osmid>", methods=["GET"])
def get_ways( type, osmid):
    request = """
    [out:json];
    """+str(type)+"""
    ("""+str(osmid)+""");
    out  tags body;
    """
    requete = requests.get("https://overpass-api.de/api/interpreter?data="+urllib.parse.quote(request))
    try:
        r = json.dumps(requete.json())
    except Exception as e:
        print(e)
        print(requete.content)
        r = {"elements":[""]}
    return str(r)

@app.route("/get_around_nodes/<int:around>/<latitude>/<longitude>", methods=["GET"])
def get_around_nodes( around, latitude, longitude):
    request = """
    [out:json];
    node
    (around:"""+str(around)+""", """+str(latitude)+""","""+str(longitude)+""")["addr:housenumber"~".*"];
    out   body;
    """
    requete = requests.get("https://overpass-api.de/api/interpreter?data="+urllib.parse.quote(request))
    try:
        r = json.dumps(requete.json())
    except Exception as e:
        print(e)
        print(requete.content)
        r = {"elements":[""]}
    return str(r)


@app.route("/get_nodes_data_from_way/<latitude>/<longitude>", methods=["POST"])
def get_nodes_data_from_way(latitude, longitude):
    json_retour = {}
    liste = json.loads(request.get_json(force=True))["elements"]
    data_points_final = []
    data_way_final = []
    # pour chaque noeud du way, chercher ses infos
    for node in liste:
        lats_vect = []
        lons_vect = []
        leaflet_acumulation_list = []
        data_points = []
        # il faut avoir les coordonnées de chaque point afin de reconstituer le polygone
        for point in node['nodes']:
            try:
                r = json.loads(json.dumps(requests.get("https://www.openstreetmap.org/api/0.6/node/"+str(point) + ".json").json()))
                point_latitude = r["elements"][0]["lat"]
                point_longitude= r["elements"][0]["lon"]
                lats_vect.append(point_latitude)
                lons_vect.append(point_longitude)
                leaflet_acumulation_list.append([point_latitude, point_longitude])
            except:
                r = None
                point_latitude = None
                point_longitude = None
            data_points.append({"osmid":str(point), "osmtype":"node", "lat":point_latitude, "lon":point_longitude})
        
        # check si mon point est dans le polygon: si oui alors je garde l'object
        if lats_vect and lons_vect:
            # si j'ai du True dans ce check, alors je peux garder cet objet et l'insérer en base
            if Polygon(np.column_stack((np.array(lons_vect), np.array(lats_vect)))).contains(Point(float(longitude),float(latitude))):
                # je peux alors chercher les infos sur chaque point
                data_points_interm = []
                for p in data_points:
                    try:
                        s = json.loads(json.dumps(requests.get("https://nominatim.openstreetmap.org/reverse.php?lat="+str(p["lat"])+"&lon="+str(p["lon"])+"&zoom=18&format=jsonv2&debug=0").json()))
                        t = p
                        if "type" in s:
                            t["type_batiment"] = translate("a " + s["type"], "en", "fr")
                        if "address" in s:
                            t["num_rue"] = s["address"]["house_number"] if "house_number" in s["address"] else None
                            t["rue"] =  re.sub(r"(((COURS)|(RUE)|(PLACE)|(BOULEVARD)|(AVENUE)|(QUAI)|(COUR)) ((D((E(S)?)|(U)).*)|(L.*))?) (.*)$", r"\17, \1", s["address"]["road"].upper()) if "road" in s["address"] else None
                            t["quartier"] = s["address"]["city_block"] if "city_block" in s["address"] else None
                            t["code_postal"] = s["address"]["postcode"] if "postcode" in s["address"] else None
                    except:
                        t = p
                    data_points_interm.append(t)
                data_points_final = data_points_final + data_points_interm
                # infos du node (way) que si mon point est dans le node
                data_way = {}
                data_way["osmtype"] = "way"
                data_way["osmid"] = node["id"]
                data_way["coordinates"] = leaflet_acumulation_list
                data_way.update(tags_to_descriptive_data(node["tags"]))
                data_way_final = data_way_final + [data_way]
                # TODO: faire un appel à nominatim pour avoir les détails grace au osmid du way

    return json.dumps({"data_points":data_points_final, "data_ways":data_way_final})