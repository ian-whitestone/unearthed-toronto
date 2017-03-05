import requests
import json


BASE_URL = "https://mrdata.usgs.gov/general/near-point.php?x={0}&y={1}&d=0.01"

FIELDS_MAP = {
    'USGS Publications': 'pubs',
    'Estimates of undiscovered mineral resources': 'nmra'
}

def getUSGS(lon, lat):
    url = BASE_URL.format(lon, lat)
    print (url)
    r = requests.get(url)
    d = json.loads(r.text)
    data = {d['title']:d for d in d['dataset']}

    cleaned_data = {}
    for k, v in FIELDS_MAP.items():
        records = data.get(k, None)
        if records:
            cleaned_data[v] = records['record_list']
    return cleaned_data


## SAMPLE CALL
# data = getUSGS(-116.56974308104218, 40.16796257866798)
