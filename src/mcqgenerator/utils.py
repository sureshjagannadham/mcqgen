import os
import json
import traceback
import pypdf



def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            # Using the modern pypdf package library
            pdf_reader = pypdf.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
            
        except Exception as e:
            raise Exception("error reading the PDF file")
            
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
        
    else:
        raise Exception(
            "unsupported file format only pdf and text file supported"
        )



def get_table_data(quiz_str):
    try:
        # convert the quiz from a str to dict
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []
        
        # iterate over the quiz dictionary and extract the required information
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " || ".join(
                [
                    f"{option}-> {option_value}" for option, option_value in value["options"].items()
                ]
            )
            
            correct = value["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})
            
        return quiz_table_data
        
    except Exception as e:
        # Handles potential JSON parsing errors safely
        traceback.print_exception(type(e), e, e.__traceback__)
        return False
