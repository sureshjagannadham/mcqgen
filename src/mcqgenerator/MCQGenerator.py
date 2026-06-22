import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv

# Your custom module imports
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging

# Modern LangChain packages (Replaces everything below line 9 in your screenshot)
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


#load the environment variables from the .env file
load_dotenv()

key =os.getenv("OPENAI_API_KEY")  # Ensure the API key is set in your environment

llm = ChatOpenAI(openai_api_key=key, model_name="gpt-4", temperature=0.7)

TEMPLATE="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE
)

quiz_chain = {"quiz": quiz_generation_prompt | llm}

TEMPLATE2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis,\
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student\
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"], 
    template=TEMPLATE2
)

# 2. Modern replacement for LLMChain with output_key="review" and verbose=True
review_chain = {"review": quiz_evaluation_prompt | llm}


# 2. Add string parsers so the text flows cleanly from step 1 to step 2
quiz_maker = quiz_generation_prompt | llm | StrOutputParser()
quiz_reviewer = quiz_evaluation_prompt | llm | StrOutputParser()

# 3. Connect them sequentially (This replaces the old SequentialChain!)
generate_evaluate_chain = (
    RunnablePassthrough.assign(quiz=quiz_maker)
    | RunnablePassthrough.assign(review=quiz_reviewer)
)

