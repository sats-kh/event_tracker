from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from datetime import datetime
import pytz
import csv

app = Flask(__name__)

# Ensure the results directory exists within static
os.makedirs(os.path.join(app.static_folder, 'results'), exist_ok=True)


def write_click_data(data):
    total_clicks = data.get('totalClicks', 0)
    total_circles = data.get('totalCircles', 10)
    duration = data.get('duration', 'N/A')
    circle_positions = data.get('circlePositions', [])
    click_positions = data.get('clickPositions', [])
    test_type = data.get('testType', 'test')

    # Get current time in Korea Standard Time (KST)
    kst = pytz.timezone('Asia/Seoul')
    current_time = datetime.now(kst).strftime('%Y-%m-%d_%H-%M-%S')

    # Prepare filename in the static/results directory
    filename = f"{current_time}_{test_type}.csv"
    filepath = os.path.join(app.static_folder, 'results', filename)

    # Write data to CSV file
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
                        
        # Write circle positions
        writer.writerow(['Circle Index', 'Circle X', 'Circle Y', 'User X', 'User Y'])
        for index, position in enumerate(circle_positions, ):
            writer.writerow([index + 1, position['x'], position['y'], click_positions[index]['x'], click_positions[index]['y']])
        writer.writerow(['Total Clicks', 'Total Circles', 'Success Rate'])
        writer.writerow([total_clicks - 1, total_circles, total_clicks/total_circles * 100])

def write_drag_data(data):
    total_drags = data.get('totalDrags', 0)
    total_circles = data.get('totalCircles', 10)
    duration = data.get('duration', 'N/A')
    circle_positions = data.get('circlePositions', [])
    drag_positions = data.get('dragPositions', [])
    test_type = data.get('testType', 'test')

    # Get current time in Korea Standard Time (KST)
    kst = pytz.timezone('Asia/Seoul')
    current_time = datetime.now(kst).strftime('%Y-%m-%d_%H-%M-%S')

    # Prepare filename in the static/results directory
    filename = f"{current_time}_{test_type}.csv"
    filepath = os.path.join(app.static_folder, 'results', filename)

    # Write data to CSV file
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
                        
        # Write circle positions
        writer.writerow(['Circle Index', 'Circle X', 'Circle Y', 'User-startX', 'User-startY', 'User-endX', 'User-endY'])
        for index, position in enumerate(circle_positions, ):
            writer.writerow([index + 1, position['x'], position['y'], drag_positions[index]['startX'], drag_positions[index]['startY'],drag_positions[index]['endX'], drag_positions[index]['endY']])
        writer.writerow(['Total Drags', 'Total Circles', 'Success Rate'])
        writer.writerow([total_drags - 1, total_circles, total_drags/total_circles * 100 ])

def write_swipe_data(data):
    total_swipes = data.get('totalSwipes', 0)
    total_circles = data.get('totalCircles', 10)
    duration = data.get('duration', 'N/A')
    circle_positions = data.get('circlePositions', [])
    swipe_positions = data.get('swipePositions', [])
    test_type = data.get('testType', 'swipe')

    # Get current time in Korea Standard Time (KST)
    kst = pytz.timezone('Asia/Seoul')
    current_time = datetime.now(kst).strftime('%Y-%m-%d_%H-%M-%S')

    # Prepare filename in the static/results directory
    filename = f"{current_time}_{test_type}.csv"
    filepath = os.path.join('static', 'results', filename)

    # Write data to CSV file
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)

        # Write circle positions
        writer.writerow(['Circle Index', 'Circle X', 'Circle Y', 'Swipe-startX', 'Swipe-startY', 'Swipe-endX', 'Swipe-endY'])
        for index, position in enumerate(circle_positions):
            writer.writerow([index + 1, position['x'], position['y'], 
                             swipe_positions[index]['startX'], swipe_positions[index]['startY'], 
                             swipe_positions[index]['endX'], swipe_positions[index]['endY']])

        # Write summary data
        writer.writerow(['Total Swipes', 'Total Circles', 'Success Rate'])
        writer.writerow([total_swipes, total_circles, (total_swipes / total_circles) * 100])
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/click')
def click():
    return render_template('click.html')

@app.route('/drag')
def tap():
    return render_template('drag.html')

@app.route('/swipe')
def swipe():
    return render_template('swipe.html')

@app.route('/save_results', methods=['POST'])
def save_results():
    data = request.get_json()
    print(data)
    if data['testType'] == 'click':
        write_click_data(data)
    elif data['testType'] == 'drag':
        write_drag_data(data)
    else:
        write_swipe_data(data)
      
    return jsonify({"status": "success"})

@app.route('/results')
def list_results():
    # List CSV files in the static/results directory
    results_dir = os.path.join(app.static_folder, 'results')
    files = [f for f in os.listdir(results_dir) if f.endswith('.csv')]

    # Sort files by creation time in descending order (most recent first)
    files = sorted(files, key=lambda f: os.path.getctime(os.path.join(results_dir, f)), reverse=True)

    print("Files found:", files)  # Debugging line
    return render_template('results.html', files=files)

@app.route('/results/view/<filename>')
def view_file(filename):
    # Ensure the path is within the `static/results` directory
    results_dir = os.path.join(app.static_folder, 'results')
    filepath = os.path.abspath(os.path.join(results_dir, filename))

    # Confirm that the resolved path is within the `results_dir`
    if not filepath.startswith(os.path.abspath(results_dir)) or not os.path.isfile(filepath):
        return "File not found", 404

    # Read the CSV file content
    rows = []
    with open(filepath, newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)

    return render_template('view_file.html', filename=filename, rows=rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

