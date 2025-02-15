import os
from flask import Flask, render_template, request
app = Flask(__name__)

UPLOAD_FOLDER = "uploads" 
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def process_file(file_path):
    return f"Processed file: {os.path.basename(file_path)}"


@app.route("/", methods=["GET", "POST"])
def upload_file():
    result = None  # Default value

    if request.method == "POST":
        if "file" not in request.files:
            result = "No file part"
        else:
            file = request.files["file"]
            if file.filename == "":
                result = "No selected file"
            else:
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(file_path)  # Save file

                # Dummy test value
                result = process_file(file_path) # Instead of calling a function, just testing

    return render_template("index.html", output=result)  # Always pass 'result'

if __name__ == "__main__":
    app.run(debug=True)