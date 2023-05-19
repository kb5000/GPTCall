# GPTCall

GPTCall是一个Python编写的库，用于桥接你的自定义函数与OpenAI的ChatGPT。借助简单的装饰器语法，你可以以交互式对话的方式调用你自己的函数，极大地增强了代码的可交互性。

## 主要特性

- 易于使用的装饰器：通过在函数上添加@gpt_plugin装饰器，即可使该函数成为GPTCall的一部分，无需复杂的配置。
- 交互式命令执行：利用ChatGPT的对话接口，你可以以对话的形式发出指令，由GPTCall自动调用相应的函数。
- 自定义函数：GPTCall提供了强大的扩展性，你可以根据实际需求，为其添加任意自定义函数。

## 快速开始

首先，你需要导入GPTCall。

然后，在你的python脚本中引入GPTCall，并定义你的函数。请注意，input_args和input_example的参数结构需要与函数的参数结构一致：

```python
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
```

之后，你就可以通过 `start_chat(query)`去通过对话的形式调用你的函数了。
