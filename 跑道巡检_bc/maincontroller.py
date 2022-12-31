from flask import Flask
from flask import request
from flask_cors import *
from manager import mainManager

app = Flask(__name__)
CORS(app)

#home
@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'


#收到图片json参数
@app.route("/detectio", methods=["POST"])
def detectio():
    jsondata = request.get_json()
    return mainManager.receive_image_data(jsondata)

@app.route("/detectio_img",methods=["POST"])
def detectio_img():
    origin_image = request.files["origin_image"]
    current_image = request.files["current_image"]
    return mainManager.receive_image(origin_image,current_image)





if __name__ == "__main__":
    app.run(host = "0.0.0.0",port=5008)
