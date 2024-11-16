import json
import os
from GridTools import Grid, GridTransformation, GridCell, GridUtils, Entity # Import your GridTools classes
from GridTools import *


from flask import Flask, jsonify, request, render_template
import sys
import io
import traceback
import uuid
import contextlib

app = Flask(__name__, static_folder="static")

# Serve the HTML interface
@app.route('/')
def index():
    return app.send_static_file('testing_interface.html')

# Load training data
def load_json_data(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data

@app.route('/get_task', methods=['POST'])
def get_task():
    task_id = request.json.get('task_id')
    file_path = os.path.join("data/training", f"{task_id}.json")
    if not os.path.exists(file_path):
        return jsonify({"error": "Task not found"}), 404
    task_data = load_json_data(file_path)
    return jsonify(task_data)

@app.route('/execute_code', methods=['POST'])
def execute_code():
    try:
        code = request.json.get('code')
        input_grid_data = request.json.get('input_grid')

        # Redirect stdout to capture print statements
        stdout = io.StringIO()
        sys.stdout = stdout

        # Prepare the execution environment
        exec_globals = {
            '__builtins__': __builtins__,
            'Grid': Grid,
            'GridCell': GridCell,
            'GridTransformation': GridTransformation,
            'input_grid_data': input_grid_data  # Make input_grid_data available
        }
        exec_locals = {}

        # Execute the user's code
        exec(code, exec_globals, exec_locals)

        # Retrieve the output grid from the exec environment
        output_grid = exec_locals.get('output_grid')
        if output_grid is None:
            return jsonify({'error': 'Your code must define an output_grid variable.'}), 400

        # Convert output_grid to list if necessary
        if isinstance(output_grid, Grid):
            output_grid_data = output_grid.to_list()
        else:
            output_grid_data = output_grid  # Assume it's already a list

        # Get any print output
        print_output = stdout.getvalue()
        print(print_output)
        # Reset stdout
        sys.stdout = sys.__stdout__

        return jsonify({
            'output_grid': output_grid_data,
            'print_output': print_output
        })
    except Exception as e:
        # Reset stdout in case of an exception
        sys.stdout = sys.__stdout__
        error_trace = traceback.format_exc()
        return jsonify({'error': str(e), 'traceback': error_trace}), 500

app.run(debug=True)
