# Oblicode_AI

## 📌 Project Description
Oblicode_AI is an intelligent **chatbot** built using **Retrieval-Augmented Generation (RAG)** and **Google Gemini API**.  
It is designed to answer questions related to the **Senegalese Civil and Commercial Obligations Code**, leveraging document embeddings and vector search for accurate responses.

## 🚀 Features
- ✅ Uses **RAG** architecture for improved context-based answers  
- ✅ Integrated with **Google Gemini API**  
- ✅ Handles Senegalese legal documents (Civil & Commercial Obligations Code)  
- ✅ Containerized with **Docker**  
- ✅ Automated deployment via **GitHub Actions** to **AWS EC2**

## 🛠️ Tech Stack
- **Python (Flask)**
- **ChromaDB** for vector storage
- **Docker** for containerization
- **GitHub Actions** for CI/CD
- **AWS EC2** for hosting

## ▶️ How to Run Locally
```bash
git clone https://github.com/thierrosyrius/Oblicode_AI.git
cd Oblicode_AI
docker build -t oblicode_ai .
docker run -p 5001:5001 oblicode_ai
