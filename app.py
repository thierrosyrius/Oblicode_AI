from flask import Flask, request, render_template
import os
from gen_ai_app import load_pdf, split_text, create_chroma_db, load_chroma_collection, get_relevant_passage, make_rag_prompt, generate_answer

app = Flask(__name__)

# Configuration
pdf_path = "/app/data/Senegal_Civil_Commercial_Obligations_Code.pdf"
#r"C:\Users\VegaNtech\Documents\5-Day-Gen-AI-Intensive-Google\gen_ai_rag_app\data\Senegal_Civil_Commercial_Obligations_Code.pdf"
db_folder = "chromadb"
db_name = "rag_experiment"
db_path = os.path.join(os.getcwd(), db_folder)

# Create chroma_db folder if none exists
if not os.path.exists(db_folder):
    os.makedirs(db_folder)

# Initialize in advance
pdf_text = load_pdf(pdf_path)
chunked_text = split_text(pdf_text)

# Check if DB exists, otherwise create it
if not os.path.exists(os.path.join(db_folder, f"{db_name}.sqlite3")):
    db = create_chroma_db(chunked_text, db_path, db_name)
else:
    db = load_chroma_collection(db_path, db_name)

# Main road
@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_query = request.form["query"]
        relevant_texts = get_relevant_passage(user_query, db, n_results=1)
        final_prompt = make_rag_prompt(user_query, "".join(relevant_texts))
        answer = generate_answer(final_prompt)
        return render_template('index.html', answer=answer)
    return render_template('index.html', answer=None)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

