import json

def build_prompt(prompt_type: str):
   '''Fetches json data with key PROMPT_TYPE from file prompt_builder/builder_config.json'''

   with open('prompt_builder/builder_configs/prompt_config.json', 'r') as prompt_config:
        config_data = json.load(prompt_config)[prompt_type]
   prompt = ""

   for instruction in config_data["instructions"]:
        prompt += f"{instruction}\n"
   for i, question in enumerate(config_data["questions"]):
        prompt += f"{i}. {question}\n"
   return prompt

def get_bot_config(bot_type: str): 
    '''Fetches json data with key BOT_TYPE from file prompt_builder/bot_config.json'''

    with open('prompt_builder/builder_configs/bot_config.json', 'r') as bot_config:
        config_data = json.load(bot_config)[bot_type]
    return config_data
