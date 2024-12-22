import asyncio
import json
import os
import random
import time

import aiohttp
from tqdm.asyncio import tqdm_asyncio


# 从配置文件读取
def load_config(config_path: str) -> dict[str, any]:
    if not os.path.exists(config_path):
        print(f"配置文件未找到：{config_path}")
        exit(1)
    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)


config: dict[str, any] = load_config("config.json")
onebot_api: str = config.get("onebot_api_http_server", "http://localhost:3000")
group_id_list: list[int] = config.get("group_id_list", [])
# 默认消息为打卡
messages: list[str] = config.get("messages", ["打卡"])


def get_mag() -> str:
    """随机获取一个睡觉打卡消息

    Returns:
        str: 打卡消息
    """
    return random.choice(messages)


async def send_group_msg_rate_limited(group_id: int, msg: str) -> tuple[str, int]:
    """发送消息到指定群组，限制发送频率

    Args:
        group_id (int): 群号
        msg (str): 消息内容

    Returns:
        _type_: _description_
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{onebot_api}/send_group_msg_rate_limited",
            json={
                "group_id": group_id,
                "message": msg,
            },
        ) as response:
            await response.text()
            return msg, group_id


async def main():
    tasks = [
        send_group_msg_rate_limited(group_id, get_mag()) for group_id in group_id_list
    ]
    results = []
    for core in tqdm_asyncio.as_completed(tasks, desc="发送进度", total=len(tasks)):
        msg, group_id = await core
        results.append((msg, group_id))

    for msg, group_id in results:
        print(f"发送成功：{group_id} -> {msg}")
    print(f"已发送 {len(results)} 条消息")


if __name__ == "__main__":
    asyncio.run(main())
    print("30 秒后自动结束程序")
    time.sleep(30)
