<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://s2.loli.net/2022/06/16/opBDE8Swad5rU3n.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://s2.loli.net/2022/06/16/xsVUGRrkbn1ljTD.png" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-arcaeabot

_✨ Arcaea查分插件 ✨_
</div>


## 功能 Resume

Arcaea 查分器。

使用 /arc help查看帮助信息

[更新日志](https://github.com/SEAFHMC/nonebot-plugin-arcaeabot/blob/v3.0.0/CHANGELOG.MD)

## 如何开始 Quick Start

***请注意! 您需要填写相关配置才能正常使用***

使用前请确保您的Python版本>=3.8

项目默认使用AUA (ArcaeaUnlimitedApi)，您需要申请相关apiurl与token(user-agent)并在机器人所在目录`data\arcaea\config.yml`中填写

<div align="center">

| 参数               | 描述                                                         |
| ------------------ | ------------------------------------------------------------ |
| AUA_URL | AUA的地址，如"https://www.example.com"</br>（不需要添加/botarcapi） |
| AUA_UA | AUA请求头User-Agent，如"Grievous Lady (Linux; U; Android 2.3.3; BotArcAPI)" |

</div>

使该项目被您的 NoneBot2 (nonebot2 及 nonebot-adapter-onebot 版本不得低于 `2.0.0-beta2` ) 机器人作为插件加载, 至于如何做, 您应该懂的。

### 首次使用您需要更新资源文件(assets/song, assets/char)

- 向bot发送"/arc assets_update"以更新资源文件。
- 如果更新失败（资源更新服务器炸了）您可以使用[ArcaeaAssetsUpdater](https://github.com/SEAFHMC/ArcaeaAssetsUpdater)搭建自己的资源更新服务器，然后在 config.yml 中填写您的api地址)
- 还可以直接从[百度云](https://pan.baidu.com/s/1rR5NOy1zSeHIGZ97oNElTQ?pwd=c4iv)下载资源文件（更新至3.12.10c），并放置于bot目录/data/arcaea/assets中

## 指令 Command

<div align="center">

| 指令                                        | 描述                                                              |
| ------------------------------------------- | ------------------------------------------------------------      |
| /arc assets_update                          | 更新曲绘, 请务必在您初次使用该插件或者 Arcaea 版本有更新时发送此命令   |
| /arc help                                   | 查看该插件的帮助文档                                                |
| /arc bind {id}                              | 绑定您的 Arcaea 账户, 可以是id也可以是用户名                          |
| /arc info                                   | 查询您的绑定信息                                                   |
| /arc recent                                 | 查询您的最近游玩信息                                               |
| /arc b30                                    | 查询您的 best 30 记录                                              |
| /arc best {songname} {difficulty}           | 查询您的单曲最佳记录                                               |
| /arc song {songname} {difficulty}           | 查询歌曲信息                                                       |
| /arc random {start} {end} {difficulty}      | 随机歌曲                                                          |
| /arc preview {songname} {difficulty}         | 查询歌曲谱面预览                                                          |

</div>
  
## To Do
- 咕咕咕

## 感谢

- [Awbugl/Andreal](https://github.com/Awbugl/Andreal)
- [DiheChen/nonebot-plugin-arcaea](https://github.com/DiheChen/nonebot-plugin-arcaea)
- [iyume/nonebot-plugin-arcaea](https://github.com/iyume/nonebot-plugin-arcaea)
