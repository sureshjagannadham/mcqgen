# ===========================
# MCQGenerator.py (Main Quiz Generator Logic)
# ===========================

# Import standard libraries
import os              # For environment variables and file paths
import json            # For handling JSON data structures
import traceback       # For error debugging and stack traces
import pandas as pd    # For working with tabular data (CSV, DataFrames)
from dotenv import load_dotenv  # To load API keys from .env file

# Import custom helper functions from your project
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging   # Use the logging system we set up earlier

# Import modern LangChain packages
from langchain_openai import ChatOpenAI       # OpenAI chat model wrapper
from langchain_core.prompts import PromptTemplate  # For structured prompts
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# ===========================
# Environment Setup
# ===========================

# Load environment variables from .env file (contains OPENAI_API_KEY)
load_dotenv()

# Get the OpenAI API key from environment
key = os.getenv("OPENAI_API_KEY")

# Initialize the LLM (Large Language Model) with GPT-4
llm = ChatOpenAI(openai_api_key=key, model_name="gpt-4", temperature=0.7)
# temperature=0.7 → controls creativity (higher = more creative, lower = more factual)

# ===========================
# Prompt for Quiz Generation
# ===========================

TEMPLATE = """
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
"""

# Define the prompt template for quiz generation
quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE
)

# Chain for quiz generation
quiz_chain = {"quiz": quiz_generation_prompt | llm}

# ===========================
# Prompt for Quiz Evaluation
# ===========================

TEMPLATE2 = """
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis,\
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student\
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

# Define the prompt template for quiz evaluation
quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template=TEMPLATE2
)

# Chain for quiz review
review_chain = {"review": quiz_evaluation_prompt | llm}

# ===========================
# Output Parsing & Sequential Flow
# ===========================

# Add string parsers so the text flows cleanly
quiz_maker = quiz_generation_prompt | llm | StrOutputParser()
quiz_reviewer = quiz_evaluation_prompt | llm | StrOutputParser()

# Connect them sequentially (modern replacement for SequentialChain)
generate_evaluate_chain = (
    RunnablePassthrough.assign(quiz=quiz_maker)
    | RunnablePassthrough.assign(review=quiz_reviewer)
)

# ===========================
# PURPOSE OF THIS FILE:
# ---------------------------
# - Reads input text and generates MCQs using GPT-4.
# - Ensures quiz follows JSON format for easy parsing.
# - Evaluates the quiz complexity and tone for students.
# - Uses modern LangChain pipeline (RunnablePassthrough + StrOutputParser).
# - Acts as the "brain" of your MCQ Generator project.
# ===========================
