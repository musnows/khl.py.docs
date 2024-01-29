import traceback

from khl import Bot, Message, command

from utils.file import open_file

# 打开config.json
config = open_file("./config/config.json")

# 初始化机器人
bot = Bot(token=config["token"])  # 默认采用 websocket


@bot.command(name='test')
async def test_cmd(msg: Message):
    try:
        print("test cmd recv!")
        guild = await bot.client.fetch_guild("")
        # 方法1，直接使用id
        role_id = 100 # 假设这是一个角色id
        await guild.grant_role("用户id",role_id) # 第二个参数是角色id

        # 方法2，使用用户对象
        guild_user = await guild.fetch_user("用户ID")
        # 用户缺少该角色才给他上
        if role_id not in guild_user.roles:
            await guild.grant_role(guild_user,role_id) # 第二个参数是角色id

        # 方法3，使用用户对象和角色对象
        guild_roles = await guild.fetch_roles()
        # 用户缺少该角色才给他上
        if role_id not in guild_user.roles:
            for role in guild_roles:
                if role.id == role_id: # 是我们的目标role_id
                    await guild.grant_role(guild_user,role)
                    break
        
        # 下角色
        await guild.revoke_role("用户ID",role_id)
        
    except Exception as result:
        print(traceback.format_exc())  # 打印报错详细信息

if __name__ == '__main__':
    print("bot start")
    bot.run()