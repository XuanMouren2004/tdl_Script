import os
import re
import sys
import json
import subprocess
import time

# 确保基础库存在
try:
    import requests
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt, Confirm
except ImportError:
    print("❌ 缺少必要库，请先运行: pip install rich requests")
    input("按回车退出...")
    sys.exit(1)

console = Console()

# --- 核心性能参数 ---
os.environ["TDL_THREADS"] = "8"
os.environ["TDL_LIMIT"] = "4"
os.environ["TDL_POOL"] = "8"
os.environ["TDL_RECONNECT_TIMEOUT"] = "0"

# --- 登录 Session 名称修改为你的要求 ---
SESSION_NAME = "lks"

# --------------------获取 tdl.exe 路径--------------------
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

tdl_path = os.path.join(base_path, "tdl.exe")
if not os.path.exists(tdl_path):
    tdl_path = "tdl.exe"

# --------------------智能 WHOAMI (零干扰版)--------------------
def smart_whoami():
    session_arg = f"-n {SESSION_NAME}"
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(Panel(f"[bold bright_white on blue] 🆔 账号详细信息 [Account Info] [/bold bright_white on blue]"))
    
    # 静默探测：判断是否安装扩展
    check_ext = os.system(f'"{tdl_path}" {session_arg} whoami >nul 2>&1')
    
    if check_ext == 0:
        console.print(f"[cyan]正在请求数据...[/cyan]\n")
        # 只在这里运行一次！
        os.system(f'"{tdl_path}" {session_arg} whoami')
    else:
        console.print("\n[yellow]⚠️ 未检测到 whoami 扩展，准备自动安装...[/yellow]")
        if os.system(f'"{tdl_path}" extension install whoami') == 0:
            console.print("[green]✅ 安装成功，正在获取信息...[/green]\n")
            os.system(f'"{tdl_path}" {session_arg} whoami')
        else:
            console.print("[bold red]❌ 扩展安装失败[/bold red]")

    console.print("\n[dim]查询完毕，按回车返回菜单...[/dim]")
    # 这里我们只留这一个 input
    input()

# --------------------工具函数--------------------
def parse_tg_link(input_str):
    input_str = input_str.split('?')[0].strip()
    clean_url = re.sub(r'^https?://', '', input_str).strip('/')
    if not clean_url.startswith('t.me/'):
        return None
    path_parts = clean_url.replace('t.me/', '').split('/')
    if path_parts[0] == 'c':
        path_parts.pop(0)
    if len(path_parts) == 3:
        return {"peer": path_parts[0], "topic": path_parts[1], "msg_id": path_parts[2]}
    elif len(path_parts) == 2:
        return {"peer": path_parts[0], "topic": None, "msg_id": path_parts[1]}
    return None

def get_params_with_confirm(role="源端"):
    # 使用块状色彩强化输入提示
    raw_input_val = Prompt.ask(f"[bold bright_white on blue] 📥 请输入{role}链接或ID/用户名 [/bold bright_white on blue]")
    parsed = parse_tg_link(raw_input_val)
    if parsed:
        # 炫彩信息表
        table = Table(title=f"[bold underline bright_cyan]识别到{role}核心信息[/bold underline bright_cyan]", show_header=True, header_style="bold bright_white on dark_magenta")
        table.add_column("项目", style="bold bright_yellow")
        table.add_column("解析结果", style="bold bright_green")
        table.add_row("频道/群组 ID", parsed['peer'])
        table.add_row("话题ID", parsed['topic'] if parsed['topic'] else "[dim bright_white]无[/dim bright_white]")
        table.add_row("消息ID", f"[bold reverse] {parsed['msg_id']} [/bold reverse]")
        console.print(table)
        if Confirm.ask("[bold blink bright_red]确认使用这些参数吗?[/bold blink bright_red]"):
            return parsed['peer'], parsed['topic'], parsed['msg_id']
    
    # 手动输入部分的颜色美化
    peer = parsed['peer'] if parsed else raw_input_val
    topic = Prompt.ask(f"[bold bright_yellow]手动输入话题ID[/bold bright_yellow]", default="")
    msg_id = Prompt.ask(f"[bold bright_yellow]手动输入起始消息ID[/bold bright_yellow]", default="1")
    return peer, topic, msg_id

