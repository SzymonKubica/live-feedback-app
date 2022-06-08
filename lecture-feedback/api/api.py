from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_folder='../build', static_url_path='/')
CORS(app)

@app.route("/")
@cross_origin()
def index():
    return app.send_static_file("index.html")

@app.route("/test")
@cross_origin()
def test():
    import random
    return {"test":random.randint(0,100)}

if __name__ == "__main__":
    app.run()