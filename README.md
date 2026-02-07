# 📦 tdl Telegram 工具箱 · 使用说明

本项目是一个基于 [**iyear/tdl（Telegram Downloader）**](https://github.com/iyear/tdl) 的 **Telegram 工具箱脚本**，
---

## 🚀 发行版说明（已内置 tdl）

本项目已发布 **Windows 可执行发行版**：

👉 **Release 下载地址**
[https://github.com/XuanMouren2004/tdl_Script/releases/](https://github.com/XuanMouren2004/tdl_Script/releases/)

### ✅ 发行版特性

* ✅ **已内置 `tdl.exe`，开箱即用**
* ✅ 无需额外下载 tdl
* ✅ 解压即可运行
* ✅ 已自动适配 `tdl.exe` 路径

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
  * <img width="855" height="328" alt="image" src="https://github.com/user-attachments/assets/483a93de-9f81-4a39-8776-c66ab3294a83" />
  * <img width="1186" height="327" alt="image" src="https://github.com/user-attachments/assets/8fd7d148-fe82-4dd4-81be-6a88c44cb1e5" />



* 使用 tdl 官方下载机制

---

### 🔄 消息转发

* 支持源端 ➡️ 目标端转发
* 支持普通群与话题群
* 使用 **clone 模式**：

  * 尽量保留原消息内容
  * 保留附件、文本结构

---

### 🚀 下载并转发

* 一次输入源端和目标端
* 自动执行完整流程：

  1. 导出消息
  2. 下载内容
  3. 转发消息
* 适合：

  * 频道迁移
  * 群组内容备份后再转发

---

### 🌐 代理管理

* 支持设置 / 清除 `TDL_PROXY`
* 支持 SOCKS5 / HTTP 代理
* 提供基础连接测试 **[❌不可用，修复中]**

---

### 🔑 登录管理  **[❌不可用，修复中]**

* 调用 `tdl login`
* 使用 tdl 官方登录流程
* 支持首次登录与会话复用

---

## 🛠 二次编写 / 二次打包说明

### 🔹 关于 tdl 的说明

* 本项目发行版 **已内置 tdl.exe**
* tdl 为第三方工具，其版权与维护权归原作者所有

👉 **tdl 原作者项目地址**
[https://github.com/iyear/tdl](https://github.com/iyear/tdl)

---

### 🔹 二次开发建议

如果你计划：

* 修改本脚本逻辑
* 重新打包成 EXE
* 发布你自己的版本

建议：

1. 明确标注：

   * 项目基于 tdl
   * 并注明原作者项目地址
2. 遵守 tdl 项目的开源协议

好，这里我**只重写你点名的这一小节**，不动前后结构，语气偏 **开发者向 / 说明清晰 / 不绕**，而且**明确：tdl.exe 需要自行从原作者项目下载，并在打包时一并带上**。

你可以 **直接整体替换原来的这一段** 👇

---

## 📦 自行打包说明（开发者）

如果你是从源码自行打包本项目（例如使用 `main.py` 与 `app.ico`），请注意：

### 1️⃣ 获取 tdl.exe（必须）

本项目依赖 **tdl** 执行 Telegram 的下载与转发等操作。
在自行打包前，**开发者需要自行从原作者项目下载 `tdl.exe`**。

👉 **tdl 官方项目地址**
[https://github.com/iyear/tdl](https://github.com/iyear/tdl)

请下载 **Windows 版本的 `tdl.exe`**。

---

### 2️⃣ 示例目录结构

在打包前，请确保你的目录结构如下：

```text
project/
├─ main.py
├─ app.ico
├─ tdl.exe   # 从 iyear/tdl 官方项目下载
```

---

### 3️⃣ PyInstaller 打包示例

推荐使用以下命令进行打包：

```bash
pyinstaller -F -i app.ico --add-binary "tdl.exe;." main.py
```

说明：

* `--add-binary "tdl.exe;."`
  用于将 `tdl.exe` 一并打包进最终的可执行文件目录
* 打包完成后，`tdl.exe` 会被自动释放到程序运行目录

---

### 4️⃣ 打包完成后的注意事项

* 请确认程序运行目录中能够正确访问 `tdl.exe`
* 若程序无法找到 `tdl.exe`，下载 / 转发等功能将无法使用
* 建议在你自己的项目说明中注明：

  * 本项目基于 tdl
  * 并附上原作者项目地址
