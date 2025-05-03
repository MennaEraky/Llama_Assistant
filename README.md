# 🤖 Your Llama Assistant


A Streamlit app that leverages OpenAI (via Gemini API and Ollama LLaMA3) to help users gather and summarize company website content into a concise brochure. It also supports tools like date retrieval and webpage scraping for enhanced interactivity.

---

## 🔧 Features

- ✅ Extracts relevant links from company websites
- ✅ Summarizes and builds a company brochure using Gemini (via OpenAI SDK)
- ✅ Local LLM chat integration using [Ollama](https://ollama.com)
- ✅ Tool usage via OpenAI-style function calling
- ✅ Clean logging with `python-json-logger`

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/MennaEraky/helpful-assistant.git
cd Llama_Assistant

---

## 🔧 Features

- ✅ Extracts relevant links from company websites
- ✅ Summarizes and builds a company brochure using Gemini (via OpenAI SDK)
- ✅ Local LLM chat integration using [Ollama](https://ollama.com)
- ✅ Tool usage via OpenAI-style function calling
- ✅ Clean logging with `python-json-logger`

---

## 🛠️ Installation

### 1. Clone the Repository


git clone https://github.com/MennaEraky/Llm-Assistant.git
cd Llm-Assistant

2. Set up Python Environment
python3 -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt

3. Configure Environment Variables
Create a .env file in the root directory and add:

GOOGLE_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_key_or_ollama_token

4. Start Ollama Server (for LLaMA)
Install Ollama and pull LLaMA 3 model:
brew install ollama
ollama serve
ollama pull llama3

##🚀 Run the App
streamlit run p.py
Open http://localhost:8501 in your browser.

##💡 How It Works
You provide a company URL and name.

The app scrapes the landing page and relevant internal links.

It builds a brochure using Gemini (gemini-1.5-flash) via OpenAI SDK.

You can also chat with a local model (LLaMA3 via Ollama).

The assistant dynamically uses tools when needed (like get_brochure or todays_date).

##📂 File Structure
.
├── streamlit_app.py      # Main Streamlit App
├── requirements.txt      # Python dependencies
├── .env                  # API keys and secrets
├── README.md             # Project documentation
📦 Dependencies
Key libraries used:

streamlit

requests, beautifulsoup4

openai (used for Gemini & Ollama API compatibility)

python-dotenv

python-json-logger

ollama (LLaMA runtime)

##🧠 Model Details
Gemini (via OpenAI SDK): for structured, cloud-based summarization.

LLaMA3 via Ollama: runs locally for chat and tool-based assistance.

##🛡️ Notes
Ensure your IP is not blocked by sites you are scraping.

Gemini API requires access to https://generativelanguage.googleapis.com.

📃 License
MIT License

🙋‍♂️ Questions?
Feel free to open issues or contribute!
