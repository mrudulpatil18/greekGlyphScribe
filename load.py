from keras.models import model_from_json
import pandas as pd

def init():
    json_file = open('models/model_33.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("models/model_33.h5")
    print("Loaded Model from disk")
    loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return loaded_model

def get_df():
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

    data = []

    for latex, index in greek_symbols.items():
        name = latex[1:]  # Remove the backslash to get the name
        link = f"https://en.wikipedia.org/wiki/{name}"  # Generate Wikipedia link
        data.append([latex, name, link, index])
        df = pd.DataFrame(data, columns=['LaTeX', 'Name', 'Link', 'Index'])
    return df
