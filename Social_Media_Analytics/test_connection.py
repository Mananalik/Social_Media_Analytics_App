import requests
url = "https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english/resolve/main/config.json"
try:
    response = requests.get(url)
    if response.status_code == 200:
        print("Connection to Hugging Face model successful.")
        print("Content:", response.json())
    else:
        print(f"Failed to connect. Status code: {response.status_code}")
        print("Response:", response.text)
except Exception as e:
    print(f"An error occurred: {e}")