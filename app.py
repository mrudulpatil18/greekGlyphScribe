import base64
import os
import re
from flask import Flask, render_template, request
from cv2 import imread, resize
import numpy as np
from load import *
import matplotlib.pyplot as plt

app = Flask(__name__)
model = init()

df = get_df()

print(df)
def return_json(out):
    out = out.reshape(33)
    out = out*100
    idx = out.argsort()[-3:][::-1]
    predictions = df[df['Index'].isin(idx)]
    predictions["Confidence"] = out[predictions['Index']]
    predictions = predictions.sort_values(by="Confidence", ascending=False)
    print(predictions.to_json(orient = 'records'))
    return predictions.to_json(orient = 'records')

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/predict/', methods=['GET', 'POST'])
def predict():
    parseImage(request.get_data())

    x = imread('./output.png', 0)
    x = resize(x, (32, 32))
    x = x.reshape(1, 32, 32, 1)
    x = np.array(x)
    new_x = x
    new_x = new_x.reshape([32, 32])
    plt.imsave('output_reduced.png', new_x, cmap='gray')
    x = x / 255
    out = model.predict(x)

    str = return_json(out)
    return str


def parseImage(imgData):
    imgstr = re.search(b'base64,(.*)', imgData).group(1)
    with open('output.png', 'wb') as output:
        output.write(base64.decodebytes(imgstr))


if __name__ == '__main__':
    app.run()
