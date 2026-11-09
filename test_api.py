import requests

url = "http://127.0.0.1:5000/predict"

with open("samples/Untitled_1.png", "rb") as image:
    reply = requests.post(url, files={"image":image})

print(f"status: {reply.status_code}")
print(f"content: {reply.text}")