from flask import Flask
app = Flask(__name__)

@app.route("/api/v1/hello-world/22")
def hello():
  return "Hello World!"

@app.route("/")
def ok():
  hello()
if __name__ == "__main__":
  app.run()
