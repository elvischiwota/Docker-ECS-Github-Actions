from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to Python V2 🎉"

if __name__ == "__main__":
    # Bind to 0.0.0.0 so it works in Docker/ECS
    app.run(host="0.0.0.0", port=5000) 