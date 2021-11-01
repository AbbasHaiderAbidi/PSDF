import yaml

jsonstr = "{'amountasked': '98', 'schedule': '78', 'proname': 'lollol', 'boq': [{'itemname': 'Kill You', 'itemno': '21', 'itemdesc': 'I will definitly kill you', 'itemqty': '87', 'itemprice': '1234', 'itemcost': '107358.0'}, {'itemname': 'Kill me', 'itemno': '42', 'itemdesc': 'I will most definitly kill you', 'itemqty': '876', 'itemprice': '34', 'itemcost': '29784.0'}]}"
boq = yaml.load(jsonstr, yaml.FullLoader)
print(boq['boq'][0]['itemname'])