from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from datetime import datetime
import pytz
import csv

app = Flask(__name__)

# Ensure the results directory exists within static
os.makedirs(os.path.join(app.static_folder, 'results'), exist_ok=True)

def write_data_to_csv(filename, header, data_rows, summary_header, summary_data):
    """Helper function to write data to a CSV file."""
    results_dir = os.path.join(app.static_folder, 'results')
    os.makedirs(results_dir, exist_ok=True)
    filepath = os.path.join(results_dir, filename)

    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Write header
            writer.writerows(data_rows)  # Write data rows
            writer.writerow([])  # Empty row
            writer.writerow(summary_header)  # Write summary header
            writer.writerow(summary_data)  # Write summary data
    except Exception as e:
        print("Error writing data to CSV:", e)
        raise


def generate_filename(prefix):
    """Helper function to generate a timestamped filename."""
    kst = pytz.timezone('Asia/Seoul')
    current_time = datetime.now(kst).strftime('%Y-%m-%d_%H-%M-%S')
    return f"{current_time}_{prefix}.csv"

def write_click_data(data):
    """Process and write click data to a CSV file."""
    total_clicks = data.get('totalClicks', 0)
    total_circles = data.get('totalCircles', 10)
    circle_positions = data.get('circlePositions', [])
    click_positions = data.get('clickPositions', [])
    results = data.get('results', [])
    # Ensure synchronized positions
    for _ in range(len(circle_positions) - len(click_positions)):
        click_positions.append({'x': 0, 'y': 0})

    # Prepare rows for CSV
    data_rows = [
        [index + 1, pos['x'], pos['y'], click['x'], click['y'], result]
        for index, (pos, click, result) in enumerate(zip(circle_positions, click_positions, results))
    ]
    summary_header = ['Total Clicks', 'Total Circles', 'Success Rate (%)']
    summary_data = [total_clicks, total_circles, round((total_clicks / total_circles) * 100, 2)]

    filename = generate_filename('click')
    header = ['Index', 'Circle X', 'Circle Y', 'User X', 'User Y', 'Result']
    write_data_to_csv(filename, header, data_rows, summary_header, summary_data)


def write_drag_data(data):
    """Process and write drag data to a CSV file."""
    total_drags = data.get('totalDrags', 0)
    total_circles = data.get('totalCircles', 10)
    circle_positions = data.get('circlePositions', [])
    drag_positions = data.get('dragPositions', [])
    results = data.get('results', [])
    # Ensure synchronized positions
    for _ in range(len(circle_positions) - len(drag_positions)):
        drag_positions.append({'startX': 0, 'startY': 0, 'endX': 0, 'endY': 0})

    # Prepare rows for CSV
    data_rows = [
        [index + 1, pos['x'], pos['y'], drag['startX'], drag['startY'], drag['endX'], drag['endY'], result]
        for index, (pos, drag, result) in enumerate(zip(circle_positions, drag_positions, results))
    ]
    summary_header = ['Total Drags', 'Total Circles', 'Success Rate (%)']
    summary_data = [total_drags, total_circles, round((total_drags / total_circles) * 100, 2)]

    filename = generate_filename('drag')
    header = ['Index', 'Circle X', 'Circle Y', 'User-startX', 'User-startY', 'User-endX', 'User-endY', 'Results']
    write_data_to_csv(filename, header, data_rows, summary_header, summary_data)

def write_swipe_data(data):
    """Process and write swipe data to a CSV file."""
    total_swipes = data.get('totalSwipes', 0)
    total_circles = data.get('totalCircles', 10)
    circle_positions = data.get('circlePositions', [])
    swipe_positions = data.get('swipePositions', [])
    results = data.get('results', [])
    # Ensure synchronized positions
    for _ in range(len(circle_positions) - len(swipe_positions)):
        swipe_positions.append({'startX': 0, 'startY': 0, 'endX': 0, 'endY': 0})

    # Prepare rows for CSV
    data_rows = [
        [index + 1, pos['x'], pos['y'], swipe['startX'], swipe['startY'], swipe['endX'], swipe['endY'], result]
        for index, (pos, swipe, result) in enumerate(zip(circle_positions, swipe_positions, results))
    ]
    summary_header = ['Total Swipes', 'Total Circles', 'Success Rate (%)']
    summary_data = [total_swipes, total_circles, round((total_swipes / total_circles) * 100, 2)]

    filename = generate_filename('swipe')
    header = ['Index', 'Circle X', 'Circle Y', 'Swipe-startX', 'Swipe-startY', 'Swipe-endX', 'Swipe-endY', 'Result']
    write_data_to_csv(filename, header, data_rows, summary_header, summary_data)

def write_two_finger_swipe_data(data):
    """Process and write two-finger swipe data to a CSV file."""
    total_swipes = data.get('totalSwipes', 0)
    total_pairs = data.get('totalPairs', 10)
    circle_positions = data.get('circlePositions', [])
    swipe_positions = data.get('swipePositions', [])
    results = data.get('results', [])

    # Prepare rows for CSV
    data_rows = [
        [
            index + 1,
            pair['Circle1']['x'], pair['Circle1']['y'],
            pair['Circle2']['x'], pair['Circle2']['y'],
            swipe['Circle1']['Circle1_startX'], swipe['Circle1']['Circle1_startY'], swipe['Circle1']['Circle1_endX'], swipe['Circle1']['Circle1_endY'],
            swipe['Circle2']['Circle2_startX'], swipe['Circle2']['Circle2_startY'], swipe['Circle2']['Circle2_endX'], swipe['Circle2']['Circle2_endY'],
            result
        ]
        for index, (pair, swipe, result) in enumerate(zip(circle_positions, swipe_positions, results))
    ]
    summary_header = ['Total Swipes', 'Total Pairs', 'Success Rate (%)']
    success_rate = round((total_swipes / total_pairs) * 100, 2) if total_pairs > 0 else 0
    summary_data = [total_swipes, total_pairs, f"{success_rate:.2f}"]
    header = ['Index','Circle1 X', 'Circle1 Y','Circle2 X', 'Circle2 Y','Start X1', 'Start Y1', 'End X1', 'End Y1','Start X2','Start Y2', 'End X2', 'End Y2', 'Results']
    filename = generate_filename('two_finger_swipe')
    write_data_to_csv(filename, header, data_rows, summary_header, summary_data)

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

