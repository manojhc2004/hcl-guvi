import base64

with open(r"C:\Users\manoj\Downloads\sample-7.mp3", "rb") as f:
    encoded = base64.b64encode(f.read()).decode()

print(encoded)

