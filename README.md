# qqbot-auto-send-message-to-group

> 一个基于 OneBot API 的简易异步 QQ 群批量发消息脚本

![GitHub](https://img.shields.io/github/license/HowieHz/qqbot-auto-send-message-to-group)
![GitHub all releases](https://img.shields.io/github/downloads/HowieHz/qqbot-auto-send-message-to-group/total)
![GitHub release (latest by date)](https://img.shields.io/github/downloads/HowieHz/qqbot-auto-send-message-to-group/latest/total)
![GitHub repo size](https://img.shields.io/github/repo-size/HowieHz/qqbot-auto-send-message-to-group)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/a657069d04fe47588b6c44d55883c4e1)](https://app.codacy.com/gh/HowieHz/qqbot-auto-send-message-to-group/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

可能更好的阅读体验：[文档](https://howiehz.top/archives/Simple-Asynchronous-QQ-Group-Batch-Messaging-Script-Based-on-OneBot-API)

亮点

- 高效异步执行
- 自带进度条
- 支持随机选择信息
- 易于使用
- 轻量 - 仅引用两个第三方库（一个用于异步发送请求，另一个用于显示进度条）

注意：为适配自动化框架，程序将在运行结束 30 秒后自动退出。

## 如何使用

### 部署 OneBot API 软件

使用这个脚本前要部署完成实现了 OneBot API 的软件

一种 onebot api 的实现软件：[NapCat | NapCatQQ | 开始安装](https://napneko.pages.dev/guide/start-install)

运行脚本前请记得创建\开启 http 服务器，开启 `0.0.0.0:3000` 作为服务器地址（`http://localhost:3000` 地址是默认的地址，如果你开启的是 `0.0.0.0:3000`，那么下面示例配置文件的 `onebot_api_http_server` 这一项无需修改）

### 填写配置文件

需要在脚本同目录创建 `config.json` 作为配置文件

onebot_api_http_server：指的是 http 服务器 地址\
group_id_list：指的是你要发送信息的群\
messages：指的是从其中随机选一个消息发送\
（注意：`"messages": [ "" ]`，将不会发出任何消息。如果设置为 `"messages": [ "打卡",  "" ]` 那将会有 50% 的概率发送打卡消息）\
（编辑配置文件的时候请注意在 JSON 中，​尾随逗号（即在最后一个元素后添加的逗号）是不被允许的。建议在编辑完之后使用在线 JSON 检查工具检查正确性）

以下是一个示例配置文件，请将 `onebot_api_http_server` 和 `group_id_list` 改为实际的地址和实际的目标群号。

```json
{
    "onebot_api_http_server": "http://localhost:3000",
    "group_id_list": [
        "123123125",
        "123123124",
        "123123123"
    ],
    "messages": [
        "冒泡睡觉🌙",
        "打卡睡觉🌙",
        "群友晚安🌙",
        "碎觉时间到🌙"
    ]
}
```

### 运行程序

#### 从二进制文件运行（一键启动）

下载地址：[软件发布页](https://github.com/HowieHz/qqbot-auto-send-message-to-group/releases)

点击 `qqbot-auto-send-message-to-group.exe` 下载即可

#### 从源代码运行

见 [CONTRIBUTING](./CONTRIBUTING)

## 代码可能的改进点

1. 代码中抛弃了 `await response.text()` 的返回值，因为在 [NapCat](https://napneko.pages.dev/) 实现中，发现返回值为 `{"status":"failed","retcode":200,"data":null,"message":"Timeout: NTEvent serviceAndMethod:NodeIKernelMsgService/sendMsg ListenerName:NodeIKernelMsgListener/onMsgInfoListUpdate EventRet:\n{\n    \"result\": 0,\n    \"errMsg\": \"\"\n}\n","wording":"Timeout: NTEvent serviceAndMethod:NodeIKernelMsgService/sendMsg ListenerName:NodeIKernelMsgListener/onMsgInfoListUpdate EventRet:\n{\n    \"result\": 0,\n    \"errMsg\": \"\"\n}\n","echo":null}` 而不是类似 `{"status":"ok","retcode":0,"data":{"message_id":409173648},"message":"","wording":"","echo":null}` 但是消息依然是发送成功的，所以我选择忽略此返回值。
2. 无法设置每日自动某时刻发送消息。此处我选择通过外部软件进行定时任务设置，如 Windows 的“任务计划程序”。

## 开发指南

见 [CONTRIBUTING](./CONTRIBUTING)

## 更新日志

见 [Releases](https://github.com/HowieHz/qqbot-auto-send-message-to-group/releases)

## 项目数据统计

### Star History

<a href="https://star-history.com/#HowieHz/qqbot-auto-send-message-to-group&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=HowieHz/qqbot-auto-send-message-to-group&type=Date&theme=dark" loading="lazy" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=HowieHz/qqbot-auto-send-message-to-group&type=Date" loading="lazy" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=HowieHz/qqbot-auto-send-message-to-group&type=Date" loading="lazy" />
 </picture>
</a>
