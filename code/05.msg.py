import json
import traceback
from khl import Bot, Message, MessageTypes
from khl.card import Card, CardMessage, Module, Types, Element, Struct

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
            await msg.reply("这是一个没有引用的KMD消息", use_quote=False)
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
            await msg.reply(cm_json, type=MessageTypes.CARD)
        else:
            # 发送图片
            img_url = await bot.client.create_asset("./config/logo.png")  # 先上传图片并获取链接
            await msg.reply(img_url, type=MessageTypes.IMG)
            print(f"send img | {img_url}")

    except Exception as result:
        print(traceback.format_exc())


@bot.command(name="card")
async def card_msg_cmd(msg: Message, *arg):
    """发送卡片消息"""
    try:
        print(f"/card cmd recv from {msg.author_id}")
        cm = CardMessage()
        # 1.文本
        # 新版本的khl.py已经默认为KMD
        c = Card(
            Module.Header("标题内容，不支持`KMD`"),
            Module.Context("小字，支持`KMD`"),
            Module.Section("正文内容，支持`KMD`"),
        )

        # # 手动指定使用kmd
        c1 = Card(Module.Header("标题内容，不支持`KMD`"), color="#1f1f1f")  # 传入color指定卡片边栏颜色
        c1.append(Module.Context(Element.Text("小字，支持`KMD`", Types.Text.KMD)))
        c1.append(Module.Divider())  # 分隔符
        c1.append(Module.Section(Element.Text("正文内容，支持`KMD`", Types.Text.KMD)))

        # 2.多列文本，最多3列
        c2 = Card(
            Module.Section(
                Struct.Paragraph(
                    3,
                    Element.Text("这是第一列", type=Types.Text.KMD),
                    Element.Text("这是第二列", type=Types.Text.KMD),
                    Element.Text("这是第三列", type=Types.Text.KMD),
                )
            )
        )

        # 3.图片
        img_src = "https://img.kookapp.cn/attachments/2023-05/29/k2jUQW81GC05k05k.png"
        c3 = Card(Module.Container(Element.Image(src=img_src)))
        c4 = Card(
            Module.Section(
                Element.Text("文字在右侧", type=Types.Text.KMD),
                Element.Image(src=msg.author.avatar, alt="left"),
            )
        )

        # 插入到卡片消息中
        cm.append(c3)
        cm.append(c4)
        # cm.append(c1)
        await msg.reply(cm)

    except Exception as result:
        print(traceback.format_exc())


from datetime import datetime, timedelta


@bot.task.add_date((datetime.now() + timedelta(seconds=10)), timezone="Asia/Shanghai")
async def test_date_task():
    ...


@bot.on_shutdown
async def test_shutdown_task(b: Bot):
    ...


print("bot start")
bot.run()
