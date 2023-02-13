import requests

def geocode_address(address, api_key):
    # Build the URL for the API request
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    
    # Make the API request
    response = requests.get(url)
    response_json = response.json()
    
    # Extract the latitude and longitude from the API response
    latitude = response_json["results"][0]["geometry"]["location"]["lat"]
    longitude = response_json["results"][0]["geometry"]["location"]["lng"]
    
    return latitude, longitude