from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

#Get Location
def get_location(ip):
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/")
        data = response.json()
        return data['city'], data['latitude'], data['longitude']
    except Exception as e:
        return None, None, None


#Get Temperature
def get_temperature(lat, lon):
    api_key = "45d69227f2d64a2a90d20ede96627feb"
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data['main']['temp']


#Create Endpoint
@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'Guest')
    client_ip = request.remote_addr
    
    city, latitude, longitude = get_location(client_ip)
    if city:
        temperature = get_temperature(latitude, longitude)
        greeting = f"Hello, {visitor_name.strip('"')}!, The temperature is {temperature} degrees Celsius in {city}"
    else:
        city = "Unknown"
        greeting = f"Hello, {visitor_name.strip('"')}!, We couldn't determine your location."

    return jsonify({
        "client_ip": client_ip,
        "location": city,
        "greeting": greeting
    })

if __name__ == '__main__':
    app.run(debug=True)
