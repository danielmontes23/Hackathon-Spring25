from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import doc
from pylatex import *
import ast
import base64


texfile = doc.document_creation()
file_name =""


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)  # This will enable CORS for all routes

@app.route('/setcolor/<color>', methods=['GET'])
def set_color(color):
    valid = texfile.set_color(base64.b64decode(color).decode("utf-8"))
    return jsonify(valid), 200

@app.route('/setstyle/<style>', methods=['GET'])
def set_style(style):
    valid = texfile.set_style(base64.b64decode(style).decode("utf-8"))
    return jsonify(valid), 200

@app.route('/setpersonals/<socials>', methods=['GET'])
def set_personals(socials):
    sd = ast.literal_eval(base64.b64decode(socials).decode("utf-8"))

    global file_name 
    file_name = f"{sd['lname']}_{sd['fname']}_resume"

    phone = social = email = homepage = None
    if 'email' in sd.keys():
        email = sd['email']
    if 'phone' in sd.keys():
        phone = sd['phone']
    if 'social' in sd.keys():
        social = sd['social']
    if 'homepage' in socials:
        homepage = sd['homepage']
    valid = texfile.personal_info(sd['fname'],sd['lname'],sd['title'],sd['faddress'],sd['laddress'],email,phone,social,homepage)
    return jsonify(valid), 200

@app.route('/generate', methods=['POST'])
def generate():
    # Check if color, style, and personal info are set
    if not texfile.color or not texfile.style or not texfile.personal_info_set:
        return jsonify({'success': False, 'message': 'Color, style, and personal info must be set first.'}), 400
    data = request.get_json()
    # texfile.generate_resume(data)
    return jsonify({'success': True, 'message': 'Resume generated!'})

@app.route('/download', methods=['GET'])
def download_file():
    return send_from_directory('output', file_name, as_attachment=True)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)