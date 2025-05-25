from flask import Flask, request, render_template, session
from transformers import pipeline
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = 'your-secret-key-123'

# Initialize QA model
qa_model = pipeline(
    "question-answering",
    model="AsmaAwad/distilbert-base-uncased-NaturalQuestions"
)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def extract_text_from_url(url):
    try:
        if not is_valid_url(url):
            return "Error: Invalid URL format"
            
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'iframe', 'img']):
            element.decompose()
        
        # Get main content or fall back to body
        main_content = soup.find('main') or soup.find('article') or soup.find('body')
        text = ' '.join(main_content.stripped_strings)
        
        if not text:
            return "Error: No text content found"
            
        return text[:3000]
    
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'history' not in session:
        session['history'] = []
    
    active_tab = session.get('active_tab', 'textTab')
    error = None
    answer = None
    confidence = None
    source_preview = None
    current_question = None
    current_context = ""
    current_url = ""

    if request.method == 'POST':
        if 'clear' in request.form:
            session['history'] = []
        else:
            # Get input data
            source_type = "url" if 'url' in request.form and request.form['url'] else "text"
            active_tab = 'urlTab' if source_type == "url" else 'textTab'
            
            question = request.form.get('question', '').strip()
            current_question = question
            source_content = ""
            
            if source_type == "url":
                url = request.form['url'].strip()
                current_url = url
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                source_content = extract_text_from_url(url)
            else:
                current_context = request.form.get('context', '')
                source_content = current_context
            
            # Process question if we have valid input
            if question and source_content and not source_content.startswith("Error:"):
                try:
                    result = qa_model(
                        question=question,
                        context=source_content,
                        max_answer_len=50,
                        max_question_len=30,
                        max_seq_len=512
                    )
                    answer = result["answer"]
                    confidence = round(result["score"] * 100, 2)
                    source_preview = source_content[:150] + ("..." if len(source_content) > 150 else "")
                    
                    session['history'].insert(0, {
                        'timestamp': datetime.now().strftime("%H:%M:%S"),
                        'source_type': source_type,
                        'question': question,
                        'answer': answer,
                        'confidence': confidence,
                        'source_preview': source_preview
                    })
                except Exception as e:
                    error = f"Processing error: {str(e)}"
            
            session['active_tab'] = active_tab
            session.modified = True

    return render_template(
        'index.html',
        history=session['history'],
        active_tab=active_tab,
        error=error,
        current_answer=answer,
        current_question=current_question,
        current_confidence=confidence,
        current_source=source_preview,
        current_context=current_context,
        current_url=current_url
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)