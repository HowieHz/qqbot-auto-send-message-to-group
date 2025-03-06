import asyncio
import json
import os
import random
import time
from dataclasses import dataclass
from typing import Generic, TypeVar, Union

import aiohttp
from tqdm.asyncio import tqdm_asyncio

T = TypeVar("T")
E = TypeVar("E")


@dataclass
class Ok(Generic[T, E]):
    value: T


@dataclass
class Err(Generic[T, E]):
    error: E


Result = Union[Ok[T, E], Err[T, E]]


# 从配置文件读取
def load_config(config_path: str) -> dict[str, any]:
    if not os.path.exists(config_path):
        print(f"配置文件未找到：{config_path}")
        with open(config_path, "w", encoding="utf-8") as file:
            json.dump(
                {
                    "onebot_api_http_server": "http://localhost:3000",
                    "group_id_list": [],
                    "messages": ["打卡"],
                },
                file,
                ensure_ascii=False,
                indent=4,
            )
        print(f"已创建默认配置文件：{config_path}")
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


async def send_group_msg_rate_limited(
    group_id: int, msg: str
) -> Result[tuple[str, int], tuple[str, int]]:
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
            response_json = await response.json()
            match response_json["status"]:
                case "failed":
                    return Err((msg, group_id))
                case "ok":
                    return Ok((msg, group_id))
                case _:
                    return Err((msg, group_id))


async def process_tasks(
    tasks: list[asyncio.Task],
) -> list[Result[tuple[str, int], tuple[str, int]]]:
    results: list[Result[tuple[str, int], tuple[str, int]]] = []
    for core in tqdm_asyncio.as_completed(tasks, desc="发送进度", total=len(tasks)):
        result: Result[tuple[str, int], tuple[str, int]] = await core
        results.append(result)
    return results


def process_results(
    results: list[Result[tuple[str, int], tuple[str, int]]]
) -> list[tuple[str, int]]:
    successes = [result.value for result in results if isinstance(result, Ok)]
    failures = [result.error for result in results if isinstance(result, Err)]

    for msg, group_id in successes:
        print(f"发送成功：{msg} -> {group_id}")
    for msg, group_id in failures:
        print(f"发送失败：{msg} -x {group_id}")

    print(f"{len(successes)} 条消息成功发送")
    print(f"{len(failures)} 条消息发送失败")

    return failures


async def main():
    tasks: list[asyncio.Task] = [
        send_group_msg_rate_limited(group_id, get_mag()) for group_id in group_id_list
    ]
    results: list[Result[tuple[str, int], tuple[str, int]]] = await process_tasks(tasks)
    failures: list[tuple[str, int]] = process_results(results)

    while failures:
        user_input = input("是否要重发失败消息？(y/n): ").lower()
        if user_input != "y":
            break
        tasks = [
            send_group_msg_rate_limited(group_id, msg) for msg, group_id in failures
        ]
        results = await process_tasks(tasks)
        failures = process_results(results)


if __name__ == "__main__":
    asyncio.run(main())
    print("30 秒后自动结束程序")
    time.sleep(30)
