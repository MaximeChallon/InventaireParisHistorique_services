from ..app import db
import requests
import json
from ..constantes import KEY_WS, URL_ROOT

class InventoryNumberService():
    def create(cote_physique):
        result = {}
        
        last_num = db.engine.execute("select instance.code  from instance inner join concept on concept.conceptid = instance.instancetype and concept.code = 'PHOTO' order by cast(instance.code as integer) desc limit 1").fetchall()[0][0]
        new_num = int(last_num) + 1
        #appel à insert instance pour faire la coquille
        post_headers = {"ws-key": KEY_WS}
        envoi_json = {}
        envoi_json["type"] = "PHOTO"
        envoi_json["Cote"] = cote_physique
        r = requests.post(URL_ROOT + "/insert/"+str(new_num), data=json.dumps(envoi_json), headers=post_headers)
        instanceid = json.loads((r.text))["instanceid"]

        result["Cote"] = cote_physique 
        result["instanceid"] = instanceid
        result["Numero_inventaire"] = new_num
        return result