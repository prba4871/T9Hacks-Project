from pdf2image import convert_from_path
from google.cloud import vision
import io
import os
from transformers import pipeline
from flask import Flask, render_template, request
app = Flask(__name__)

UPLOAD_FOLDER = "uploads" 
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Define the medical report PDF path
# pdf_path = "/content/Medical_Reports.pdf"

# Function to convert PDF to summarized text
def sumdr(file_path):
    # Convert PDF pages to images
    image_pages = convert_from_path(file_path)

    # Set up Google Cloud Vision API authentication
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/pradyu/T9Hacks-Project/SourceCode/dauntless-ember-451005-p2-fc46e432ae31.json"

    # Initialize Google Cloud Vision API client
    client = vision.ImageAnnotatorClient()

    # Function to extract text from an image
    def extract_text(image):
        image_memory_buffer = io.BytesIO()
        image.save(image_memory_buffer, format='JPEG')
        image_byte_data = image_memory_buffer.getvalue()
        image_vision = vision.Image(content=image_byte_data)
        response_text = client.text_detection(image=image_vision)

        if response_text.error.message:
            raise Exception(f"Error: {response_text.error.message}")

        return response_text.text_annotations[0].description if response_text.text_annotations else ""

    # List to store extracted text from each page
    full_text_list = []

    # Extract text from each image and store in full_text_list
    for i, image in enumerate(image_pages):
        page_text = extract_text(image)
        full_text_list.append(f"Page {i+1}:\n{page_text}")

    # Print extracted text for debugging
    for page in full_text_list:
        print(page)

    # Initialize Hugging Face summarizer
    summarizer = pipeline("summarization")

    # List to store summaries
    smdr = []

    # Generate summaries for each page
    for i, page_text in enumerate(full_text_list):
        try:
            summary = summarizer(page_text, max_length=500, min_length=50, do_sample=False)
            summary_text = summary[0]['summary_text']
            print(f"Summary of Page {i+1}:\n{summary_text}")
            smdr.append(summary_text)
        except Exception as e:
            print(f"Summarization failed for Page {i+1}: {e}")
            smdr.append(f"Summarization failed for Page {i+1}: {e}")

    return smdr

# Call the function
# print(sumdr(pdf_path))

# def process_file(file_path):
#     return f"Processed file: {os.path.basename(file_path)}"


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
                result = sumdr(file_path) # Instead of calling a function, just testing

    return render_template("index.html", output=result)  # Always pass 'result'

if __name__ == "__main__":
    app.run(debug=True)
