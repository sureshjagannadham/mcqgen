# ===========================
# StreamlitAPP.py (Main Web App UI)
# ===========================

# Import standard libraries
import os              # For environment variables and file paths
import json            # To load the Response.json template
import pandas as pd    # For working with tabular quiz data
import traceback       # For error debugging
import streamlit as st # Streamlit framework for building the web UI
from dotenv import load_dotenv  # Load API keys from .env file

# Import custom modules from your project
from src.mcqgenerator.utils import read_file, get_table_data   # Helpers for file reading & quiz table conversion
from src.mcqgenerator.logger import logging                    # Logging system
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain  # Core quiz generation chain

# Import modern LangChain components
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.callbacks.manager import get_openai_callback

# ===========================
# Load JSON template
# ===========================
with open("Response.json", "r") as file:
    RESPONSE_JSON = json.load(file)

# ===========================
# Streamlit UI Setup
# ===========================
st.title("MCQ Generator Application with LangChain ")

# Create a form for user inputs
with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or txt file")   # Upload study material
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)  # Number of questions
    subject = st.text_input("Insert Subject", max_chars=20)        # Subject name
    tone = st.text_input("Complexity Level Of Questions", max_chars=20, placeholder="Simple") # Tone/difficulty
    button = st.form_submit_button("Create MCQs")                  # Submit button

# ===========================
# Processing Logic (after form submission)
# ===========================
if button and uploaded_file is not None and mcq_count and subject and tone:
    with st.spinner("loading..."):   # Show spinner while processing
        try:
            text = read_file(uploaded_file)   # Convert uploaded file into plain text

            # Track token usage and cost of API call
            with get_openai_callback() as cb:
                # Modern LangChain compliance: use .invoke()
                response = generate_evaluate_chain.invoke({
                    "text": text,
                    "number": mcq_count,
                    "subject": subject,
                    "tone": tone,
                    "response_json": json.dumps(RESPONSE_JSON)
                })

            print(cb)   # Print token usage stats to terminal

        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)  # Debug errors
            st.error("Error")   # Show error in UI

        else:
            # ===========================
            # Token usage stats
            # ===========================
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost: {cb.total_cost}")

            # ===========================
            # Process LangChain response
            # ===========================
            if isinstance(response, dict):
                quiz = response.get("quiz", None)   # Extract quiz data

                if quiz is not None:
                    table_data = get_table_data(quiz)   # Convert JSON quiz → table format

                    if table_data:   # If table data is valid
                        df = pd.DataFrame(table_data)   # Create DataFrame
                        df.index = df.index + 1         # Start index at 1

                        # Display quiz table in UI
                        st.table(df)

                        # Convert DataFrame → CSV
                        csv = df.to_csv(index=False).encode('utf-8')

                        # Add download button for CSV
                        st.download_button(
                            label="Download MCQs as CSV",
                            data=csv,
                            file_name="machinelearning_quiz.csv",
                            mime="text/csv"
                        )

                        # Display review text from LangChain
                        st.text_area(label="Review", value=response.get("review", ""))

                    else:
                        st.error("Error in the table data")
                else:
                    st.error("Error: Quiz generation component missing from response.")
            else:
                # Fallback if response is a raw string
                st.write(response)

# ===========================
# PURPOSE OF THIS FILE:
# ---------------------------
# - Provides the web interface for your MCQ Generator.
# - Lets users upload study material (PDF/TXT).
# - Collects inputs: number of MCQs, subject, tone.
# - Calls LangChain chain to generate + evaluate quiz.
# - Displays quiz in a clean table.
# - Allows users to download quiz as CSV.
# - Shows review/feedback text from GPT.
# ===========================
