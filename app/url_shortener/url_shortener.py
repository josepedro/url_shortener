from flask import Flask

app = Flask("url_shortener")

@app.route("/")
def hello_world():
    return "<strong> hello_world!!!</strong>", 200

app.run(host='0.0.0.0')
