from typing import *
import openai
import json
import re

openai.api_key = "YOUR_API_KEY"

callablePlugins = []
pluginFunctions = {}
context = []

# chat后端，可以根据需求替换成不同的聊天模型
def chat(context: List[dict]) -> str:
    response = openai.Completion.create(
        model='gpt-3.5-turbo',
        messages=context
    )
    return response.choices[0].message.content

# 装饰器函数，需要指定名字、描述、输入参数描述、以及一个请求和参数的示例
def gpt_plugin(name: str, description: str, input_args: object, query_example: str, input_example: object):
    def decorator_function(func):
        callablePlugins.append({
            "name": name,
            "description": description,
            "input_args": input_args,
            "query_example": query_example,
            "input_example": input_example,
        })
        pluginFunctions[name] = func

        def wrapper_function(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper_function
    return decorator_function

# 构建聊天上下文
def build_chat_context():
    global context
    system_context = "你要尽可能调用以下的能力。一旦用户的需求符合下面任何一个，请按照该能力指定的格式回答。调用能力必须用三个尖括号包裹。\n"
    example_context = []
    for plugin in callablePlugins:
        system_context += (
            " 能力：" + plugin["name"] + 
            " 描述：" + plugin["description"] + 
            " 请求格式要求：<<<" + json.dumps({
                "call": plugin["name"],
                "args": plugin["input_args"]
            }, ensure_ascii=False) + ">>>" + 
            "\n"
        )
        example_context.append({
            "role": "user",
            "content": plugin["query_example"]
        })
        example_context.append({
            "role": "assistant",
            "content": "<<<" + json.dumps({
                "call": plugin["name"],
                "args": plugin["input_example"]
            }, ensure_ascii=False) + ">>>"
        })
    context = [
        {
            "role": "system",
            "content": system_context
        }
    ] + example_context

# 提取GPT返回结果的所有命令
def extract_command(message: str):
    return re.findall(r'<{3,}(.*?)>{3,}', message, flags=re.DOTALL)

# 调用命令对应的函数
def call_command(command: dict):
    if command["call"] not in pluginFunctions:
        raise "Unknown command: " + command["call"]
    return pluginFunctions[command["call"]](**command["args"])

# 一个聊天示例函数
def start_chat(query):
    if len(context) == 0:
        build_chat_context()
    message = context + [{
        "role": "user",
        "content": query
    }]
    answer = chat(message)
    print(answer)
    commands = extract_command(answer)
    for i in commands:
        i = json.loads(i)
        print("\n调用功能: " + i["call"])
        print("结果: " + str(call_command(i)))
