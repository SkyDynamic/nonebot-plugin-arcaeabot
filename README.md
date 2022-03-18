# nonebot-plugin-arcaeabot
An arcaea plugin for nonebot2. ( A cross platform Python async bot framework. )

## 功能 Resume

Arcaea 查分器。

## 如何开始 Quick Start

使该项目被您的 NoneBot2 (nonebot2 及 nonebot-adapter-onebot 版本不得低于 `2.0.0-beta2` ) 机器人作为插件加载, 至于如何做, 您应该懂的。
### 首次使用您需要更新资源文件(assets/song与assets/char)。
您可以使用[ArcaeaAssetsUpdater](https://github.com/SEAFHMC/ArcaeaAssetsUpdater)搭建自己的资源更新服务器，然后对bot发出/arc assets_update指令进行更新。</br>
也可以直接从[百度云](https://pan.baidu.com/s/1RuabPZq_AiIyoE1o6M_g_w?pwd=jjdf)下载资源文件（可能不是最新的）。

## 指令 Command

| 指令               | 描述                                                         |
| ------------------ | ------------------------------------------------------------ |
| /arc assets_update | 更新曲绘, 请务必在您初次使用该插件或者 Arcaea 版本有更新时发送此命令 |
| /arc help          | 查看该插件的帮助文档                                         |
| /arc bind {id}     | 绑定您的 Arcaea 账户, id 应为 9 位数字                       |
| /arc unbind        | 删除您的绑定信息                                             |
| /arc info          | 查询您的绑定信息                                             |
| /arc recent        | 查询您的最近游玩信息                                         |
| /arc b30           | 查询您的 best 30 记录                                        |

## 为什么这个插件不工作 ? Why is this plugin not working

这你得问 [estertion](https://gist.github.com/esterTion/c673a5e2547cd54c202f129babaf601d) 。

## 参考代码
- [DiheChen/nonebot-plugin-arcaea](https://github.com/DiheChen/nonebot-plugin-arcaea)
- [iyume/nonebot-plugin-arcaea](https://github.com/iyume/nonebot-plugin-arcaea)

