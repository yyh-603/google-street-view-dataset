import requests
import dotenv
import os
import pandas as pd
import random
import json
import time

dotenv.load_dotenv()

GOOGLE_MAP_API_KEY = os.getenv("GOOGLE_MAP_API_KEY")
URL = "https://maps.googleapis.com/maps/api/streetview"

CITY_MAX = 50
# CITY_LABEL = ["台北市", "新北市", "桃園市", "台中市", "台南市", "高雄市", "基隆市", "新竹市", "嘉義市", "新竹縣", "苗栗縣", "彰化縣", "南投縣", "雲林縣", "嘉義縣", "屏東縣", "宜蘭縣", "花蓮縣", "台東縣"]
CITY_LABEL = ["Taipei City", "New Taipei City", "Taoyuan City", "Taichung City", "Tainan City", "Kaohsiung City", "Keelung City", "Hsinchu City", "Chiayi City", "Hsinchu County", "Miaoli County", "Changhua County", "Nantou County", "Yunlin County", "Chiayi County", "Pingtung County", "Yilan County", "Hualien County", "Taitung County"]
CITY_RANGE = {
    "Taipei City": (24.94, 121.44, 25.22, 121.67),
    "New Taipei City": (24.65, 121.26, 25.31, 122.02),
    "Taoyuan City": (24.57, 120.96, 25.14, 121.50),
    "Taichung City": (23.98, 120.44, 24.46, 121.47),
    "Tainan City": (22.86, 120.01, 23.44, 120.67),
    "Kaohsiung City": (22.46, 120.17, 23.48, 121.06),
    "Keelung City": (25.05, 121.62, 25.18, 121.81),
    "Hsinchu City": (24.71, 120.87, 24.86, 121.04),
    "Chiayi City": (23.43, 120.38, 23.52, 120.51),
    "Hsinchu County": (24.42, 120.92, 24.95, 121.42),
    "Miaoli County": (24.28, 120.62, 24.75, 121.27),
    "Changhua County": (23.78, 120.21, 24.21, 120.68),
    "Taitung County": (22.22, 120.73, 23.45, 121.50),
    "Hualien County": (23.09, 120.98, 24.38, 121.78),
    "Yilan County": (24.30, 121.31, 24.99, 121.97),
    "Pingtung County": (21.89, 120.42, 22.89, 120.92),
    "Chiayi County": (23.20, 120.11, 23.64, 120.96),
    "Yunlin County": (23.50, 120.11, 23.87, 120.74),
    "Nantou County": (23.43, 120.61, 24.26, 121.36),
}
START_ID = 250

def get_picture(lat, lon, heading=0, pitch=0, fov=90):
    heading = random.randint(0, 359)
    url = f"{URL}?size=640x640&location={lat},{lon}&heading={heading}&pitch={pitch}&fov={fov}&key={GOOGLE_MAP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return None
    
def check_picture_exist(lat, lon):
    url = f"{URL}/metadata?location={lat},{lon}&key={GOOGLE_MAP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        status = json.loads(response.content.decode())['status']
        if status == 'OK':
            return True
        else:
            return False
    else:
        print(response.content)
        return None

def get_address(lat, lon):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={GOOGLE_MAP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content.decode())
        city = None
        address = None
        for item in data['results']:
            if 'administrative_area_level_1' in item['types']:
                city = item['formatted_address']
                break
            if 'route' in item['types']:
                address = item['formatted_address']
        if city == None:
            return None, None
        city = city.split(',')[0]
        return city, address
    else:
        return None, None
    
    

# Example usage
if __name__ == "__main__":
    # Read CSV file

    # lat, lon, city, address, picture_name
    # df = pd.DataFrame(columns=["lat", "lon", "city", "address", "picture_name"])
    df = pd.read_csv('./output.csv')

    for tar_city in CITY_LABEL:
        print("Current city: ", tar_city)
        current_cnt = 0
        try_cnt = 0
        while current_cnt < CITY_MAX:
            time.sleep(0.01)
            lat = random.uniform(CITY_RANGE[tar_city][0], CITY_RANGE[tar_city][2])
            lon = random.uniform(CITY_RANGE[tar_city][1], CITY_RANGE[tar_city][3])
            try_cnt += 1
            # print(f"Try {try_cnt}: {lat}, {lon}")
            try:
                if not check_picture_exist(lat, lon):
                    continue
                city, address = get_address(lat, lon)
                # print(city)
                if city != tar_city:
                    continue

                picture = get_picture(lat, lon)

                # save picture
                picture_name = f"{city}_{START_ID + current_cnt}.jpg"
                with open('./data/' + picture_name, 'wb') as f:
                    f.write(picture)
                
                current_cnt += 1
                
                # Append a new row to the DataFrame

                df = pd.concat([df, pd.DataFrame.from_records([{
                    "lat": lat,
                    "lon": lon,
                    "city": city,
                    "address": address,
                    "picture_name": picture_name
                }])], ignore_index=True)
                # print(df)
            except Exception as e:
                print(e)
                continue
            if current_cnt % 5 == 0:
                print(f"Current {tar_city}: {current_cnt}")
        print(f"Finish {tar_city}, use {try_cnt} times")

    # Write DataFrame to a new CSV file
    df.to_csv('./output.csv', index=False)