def get_name_from_output(json_file, peer):
    if not os.path.exists(json_file):
        return peer
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("chat_title", peer)
    except:
        return peer

# --------------------实用工具 (修正 whoami & 列表展示)--------------------
def tools_manager():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(Panel(f"[bold bright_white on blue] 🧰 实用工具箱 [Tools] (会话: {SESSION_NAME}) [/bold bright_white on blue]"))
        
        print("1. 📋 列出所有对话 [List Chats] (chat ls)")
        print("2. 🆔 查看当前账号详情 [Who Am I]")
        print("B. 返回主菜单 [Back]")
        
        choice = Prompt.ask("请选择 [Select]", choices=["1","2","B","b"])
        
        if choice == "1":
            # 为 chat ls 增加美化输出
            os.system(f'"{tdl_path}" -n {SESSION_NAME} chat ls')
            input("\n按回车返回...")
        elif choice == "2":
            smart_whoami()
        elif choice.upper() == "B": break

# --------------------代理管理 (自动检测 IP & 双语地理位置)--------------------
def proxy_manager():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(Panel("[bold bright_white on blue] 🌐 代理管理中心 [Proxy Manager] [/bold bright_white on blue]"))
        curr = os.environ.get("TDL_PROXY", "未设置 [Not Set]")
        console.print(f"当前环境变量 [Current Env]: [bold green]{curr}[/bold green]\n")
        
        print("1. 设置代理 [Set Proxy]")
        print("2. 清除代理 [Clear Proxy]")
        print("3. 自动测试当前代理状态 [Test Current Proxy]")
        print("B. 返回 [Back]")
        
        choice = Prompt.ask("请选择 [Select]", choices=["1","2","3","B","b"])
        
        if choice == "1":
            p = Prompt.ask("输入地址 [Input Address] (例 127.0.0.1:7890)")
            os.environ["TDL_PROXY"] = f"http://{p}" if "://" not in p else p
            if os.name == 'nt': 
                # 即使设置系统变量也增加安全保护
                subprocess.run(f'setx TDL_PROXY "{os.environ["TDL_PROXY"]}"', shell=True, check=False)
            console.print("[green]代理已保存 [Proxy Saved][/green]")
            time.sleep(1)

        elif choice == "2":
            os.environ["TDL_PROXY"] = ""
            if os.name == 'nt': 
                subprocess.run('setx TDL_PROXY ""', shell=True, check=False)
            console.print("[yellow]代理已清除 [Proxy Cleared][/yellow]")
            time.sleep(1)

        elif choice == "3":
            proxy = os.environ.get("TDL_PROXY")
            if not proxy:
                console.print("[bold red]错误：尚未设置代理 [Error: Proxy not set][/bold red]")
            else:
                proxies = {"http": proxy, "https": proxy}
                console.print(f"[cyan]正在检测出口 IP 及地理位置... [Detecting Location...][/cyan]")
                
                try:
                    # 1. 获取地理位置 (并发起两次请求分别获取中英文名)
                    # 增加 timeout 防止卡死
                    res_zh = requests.get("http://ip-api.com/json/?lang=zh-CN", proxies=proxies, timeout=8).json()
                    res_en = requests.get("http://ip-api.com/json/", proxies=proxies, timeout=8).json()
                    
                    if res_zh.get("status") == "success":
                        ip_addr = res_zh.get("query")
                        # 格式化国家和城市：中文 [English]
                        country = f"{res_zh.get('country')} [{res_en.get('country')}]"
                        city = f"{res_zh.get('city')} [{res_en.get('city')}]"
                        console.print(f"当前出口 IP [Public IP]: [bold cyan]{ip_addr}[/bold cyan]")
                        console.print(f"国家区域 [Country]: [bold magenta]{country}[/bold magenta]")
                        console.print(f"城市位置 [City]: [bold magenta]{city}[/bold magenta]")
                    else:
                        console.print("[yellow]无法获取位置详情 [Could not get location details][/yellow]")
                    
                    # 2. 测试 Google 延迟
                    console.print(f"\n[cyan]正在测试 Google 连通性... [Testing Google...][/cyan]")
                    start_time = time.perf_counter()
                    google_res = requests.get("https://www.google.com", proxies=proxies, timeout=8)
                    latency = int((time.perf_counter() - start_time) * 1000)
                    
                    if google_res.status_code == 200:
                        console.print(f"连接状态 [Status]: [bold green]正常 [Normal][/bold green]")
                        console.print(f"延迟 [Latency]: [bold cyan]{latency}ms[/bold cyan]")
                    else:
                        console.print(f"连接状态 [Status]: [bold yellow]异常 [Error] ({google_res.status_code})[/bold yellow]")
                        
                except Exception as e:
                    console.print(f"[bold red]❌ 测试失败 [Test Failed][/bold red]")
                    # 这里报错信息也可能含中文，确保输出安全
                    console.print(f"错误详情 [Error]: {str(e)}")
                    
            input("\n按回车返回 [Press Enter to go back]...")

        else: break

