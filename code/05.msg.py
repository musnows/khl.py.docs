import traceback
from khl import Bot, Message, MessageTypes
from khl.card import Card, CardMessage, Module, Types

from utils.file import open_file

# 打开config.json
config = open_file("./config/config.json")

# 初始化机器人
bot = Bot(token=config["token"])  # 默认采用 websocket


@bot.command(name="test")
async def test_cmd(msg: Message, type, *arg):
    """发送消息"""
    try:
        print(f"/test cmd recv from {msg.author_id}")
        if type == "0":
            await msg.reply("这是一个没有引用的KMD消息",use_quote=False)
        elif type == "1":
            await msg.reply(
                f"这是一个KMD消息！(met){msg.author_id}(met)\n(chn){msg.ctx.channel.id}(chn)"
            )
        elif type == "2":
            cm_json = [
                {
                    "type": "card",
                    "theme": "secondary",
                    "size": "lg",
                    "modules": [
                        {
                            "type": "section",
                            "text": {
                                "type": "paragraph",
                                "cols": 3,
                                "fields": [
                                    {"type": "kmarkdown", "content": "**昵称**\n怪才君"},
                                    {"type": "kmarkdown", "content": "**服务器**\n活动中心"},
                                    {
                                        "type": "kmarkdown",
                                        "content": "**在线时间**\n9:00-21:00",
                                    },
                                ],
                            },
                        }
                    ],
                }
            ]
            # 发送卡片消息
            await msg.reply(cm_json,type=MessageTypes.CARD)
        else:
            # 发送图片
            img_url = await bot.client.create_asset('./config/logo.png') # 先上传图片并获取链接
            await msg.reply(img_url,type=MessageTypes.IMG)
            print(f"send img | {img_url}")

    except Exception as result:
        print(traceback.format_exc())

print("bot start")
bot.run()
