from flask import (Flask ,render_template,send_file,jsonify )
import os
from urllib.parse import quote_plus ,unquote_plus

app = Flask(__name__)

app.jinja_env.filters['quote_plus'] = lambda u: quote_plus(u)

@app.route('/downloads/<userid>')
def listUserFiles(userid):
    currentDir  = os.path.dirname(os.path.realpath(__file__))
    try:
        UsersFiles = os.listdir(os.path.join(currentDir,f"downloads/{userid}"))
        return render_template("index.html" ,files = list(UsersFiles) , userid= userid ,error = False)
    except  Exception as e:
        print(e)
        return render_template("index.html",error=True)



@app.route('/downloads/<userid>/<filename>')
def downloadFile(userid,filename):
    filename = unquote_plus(filename)
    currentDir  = os.path.dirname(os.path.realpath(__file__))
    UsersFiles = os.listdir(os.path.join(currentDir,f"downloads/{userid}"))
    RequestedFile =  os.path.join(currentDir,f"downloads/{userid}/{filename}")

    if os.path.isfile(RequestedFile):
        # return jsonify({"name":filename}) ,200
        return send_file(RequestedFile, as_attachment=True)
    else:
        return jsonify({"error":"file not Found"}) , 404




if __name__ == '__main__':
    app.run(port=5000,use_reloader=True, debug=True)
