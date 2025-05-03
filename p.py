import streamlit as st
import os
import requests
import json
from bs4 import BeautifulSoup
from openai import OpenAI
import logging
from pythonjsonlogger import jsonlogger
from datetime import datetime
# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)

# Setup OpenAI API key and Elasticsearch connections
logger.info("Initializing API keys and clients")
google_api_key = os.getenv("GOOGLE_API_KEY")
gemini_via_openai_client = OpenAI(api_key=google_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/")
openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
MODEL_OLLAMA = "llama3.2"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}

class Webpage:
    def __init__(self, url):
        self.url = url
        try:
            logger.info(f"Fetching webpage: {url}")
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            if soup.body:  # Check if soup.body exists
                for tag in soup.body(["script", "style", "img", "input"]):
                    tag.decompose()
                self.text = soup.body.get_text(separator="\n", strip=True)
            else:
                self.text = "Body content not found."
            soup = BeautifulSoup(self.body, "html.parser")
            self.title = soup.title.string if soup.title else "No title found"
            
            for tag in soup.body(["script", "style", "img", "input"]):
                tag.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)
            
            self.links = [link.get("href") for link in soup.find_all("a") if link.get("href")]
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            self.title = f"Error fetching {url}"
            self.text = "Error occurred"
            self.links = []
            self.body = None

    def get_content(self):
        return f"Title: {self.title}\nContents: {self.text}\nLinks: {self.links}"

system_prompt = """You are a helpfull assistant that can help with the company brochure , you also help the user to make his life easier,if you need to use a tool for information, you will use the tool to get the information you need always give the output from tools prior to the response with, make each response short and concise"""

def get_links_user_prompt(website):
    logger.info("Function get_links_user_prompt called")
    user_prompt = f"Here is the list of links on the website of {website.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
    Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(website.links)
    return user_prompt

def get_links(url):
    logger.info("Function get_links called")
    link_system_prompt = "You are provided with a list of links found on a webpage. \
    You are able to decide which of the links would be most relevant to include in a brochure about the company, \
    such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
    link_system_prompt += "You should respond in JSON as in this example:"
    link_system_prompt += """
    {
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page", "url": "https://another.full.url/careers"}
    ]
    }
    """
    webpage=Webpage(url)
    logger.info("Webpage object created")
    response = gemini_via_openai_client.chat.completions.create(
    model="gemini-1.5-flash",  # Use the correct model name
    messages=[
            {"role": "system", "content": link_system_prompt},
            
            {"role": "user", "content": get_links_user_prompt(webpage)}],         
        response_format={"type": "json_object"}
    )
    response_json=json.loads(response.choices[0].message.content)
    return response_json

def get_all_details(url):
    logger.info("Function get_all_details called")
    result = "Landing page:\n"
    result += Webpage(url).get_content()
    links = get_links(url)
    # print("Found links:", links)
    for link in links["links"]:
        result += f"\n\n{link['type']}\n"
        result += Webpage(link["url"]).get_content()
    return result
def get_brochure(company_name,url):
    logger.info("Function get_brochure called")
    user_prompt = f"You are looking at a company called: {company_name}\n"
    user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
    user_prompt += get_all_details(url)
    return user_prompt

def create_brochure(company_name, url):

    logger.info(f"Requesting Gemini to create brochure for {company_name}")
    response = gemini_via_openai_client.chat.completions.create(
        model="gemini-1.5-flash",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": get_brochure(company_name, url)}
        ]
    )
    st.markdown(response.choices[0].message.content)


def todays_date():  
    logger.info("Function todays_date called")
    date="today is "+datetime.now().strftime("%Y-%m-%d")

    return date
# Corrected tool definition
tools =  [{
    "type": "function",
    "function": {
        "name": "get_brochure",
        "description": "Get Details and important links from a website",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "website url",
                },
                "company_name": {
                    "type": "string",
                    "description": "the wesite name of the  company",
                },
            },
            "required": ["url","company_name"]
        }
    }
    },
{
    "type": "function",
    "function": {
        "name": "todays_date",
        "description": "Get the current date",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}


]


openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')

openai.api_key = os.getenv("OPENAI_API_KEY")

MODEL_OLLAMA = "llama3.2"


system_message = """You are a helpfull assistant that can help with the company website brochure and alot more, you also help the user to make his life easier,if you need dont have enogh information, you can use the tool to get the information you need. always give the output from tools prior to the response with, make each response short and concise
"""   

# Chat function
def chat(message, history):
    logger.info("Chat function called")
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    logger.info("Messages created")
    # Ollama call for tool usage
    response_ollama = openai.chat.completions.create(model=MODEL_OLLAMA, messages=messages, tools=tools, tool_choice="auto")
    logger.info("Ollama call for tool usage")
    # Check if the model wants to call a tool               
    if response_ollama.choices[0].message.tool_calls:
        tool_call = response_ollama.choices[0].message.tool_calls[0]
        logger.info("Tool call found")
        function_name = tool_call.function.name.strip()  # Trim spaces
        print("function_name", function_name)
        function_map = {
            "get_brochure": get_brochure,
            "todays_date": todays_date,
        }
        if function_name == "todays_date":
            result = function_map[function_name]()
            logger.info("Result loaded%s", result)
            messages.append(response_ollama.choices[0].message)
            messages.append({
                "role": "tool",
                "content": json.dumps({"result": result}),
                "tool_call_id": tool_call.id,
            })
            # Call Ollama again to get a response incorporating the date
            response_ollama_final = openai.chat.completions.create(model=MODEL_OLLAMA, messages=messages)
            final_response = response_ollama_final.choices[0].message.content
            cleaned_result = final_response.replace("```", "").replace("markdown", "")
            st.markdown(cleaned_result)
            return cleaned_result
        else:
            arguments = json.loads(tool_call.function.arguments)
            logger.info("Arguments loaded")
            url = arguments.get("url")
            company_name = arguments.get("company_name")
            logger.info("URL and company name loaded")
            print("url", url)
            print("company_name", company_name)
            result = function_map[function_name](url, company_name)
            logger.info("Result loaded")
            messages.append(response_ollama.choices[0].message)
            messages.append({
                "role": "tool",
                "content": json.dumps({"url": url, "company_name": company_name, "result": result}),
                "tool_call_id": tool_call.id,
            })
            response_ollama_final = openai.chat.completions.create(model=MODEL_OLLAMA, messages=messages)
            final_response = response_ollama_final.choices[0].message.content
            cleaned_result = final_response.replace("```", "").replace("markdown", "")
            st.markdown(cleaned_result)
            return cleaned_result
        logger.info("Tool response appended")
    else:
        # No tool call
        logger.info("No tool call")
        response_ollama_final = openai.chat.completions.create(model=MODEL_OLLAMA, messages=messages)
        final_response = response_ollama_final.choices[0].message.content
        cleaned_result = final_response.replace("```", "").replace("markdown", "")
        st.markdown(cleaned_result)
        return cleaned_result

st.title(" Your Helpfull Assistant! 🎈")
user_input = st.text_input("Tell me what you need! 💬", "what is the date of today")

logger.info("User input loaded %s",user_input)
if st.button("Let's Go! 🚀"):
    history = st.session_state.get("history", [])
    response = chat(user_input, history)
    st.session_state["history"] = history + [{"role": "user", "content": user_input}, {"role": "assistant", "content": response}]
