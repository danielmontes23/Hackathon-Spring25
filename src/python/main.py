from flask import Flask, jsonify, send_from_directory
import doc
from pylatex import *
import ast
import base64


texfile = doc.document_creation()
file_name =""


app = Flask(__name__)
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

@app.route('/section_add/<args>', methods=['GET'])
def add_section(args):
    argsd = ast.literal_eval(base64.b64decode(args).decode("utf-8"))
    valid = {'isvalid': False}
    if len(argsd.keys()) == 2:
        valid = texfile.add_section_2(argsd['section'], argsd['section_data'])
    elif len(argsd.keys()) == 6:
        valid = texfile.add_section_6(argsd['section'],argsd['dates'],argsd['title'],argsd['company'],argsd['city'],argsd['country'], argsd['data'])
    return valid   

@app.route('/generate', methods=['GET'])
def generate():
    valid = texfile.generate("test_name")
    if not valid:
        valid = {'isvalid': False}
    return jsonify(valid)

@app.route('/download', methods=['GET'])
def download_file():
    return send_from_directory('output', file_name, as_attachment=True)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)