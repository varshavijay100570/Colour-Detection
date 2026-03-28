from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        # Get the file path from the request
        data = request.get_json()
        file_path = data.get('filePath')
        
        # Validate file path
        if not file_path or not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        # Run the script using subprocess
        result = subprocess.run(
            ['python', file_path], 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        # Return the output
        return jsonify({
            'output': result.stdout,
            'error_output': result.stderr
        })
    
    except subprocess.CalledProcessError as e:
        # Handle script execution errors
        return jsonify({
            'error': 'Script execution failed',
            'details': e.stderr
        }), 500
    
    except Exception as e:
        # Handle other potential errors
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='ip-address', port=0000, debug=True)
