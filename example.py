# %%
from gpt_call import gpt_plugin, start_chat

@gpt_plugin(
    name="calculator",
    description="计算任何数学算式。所有计算请求或者跟数学算式有关的请调用本工具。请告诉我算式内容。",
    input_args={
        "query": "数学算式的内容",
    },
    query_example="计算1 + 3的结果",
    input_example={
        "query": "1 + 3",
    },
)
def calculator(query: str):
    return eval(query)

@gpt_plugin(
    name="draw",
    description="画一张设计图。当用户需要画图时请调用本工具。请告诉我图片的提示词。",
    input_args={
        "prompt": "逗号分隔的形容词和名词",
    },
    query_example="画一张西瓜味的汽车的草图",
    input_example={
        "prompt": "car, watermelon favored, sketch",
    },
)
def draw(prompt: str):
    return prompt

# %%
start_chat("画一张水果的图片")

