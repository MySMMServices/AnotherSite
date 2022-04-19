from flask import Flask, redirect, url_for, render_template, request, flash, make_response
import Drive
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
path = os.getcwd()
app.config['UPLOAD_FOLDER'] = path
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def filters(data:list, email:str):
    data.pop(0)
    maindt = []
    post = []
    position = 0
    for dt in data:
        if dt[4] == email and not "imgur.com" in dt[13] and not 'deals4free.in' in dt[13]:
            maindt.append(dt)
            post.append(f"{position}") # here inside the post its sno and position
        position = position + 1
    return maindt, post

@app.route("/")
def indexpage():
    return render_template('index.html')

@app.route("/uploadimg", methods=["POST"])
def uploadimg():
    if 'files[]' not in request.files:
        flash('No file part')
        return redirect(request.url)
    ids = request.args.get("id")
    files = request.files.getlist('files[]')
    n = 0
    linkList = []
    for file in files:
        if n > 10:
            break
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            link = Drive.uploadFile(filename)
            if link:
                linkList.append(Drive.uploadFile(filename))
                n = n + 1
        else:
            flash("This type of file is not supported or file not found")
    if len(link):
        pass
    else:
        flash("Error while updating data please contact site owner")
    cookies = request.cookies.get("mail")
    Drive.updateseq(cookies, linkList, ids)
    return redirect(f'/submitDT?mail={cookies.split(":")[0]}')

@app.route("/submitDT")
def submitDT():
    mail = request.args.get('mail')
    allData = Drive.getDetails()
    reldt, position = filters(allData, mail)
    # 17, 20, 23, 26, 29, 32, 35, 38, 41, 44
    resp = make_response(render_template('showdata.html', data=reldt))
    resp.set_cookie('mail', f"{mail}:{position}") # here i am storing email and position which is post inside which its there is sno. and position of the mail
    # now here i am going to check mail and sno. to get the proper data and change its screenshots link
    return resp

@app.route("/index.html")
def indexpg():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=8080)
