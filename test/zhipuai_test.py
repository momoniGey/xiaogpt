from xiaogpt.bot import get_bot
from xiaogpt.config import Config

if __name__ == '__main__':
    import asyncio

    # 初始化bot
    config = Config.read_from_file('../xiao_config.json')
    c = Config(**config)
    bot = get_bot(c)


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
