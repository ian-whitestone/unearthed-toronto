import requests


req_url='https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'
api_key = 'AIzaSyBrfDTcZ9m3FnRBN4OorWa96Ox0Xa7IHfQ'

def get_coords(addr):
    address=addr +' Toronto, Ontario, Canada'
    try:
        response = requests.get(req_url.format(address,api_key))
        response_dict = response.json()
        coords=response_dict['results'][0]['geometry']['location']
        if response_dict['status'] == 'OK':
            print (response_dict)
            return coords['lat'],coords['lng'],response_dict['results'][0]['formatted_address'].replace(',','')
    except Exception as err:
        print (str(err))
        pass
    return None,None,None

def get_location_data(addr):
    address=addr +' Toronto, Ontario, Canada'
    try:
        response = requests.get(req_url.format(address,api_key))
        response_dict = response.json()
        coords=response_dict['results'][0]['geometry']['location']
        if response_dict['status'] == 'OK':
            return response_dict['results']
    except Exception as err:
        print (str(err))
        pass
    return None

def parse_location_data(data): ##data is in form {postal_code:response_dict}

    location_data={}

    for postal_code,loc in data.items():
        location_data[postal_code]={}
        location_data[postal_code]['latitude']=loc[0]['geometry']['location']['lat']
        location_data[postal_code]['longitude']=loc[0]['geometry']['location']['lng']

        loc_data = loc[0]['address_components']
        for d in loc_data:
            if 'neighborhood' in d['types']:
                location_data[postal_code]['neighborhood']=d['long_name']
            elif 'locality' in d['types']:
                location_data[postal_code]['locality']=d['long_name']

        ##insert Nulls for missing values
        if 'neighborhood' not in location_data[postal_code].keys():
            location_data[postal_code]['neighborhood']=None
        if 'locality' not in location_data[postal_code].keys():
            location_data[postal_code]['locality']=None

    return location_data ##dictionary ready for historizing
