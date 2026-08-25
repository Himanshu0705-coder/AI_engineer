import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha h bhai")

client=Groq(api_key = my_api_key)

model= "openai/gpt-oss-20b"
role = "user"


# structue it 
from pydantic import BaseModel
class Ticket(BaseModel):
    name:str
    email:str
    issue:str

schema=Ticket.model_json_schema()

response_format={
    "type":"json_object"
}

system_prompt=f"""
Extract the personal information from the ticket strictly based on this schema and give me a JSON format. and give me every information in next line.
{schema}
"""
message_system={
    "role": "system",
    "content": system_prompt
}

text = "Hello my name is HImanshu.my gf name is Aastha. I have an iphone which is not working.MY email id is panchalhimanshu0507@gmail. My phone no. is 7505536651."
prompt = f"""
    This is a customer ticket. Please extract the personal information from this.
    {text}
    """
message = {
    "role": role ,
    "content": prompt

}
messages=[message_system,message]

response = client.chat.completions.create(model=model,messages=messages, response_format=response_format)

answer = response.choices[0].message.content
print(answer)


# isko padhte kaise hai
import json
raw_json=answer
data_file=json.loads(raw_json)
ticket=Ticket(**data_file)

# inko pass kar skte h aage
print(ticket.name)
print(ticket.email)
print(ticket.issue)



# Homework
'''
take a resume in pdf or word
hr give you a list of things like skill,experience , projects
extract these information from resume
generate a percentage of matching or not

'''