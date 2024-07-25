from flask import Flask, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/search/<string:query>', methods=['GET'])
def search(query):
    api_key = ""
    
    # Define the URL and headers
    url = f'https://api.elsevier.com/content/search/sciencedirect?query={query}&count=10&sort=relevance'
    headers = {
        'X-ELS-APIKey': api_key,
        'Accept': 'application/json'
    }
    
    # Make the API request
    response = requests.get(url, headers=headers)
    
    # Check for success and return the response
    if response.status_code == 200:
        data = json.loads(response.text)
        return jsonify(data)
    else:
        return jsonify({
            'error': 'Failed to retrieve data',
            'status_code': response.status_code,
            'reason': response.text
        })

if __name__ == '__main__':
    app.run(debug=True)