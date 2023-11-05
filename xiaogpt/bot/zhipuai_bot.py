"""智谱AI大模型 https://open.bigmodel.cn/"""
from typing import Any, AsyncGenerator

# pip install zhipuai
import zhipuai

from xiaogpt.bot.base_bot import BaseBot, ChatHistoryMixin
from xiaogpt.config import Config


class ZhiPuAiBot(ChatHistoryMixin, BaseBot):
    default_options = {
        "model": "chatglm_turbo",
        "temperature": 0.95,
        "top_p": 0.7,
        "incremental": True
    }

    def __init__(self, api_key: str = "") -> None:
        self.history = []
        zhipuai.api_key = api_key

    async def ask(self, query: str, **options: Any) -> str:
        # 获取历史对话, 增加当前提示词
        dialog = self.get_messages()
        dialog.append({"role": "user", "content": query})
        # 调用参数，默认参数X自定义参数
        kwargs = {**self.default_options, **options}
        print(f"kw: {kwargs}, prompt: {dialog}")

        try:
            response = zhipuai.model_api.sse_invoke(
                prompt=dialog,
                **kwargs
            )
            this_ans = ""
            for event in response.events():
                if event.event == "add":
                    this_ans += event.data
                elif event.event == "error" or event.event == "interrupted":
                    print(event.data, end="")
                elif event.event == "finish":
                    this_ans += event.data
                    print(f'this round end: {event.meta}')
                else:
                    print(event.data, end="")
        except Exception as e:
            print('ask zhupuai exception', e)
            return ""

        self.add_message(query, this_ans)
        return this_ans

    async def ask_stream(self, query: str, **options: Any) -> AsyncGenerator[str, None]:
        raise Exception("Zhipuai do not support stream")

    @classmethod
    def from_config(cls, config: Config):
        return cls(
            api_key=config.zhipu_api_key
        )

    def has_history(self) -> bool:
        return super().has_history()


if __name__ == '__main__':
    import asyncio

    # 初始化bot
    zhipu_api_key = "xxxxxxx"
    bot = ZhiPuAiBot(zhipu_api_key)


    async def main():
        while True:
            # 从控制台读取用户输入的指令
            user_input = input("请输入指令（或输入 'exit' 退出）: ")

            if user_input == 'exit':
                # 如果用户输入 'exit'，则退出循循环
                print("程序已退出。")
                break
            elif user_input:
                ans = await bot.ask(user_input)
                print(f'bot ans: {ans}')
            else:
                print('无效输入，请重新输入')


    # 创建事件循环并运行main函数
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
