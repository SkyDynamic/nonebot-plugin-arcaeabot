from nonebot import MatcherGroup

cmd_group = MatcherGroup()
arc = cmd_group.on_command("arc", aliases={"arcaea", "a"}, priority=1)
ai_cmd = cmd_group.on_command("arcai", aliases={"arcaeaai", "aai"}, priority=0)
