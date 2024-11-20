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
    circle_positions = data.get('circlePositions', [])
    click_positions = data.get('clickPositions', [])

    # Ensure click_positions and circle_positions are synchronized
    for _ in range(len(circle_positions) - len(click_positions)):
        click_positions.append({'x': 0, 'y': 0})

    # Prepare CSV file
    kst = pytz.timezone('Asia/Seoul')
    current_time = datetime.now(kst).strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"{current_time}_click.csv"
    filepath = os.path.join(app.static_folder, 'results', filename)

    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Index', 'Circle X', 'Circle Y', 'User X', 'User Y'])
        for index, position in enumerate(circle_positions):
            click_pos = click_positions[index]
            writer.writerow([index + 1, position['x'], position['y'], click_pos['x'], click_pos['y']])
        writer.writerow(['Summary'])
        writer.writerow(['Total Clicks', 'Total Circles', 'Success Rate (%)'])
        writer.writerow([total_clicks, total_circles, (total_clicks / total_circles) * 100])

def write_drag_data(data):
    total_drags = data.get('totalDrags', 0)
    total_circles = data.get('totalCircles', 10)
    circle_positions = data.get('circlePositions', [])
    drag_positions = data.get('dragPositions', [])

    # Ensure drag_positions and circle_positions are synchronized
    for _ in range(len(circle_positions) - len(drag_positions)):
        drag_positions.append({'startX': 0, 'startY': 0, 'endX': 0, 'endY': 0})

    kst = pytz.timezone('Asia/Seoul')
    current_time = datetime.now(kst).strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"{current_time}_drag.csv"
    filepath = os.path.join(app.static_folder, 'results', filename)

    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Index', 'Circle X', 'Circle Y', 'User-startX', 'User-startY', 'User-endX', 'User-endY'])
        for index, position in enumerate(circle_positions):
            drag_pos = drag_positions[index]
            writer.writerow([index + 1, position['x'], position['y'], drag_pos['startX'], drag_pos['startY'], drag_pos['endX'], drag_pos['endY']])
        writer.writerow(['Summary'])    
        writer.writerow(['Total Drags', 'Total Circles', 'Success Rate (%)'])
        writer.writerow([total_drags, total_circles, (total_drags / total_circles) * 100])

def write_swipe_data(data):
    total_swipes = data.get('totalSwipes', 0)
    total_circles = data.get('totalCircles', 10)
    circle_positions = data.get('circlePositions', [])
    swipe_positions = data.get('swipePositions', [])

    # Ensure swipe_positions and circle_positions are synchronized
    for _ in range(len(circle_positions) - len(swipe_positions)):
        swipe_positions.append({'startX': 0, 'startY': 0, 'endX': 0, 'endY': 0})

    kst = pytz.timezone('Asia/Seoul')
    current_time = datetime.now(kst).strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"{current_time}_swipe.csv"
    filepath = os.path.join(app.static_folder, 'results', filename)

    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Index', 'Circle X', 'Circle Y', 'Swipe-startX', 'Swipe-startY', 'Swipe-endX', 'Swipe-endY'])
        for index, position in enumerate(circle_positions):
            swipe_pos = swipe_positions[index]
            writer.writerow([index + 1, position['x'], position['y'], swipe_pos['startX'], swipe_pos['startY'], swipe_pos['endX'], swipe_pos['endY']])
        writer.writerow(['Summary'])
        writer.writerow(['Total Swipes', 'Total Circles', 'Success Rate (%)'])
        writer.writerow([total_swipes, total_circles, (total_swipes / total_circles) * 100])

