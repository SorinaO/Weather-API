from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


# Domain name
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/v1/<word>")
def definition(word):
    filename = ("dictionary\dictionary.csv")
    df = pd.read_csv(filename)

    # Search for the word in the DataFrame
    result = df[df['word'].str.lower() == word.lower()]

    result_dictionary = {"word": word,
                         "definition": definition}
    return result_dictionary


if __name__ == "__main__":
    app.run(debug=True, port=5001)

