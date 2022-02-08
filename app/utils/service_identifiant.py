import hashlib

class IdentifierService():
    def create(type_entite, cle):
        table_prefixes = {"instance": "00",
                            "text": "01",
                            "concept": "02",
                            "activite": "03",
                            "referentiel": "04",
                            "synthese": "05",
                            "droit": "06",
                            "identifier": "07",
                            "geolocalisation": "08",
                            "evenement": "09",
                            "agent": "10",
                            "adresse": "11",
                            "geometry":"12"}
        hash = (hashlib.sha1(cle.encode("UTF-8")).hexdigest())[:10]
        identifier = table_prefixes[type_entite] + hash
        return identifier