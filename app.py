from flask import Flask, render_template, request
#from werkzeug import secure_filename
from PIL import Image
import cv2 as cv
import os
from pathlib import Path
from datetime import datetime
from extract_features import gabor_extractor
from Image_retrieval import run_search

app = Flask(__name__)
#UPLOAD_FOLDER='static/uploads/'

app.secret_key = "secret key"
#pp.config['UPLOAD_FOLDER'] = #UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg','gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/',methods=["GET","POST"])
def index():
    if request.method == 'POST':

        file = request.files['query_img']



        if file and allowed_file(file.filename):
            
            #query image
            query_img = Image.open(file.stream)

            #path of image
            uploaded_img_path = './BE/' + \
            datetime.now().isoformat().replace(":",".") + "_" + file.filename

            
            #saving image in uploads folder
            query_img.save(uploaded_img_path)

            #read image
            img = cv.imread(uploaded_img_path)

            #extract features of query image
            query_features = gabor_extractor(img)
            query_features = [str(f) for f in query_features]
            output_file = './features.csv'
            #save new query features to database
            with open(output_file, 'a', encoding="utf8") as f:
                f.write("%s,%s\n" % (uploaded_img_path, ",".join(query_features)))
                f.close()
            
            results = run_search(query_features)
            # results = searcher.gaborSearch(features)

            


            return render_template('index.html',query_path=uploaded_img_path, scores = results)
    else:
            
        return render_template('index.html')




if __name__ == "__main__":
    app.run(debug=True)