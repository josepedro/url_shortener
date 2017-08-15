from flask import Flask

app = Flask("url_shortener")

@app.route("/")
def hello_world():
    return "<strong> hello_world!!!</strong>", 200

def main():
	app.run(host='0.0.0.0', port=8000)
