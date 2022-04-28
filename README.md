# nonebot-plugin-arcaeabot

An arcaea plugin for nonebot2. ( A cross platform Python async bot framework. )

## 功能 Resume

Arcaea 查分器。

[更新日志](https://github.com/SEAFHMC/nonebot-plugin-arcaeabot/blob/main/CHANGELOG.MD)

## 如何开始 Quick Start

***请注意! 1.0.0后的版本更改了默认使用的api，您需要填写相关配置才能正常使用***

使用前请确保您的Python版本>=3.8

项目默认使用AUA (ArcaeaUnlimitedApi)，您需要申请相关apiurl与token(user-agent)并在机器人所在目录`data\arcaea\config.yml`中填写

| 参数               | 描述                                                         |
| ------------------ | ------------------------------------------------------------ |
| AUA_URL | AUA的地址，如"https://www.example.com"</br>（不需要添加/botarcapi） |
| AUA_UA | AUA请求头User-Agent，如"Grievous Lady (Linux; U; Android 2.3.3; BotArcAPI)" |

使该项目被您的 NoneBot2 (nonebot2 及 nonebot-adapter-onebot 版本不得低于 `2.0.0-beta2` ) 机器人作为插件加载, 至于如何做, 您应该懂的。

### 首次使用您需要更新资源文件(assets/song, assets/char以及constants.json)

- 向bot发送"/arc assets_update"以更新资源文件。（默认使用我搭建的api服务器）
- 如果更新失败（服务器炸了）您可以使用[ArcaeaAssetsUpdater](https://github.com/SEAFHMC/ArcaeaAssetsUpdater)搭建自己的资源更新服务器，然后在.env.{ENVIRONMENT}中填写src_api_url=您的api地址)
- 还可以直接从[百度云](https://pan.baidu.com/s/19tmRj4M3eAov6FB_te6f3A?pwd=7g1b)下载资源文件（更新至3.12.4c）。

## 指令 Command

| 指令                                        | 描述                                                         |
| ------------------------------------------- | ------------------------------------------------------------ |
| /arc assets_update                          | 更新曲绘, 请务必在您初次使用该插件或者 Arcaea 版本有更新时发送此命令 |
| /arc help                                   | 查看该插件的帮助文档                                         |
| /arc bind {id}                              | 绑定您的 Arcaea 账户, id 应为 9 位数字                       |
| /arc unbind                                 | 删除您的绑定信息                                             |
| /arc info                                   | 查询您的绑定信息                                             |
| /arc recent                                 | 查询您的最近游玩信息                                         |
| /arc b30                                    | 查询您的 best 30 记录                                        |
| /arc best {songname} {difficulty}           | 查询您的单曲最佳记录                                        |

## To Do
- 随机曲目推荐

## 参考代码

- [DiheChen/nonebot-plugin-arcaea](https://github.com/DiheChen/nonebot-plugin-arcaea)
- [iyume/nonebot-plugin-arcaea](https://github.com/iyume/nonebot-plugin-arcaea)
