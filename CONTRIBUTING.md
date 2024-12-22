# 贡献指南

## 部署开发环境

### 在本地部署 Python3.12 环境

[Download Python](https://www.python.org/downloads/)

### 下载项目源码，并进入到项目根目录

```bash
git clone https://github.com/HowieHz/qqbot-auto-send-message-to-group && cd qqbot-auto-send-message-to-group/
```

### 创建虚拟环境

```bash
python -m venv .venv
```

### 进入虚拟环境

在 Windows 环境下

```powershell
./.venv/Scripts/activate
```

在 Bash

```bash
source ./.venv/bin/activate
```

附：退出虚拟环境的指令

```bash
deactivate
```

### 安装项目所需库

```bash
pip install -r requirements.txt
```

创建 pre-commit 钩子，以便在每次提交前自动格式化代码

```bash
pre-commit install
```

<!-- 附：导出当前虚拟环境中的库

```bash
pip freeze > requirements.txt
``` -->

## 构建二进制文件

> Windows 环境下

```powershell
./build_scripts/build_main.bat
```
