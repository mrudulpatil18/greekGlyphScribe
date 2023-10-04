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

greek_symbols = {
    '\\pi': 0,
    '\\Sigma': 1,
    '\\lambda': 2,
    '\\Xi': 3,
    '\\Pi': 4,
    '\\tau': 5,
    '\\Phi': 6,
    '\\chi': 7,
    '\\Psi': 8,
    '\\alpha': 9,
    '\\beta': 10,
    '\\sigma': 11,
    '\\gamma': 12,
    '\\delta': 13,
    '\\Delta': 14,
    '\\zeta': 15,
    '\\eta': 16,
    '\\theta': 17,
    '\\Theta': 18,
    '\\epsilon': 19,
    '\\iota': 20,
    '\\kappa': 21,
    '\\Lambda': 22,
    '\\mu': 23,
    '\\nu': 24,
    '\\xi': 25,
    '\\rho': 26,
    '\\phi': 27,
    '\\varphi': 28,
    '\\psi': 29,
    '\\omega': 30,
    '\\Omega': 31,
    '\\varpi': 32}


def return_key(val):
    for key, value in greek_symbols.items():
        if value == val:
            return key
    return 'Key Not Found'


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
    out = out.reshape(33)
    idx = out.argsort()[-5:][::-1]
    str = ""
    for i in idx:
        str += return_key(i) + " "
    return str


def parseImage(imgData):
    imgstr = re.search(b'base64,(.*)', imgData).group(1)
    with open('output.png', 'wb') as output:
        output.write(base64.decodebytes(imgstr))


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5600))
    app.run(host='0.0.0.0', port=port)
