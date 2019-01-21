import requests
import json
import os


def get_token():
    with open('facebook_app.txt') as f:
        app_id = f.readline().rstrip()
        app_secret = f.readline().rstrip()
    res_token = requests.get("https://graph.facebook.com/oauth/access_token?client_id={}&client_secret={}&grant_type=client_credentials".format(app_id, app_secret))
    token = res_token.json()['access_token']
    return token


def get_data(keyword):
    token = get_token()
    res = requests.get('https://graph.facebook.com/search?type=place&q={}&center=21.027875,105.853654&distance=1000&fields=name,location,website&access_token={}'.format(keyword, token))
    data = res.json()
    features = []
    for i in data['data']:
        try:
            features.append(
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [i['location']["longitude"], i['location']["latitude"]],
                    },
                    "properties": {
                        'id': i['id'],
                        'name': i['name'],
                        "Address": i['location']['street'],
                        'website': i['website']
                    }
                }
            )
        except KeyError:
            try:
                features.append(
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [i['location']["longitude"], i['location']["latitude"]],
                        },
                        "properties": {
                            'id': i['id'],
                            'name': i['name'],
                            "Address": i['location']['street'],
                        }
                    }
                )
            except KeyError:
                try:
                    features.append(
                        {
                            "type": "Feature",
                            "geometry": {
                                "type": "Point",
                                "coordinates": [i['location']["longitude"], i['location']["latitude"]],
                            },
                            "properties": {
                                'id': i['id'],
                                'name': i['name'],
                                'website': i['website']
                            }
                        }
                    )
                except KeyError:
                    features.append(
                        {
                            "type": "Feature",
                            "geometry": {
                                "type": "Point",
                                "coordinates": [i['location']["longitude"], i['location']["latitude"]],
                            },
                            "properties": {
                                'id': i['id'],
                                'name': i['name'],
                            }
                        }
                    )
    return features


def make_geojson(key_list):
    features = []
    for i in key_list:
        result = get_data(i)
        features += result
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    return geojson


def main():
    path = os.path.expanduser('~') + ('/HN_center/map.geojson')
    list_item = ["coffee", "tea", "cafe", "caphe", "tra da"]
    data = make_geojson(list_item)
    with open(path, 'w') as f:
        f.write(json.dumps(data, indent=4))
    


if __name__ == '__main__':
    main()
