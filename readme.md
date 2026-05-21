🛡️ Cybersecurity RAG Chatbot

A local Retrieval-Augmented Generation (RAG) chatbot built using:

Streamlit
Ollama
Custom embedding model
Local language model
Semantic similarity search
Manual vector database

This chatbot answers cybersecurity-related questions using a local dataset and retrieval pipeline.

🚀 Features
Local AI chatbot
Cybersecurity knowledge base
Semantic search using embeddings
Similarity score visualization
Real-time streaming responses
Sidebar retrieval viewer
Fully offline RAG pipeline
Local Ollama models


🧠 RAG Architecture
User Question
      ↓
Embedding Model
      ↓
Vector Database
      ↓
Cosine Similarity Search
      ↓
Retrieve Relevant Chunks
      ↓
Context Injection
      ↓
Language Model
      ↓
AI Response


📂 Project Structure
GENAI/
│
├── app.py
├── cybersecurity-facts.txt
├── requirements.txt
└── README.md


⚙️ Models Used
Embedding Model
hf.co/CompendiumLabs/bge-base-en-v1.5-gguf

Used for:
text embeddings
semantic similarity
retrieval
Language Model
hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF

Used for:
contextual response generation
answering user questions


📦 Installation
1. Clone Repository
git clone <your-repo-url>
cd GENAI

2. Create Virtual Environment
Windows
python -m venv myvenv
myvenv\Scripts\activate

3. Install Requirements
pip install -r requirements.txt


📥 Install Ollama

Install Ollama: https://ollama.com/download

📥 Pull Required Models
ollama pull hf.co/CompendiumLabs/bge-base-en-v1.5-gguf
ollama pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF

▶️ Run Application
streamlit run app.py

Open browser:

http://localhost:8501

📄 Dataset Format

The chatbot uses:

cybersecurity-facts.txt

Each line represents one knowledge chunk.

Example:

Phishing attacks steal credentials.
SOC analysts monitor SIEM alerts.
Ransomware encrypts files.


🔍 How Retrieval Works
1. User enters a question
2. Query embedding is generated
3. Cosine similarity compares vectors
4. Top matching chunks are retrieved
5. Retrieved context is sent to LLM
6. AI generates contextual answer


📊 Similarity Scoring

The sidebar displays:

    ->retrieved chunks
    ->similarity percentage
    ->retrieval ranking
    ->semantic match score

Example:

Result 1
Similarity Score: 92.14%


🛡️ Cybersecurity Topics Covered
Phishing
SIEM
Malware
Ransomware
Threat Intelligence
Incident Response
DDoS
Vulnerability Assessment
Endpoint Security
Threat Hunting
Encryption
Digital Forensics
Network Security
Cloud Security
Security Monitoring
💡 Example Questions
    =>How do SOC analysts detect phishing attacks?
    =>What is ransomware?
    =>How does threat intelligence help defenders?
    =>What is SIEM?

🧪 Technologies Used
Technology	        Purpose
Python	            Backend
Streamlit	        Frontend UI
Ollama	            Local AI runtime
Embeddings	        Semantic search
Cosine Similarity	Retrieval ranking
RAG	                Contextual AI generation


🧑‍💻 Author

Guru Prasath M