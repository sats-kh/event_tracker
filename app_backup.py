from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime
import pytz
import csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/click')
def click():
    return render_template('click.html')

@app.route('/tap')
def tap():
    return render_template('tap.html')

@app.route('/swipe')
def swipe():
    return render_template('swipe.html')

@app.route('/save_results', methods=['POST'])
def save_results():
    data = request.get_json()
    total_clicks = data.get('totalClicks', 0)
    total_circles = data.get('totalCircles', 10)
    duration = data.get('duration', 'N/A')
    circle_positions = data.get('circlePositions', [])
    click_positions = data.get('clickPositions', [])
    test_type = data.get('testType', 'test')

    # Get current time in Korea Standard Time (KST)
    kst = pytz.timezone('Asia/Seoul')
    current_time = datetime.now(kst).strftime('%Y-%m-%d_%H-%M-%S')

    # Prepare filename
    filename = f"{current_time}_{test_type}.csv"

    # Write data to CSV file
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        
        # Write headers
        writer.writerow(['Total Clicks', 'Total Circles'])
        writer.writerow([total_clicks, total_circles])
        
        # Add a blank row
        writer.writerow([])
        
        # Write circle positions
        writer.writerow(['Circle Index', 'Circle X', 'Circle Y'])
        for index, position in enumerate(circle_positions, ):
            writer.writerow([index + 1, position['x'], position['y'], click_positions[index]['x'], click_positions[index]['y']])

    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

