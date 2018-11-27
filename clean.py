import urllib.request, json, os, getpass

prefix = input("Please enter Prefix: ")
type = input("Please enter Type: ")
password = getpass.getpass()

def find_objects(prefix,type, password = password):
    extra_suffix = ""
    if type == "domain":
        extra_suffix = "&flags=no-irt&flags=reverse-domain"
    link = f"https://rest.db.ripe.net/search.json?query-string={prefix}&type-filter={type}&flags=all-more&flags=no-filtering{extra_suffix}&source=RIPE"
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
        if object['type'] == "route":
            objects.append(object["primary-key"]["attribute"][0]["value"]+object["primary-key"]["attribute"][1]["value"])

    for object in objects:
        object = object.replace(' ', '')
        print(object)
        os.system(f"curl -X DELETE 'https://rest.db.ripe.net/ripe/{type}/{object}?password={password}'")

if type == "all":
    find_objects(prefix, "inetnum")
    find_objects(prefix, "route")
    find_objects(prefix, "domain")
else:
    find_objects(prefix, type)