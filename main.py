import folium
import requests


def get_coordinates(city):
    url = f"http://nominatim.openstreetmap.org/search?q={city}&format=json"
    response = requests.get(url)
    data = response.json()
    lat = data[0]["lat"]
    lon = data[0]["lon"]
    return lat, lon


def get_time_zone_data(city):
    url = f"http://api.timezonedb.com/v2.1/get-time-zone?key=AES2A44IJPWD&format=json&by=position&lat={get_coordinates(city)[0]}&lng={get_coordinates(city)[1]}"
    response = requests.get(url)
    data = response.json()
    return data


def get_time_diff(city1, city2):
    time_zone_data1 = get_time_zone_data(city1)
    time_zone_data2 = get_time_zone_data(city2)
    timezone1 = time_zone_data1["gmtOffset"]
    timezone2 = time_zone_data2["gmtOffset"]
    return (timezone2 - timezone1) / 3600


def display_map(city1, city2, time1, time2, data1, data2):
    city1_lat, city1_lon = get_coordinates(city1)
    city2_lat, city2_lon = get_coordinates(city2)
    map = folium.Map(location=[(float(city1_lat) + float(city2_lat)) / 2, (float(city1_lon) + float(city2_lon)) / 2],
                     zoom_start=2)
    folium.Marker(location=[city1_lat, city1_lon],
                  popup=f"<b><font color='red'>{city1.capitalize()}: {time1}</font></b><br><b><font color='purple'>Timezone: {data1['zoneName']}</font></b><br><b><font color='blue'>GMT offset: {'+' if data1['gmtOffset'] / 3600 > 0 else '-'}{data1['gmtOffset'] / 3600} hours</font></b><br><b><font color='green'>Country: {data1['countryName']}</font></b> <br><b><font color='orange'>Region: {data1['regionName']}</font></b>").add_to(
        map)

    folium.Marker(location=[city2_lat, city2_lon],
                  popup=f"<b><font color='red'>{city2.capitalize()}: {time2}</font></b><br><b><font color='purple'>Timezone: {data2['zoneName']}</font></b><br><b><font color='blue'>GMT offset: {'+' if data2['gmtOffset'] / 3600 > 0 else '-'}{data2['gmtOffset'] / 3600} hours</font></b><br><b><font color='green'>Country: {data2['countryName']}</font></b> <br><b><font color='orange'>Region: {data2['regionName']}</font></b>").add_to(
        map)
    map.save("map_time.html")



while True:
    try:
        city1 = input("Enter the first city: ").capitalize()
        lat, lon = get_coordinates(city1)
        break
    except:
        print(f"Invalid city name: {city1}")

while True:
    try:
        city2 = input("Enter the second city: ").capitalize()
        lat, lon = get_coordinates(city2)
        break
    except:
        print(f"Invalid city name: {city2}")


while True:
    try:
        time1 = input("Enter the time in the first city (hh:mm): ")
        hour = int(time1.split(":")[0])
        minute = int(time1.split(":")[1])
        if hour >= 0 and hour <= 23 and minute >= 0 and minute <= 59:
            break
        else:
            raise Exception("Invalid time range")
    except:
        print(f"Invalid time format: {time1}. Please enter time in the format hh:mm with a valid range of 00:00-23:59")





time_diff = get_time_diff(city1, city2)
time2 = str(int(time1.split(":")[0]) + int(time_diff)) + ":" + time1.split(":")[1]

url = f"http://api.timezonedb.com/v2.1/get-time-zone?key=AES2A44IJPWD&format=json&by=position&lat={get_coordinates(city1)[0]}&lng={get_coordinates(city1)[1]}"
response = requests.get(url)
data1 = response.json()

url = f"http://api.timezonedb.com/v2.1/get-time-zone?key=AES2A44IJPWD&format=json&by=position&lat={get_coordinates(city2)[0]}&lng={get_coordinates(city2)[1]}"
response = requests.get(url)
data2 = response.json()

display_map(city1, city2, time1, time2, data1, data2)