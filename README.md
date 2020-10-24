# HackDuke2019

## Setting up Docker

Create a Tensorflow (or whatever) base image. The `-p 5000:5000` means the container will broadcast its webpage to port 5000 on localhost.

    docker run -it -p 5000:5000 tensorflow/tensorflow:latest

Once inside the interactive Tensorflow container, install Flask and a text editor.

    apt update && apt install vim
    pip install flask

Create a root for the Flask server.

    from flask import Flask
    app = Flask(__name__)

    @app.route("/")
    def home():
        return "Hello World!"

    if __name__ == "__main__":
        # Choice of host must be 0.0.0.0, port must match the chosen -p
        app.run(host="0.0.0.0", port="5000")

Access the Flask server by going to (e.g.) 10.194.223.134:5000.
# postive.ly