def write_two_finger_swipe_data(data):
    total_swipes = data.get('totalSwipes', 0)
    total_pairs = data.get('totalPairs', 10)
    circle_positions = data.get('circlePositions', [])
    swipe_positions = data.get('swipePositions', [])

    # Debug: Print received data
    print("Received data for two-finger swipe:", data)

    # Set up the filename and path
    kst = pytz.timezone('Asia/Seoul')
    current_time = datetime.now(kst).strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"{current_time}_two_finger_swipe.csv"
    results_dir = os.path.join(app.static_folder, 'results')
    filepath = os.path.join(results_dir, filename)

    # Ensure the directory exists
    os.makedirs(results_dir, exist_ok=True)

    # Write data to CSV
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Header
            writer.writerow([
                'Index',
                'Circle1 X', 'Circle1 Y',
                'Circle2 X', 'Circle2 Y',
                'Start X1', 'Start Y1', 'End X1', 'End Y1',
                'Start X2', 'Start Y2', 'End X2', 'End Y2'
            ])

            # Write data rows
            for index, (circle_pair, swipe_pair) in enumerate(zip(circle_positions, swipe_positions)):
                # Debug: Log each pair
                print(f"Processing pair {index + 1}: Circle {circle_pair}, Swipe {swipe_pair}")

                circle1 = circle_pair.get('Circle1', {})
                circle2 = circle_pair.get('Circle2', {})
                swipe1 = swipe_pair.get('Circle1', {})
                swipe2 = swipe_pair.get('Circle2', {})

                # Write each pair's data
                writer.writerow([
                    index + 1,
                    circle1.get('x', 0), circle1.get('y', 0),
                    circle2.get('x', 0), circle2.get('y', 0),
                    swipe1.get('Circle1_startX', 0), swipe1.get('Circle1_startY', 0),
                    swipe1.get('Circle1_endX', 0), swipe1.get('Circle1_endY', 0),
                    swipe2.get('Circle2_startX', 0), swipe2.get('Circle2_startY', 0),
                    swipe2.get('Circle2_endX', 0), swipe2.get('Circle2_endY', 0)
                ])

            # Add summary row
            success_rate = (total_swipes / total_pairs) * 100 if total_pairs > 0 else 0
            writer.writerow([])
            writer.writerow(['Summary'])
            writer.writerow(['Total Swipes', 'Total Pairs', 'Success Rate (%)'])
            writer.writerow([total_swipes, total_pairs, f"{success_rate:.2f}"])
    except Exception as e:
        print("Error writing data to CSV:", e)




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/click')
def click():
    return render_template('click.html')

@app.route('/drag')
def drag():
    return render_template('drag.html')

@app.route('/swipe')
def swipe():
    return render_template('swipe.html')

@app.route('/two_finger_swipe')
def two_finger_swipe():
    return render_template('two_finger_swipe.html')

@app.route('/save_results', methods=['POST'])
def save_results():
    data = request.get_json()
    print("Incoming data:", data)  # Debug: Log the incoming data

    # if not data:
    #     return jsonify({"status": "error", "message": "No data provided"}), 400

    test_type = data.get('testType', '')
    try:
        if test_type == 'click':
            write_click_data(data)
        elif test_type == 'drag':
            write_drag_data(data)
        elif test_type == 'swipe':
            write_swipe_data(data)
        elif test_type == 'two-finger-swipe':
            write_two_finger_swipe_data(data)
        else:
            return jsonify({"status": "error", "message": "Unknown test type"}), 400

        return jsonify({"status": "success"})
    except Exception as e:
        print("Error processing data:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/log_debug', methods=['POST'])
def log_debug():
    data = request.get_json()
    print("Frontend Debug Log:", data.get('log'))
    return jsonify({"status": "success"})


@app.route('/results')
def list_results():
    # List CSV files in the static/results directory
    results_dir = os.path.join(app.static_folder, 'results')
    files = [f for f in os.listdir(results_dir) if f.endswith('.csv')]

    # Sort files by creation time in descending order (most recent first)
    files = sorted(files, key=lambda f: os.path.getctime(os.path.join(results_dir, f)), reverse=True)

    # print("Files found:", files)  # Debugging line
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

