import os
import requests
from chat_prompt import gpt_api

import openai
import os
import json

DEFAULT_CONTEXT = ""

JSON_STYLE = """Create your reply so it can be easily transformed into json file. Provide the results in a list of json objects of the following object format:
   [
    {
    "question": "What is the key difference between Python 2 and Python 3?",
    "options": [
        "AAA",
        "BBB",
        "CCC",
        "DDD"
      ],
    "correct_answer_id": 2,
    "explanation": short explanation of the correct answer in one short sentence,
    "topic":
    }, 
    ...
    ]
"""

class gpt_api:
    def __init__(self, key=None) -> None:
        self.model = "gpt-3.5-turbo"
        self.debug_mode = False
        self.context = ""
        if key:
            self.key = key
        else:
            self.key = None
    
    def read_key_from_file(self, file_name="api_key.txt"):
        with open(file_name, 'r') as file:
            self.key = file.readline()

    def json_style(self, style=""):
        self.context = self.context + style

    def debug(self, value=True):
        self.debug_mode =  value

    def set_gpt_model(self, chat_model=None):
        if chat_model is None:
            print("\nNo model has been specified!\n")
            return
        self.model = chat_model

    def get_topics(self, max_topics=3):

        new_promt = f"""Given my field of interest, select up to {max_topics} different topics.
        These topics will be later used to learn about the selected field of interest.
        The reply formating should be [topic 1, topic 2, ..., topic 5]."""

        self.prompt(text=new_promt)

    def get_completion(self, prompt):
        messages = [{"role": "user", "content": prompt}]

        openai.api_key = self.key
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=0, # this is the degree of randomness of the model's output
        )

        return response.choices[0].message["content"]
    
    def prompt(self, text=None):

        if text is None:
            raise ValueError("No text has been provided, exiting")

        self.json_style(JSON_STYLE) # add json information

        prompt = f"{self.context}{text}"
        response = self.get_completion(prompt)
        if self.debug_mode:
            print("\nquery:\n" + prompt + "\n" + "response:\n")
            print(response)
        return response
    
    def create_prompt(self):
        raise NotImplementedError
    
    def ask_prompt(self):
        raise NotImplementedError


### example run
def gpt_example_run():
    tmp_api = gpt_api("catch me if you can")
    tmp_api.read_key_from_file("api_key.txt")
    tmp_api.debug(True)
    tmp_api.json_style(JSON_STYLE)
    tmp_api.prompt(text="Give me two true or false coding question answer pairs based on python, return it in json format, keep the difficulty level on very hard, provide examples for each question")
# gpt_example_run()


