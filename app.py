"""from flask import Flask
import random
import requests
import datetime
import time
import json
from yolo.logic import time_update 

app = Flask(__name__)

api_key = 'up87un4nhriz1agk873vtsjwppy47hgd'

url1 = f'http://apis.mapmyindia.com/advancedmaps/v1/{api_key}/distance?center=12.921288,77.668916%7C&pts=12.922310,77.668916'
url2 = f'http://apis.mapmyindia.com/advancedmaps/v1/{api_key}/distance?center=12.922310,77.668916%7C&pts=12.922610,77.669872'
url3 = f'http://apis.mapmyindia.com/advancedmaps/v1/{api_key}/distance?center=12.922610,77.669872%7C&pts=12.923450,77.671286'
url4 = f'http://apis.mapmyindia.com/advancedmaps/v1/{api_key}/distance?center=12.923450,77.671286%7C&pts=12.925450,77.671286'
url5 = f'http://apis.mapmyindia.com/advancedmaps/v1/{api_key}/distance?center=12.925450,77.671286%7C&pts=12.924118,77.673142'

@app.route('/api')
def api():
    while(True):
        severity = random.random()

        body = requests.get(url1)
        body = json.loads(body.text)
        time_update(int(int(body["results"][0]["duration"])/7), severity)
        time.sleep(int(int(body["results"][0]["duration"])/7))
        body = requests.get(url2)
        body = json.loads(body.text)
        time_update(int(int(body["results"][0]["duration"])/7), severity)
        time.sleep(int(int(body["results"][0]["duration"])/7))
        body = requests.get(url3)
        body = json.loads(body.text)
        time_update(int(int(body["results"][0]["duration"])/7), severity)
        time.sleep(int(int(body["results"][0]["duration"])/7))
        body = requests.get(url4)
        body = json.loads(body.text)
        time_update(int(int(body["results"][0]["duration"])/7), severity)
        time.sleep(int(int(body["results"][0]["duration"])/7))
        body = requests.get(url5)
        body = json.loads(body.text)
        time_update(int(int(body["results"][0]["duration"])/7), severity)
        time.sleep(int(int(body["results"][0]["duration"])/7))
    return 'hello world'

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True,port=4000)"""
from flask import Flask, jsonify
import random
import requests
import json
import threading
import time
from yolo.logic import time_update 

app = Flask(__name__)

api_key = 'up87un4nhriz1agk873vtsjwppy47hgd'

# URLs for the MapMyIndia API
url1 = f'http://apis.mapmyindia.com/advancedmaps/v1/{api_key}/distance?center=12.921288,77.668916%7C&pts=12.922310,77.668916'
url2 = f'http://apis.mapmyindia.com/advancedmaps/v1/{api_key}/distance?center=12.922310,77.668916%7C&pts=12.922610,77.669872'
url3 = f'http://apis.mapmyindia.com/advancedmaps/v1/{api_key}/distance?center=12.922610,77.669872%7C&pts=12.923450,77.671286'
url4 = f'http://apis.mapmyindia.com/advancedmaps/v1/{api_key}/distance?center=12.923450,77.671286%7C&pts=12.925450,77.671286'
url5 = f'http://apis.mapmyindia.com/advancedmaps/v1/{api_key}/distance?center=12.925450,77.671286%7C&pts=12.924118,77.673142'

def update_traffic_data():
    while True:
        severity = random.random()

        # List of URLs to iterate through
        urls = [url1, url2, url3, url4, url5]
        
        for url in urls:
            try:
                response = requests.get(url)
                data = response.json()
                duration = int(data["results"][0]["duration"])
                time_update(int(duration / 7), severity)
                time.sleep(duration / 7)  # sleep between requests
            except Exception as e:
                print(f"Error fetching data from {url}: {e}")
                continue

@app.route('/api')
def api():
    # Run traffic update function in the background
    traffic_thread = threading.Thread(target=update_traffic_data, daemon=True)
    traffic_thread.start()

    # Respond immediately
    return jsonify({"message": "Traffic update process started."})

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, port=4000)
def fetch_distance(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        data = response.json()  # Parse JSON response
        if data:
            return data
        else:
            print("No data returned from API.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except ValueError:
        print("Malformed response returned, could not parse JSON.")

api_url = "http://apis.mapmyindia.com/advancedmaps/v1/up87un4nhriz1agk873vtsjwppy47hgd/distance?center=12.923450,77.671286%7C&pts=12.925450,77.671286"
fetch_distance(api_url)

