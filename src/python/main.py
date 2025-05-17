from flask import Flask, request, jsonify, send_from_directory, after_this_request
from flask_cors import CORS
import doc
from pylatex import *
import ast
import base64
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

texfile = doc.document_creation()
file_name = ""

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)  # Enable CORS for all routes

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
    if 'homepage' in sd.keys():
        homepage = sd['homepage']
    valid = texfile.personal_info(sd['fname'],sd['lname'],sd['title'],sd['faddress'],sd['laddress'],email,phone,social,homepage)
    return jsonify(valid), 200

@app.route('/section_add2/<args>', methods=['GET'])
def add_section(args):
    argsd = ast.literal_eval(base64.b64decode(args).decode("utf-8"))
    valid = {'isvalid': False}
    if len(argsd.keys()) == 2:
        if "Summary" in argsd.keys():
            valid = texfile.add_summary(argsd['section'], argsd['section_data'])
        else:
            valid = texfile.add_section_2(argsd['section'], argsd['section_data'])

    return jsonify(valid), 200

@app.route('/section_add6/<args>', methods=['GET'])
def add_section6(args):
    argsd = ast.literal_eval(base64.b64decode(args).decode("utf-8"))
    valid = texfile.add_section_6(argsd['section'], argsd['section_data'])
    return jsonify(valid), 200

@app.route('/generate', methods=['POST'])
def generate():
    # Check if color, style, and personal info are set
    if not getattr(texfile, 'color', None) or not getattr(texfile, 'style', None) or not getattr(texfile, 'personal_info_set', True):
        return jsonify({'success': False, 'message': 'Color, style, and personal info must be set first.'}), 400
    data = request.get_json()
    # texfile.generate_resume(data)
    return jsonify({'success': True, 'message': 'Resume generated!'})

@app.route('/download', methods=['GET'])
def download_file():
    filename = f"{file_name}.pdf"
    tex_filename = f"{file_name}.tex"

    @after_this_request
    def cleanup(response):
        try:
            tex_path = os.path.join(OUTPUT_DIR, tex_filename)
            if os.path.exists(tex_path):
                os.remove(tex_path)
                print(f"Removed: {tex_path}")
        except Exception as e:
            print(f"Failed to remove .tex file: {e}")
        return response

    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)