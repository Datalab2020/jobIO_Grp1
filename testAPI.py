#!/usr/bin/python3

import yaml, requests, pprint
from pymongo import MongoClient

confAll = yaml.safe_load(open("./config.yaml"))
print(confAll)

conf = confAll['mongo']
str = 'mongodb://%s:%s@%s/?authSource=%s' % (conf['user'], conf['password'], conf['host'], conf['authSource'])
print("mongo conn:", str)
client = MongoClient(str)
db = client['Datalab2020']
collec = db['P9_grp1_event']
#collec.save({"P9_grp1_event": "test"})

conf = confAll['pole_emploi']
print('conf:', conf)

# On renseigne les variables utilisées pour la requète POST
URL = 'https://entreprise.pole-emploi.fr/connexion/oauth2/access_token'
app = 'api_anoteav1 api_evenementsv1 evenements'
scope="application_"+conf['PAR']+" "+app
print('scope: ', scope)

params={"realm":"/partenaire"}
post_data = {"grant_type": "client_credentials",
	"client_id": conf['PAR'],
	"client_secret": conf['SEC'],
	"scope": scope}
headers = {"content-type": "application/x-www-form-urlencoded"}

# Execution de la requète
req = requests.post(URL, params=params, data=post_data, headers=headers)
resp = req.json()
pprint.pprint(resp)
# Le token !!!
token = resp['access_token']
print("access token: ", token)
print("-------------------------------------------------")

# Utilisation du token pour faire une requête anotea
# https://pole-emploi.io/data/api/anotea?tabgroup-api=documentation&doc-section=api-doc-section-rechercher-les-notes-et-avis-de-formations
URL = 'https://api.emploi-store.fr/partenaire/anotea/v1/avis'
params={"page":"1", "items_par_page":"10", "certif_info":"88141"}
headers = {"Authorization": "Bearer "+token}

req = requests.get(URL, params=params, headers=headers)
resp = req.json()

for avis in resp['avis']:
    print(avis['id'], avis['date'])

#~ pprint.pprint(resp)

print("-------------------------------------------------")

# https://pole-emploi.io/data/api/evenements-pole-emploi
URL = 'https://api.emploi-store.fr/partenaire/evenements/v1/salonsenligne'
params={}
headers = {"Authorization": "Bearer "+token,
    "Accept":"application/json"}

req = requests.get(URL, params=params, headers=headers)
#~ print(req.content)
resp = req.json()

#f = open('evt_desc.html', 'w')

#print("<html><body>", file=f)

#~ pprint.pprint(resp)
for evt in resp:
    collec.save(evt)
    print(evt['titre'], evt['localisation'])
    #print(f"<h1>{evt['titre']}<h1>{evt['description']}<hr>", file=f)

#print("</body></html>", file=f)
