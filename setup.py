# ===========================
# setup.py (Project Packaging Script)
# ===========================

# Import setuptools helpers
from setuptools import find_packages, setup

# Define the package configuration
setup(
    name="mcqgenerator",                 # Project/package name
    version="0.1.0",                     # Version number (first release)
    author='suresh kumar',               # Author name
    author_email='sureshjagannadham668@gmail.com',  # Author contact email

    # Dependencies required for this project
    install_requires=[
        "openai",        # OpenAI client library
        "langchain",     # LangChain framework
        "streamlit",     # Web app UI framework
        "python-dotenv", # Load environment variables from .env
        "PyPDF2"         # PDF reading library (older version, note: you also use pypdf)
    ],

    # Automatically find all packages inside the project (like src.mcqgenerator)
    packages=find_packages()
)

# ===========================
# PURPOSE OF THIS FILE:
# ---------------------------
# - setup.py makes your project installable as a Python package.
# - When someone runs: pip install -e .
#   → It installs your project + dependencies listed here.
# - Ensures you can import your own modules cleanly (e.g., src.mcqgenerator.utils).
# - Provides metadata (name, version, author) for distribution.
# ===========================

# WHY WRITTEN HERE:
# ---------------------------
# - This file is standard in Python projects meant to be reused or shared.
# - It allows others (or you on another machine) to install the MCQ Generator easily.
# - Keeps dependency management consistent with requirements.txt.
# ===========================
