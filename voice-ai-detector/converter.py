import base64

with open("D:\Downloads\Every_Voice_is_Different__The_5_Voice_Types(256k).mp3","rb") as f:
    print(base64.b64encode(f.read()).decode())
