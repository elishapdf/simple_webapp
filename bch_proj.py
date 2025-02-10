import json
import requests
from flask import Flask, render_template

app = Flask(__name__)

# Load configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

@app.route('/')
def index():
    websites = config.get('websites', [])
    website_data = []  # List to store website info with status

    # Loop through each website entry
    for website in websites:
        name = website.get('name')
        url = website.get('url')
        description = website.get('description')
        email = website.get('email')
        contact_name = website.get('contact_name')
        
        # Try to get a response from the URL
        try:
            response = requests.get(url, timeout=5)
            # We consider the website "up" if we get a 200 status code.
            if response.status_code == 200:
                status = "Up"
            else:
                status = f"Returned {response.status_code}"
        except requests.exceptions.RequestException as e:
            # Any exception (timeout, connection error, etc.) is interpreted as the site being down.
            status = "Down"
        
        # Append a dictionary with all information
        website_data.append({
            "name": name,
            "url": url,
            "status": status,
            "description": description,
            "email": email, 
            "contact_name": contact_name
        })
    
    # Render the template and pass the list of website data
    return render_template("index.html", websites=website_data)

if __name__ == '__main__':
    app.run(debug=True)

