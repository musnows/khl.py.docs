---
title: 机器人初始化
description: 如何初始化你的机器人？
---

## 目录

[[toc]]

## 1.前言

在khlpy中，绝大部分操作都需要基于Bot对象来执行。所以，要想让机器人跑起来，我们要先把机器人的身体做出来，有了身体，才能让这个机器人去做我们想要做的事情

阅读本文之前，请再次确认您已经在 [kook开发者中心](https://developer.kookapp.cn/) 申请了开发者权限，并能正常进入 [开发者机器人管理后台](https://developer.kookapp.cn/bot/)

## 2.机器人管理后台

### 创建机器人

进入开发者后台-应用，点击右上角创建应用，即可创建一个新的机器人

![image-20230525225030524](./img/image-20230525225030524.png)

填入应用名称（即机器人名称，后续还可以更改），点击确定，创建机器人

![image-20230525225157075](./img/image-20230525225157075.png)

![image-20230525225252746](./img/image-20230525225252746.png)

点击左侧 `机器人` 按钮，即可进入机器人token的页面。

### 获取机器人token

在此页面，你可以

* 修改机器人的连接方式
* 获取机器人的token
* 是否开启公共机器人（若不开启，则只有机器人开发者可以邀请机器人到其他服务器）

![image-20230525225334570](./img/image-20230525225334570.png)

如果是webhook链接方式，则还需要填入机器人的 `Callback Url`

![image-20230525225601764](./img/image-20230525225601764.png)

### 机器人权限

在 `邀请链接` 界面，您可以看到机器人的邀请链接，并可以设置机器人被邀请到服务器内的默认权限。

权限设置请按照机器人的功能进行选择。如果你不知道应该选择什么权限，可以无脑选择管理员。

![image-20230525225515363](./img/image-20230525225515363.png)

## 3.两种连接模式

KOOK的机器人有两种连接模式：

* webscoket
* webhook

列个表，来看看二者的主要区别

| websocket      | webhook                                    |
| -------------- | ------------------------------------------ |
| 不需要公网地址 | 需要一个可访问的**公网地址**               |
| 只需要token    | 除了token，还需要verify-token和encrypt-key |

在 [@musnows](https://github.com/musnows/) 的实测下，webhook 连接方式的稳定性略高于 websocket 。

* 如果你的机器人已经基本开发完毕，功能完好无bug，则更推荐使用webhook方式部署机器人，实现长期稳定运行；
* 如果你的机器人是部署在家中，无可用公网地址，则可以使用websocket；
* 二者并没有严格意义上的孰强孰弱，根据自己的实际使用情况选择即可

知道了这两种方式的区别了，下面来看看如何给我们的机器人造一个身子吧！

## 4.实例化Bot对象

下面便是使用两种办法创建机器人对象的代码

### websocket

~~~python
from khl import Bot
## websocket
bot = Bot(token = 'token') 
~~~

### webhook

~~~python
from khl import Bot
## webhook
webhook_port = 5000 ## 机器人webhook服务绑定端口，默认为5000
webhook_route = '/khl-wh' ## 机器人webhook服务器回调地址，默认为/khl-wh
## 按如上配置，回调地址是 http://ip:5000/khl-wh
## 将此地址填入kook机器人后台的callback url，即可上线机器人
## 记得开启云服务器防火墙中对5000端口的tcp访问

bot = Bot(cert = Cert(token = 'token',
                      verify_token = 'verify_token',
                      encrypt_key = 'encrypt'),
          port = webhook_port,
          route = webhook_route
)
~~~

### 可选参数

* `compress`，是否压缩，默认为 True
* 其余参数基本用不上...

## 5.启动

有了机器人对象，添加了机器人功能模块（这部分将在其他文档中讲解）后，就可以让机器人跑起来了！

### 直接启动

以websocket连接方式为例，使用 `bot.run()` 函数启动机器人

~~~python
from khl import Bot
## websocket
bot = Bot(token = 'token') 

## 添加功能模块
## ......

## 开跑
bot.run() 
~~~

### 和其他异步模块一起运行

除了直接运行，我们还可以给机器人进程添加其他异步模块，集合为单个进程运行

~~~python
import asyncio
from aiohttp import web,web_request
from khl import Bot
## websocket
bot = Bot(token = 'token') 
## 初始化节点
routes = web.RouteTableDef()

## 请求routes的根节点
@routes.get('/')
async def hello_world(request:web_request.Request):
    return web.Response(body="hello")

## 添加routes到app中
app = web.Application()
app.add_routes(routes)

## 同时运行app和bot
HOST,PORT = '0.0.0.0',14725
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(
        asyncio.gather(web._run_app(app, host=HOST, port=PORT), bot.start()))
~~~

使用如上的代码，我们将在单个进程中，异步运行 `aiohttp.web` 实现的 http 请求处理器（app），和机器人本身（bot）

注意，如果这里的 `aiohttp.web` 服务需要外网访问，则一定要将 `HOST` 填为 `0.0.0.0`。如果是 `127.0.0.1`，是不支持外网访问的！

将如上代码写入 `test.py` 文件

~~~
python3.10 test.py 
~~~

运行程序，效果如下

![image-20230525230129442](./img/image-20230525230129442.png)

点击终端中的链接，可以在本地访问到 `aiohttp.web` 服务。

> 如果需要公网访问此链接，则需要修改为 `http://公网ip:14725`，并在防火墙中开启14725端口的tcp访问

![image-20230525230207657](./img/image-20230525230207657.png)

此时，两个异步程序就在单个进程中运行了！

使用相同办法，你还可以实现两个完全不同的独立机器人在单进程中执行。

#### 屏蔽eventloop警告

这里还出现了一个无关紧要的警告，其并不会影响程序正常运行，我们可以添加如下代码，禁止掉这个警告

~~~python
## 屏蔽报错
## ignore warning 'DeprecationWarning: There is no current event loop'
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
~~~

![image-20230525230459360](./img/image-20230525230459360.png)

### 后台运行（Linux）

如果你使用的是 Linux 来部署机器人，使用`nohup`命令就能很方便地让机器人在后台运行

~~~bash
nohup python3.10 -u test.py >> ./nohup.log 2>&1 &
~~~

此时会创建一个后台进程，并将机器人的所有输出重定向到当前目录下的 `nohup.log` 文件中。

如果想要找到对应的进程，可以使用 `ps` 命令

~~~bash
ps axj | head -1 && ps jax | grep test.py
~~~

这个命令会找到后台运行的 `test.py` 程序，此时可以给机器人程序发送信号，让其中止

~~~bash
kill -9 进程号
~~~

进程号是 `ps` 命令输出结果中，第二列的数字

![image-20230526120055830](./img/image-20230526120055830.png)

## Over

机器人初始化的基本操作就是这些了~
