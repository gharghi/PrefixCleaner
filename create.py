import urllib.request, json, getpass, requests, untangle, netaddr

prefix = input("Please enter Prefix: ")
size = input("Please enter subnet size: ")
asn = input("Please enter AS Number: ")
mnt = input("Please enter your maintainer: ")
password = getpass.getpass()
prefix = netaddr.IPNetwork(prefix)

def create(prefix, asn = asn, mnt = mnt, password=password):
    # data_xml = f'<?xml version="1.0" encoding="UTF-8" standalone="no"?><whois-resources><objects><object type="person"><source id="RIPE"/><attributes><attribute name="route" value="{prefix}"/><attribute name="origin" value="{asn}"/><attribute name="mnt-by" value="{mnt}"/><attribute name="source" value="RIPE"/></attributes></object></objects></whois-resources>'
    data_json = '{"objects": {"object": [{"source": {"id": "RIPE"},"attributes": {"attribute": [{"name": "route","value": "' + str(prefix) + '"},{"name": "origin","value": "' + str(asn) + '"},{"name": "mnt-by","value": "' + str(mnt) +'"},{"name": "source","value": "RIPE"}]}}]}}'
    url = f"https://rest.db.ripe.net/ripe/route"
    headers = {'Content-Type': 'application/json','Accept': 'application/json'}
    querystring = {"password": password}
    response = requests.post( url, data=data_json, params=querystring, headers=headers)
    response_json = response.json()

    if response.status_code == 200:
        return response_json["objects"]["object"][0]["primary-key"]["attribute"][0]["value"] + " route with " + response_json["objects"]["object"][0]["primary-key"]["attribute"][1]["value"] + " has been created!"
    elif response.status_code == 409:
        return str(prefix) + " has already created!"
    elif response.status_code == 401:
        return "Password is wrong"
    else:
        return response.text

print(create(prefix))
for subnet in prefix.subnet(int(size)):
    print(create(subnet))
    # print(f"route:\t{subnet}\norigin:\tAS43754\nmnt-by:\tASIATECH-MNT\nsource:\tRIPE\n") #for manual creation uncomment this

