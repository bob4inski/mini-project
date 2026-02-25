from flask import Flask

app = Flask(__name__)


@app.route("/hello", methods=["GET"])
def hello():
    return "Hello, World!", 200


@app.route("/hello", methods=["POST"])
def hello_post():
    return "Hello, POST", 200


@app.route("/bye", methods=["GET"])
def bye():
    return "Bye, World!", 404


if __name__ == "__main__":
    app.run(debug=True)
