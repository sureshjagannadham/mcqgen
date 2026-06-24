# ===========================
# utils.py (Helper Functions)
# ===========================

# Import standard libraries
import os            # For file handling
import json          # To parse JSON strings into Python dicts
import traceback     # For error debugging
import pypdf         # Modern library to read PDF files

# ===========================
# Function 1: read_file(file)
# ===========================
def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            # Use pypdf to read PDF files
            pdf_reader = pypdf.PdfReader(file)
            text = ""
            # Extract text from each page
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            # If PDF reading fails, raise a custom error
            raise Exception("error reading the PDF file")

    elif file.name.endswith(".txt"):
        # If file is plain text, read and decode it
        return file.read().decode("utf-8")

    else:
        # Reject unsupported formats
        raise Exception(
            "unsupported file format only pdf and text file supported"
        )

# PURPOSE:
# - This function ensures the app can handle both PDF and TXT uploads.
# - Converts uploaded file into plain text for the MCQ generator to process.
# - Centralizes file reading logic so other parts of the project don’t repeat code.

# ===========================
# Function 2: get_table_data(quiz_str)
# ===========================
def get_table_data(quiz_str):
    try:
        # Convert quiz string (JSON format) into Python dictionary
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []

        # Iterate over each MCQ entry in the dictionary
        for key, value in quiz_dict.items():
            mcq = value["mcq"]   # The question text

            # Format options neatly: "A-> Option1 || B-> Option2"
            options = " || ".join(
                [
                    f"{option}-> {option_value}" 
                    for option, option_value in value["options"].items()
                ]
            )

            correct = value["correct"]  # Correct answer

            # Append structured data for table display
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

        return quiz_table_data

    except Exception as e:
        # If JSON parsing fails, print error details
        traceback.print_exception(type(e), e, e.__traceback__)
        return False

# PURPOSE:
# - Converts raw quiz JSON into a clean table format.
# - Makes it easy to display MCQs in Streamlit as a DataFrame/table.
# - Handles errors gracefully if JSON is invalid.
# ===========================

# WHY THIS FILE EXISTS:
# ---------------------------
# - utils.py is a "helper module" that keeps reusable functions separate.
# - read_file() → handles file uploads (PDF/TXT → text).
# - get_table_data() → converts quiz JSON into structured table data.
# - By isolating these utilities, the main app (StreamlitAPP.py & MCQGenerator.py)
#   stays clean and focused only on quiz logic.
# ===========================
