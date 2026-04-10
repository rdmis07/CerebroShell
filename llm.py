import requests

API_URL = "http://127.0.0.1:1234/v1/chat/completions"

MODEL_NAME = "qwen/qwen2.5-vl-7b"

def nlp_to_shell_command(nlp_text):
    headers = {
        "Content-Type": "application/json"
    }

    messages = [
    {
        "role": "user",
        "content": f"""You are an assistant that converts natural language instructions into safe Windows shell commands. Only return the final command as a single line of text. Do not include explanations, quotes, code blocks, or formatting. Use standard Windows commands and built-in executables. Examples: 

- "open notepad" -> start notepad  
- "launch chrome" -> start chrome.exe  
- "open calculator" -> calc  
- "open command prompt" -> cmd  
- "open paint" -> mspaint  

Now, convert the following instruction into a safe Windows shell command:  
{nlp_text}"""
    }

]
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()

    command = response.json()['choices'][0]['message']['content'].strip()
    return command


def Query(Q):
    headers = {
        "Content-Type": "application/json"
    }

    messages = [
    {
        "role": "user",
        "content":f"response should be clear to the point{Q}" 
    }

]
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()

    command = response.json()['choices'][0]['message']['content'].strip()
    return command