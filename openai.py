# create.py
 import os
 import openai

 PROMPT = ""
 openai.api_key = os.getenv("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")
response = openai.Image.create(
    prompt=PROMPT,
    n=1,
    size="256x256",
)

print(response["data"][0]["url"])