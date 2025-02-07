from flask import Flask, request, jsonify, render_template
import util
from flask_cors import CORS

app = Flask(__name__)  # Serve static files from the 'static' folder
CORS(app)  # Allow cross-origin requests

@app.route('/')
def home():
    """ Serve the HTML page """
    return render_template('app.html')

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    """ Returns a list of locations for the frontend dropdown """
    response = jsonify({'locations': util.get_location_names()})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    """ Predicts home price based on user input """
    try:
        data = request.form if request.form else request.json  # Handle both form and JSON requests
        total_sqft = float(data['total_sqft'])
        location = data['location']
        bhk = int(data['bhk'])
        bath = int(data['bath'])
        balcony = int(data['balcony'])

        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath, balcony)

        response = jsonify({'estimated_price': estimated_price})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run(debug=True)  # Enable debug mode for easier troubleshooting
