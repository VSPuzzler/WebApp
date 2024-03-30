from flask import Flask, request, render_template, send_from_directory, jsonify
import os
import subprocess
import time
import random

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        #process = subprocess.Popen('asd', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        #stdout, stderr = process.communicate()        

        time.sleep(random.randint(1, 2))  # Random delay between 20 to 30 seconds
        # Assuming processing creates an output file named 'output_file.nii.gz' in OUTPUT_FOLDER
        if filename == "MRA_001.nii.gz":
            output_filename = "ARTERY_001.nii.gz"
            model_url = "static/ARTERY_001.glb"
            aneursym_filename = "ANEURYSM_MASK_001.nii.gz"
        elif filename == "MRA_002.nii.gz":
            output_filename = "ARTERY_002.nii.gz"
            model_url = "static/ARTERY_002.glb"
            aneursym_filename = "ANEURYSM_MASK_001.nii.gz"
        elif filename == "MRA_003.nii.gz":
            output_filename = "ARTERY_003.nii.gz"
            model_url = "static/ARTERY_003.glb"
        else:
            output_filename = "ARTERY_002.nii.gz"
        return jsonify({"success": "File processed successfully", "filename": output_filename, "model_url": model_url, "aneurysm_filename": aneursym_filename})
    else:
        return jsonify({"error": "Only .nii.gz files are allowed"})
        #if process.returncode == 0:
            # Command was successful
          #  return jsonify({"success": True})
        #else:
            # Command failed
          #  return jsonify({"error": "Command failed", "details": stderr.decode()})

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory("output", filename, as_attachment=True)
        
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 2)[-2:] == ['nii', 'gz']
if __name__ == '__main__':
    app.run(debug=True)
