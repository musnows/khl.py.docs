import traceback

from khl import Bot, Message, command

from utils.file import open_file

# 打开config.json
config = open_file("./config/config.json")

# 初始化机器人
bot = Bot(token=config["token"])  # 默认采用 websocket


@bot.command(name="test", prefixes=['/', '.'], aliases=['tb', 'ta'], case_sensitive=False)
async def test_cmd(msg: Message):
    """测试命令"""
    print(f"get test cmd from", msg.author_id)
    await msg.reply(f"get test cmd!")


@bot.command(regex=r'^(?:搜索|点歌)(.+)')
async def search_music(msg: Message, music_name: str):
    print("get search music cmd from", msg.author_id)
    print(f"music name [{music_name}]")
    await msg.reply(f"get search music cmd! [{music_name}]")


def test_rules(msg: Message):
    """这是一个命令规则，只有命令中包含khl才能被执行"""
    if 'khl' in msg.content:
        return True
    return False


async def test_exc_handlers(cmd: command.Command, exception: Exception, msg: Message):
    """异常处理函数"""
    print("get exception from", msg.author_id)
    print("exception type:", type(exception))


@bot.command(name="tf",
             rules=[test_rules],
             exc_handlers={command.exception.Exceptions.Handler.RuleNotPassed: test_exc_handlers})
async def test_func_cmd(msg: Message, text: str):
    """测试命令"""
    try:
        print(f"get test func cmd from", msg.author_id)
        await msg.reply(f"get test func cmd!")
    except:
        print("test func cmd", traceback.format_exc())


@bot.command(name="help")
async def help_cmd(msg: Message, text: str, info: str=""):
    """测试命令"""
    print("get help cmd from", msg.author_id, text, info)
    await msg.reply(f"get help cmd: {text} | {info}")

@bot.command(name="num")
async def num_cmd(msg: Message, index:float):
    """命令参数类型测试"""
    print("get num cmd from", msg.author_id, index)
    await msg.reply(f"get num cmd: {index}")


@bot.command(name="larg")
async def long_arg_cmd(msg: Message,*args):
    """测试命令"""
    print("get long arg cmd from", msg.author_id)
    content = " ".join(args)
    await msg.reply(f"get long arg cmd: {content}")

if __name__ == '__main__':
    print("bot start")
    bot.run()
