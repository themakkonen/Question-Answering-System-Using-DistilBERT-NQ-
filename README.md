# Question Answering System Using DistilBERT-NQ

This is a web-based Question Answering (QA) system built using the pretrained DistilBERT model fine-tuned on the Natural Questions dataset. It allows users to input a passage and ask a question related to it, and returns the most probable answer using deep learning.

## 🧠 Features

- Uses `AsmaAwad/distilbert-base-uncased-NaturalQuestions` transformer model
- Accepts user-provided paragraph and question inputs
- Predicts and highlights the most relevant answer
- Flask backend for inference API
- Simple, user-friendly web interface

## 🔧 Tech Stack

- **Frontend:** HTML, CSS, Bootstrap
- **Backend:** Python, Flask
- **AI Engine:** Hugging Face Transformers, DistilBERT
- **Model:** `AsmaAwad/distilbert-base-uncased-NaturalQuestions`

## 🖥️ Screenshots

| Input Page | Output Page |
|------------|-------------|
| ![Input Screenshot](static/images/input_example.png) | ![Output Screenshot](static/images/output_example.png) |

> _Note: Replace with actual screenshots in your project path._

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Question-Answering-System-Using-DistilBERT-NQ.git
cd Question-Answering-System-Using-DistilBERT-NQ
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
pip install -r requirements.txt
pip install flask transformers torch
python app.py
QA System/
│
├── app.py                # Flask application
├── templates/
│   └── index.html        # HTML form for user input
├── static/
│   └── styles.css        # Styling
├── model/
│   └── [optional model loading or tokenizer cache]
└── README.md             # Project overview
