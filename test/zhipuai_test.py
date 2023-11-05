import asyncio

from xiaogpt.bot import get_bot
from xiaogpt.config import Config

if __name__ == '__main__':
    async def main():
        config = Config.read_from_file('../xiao_config.json')
        c = Config(**config)
        bot = get_bot(c)

        ans = await bot.ask("天空为什么是蓝色的")
        print(ans)


    # 创建事件循环并运行main函数
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