# --------------------登录管理 (修正 whoami 命令)--------------------
def login_manager():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(Panel(
            f"[bold bright_white on blue] 🔑 tdl 登录管理 [Login] (会话: {SESSION_NAME}) [/bold bright_white on blue]\n\n"
            "注意：当前仅支持 [bold cyan]短信验证码模式 (-T code)[/bold cyan]",
            border_style="bright_cyan"
        ))

        table = Table(show_header=False, box=None)
        table.add_row("1", "📱 短信验证码登录 [Login via SMS]")
        table.add_row("2", "🔍 检查登录状态 [Check Status]")
        table.add_row("3", "🆔 查看账号信息 [Who Am I]") 
        table.add_row("B", "返回主菜单 [Back]")
        console.print(table)

        choice = Prompt.ask("请选择 [Select]", choices=["1","2","3","B","b"])

        if choice == "1":
            os.system(f'"{tdl_path}" login -n {SESSION_NAME} -T code')
            input("\n操作结束，按回车返回...")
        elif choice == "2":
            try:
                res = subprocess.run(f'"{tdl_path}" -n {SESSION_NAME} chat ls -l 1', shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
                if res.returncode == 0: console.print("[bold white on green] ✅ 登录有效 [Valid] [/bold white on green]")
                else: console.print("[bold white on red] ❌ 未检测到登录 [Invalid] [/bold white on red]")
            except: console.print("[yellow] ⚠️ 无法获取状态 [/yellow]")
            input("\n按回车返回...")
        elif choice == "3":
            smart_whoami()
        elif choice.upper() == "B": break

# --------------------执行任务--------------------
def execute_task(mode):
    # 获取源端起始消息ID
    src_peer, src_topic, src_start = get_params_with_confirm("[bold bright_cyan]源端[/bold bright_cyan]")

    # 获取源端结束消息ID（通过用户输入链接解析）
    if not src_topic:
        console.print(f"[bold dark_blue]🔍 请提供源端结束消息链接，以获取结束ID[/bold dark_blue]")
        _, _, src_end = get_params_with_confirm("[bold bright_cyan]源端结束消息[/bold bright_cyan]")
    else:
        src_end = None  # 话题群直接导出全部，不需要结束ID

    # 构造导出命令
    if src_topic:
        export_cmd = f'"{tdl_path}" -n lks chat export -c {src_peer} --topic {src_topic} -o output.json'
    else:
        export_cmd = f'"{tdl_path}" -n lks chat export -c {src_peer} -i {src_start},{src_end} -T id -o output.json'

    src_name = get_name_from_output("output.json", src_peer)
    console.print(f"[bold bright_cyan]📤 源端实体名称:[/bold bright_cyan] [bold bright_white on dark_green] {src_name} [/bold bright_white on dark_green]")

    subprocess.run(export_cmd, shell=True)

    # 下载
    if mode in ['dl', 'both']:
        console.print(f"[bold bright_white on blue] ⏬ 正在开始下载任务，发送方: {src_name} [/bold bright_white on blue]")
        subprocess.run(f'"{tdl_path}" -n lks dl -f output.json --continue -d {src_peer}', shell=True)

    # 转发
    if mode in ['fw', 'both']:
        dest_peer, dest_topic, _ = get_params_with_confirm("[bold bright_cyan]目标端[/bold bright_cyan]")
        to_param = f'"{{\\"Peer\\": \\"{dest_peer}\\", \\"Thread\\": \\"{dest_topic}\\"}}"' if dest_topic else dest_peer
        dest_name = get_name_from_output("output.json", dest_peer)
        console.print(f"[bold bright_white on dark_magenta] 🔄 正在转发: {src_name} ➔ {dest_name} [/bold bright_white on dark_magenta]")
        forward_cmd = f'"{tdl_path}" -n lks forward --from output.json --to {to_param} --mode clone --desc'
        subprocess.run(forward_cmd, shell=True)

    if os.path.exists("output.json"):
        os.remove("output.json")
    
    console.print("\n[bold bright_white on green] ✨ 操作顺利完成！ ✨ [/bold bright_white on green]")
    console.print("\n[bold bright_white]按回车返回菜单...[/bold bright_white]")
    input()

# --------------------主界面 (保留说明)--------------------
def show_header():
    description = """
📦 [bold bright_white on cyan] tdl Telegram 工具箱整合版 [/bold bright_white on cyan]

[bold bright_green]功能说明[/bold bright_green]:
1. ⏬ [bold yellow]批量下载[/bold yellow] (普通群/话题群)
2. 🔄 [bold yellow]消息转发[/bold yellow] (支持防盗链群组)
3. 🚀 [bold yellow]下载并转发[/bold yellow] (一键备份)
4. 🌐 [bold yellow]代理 & 登录[/bold yellow] (环境配置)

[bold magenta]提示:[/bold magenta] 
粘贴链接时，支持 `t.me/c/xxxx/xxxx` 格式自动解析。
    """
    console.print(Panel(description, title="[bold magenta] tdl GUI Wrapper [/bold magenta]", border_style="bright_blue"))

# --------------------主菜单 (关联工具箱)--------------------
def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        show_header()
        table = Table(show_header=False, box=None)
        table.add_row("[bold cyan]1[/bold cyan]", "⏬ 批量下载 [Batch Download]")
        table.add_row("[bold cyan]2[/bold cyan]", "🔄 消息转发 [Forward Messages]")
        table.add_row("[bold cyan]3[/bold cyan]", "🚀 下载并转发 [Download & Forward]")
        table.add_row("[bold cyan]4[/bold cyan]", "🧰 [bold yellow]实用工具 [Tools][/bold yellow]") # 关联功能
        table.add_row("[bold cyan]P[/bold cyan]", "🌐 [bold magenta]代理管理 [Proxy][/bold magenta]")
        table.add_row("[bold cyan]L[/bold cyan]", "🔑 [bold magenta]登录管理 [Login][/bold magenta]")
        table.add_row("[bold cyan]Q[/bold cyan]", "❌ 退出 [Exit]")
        console.print(table)

        choice = Prompt.ask("请选择 [Select]", choices=["1","2","3","4","P","p","L","l","Q","q"])
        
        if choice=="1": execute_task("dl")
        elif choice=="2": execute_task("fw")
        elif choice=="3": execute_task("both")
        elif choice=="4": tools_manager() # 进入工具箱
        elif choice.upper()=="P": proxy_manager()
        elif choice.upper()=="L": login_manager()
        elif choice.upper()=="Q": break

if __name__=="__main__":
    try:
        main()
    except Exception as e:
        print(f"程序崩溃: {e}")
        input("按回车退出，防止闪退...")
