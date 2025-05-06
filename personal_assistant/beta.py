from autogen import ConversableAgent
import os
import sys

api_key = os.environ.get("4o_api")
base_url = os.environ.get("4o_endpoint")
config_list = {
    "model": "gpt-4o",
    "api_key": api_key,
    "api_type": "azure",
    "base_url": base_url,
    "api_version": "2024-12-01-preview",
}

user_proxy = ConversableAgent(
    "user_proxy",
    system_message="",
    human_input_mode="ALWAYS",
)

def write_artical():
    pass

def write_baidu():
    pass

def search_internet():
    pass

def search_KB():
    pass