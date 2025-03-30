import requests

def get_latest_release():
    url = "https://api.github.com/repos/triisdang/Bloxskull/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("tag_name", None)  
    return None


latest_version = get_latest_release()
# local_version = localversion()
local_version = "0.0.0" # test this 

def newupdates() :
    latest_version = get_latest_release()
    local_version = "1.0.1"
    if latest_version and latest_version != local_version:
        return(True)
    else:
        return(False)
