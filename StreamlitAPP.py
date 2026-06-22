import os
import json
import pandas as pd
import traceback
import streamlit as st
from dotenv import load_dotenv

# Import custom modules from your src package
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain

# Modern LangChain core components
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.callbacks.manager import get_openai_callback


with open("Response.json", "r") as file:
    RESPONSE_JSON = json.load(file) 

st.title("MCQ Generator Application with LangChain ")

# Create a form using st.form
with st.form("user_inputs"):
    # File Upload
    uploaded_file = st.file_uploader("Upload a PDF or txt file")
    
    # Input Fields
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)
    
    # Subject
    subject = st.text_input("Insert Subject", max_chars=20)
    
    # Quiz Tone
    tone = st.text_input("Complexity Level Of Questions", max_chars=20, placeholder="Simple")
    
    # Add Button
    button = st.form_submit_button("Create MCQs")
    # Check if the button is clicked and all fields have input
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text = read_file(uploaded_file)
                
                # Count tokens and the cost of API call
                with get_openai_callback() as cb:
                    # Fixed: Added .invoke() for modern LangChain compliance
                     response = generate_evaluate_chain.invoke({
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    })
                    
                # Print token usage costs to your terminal logs
                print(cb)
                
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")
            
            else: 
                # 1. Print token usage statistics to your terminal console logs
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Total Cost: {cb.total_cost}")
                
                # 2. Safely parse and process the LangChain response object
                if isinstance(response, dict):
                    # Extract the quiz data from the response dictionary
                    quiz = response.get("quiz", None)
                    
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        
                        # FIXED: Changed from 'is not None' to handle 'False' safely
                        if table_data:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            
                            # Render the clean question matrix table grid interface
                            st.table(df)
                            
                            # Display the review text safely in a text area box element
                            st.text_area(label="Review", value=response.get("review", ""))
                        else:
                            st.error("Error in the table data")
                    else:
                        st.error("Error: Quiz generation component missing from response.")
                        
                else:
                    # Fallback if response is unexpectedly a raw string rather than a dictionary
                    st.write(response)


                        
