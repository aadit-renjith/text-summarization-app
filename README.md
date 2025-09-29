# Text Summarization Web Application

This project is a web application built with Flask that provides two modes of text summarization:

- **Abstractive summarization:** Generates new sentences that capture the core meaning of the input text using the BART transformer model from Hugging Face.
- **Extractive summarization:** Selects important sentences directly from the input text using the LexRank algorithm implemented in the Sumy library.

---

## Features

- Dual summarization modes (abstractive and extractive)
- Adjustable summary length for extractive mode
- Simple and responsive web interface
- Backend API built with Flask
- Uses state-of-the-art NLP models and classical algorithms

---

## Project Structure
backend/ ├── app.py # Flask application ├── summarizers.py # Summarization logic (BART and LexRank) ├── requirements.txt # Python dependencies ├── static/ # Frontend files (HTML, CSS, JS) │ ├── index.html │ ├── style.css │ └── script.js ├── report.tex # Project report in LaTeX ├── abstractive_mode.png # Screenshot of abstractive mode ├── extractive_mode.png # Screenshot of extractive mode └── README.md # This file


---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name/backend
   python -m venv venv
   venv\Scripts\activate
  


pip install -r requirements.txt
python -m nltk.downloader punkt stopwords
python app.py
http://127.0.0.1:5000/


Dependencies
Python 3.10+
Flask 2.3.3
Transformers 4.35.2
PyTorch 2.1.2
Sumy 0.11.0
NLTK 3.8.1
NumPy < 2.0

