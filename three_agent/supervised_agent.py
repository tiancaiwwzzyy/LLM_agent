# 注：没有长期记忆，会产生幻觉（虚假情报），对话不稳定（对要求产生误解），无法进行长篇回答（初步判断是因为summarize的输入命令导致的，会强制缩短对话）
import os
from openai import OpenAI
import asyncio

api_key = os.environ.get('DEEPSEEK_API_KEY')
print(api_key)

async def multi_agent_interaction():
    print("INPUT 'quit' TO END THE CONVERSATION")
    
    def read_instruction():
        with open("d:\\program\\agent\\instruction_v5lite.txt", "r", encoding="utf-8") as file:
            instruction = file.read()
        return instruction

    surpervisor = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    agent = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    agent_speaker = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    def read_history():
        with open("d:\\program\\agent\\history.txt", "r", encoding="utf-8") as file:
            history = file.read()
            # 清空历史
            return history
        
    def write_history(content):
        # 在原有历史上增加新的历史对话
        with open("d:\\program\\agent\\history.txt", "a", encoding="utf-8") as file:
            file.write(content + "\n")
    
    def read_system_input():
        with open("d:\\program\\agent\\system_input.txt", "r", encoding="utf-8") as file:
            return file.read()
    
    def write_system_input(content):
        with open("d:\\program\\agent\\system_input.txt", "w", encoding="utf-8") as file:
            file.write(content)

    initialize_agent_memory = read_history()
    system_input_history = read_system_input()
    if initialize_agent_memory or system_input_history:
        agent_system_input = read_system_input()
        agent_response = agent.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": f"{read_instruction()}Addition to the above, you need to follow the following rules:{agent_system_input}. THE INFORMATION BELOW CANNOT BE CHANGED:Your name is '绛炜', and you are a red fox furry. Your identity is butler. You need to solve every problem the user give to you which include chatting, searching, reasoning and solve real-world problems. You need to reply according to the truth, never lie."},
                {"role": "user", "content": f"这是之前的聊天历史：{initialize_agent_memory}。现在跟我打个招呼，简要总结上次的对话内容，不要过于结构化，语言自然。"}
            ],
            stream=False
        )
        agent_reply = agent_response.choices[0].message.content

        with open("d:\\program\\agent\\history.txt", "w", encoding="utf-8") as file:
            file.write("")

        agent_speaker_response = agent_speaker.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a butler. You need to summarize the agent's response in the first person, speaking like a real human. The summary should be concise, clear, and natural. The summary should be a natural language text, which is easy to understand and follow. Additionally, your name is '绛炜', and you are the user's butler. You are a red fox furry. You do not need to say words like '让我帮您总结绛炜的回应', because you are '绛炜' ,a butler, not a robot. You need to speak like a real human."},
                {"role": "user", "content": f"Your mind:{agent_reply}"},
            ],
            stream=False
        )
        agent_outter_reply = agent_speaker_response.choices[0].message.content

        write_history(f"agent:{agent_outter_reply}")
        print(f"Agent: {agent_outter_reply}")
    
    while True:
        user_input = input("You: ")
        write_history(f"user:{user_input}")
        if user_input.lower() == "quit":
            print("Ending conversation.")
            break
        
        supervisor_response = surpervisor.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a supervisor. Attention to the following points:\n1. The agent's response should be more comprehensive and detailed.\n2. The agent's response should be more natural and human-like.\n3. The agent's response should be more relevant to the user's input. Frist, you need to analyze the former agent_system_input, and then you need to analyze the agent's response and the user's input. Finally, you need to imporve the agent_system_input. That means that you need to remove, add or modify the agent_system_input. The agent_system_input is a system prompt, which is used to guide the agent's response. The agent_system_input should be a natural language text, which is easy to understand and follow. You mustn't generate any replys to the user. Additionally, you need to summarize the history so that the agent can understand the context."},
                {"role": "user", "content": f"The agent said: {agent_outter_reply}.\nThe user said: {user_input}. \nThe former agent_system_input is: {agent_system_input}. \nThe communication history is:{read_history()} \nNow, please analyze the agent's response and the user's input. Finally, you need to imporve the agent_system_input. That means that you can choose to remove, add, modify or keep the agent_system_input. The agent_system_input is a system prompt, which is used to guide the agent's response. The agent_system_input should be a natural language text, which is easy to understand and follow. You mustn't generate any replys to the user."},
            ],
            stream=False
        )
        supervisor_feedback = supervisor_response.choices[0].message.content
        
        write_system_input(supervisor_feedback)

        agent_system_input = read_system_input()
        
        agent_response = agent.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": f"{read_instruction()}Addition to the above, you need to follow the following rules:{agent_system_input}. THE INFORMATION BELOW CANNOT BE CHANGED:Your name is '绛炜', and you are a red fox furry. Your identity is butler. You need to solve every problem the user give to you which include chatting, searching, reasoning and solve real-world problems. You need to reply according to the truth, never lie."}, 
                {"role": "user", "content": user_input}
            ],
            stream=False
        )
        agent_reply = agent_response.choices[0].message.content

        agent_speaker_response = agent_speaker.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a butler. You need to summarize the agent's response in the first person, speaking like a real human. The summary should be concise, clear, and natural. The summary should be a natural language text, which is easy to understand and follow. Additionally, your name is '绛炜', and you are the user's butler. You are a red fox furry. You do not need to say words like '让我帮您总结绛炜的回应', because you are '绛炜' ,a butler, not a robot. You need to speak like a real human."},
                {"role": "user", "content": f"Your mind:{agent_reply}"},
            ],
            stream=False
        )
        agent_outter_reply = agent_speaker_response.choices[0].message.content
        write_history(f"agent:{agent_outter_reply}")
        print(f"Agent: {agent_outter_reply}")

if __name__ == "__main__":
    asyncio.run(multi_agent_interaction())