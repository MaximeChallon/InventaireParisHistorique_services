import os
import dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv.load_dotenv(os.path.join(BASE_DIR, '.env'))

DEBUG = os.environ['DEBUG']
SECRET_KEY = os.environ['SECRET_KEY']
KEY_WS = os.environ["KEY_WS"]
SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
SQLALCHEMY_DATABASE_URI_ABSOLUTE = os.environ["SQLALCHEMY_DATABASE_URI_ABSOLUTE"]
URL_ROOT  = os.environ["URL_ROOT"]
PARIS_PBF_FILE= os.environ["PARIS_PBF_FILE"]
OSM_TAGS_KEPT = [  "addr:city" ,  "addr:housename",  "addr:housenumber",    "addr:place",  "addr:postcode",  "addr:province",   "addr:street",  "addr:streetnumber",   "building",   "amenity",  "bridge",  "historic",  "int_name",  "int_ref",  "landuse",  "leisure",  "loc_name",  "loc_ref",  "man_made",  "military",  "name",  "nat_name",  "nat_ref",  "natural",  "office",  "official_name",  "operator",  "place",  "postal_code",  "ref",  "shop",  "short_name",  "tourism",  "waterway",  "wikipedia", "wikidata"]

REFERENTIELS = [{"Code": "COULEUR", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Colorisation de la photographie"}]},{"Code": "SUPPORT", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Support physique des instances"}]},{"Code": "GENERALITE_ARCHITECTURE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Généralités d'architecture"}]},{"Code": "MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Descripteurs-sujet des photographies"}]},{"Code": "ENTITE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Référentiel des entités instance"}]},{"Code": "MH", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Classement sur la liste des Monuments Historiques"}]} ,{"Code": "TAILLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Dimensions du support"}]} ]

COULEUR = [{"Code":"COULEUR", "Referentiel":"COULEUR", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Colorisé"}]},{"Code":"N&B", "Referentiel":"COULEUR", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Noir et blanc"}]},{"Code":"SEPIA", "Referentiel":"COULEUR", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Sépia"}]}]
CLASSEMENT_MH = [{"Code":"OUI", "Referentiel":"MH", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Classé"}]},{"Code":"NON", "Referentiel":"MH", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Non classé"}]},{"Code":"INCONNU", "Referentiel":"MH", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Indéterminé"}]}]
ENTITE = [{"Code":"PHOTO", "Referentiel":"ENTITE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Photographie"}]},{"Code":"COLLECTION", "Referentiel":"ENTITE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Collection de photographies"}]}]
SUPPORT = [{"Code":"AFFICHE", "Referentiel":"SUPPORT", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Affiche"}]},{"Code":"CARTE POSTALE", "Referentiel":"SUPPORT", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Carte postale"}]},{"Code":"CONTRECOLLE", "Referentiel":"SUPPORT", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Contrecollé sur bois ou carton"}]},{"Code":"DIAPOSITIVE", "Referentiel":"SUPPORT", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Diapositive"}]},{"Code":"FILM", "Referentiel":"SUPPORT", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Film"}]},{"Code":"GRAVURE", "Referentiel":"SUPPORT", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Gravure"}]},{"Code":"NEGATIF", "Referentiel":"SUPPORT", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Négatif"}]},{"Code":"NUMERIQUE", "Referentiel":"SUPPORT", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Fichier numérique"}]},{"Code":"TIRAGE PAPIER", "Referentiel":"SUPPORT", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Tirage papier"}]}]
GENERALITE_ARCHITECTURE = [{"Code":"COMMÉMORATIVE_VOTIVE_FUNÉRAIRE", "Referentiel":"GENERALITE_ARCHITECTURE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Architecture commémorative, votive ou funéraire"}]},{"Code":"JARDINS_EAUX", "Referentiel":"GENERALITE_ARCHITECTURE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Jardin, square, parc, fontaine, bassin"}]},{"Code":"INDUSTRIELLE", "Referentiel":"GENERALITE_ARCHITECTURE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Architecture industrielle"}]},{"Code":"MILITAIRE", "Referentiel":"GENERALITE_ARCHITECTURE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Architecture militaire"}]},{"Code":"PRIVÉE", "Referentiel":"GENERALITE_ARCHITECTURE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Architecture privée"}]},{"Code":"PUBLIQUE", "Referentiel":"GENERALITE_ARCHITECTURE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Architecture publique"}]},{"Code":"GÉNIE_CIVIL", "Referentiel":"GENERALITE_ARCHITECTURE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Architecture se rapportant au génie civil (ponts, etc)"}]},{"Code":"HÔTEL_PARTICULIER", "Referentiel":"GENERALITE_ARCHITECTURE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Hôtel particulier"}]},{"Code":"VOIRIES_ESPACES_LIBRES", "Referentiel":"GENERALITE_ARCHITECTURE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Voirie et espaces publics sur la voie publique"}]}]
MOT_CLE = [{"Code":"ACCUEIL_PUBLIC", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Accueil du public"}]},{"Code":"ANNIVERSAIRE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Anniversaire"}]},{"Code":"APRÈS_INCENDIE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Situation après un incendie"}]},{"Code":"APRÈS_RESTAURATION", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Situation après une restauration ou une restructuration"}]},{"Code":"ARCHITECTURE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Architecture"}]},{"Code":"ARCHIVES", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Archives"}]},{"Code":"ART", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Art"}]},{"Code":"ATTENTATS_13/11/2015", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Attentats du 13 novembre 2015 à Paris et Saint-Denis"}]},{"Code":"AVANT_INCENDIE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Situation avant un incendie"}]},{"Code":"AVANT_RESTAURATION", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Situation avant une restauration ou une restructuration"}]},{"Code":"BALCON", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Balcon"}]},{"Code":"BIBLIOTHÈQUE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Bibliothèque"}]},{"Code":"BUREAUX_DIRECTION", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Bureaux de la direction"}]},{"Code":"CAMPAGNE_RESTAURATION", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Situation pendant une campagne de restauration ou une restructuration"}]},{"Code":"CANAL_PLEIN", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Canal rempli"}]},{"Code":"CANAL_VIDÉ", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Canal vide"}]},{"Code":"CELLIER", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Cellier ou cave"}]},{"Code":"CHANTIER", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Chantier en cours"}]},{"Code":"CHANTIER_JEUNES", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Chantier de jeunes bénévoles"}]},{"Code":"CHAPELLE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Chapelle"}]},{"Code":"CHAPITEAU", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Chapiteau"}]},{"Code":"CHARLIE_HEBDO_11/01/21015", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Attentat du 11 janvier 2015 à Paris"}]},{"Code":"CHIEN_ASSIS", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Chien assis"}]},{"Code":"CIMETIÈRE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Cimétière"}]},{"Code":"COLONNE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Colonne ou colonnade"}]},{"Code":"COMMERCES", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Commerces"}]},{"Code":"CONCERT", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Concert"}]},{"Code":"CONFÉRENCE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Conférence"}]},{"Code":"CONSTRUCTION_EN_COURS", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Construction en cours"}]},{"Code":"COUPOLE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Coupole"}]},{"Code":"COUR", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Cour"}]},{"Code":"COURETTE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Courette"}]},{"Code":"CRUE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Crue"}]},{"Code":"DÉCORATION_EXTÉRIEURE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Eléments de décoration extérieure"}]},{"Code":"DÉCORATION_INTÉRIEURE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Eléments de décoration intérieure"}]},{"Code":"DÉMOLITION", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Démolition en cours"}]},{"Code":"EGLISE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Eglise ou édifice religieux apparenté"}]},{"Code":"ENCEINTE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Enceinte ou muraille"}]},{"Code":"ESCALIER", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Escalier"}]},{"Code":"ÉVÉNEMENTS", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Evénement public ou privé (réception, spectacle, etc)"}]},{"Code":"EXTÉRIEUR", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Vue extérieure"}]},{"Code":"EXTÉRIEUR_SUR_RUE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Vue extérieure sur la rue"}]},{"Code":"FAÇADE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Façade"}]},{"Code":"FER", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Fer"}]},{"Code":"FERRONNERIE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Eléments de ferronnerie"}]},{"Code":"FESTIVAL_DU_MARAIS", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Festival du Marais"}]},{"Code":"FILMS", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Films"}]},{"Code":"FONTAINE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Fontaine"}]},{"Code":"FOUILLES_ARCHÉOLOGIQUES", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Fouilles archéologiques en cours de réalisation"}]},{"Code":"FRONTON", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Fronton"}]},{"Code":"HALL", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Hall"}]},{"Code":"HÔTEL", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Hôtel particulier ou hôtel commmercial"}]},{"Code":"IMMEUBLE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Immeuble"}]},{"Code":"INTÉRIEUR", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Vue intérieure"}]},{"Code":"INTÉRIEUR_APRÈS_RESTAURATION", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Situation de l'intérieur après une restauration ou une restructuration"}]},{"Code":"INTÉRIEUR_AVANT_RESTAURATION", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Situation de l'intérieur avant une restauration ou une restructuration"}]},{"Code":"INTÉRIEUR_PENDANT_RESTAURATION", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Situation de l'intérieur pendant une restauration ou une restructuration"}]},{"Code":"JARDIN", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Jardin ou espace vert"}]},{"Code":"JOURNÉES_DU_PATRIMOINE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Journées du patrimoine"}]},{"Code":"KIOSQUE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Kiosque"}]},{"Code":"LIBRAIRIE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Librairie"}]},{"Code":"LUCARNE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Lucarne"}]},{"Code":"MANIFESTATION", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Manifestation sur la voie publication"}]},{"Code":"MANSARDE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Mansarde"}]},{"Code":"MAQUETTE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Maquette"}]},{"Code":"MASCARONS", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Mascarons"}]},{"Code":"MENACES", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Menaces"}]},{"Code":"MÉTRO", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Métro"}]},{"Code":"MEUBLES", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Mobilier"}]},{"Code":"MOULURE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Eléments de moulure"}]},{"Code":"MUR", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Mur hors domaine militaire"}]},{"Code":"NICHES", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Niches"}]},{"Code":"OCULUS", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Oculus"}]},{"Code":"PARIS_HISTORIQUE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Association du Paris Historique"}]},{"Code":"PASSAGE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Passage"}]},{"Code":"PEINTURES_MURALES", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Peintures et fresques murales"}]},{"Code":"PENDANT_RESTAURATION", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Situation pendant une restauration ou une restructuration"}]},{"Code":"PLACE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Place publique"}]},{"Code":"PLAN", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Plan"}]},{"Code":"PONT", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Pont"}]},{"Code":"PORTE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Porte ou portail"}]},{"Code":"POUTRES", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Poutres"}]},{"Code":"POUTRES_DE_LAMOIGNON", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Poutres de l'hôtel Lamoignon"}]},{"Code":"PREMIER_ÉTAGE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Premier étage"}]},{"Code":"QUADRIGES", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Quadriges"}]},{"Code":"REZ_DE_CHAUSSÉE_BAS", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Rez-de-chaussée bas"}]},{"Code":"REZ_DE_CHAUSSÉE_HAUT", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Rez-de-chaussée haut"}]},{"Code":"SALLE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Salle"}]},{"Code":"SALLE_CONFÉRENCE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Salle de conférence"}]},{"Code":"SCULPTURE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Sculpture"}]},{"Code":"SEINE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Seine (fleuve)"}]},{"Code":"SITE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Site"}]},{"Code":"SOUS-SOL", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Sous-sol"}]},{"Code":"STATUE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Statue"}]},{"Code":"TABLEAU", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Tableau (art)"}]},{"Code":"TOIT", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Toit"}]},{"Code":"TOUR", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Tour ou tourelle"}]},{"Code":"VESTIGES", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Vestiges historiques"}]},{"Code":"VIE_ASSOCIATION", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Vie de l'association"}]},{"Code":"VIERGE_OURSCAMP", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Vierge d'Ourscamp"}]},{"Code":"VILLA", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Villa"}]},{"Code":"VITRAUX", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Vitraux"}]},{"Code":"VOÛTE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Voûte"}]},{"Code":"VUE_AERIENNE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Vue aérienne"}]},{"Code":"VUE_ENSEMBLE", "Referentiel":"MOT_CLE", "Textes":[{"texttype": "Label", "textlang":"fre", "textvalue":"Vue d'ensemble"}]}]