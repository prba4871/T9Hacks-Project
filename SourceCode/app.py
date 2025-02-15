from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file.filename.endswith(".pdf"):
            return "File uploaded successfully!"
        else:
            return "Only PDF files are allowed!", 400
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)