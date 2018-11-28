import urllib.request, json, getpass, requests, untangle

prefix = input("Please enter Prefix: ")
type = input("Please enter Type: ")
password = getpass.getpass()

def find_objects(prefix,type, all_flag, password = password):
    if all_flag is 1:
        all_flag = '&flags=all-more'
    else:
        all_flag = ''
    extra_suffix = ""
    if type == "domain":
        extra_suffix = "&flags=no-irt&flags=reverse-domain"
    link = f"https://rest.db.ripe.net/search.json?query-string={prefix}&type-filter={type}{all_flag}&flags=no-filtering{extra_suffix}&source=RIPE"
    objects = []
    try:
        with urllib.request.urlopen(link) as url:
            data = json.loads(url.read().decode())
    except urllib.request.HTTPError:
        print(f"\nThere is no {type} object")
        return

    for object in data["objects"]["object"]:
        if object['type'] == "inetnum" or object['type'] == "domain":
            objects.append(object["primary-key"]["attribute"][0]["value"])
            for key in object["attributes"]["attribute"]:
                if key['name'] == 'status':
                    if key['value'] == 'ALLOCATED PA':
                        return
        if object['type'] == "route":
            objects.append(object["primary-key"]["attribute"][0]["value"]+object["primary-key"]["attribute"][1]["value"])

    for object in objects:
        object = object.replace(' ', '')
        url = f"https://rest.db.ripe.net/ripe/{type}/{object}"
        querystring = {"password": password}
        response = requests.request("DELETE", url, params=querystring)
        tree = untangle.parse(response.text)
        if type == 'inetnum' or type == 'domain':
            print(tree.whois_resources.objects.object.primary_key.attribute['name'] + ' object: ' + tree.whois_resources.objects.object.primary_key.attribute['value'] + ' has been deleted.')
        if type == 'route':
            print(tree.whois_resources.objects.object.primary_key.attribute[0]['name'] + ' object: ' + tree.whois_resources.objects.object.primary_key.attribute[0]['value'] + ' has been deleted.')

if type == "all":
    find_objects(prefix, "inetnum", 0)
    find_objects(prefix, "inetnum", 1)
    find_objects(prefix, "route", 0)
    find_objects(prefix, "route", 1)
    find_objects(prefix, "domain", 1)
else:
    find_objects(prefix, type, 0)
    find_objects(prefix, type, 1)