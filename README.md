# 📦 tdl Telegram 工具箱 · 使用说明

本项目是一个基于  
👉 [**iyear/tdl（Telegram Downloader）**](https://github.com/iyear/tdl)
封装的 **Telegram 多功能控制台工具箱**，  
用于 **批量下载 / 消息转发 / 代理管理 / 登录管理** 等操作。

---

## 🚀 发行版说明（已内置 tdl）

本项目已发布 **Windows 可执行发行版（EXE）**：

👉 **Release 下载地址**  
https://github.com/XuanMouren2004/tdl_Script/releases/

### ✅ 发行版特性

* ✅ **已内置 `tdl.exe`，开箱即用**
* ✅ 无需额外下载 tdl
* ✅ 解压即可运行
* ✅ 自动适配 `tdl.exe` 路径
* ✅ 支持会话复用（Session）

---

## ✅ 功能一览

| 模块 | 功能 |
|----|----|
| ⏬ 下载 | 普通群 / 频道 / 话题群批量下载 |
| 🔄 转发 | clone 模式消息转发（保留结构与附件） |
| 🚀 联合模式 | 下载 + 转发一体化流程 |
| 🔗 链接解析 | 自动解析 t.me / t.me/c 链接 |
| 🧰 工具 | 列出对话 / 账号信息 |
| 🌐 代理 | 设置 / 清除 / 连通性测试 |
| 🔑 登录 | 短信验证码登录 / 会话复用 |

---

## 🧰 功能介绍

### ⏬ 批量下载

* 支持：
  * 普通群 / 频道
  * 话题群（Topic）
* 支持直接粘贴 **Telegram 消息链接**
* 自动解析：
  * 群组 / 频道 ID
  * 话题 ID（如存在）
  * 消息 ID
* 使用 tdl 官方下载机制

---

### 🔄 消息转发

* 支持源端 ➡️ 目标端转发
* 支持普通群与话题群
* 使用 **clone 模式**：
  * 尽量保留原消息内容
  * 保留文本结构、附件、顺序

---

### 🚀 下载并转发

* 一次性输入源端与目标端
* 自动执行完整流程：
  1. 导出消息
  2. 下载内容
  3. 转发消息
* 适用于：
  * 频道迁移
  * 群组备份后再转发

---

### 🧰 实用工具箱（Tools）

* 📋 **列出所有对话**
  * 调用 `tdl chat ls`
  * 快速查看当前账号下的群组 / 频道 / 私聊

* 🆔 **账号信息查看（Who Am I）**
  * 自动检测 `whoami` 扩展
  * 若未安装将自动安装
  * 显示当前登录账号详细信息

---

### 🌐 代理管理

* 支持设置 / 清除 `TDL_PROXY`
* 支持 HTTP / SOCKS5 代理
* 支持写入系统环境变量（Windows）
* 内置代理连通性测试：
  * 自动检测当前出口 IP
  * 显示国家 / 城市（中英文）
  * 测试 Google 连接状态与延迟（⚠️部分代理可能因证书问题失败）

---

### 🔑 登录管理

* 使用 tdl 官方登录流程
* 当前支持 **短信验证码登录（-T code）**
* 支持自定义 Session 名称
* 支持会话复用
* 支持登录状态检测
* 可直接查看当前账号信息（Who Am I）

---

## 🛠 自行打包说明（开发者）

如果你是基于源码自行打包本项目，请注意以下事项。

### 1️⃣ 获取 tdl.exe（必需）

本项目依赖 **tdl** 执行 Telegram 操作。  
在打包前，需自行从原作者项目下载 `tdl.exe`。

👉 [tdl发行版：https://github.com/iyear/tdl/releases](https://github.com/iyear/tdl/releases)

---

### 2️⃣ 示例目录结构

```text
project/
├─ main.py
├─ app.ico
├─ tdl.exe
```
---

### 3️⃣ PyInstaller 打包示例

```bash
pyinstaller -F -i app.ico --add-binary "tdl.exe;." main.py
```

**说明：**

* `-F`
  打包为单文件可执行程序

* `-i app.ico`
  指定程序图标（可选）

* `--add-binary "tdl.exe;."`
  将 `tdl.exe` 一并打包，并在运行时释放到程序所在目录

  > ⚠️ Windows 下必须使用 `;` 作为分隔符

* `main.py`
  程序入口文件

---

### 4️⃣ 注意事项

* 请确保程序运行目录中可以正确访问 `tdl.exe`
* 若程序未能找到 `tdl.exe`：

  * 下载功能不可用
  * 转发功能不可用
* 若你发布二次版本，请在说明中明确标注：

  * 本项目基于 **tdl**
  * 并附上原作者项目地址

---

## 📌 版权与说明

* 本项目基于第三方工具 **tdl**
* `tdl` 的版权与维护权归原作者所有

* 📥 **A Telegram toolkit written in Golang**
  * 👉 [https://github.com/iyear/tdl](https://github.com/iyear/tdl)
 
---
