from flask import Flask
app = Flask(__name__)

@app.route("/api/v1/hello-world/22")
def hello():
  return "Hello World!"+str(22)

@app.route("/")
def ok():
  return hello()
if __name__ == "__main__":
  app.run()