### PDF GPT
class chatpdf_api:
    def __init__(self, key=None, pdf_path="", key_path="") -> None:

        self.debug_mode = False
        if key is None:
            self.key = self.read_key_from_file(key_path)
        else:
            self.key = key 
        self.context = DEFAULT_CONTEXT
        self.pdf_source_id = self.upload_pdf(pdf_path)
        print(self.pdf_source_id)

    def read_key_from_file(self, file_name=""):
        try:
            with open(file_name, 'r') as file:
                if self.debug_mode:
                    print(self.key)
                return file.readline()
        except:
            print("ERROR: key file doesnt exist")
    
    def upload_pdf(self, pdf_path):

        if not os.path.isfile(pdf_path):
            raise ValueError("No pdf to be uploaded!")

        files = [('file', ('file', open(pdf_path, 'rb'), 'application/octet-stream'))]
        headers = {'x-api-key': self.key}

        response = requests.post(
            'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)
        
        if response.status_code == 200:
            if self.debug:
                print('Source ID:', response.json()['sourceId'])
            return response.json()['sourceId']
        else:
            print('Status:', response.status_code)
            print('Error:', response.text)
            exit()

    def debug(self, value=True):
        self.debug_mode =  value

    def create_prompt(self, question, rqst_sources=False):
        
        tmp_rqst = {"referenceSources": rqst_sources,
         "sourceId": self.pdf_source_id,
         "messages": [
            {
            "role": "user",
            "content": f"{question}"
            }]
        }
        return tmp_rqst

    def get_topics(self, max_topics=3):

        new_promt = f"""Given the pdf file, select up to {max_topics} different topics.
        These topics will be later used to learn about the provided pdf.
        The reply formating should be [topic 1, topic 2, ..., topic 5]."""

        tmp_prompt = self.create_prompt(new_promt)
        tmp_result = self.ask_prompt(tmp_prompt)

        return tmp_result.json()['content']

    def ask_prompt(self, query=None):
        headers = {'x-api-key': self.key, "Content-Type": "application/json",}
        response = requests.post(
            'https://api.chatpdf.com/v1/chats/message', headers=headers, json=query)

        if response.status_code == 200:
            print('Result:', response.json()['content'])
            if "refererces" in response.json():
                print('References', response.json()['references'])
        else:
            print('Status:', response.status_code)
            print('Error:', response.text)
        
        return response

    def generate_reinforce(self, ):
        pass

    def test_run(self):
        self.debug()
        #tmp_api.upload_pdf("provided_file.pdf")
        
        if self.debug:
            print("Start: get topics")
        topics = self.get_topics(5)
        
        question = f"Give me a multiple choice question regarding the provided topics {topics} from the pdf file. {JSON_STYLE}."
        tmp_rqst = self.create_prompt(question, rqst_sources=True)

        self.ask_prompt(tmp_rqst)

### general api
class any_api():
    def __init__(self, api_service=None) -> None:
        self.service = api_service
        self.key = None

    def read_key(self, path):
        try:
            with open(path, 'r') as file:
                return file.readline()
        except:
            print("ERROR: key file doesnt exist")

    def init_question(self, profile, pdf_path, opt_context="", key_path=""):
        
        self.key = self.read_key(key_path)
        
        if os.path.isfile(pdf_path):
            self.service = chatpdf_api(pdf_path=pdf_path, key=self.key)
            print("Exploiting pdf")
        else:
            self.service = gpt_api(self.key)
            print("Exploiting vanilla gpt")

        topics = self.service.get_topics(5)
        self.topics = topics

        question = profile + f"Give me a multiple choice question regarding the provided topics {topics} from the pdf file." + JSON_STYLE
        tmp_query = self.service.create_prompt(question)
        response = self.service.ask_prompt(tmp_query)
        return {"topics": topics,
                "response": json.loads(response.json()['content'])}
    
    
    def topic_qst(self, topic=None):
        # given the topic, ask the api to generate a question
        question = profile + f"Give me as many multiple choice questions as you can fully fit in one reply. These questions shoud be regarding the provided topic {topic} based on the pdf file." + JSON_STYLE
        tmp_query = self.service.create_prompt(question)
        response = self.service.ask_prompt(tmp_query)
        print(response)

    def reinforce_topic(self, topic=""):
        # generate more questions about a given topic
        pass    
    
    def reinfoce_auto(self):
        # generate more questions by default
        raise NotImplemented
    
    def adjust_difficulty_topic(topics):
        raise NotImplemented
    
    def keep_going(self):
        raise NotImplemented

# tmp_api = chatpdf_api(pdf_path="provided_file.pdf", key_path="chatpdf_key.txt")
# tmp_api.test_run()

# comes from front end
profile_background = "junior developer"
profile_aim = "learn python" 
profile = f"I am a {profile_background}. I want to {profile_aim}"
pdf = "./gpt/provided_file.pdf"
opt_context = ""  

# run question creator
our_api = any_api()
if pdf is not None:
    key_path = "./gpt/chatpdf_key.txt"
else:
    key_path = "./gpt/api_key.txt"

print(our_api.init_question(profile=profile, pdf_path=pdf, opt_context=opt_context, key_path=key_path)["response"][0]['question'])
 
#our_api.topic_qst("Potential impact of NanoScribe")