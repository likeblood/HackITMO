import flask
from flask import Flask, request

from prepare_data import main_predict

app = Flask(__name__)


@app.route('/predict', methods = ['POST'])
def predict():
    if flask.request.method == "POST":
        json_ = request.json

        if json_ == None or json_ == "" or json_ == "null":
            response = "no data"
            code = 400
            print(f"code == {code}")
        else:
            if json_["event_type"] == "toxic_or_not":
                response = main_predict(json_)
                code = 200

        return response, code


if __name__ == '__main__':
    app.run(debug=True)
