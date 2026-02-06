import os
import re
import sys
import json
import subprocess
import socket
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm

console = Console()

# --- 核心性能参数 ---
os.environ["TDL_THREADS"] = "8"
os.environ["TDL_LIMIT"] = "4"
os.environ["TDL_POOL"] = "8"
os.environ["TDL_RECONNECT_TIMEOUT"] = "0"

# --------------------获取 tdl.exe 路径--------------------
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

tdl_path = os.path.join(base_path, "tdl.exe")

# --------------------工具函数--------------------
def parse_tg_link(input_str):
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

# --------------------代理功能--------------------
def check_proxy_status():
    proxy = os.environ.get("TDL_PROXY", "")
    if not proxy:
        console.print("[bold bright_yellow]未配置代理，正在测试直连 Telegram...[/bold bright_yellow]")
    else:
        console.print(f"[bold bright_cyan]正在检测代理连通性: [reverse]{proxy}[/reverse][/bold bright_cyan]")

    target_host = "api.telegram.org"
    target_port = 443
    try:
        socket.setdefaulttimeout(5)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((target_host, target_port))
        console.print(f"[bold bright_white on green] ✅ 连接成功! 能够访问 {target_host} [/bold bright_white on green]")
    except Exception as e:
        console.print(f"[bold bright_white on red] ❌ 连接失败! 无法访问 Telegram 服务器。错误: {e} [/bold bright_white on red]")
        console.print("[dim bright_white]请检查系统时间是否同步或代理是否可用[/dim bright_white]")

def proxy_manager():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(Panel("[bold bright_white on blue] 🌐 代理管理中心 [/bold bright_white on blue]", border_style="bright_cyan"))
        current_proxy = os.environ.get("TDL_PROXY", "未设置")
        console.print(f"当前环境变量 TDL_PROXY: [bold bright_green]{current_proxy}[/bold bright_green]")
        table = Table(show_header=False, box=None)
        table.add_row("[bright_cyan]1[/bright_cyan]", "设置代理 [dim](例如 socks5://127.0.0.1:7890)[/dim]")
        table.add_row("[bright_cyan]2[/bright_cyan]", "清除代理")
        table.add_row("[bright_cyan]3[/bright_cyan]", "测试连接状态")
        table.add_row("[bright_magenta]B[/bright_magenta]", "返回主菜单")
        console.print(table)
        choice = Prompt.ask("[bold bright_yellow]请选择操作[/bold bright_yellow]", choices=["1","2","3","B","b"])
        if choice == "1":
            new_proxy = Prompt.ask("[bold bright_cyan]请输入新的代理地址[/bold bright_cyan]")
            os.environ["TDL_PROXY"] = new_proxy
            subprocess.run(f'setx TDL_PROXY "{new_proxy}"', shell=True, capture_output=True)
            console.print("[bold bright_green]代理已设置！(系统变量可能需要重启终端生效)[/bold bright_green]")
        elif choice == "2":
            os.environ["TDL_PROXY"] = ""
            subprocess.run('setx TDL_PROXY ""', shell=True, capture_output=True)
            console.print("[bold bright_red]代理已清除[/bold bright_red]")
        elif choice == "3":
            check_proxy_status()
            console.print("\n[bold bright_white]按回车返回菜单...[/bold bright_white]")
            input()
        elif choice.upper() == "B":
            break

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

# --------------------菜单--------------------
def show_header():
    description = """
📦 [bold bright_white on cyan] tdl Telegram 工具箱整合版 [/bold bright_white on cyan]

[bold bright_green]功能说明[/bold bright_green]:

1. ⏬ [bold bright_yellow]批量下载[/bold bright_yellow] ([bold yellow]普通群/话题群[/bold yellow])
2. 🔄 [bold bright_yellow]消息转发[/bold bright_yellow] ([bold yellow]源端 ➡️ 目标端[/bold yellow])
3. 🚀 [bold bright_yellow]下载并转发[/bold bright_yellow] ([bold yellow]组合联动一键操作[/bold yellow])
4. 🌐 [bold bright_yellow]代理管理[/bold bright_yellow] ([bold yellow]设置/清除/测试代理[/bold yellow])

[bold bright_magenta]💡 提示:[/bold bright_magenta]
- 直接粘贴消息链接，程序将自动解析频道 ID、话题 ID 及消息 ID。
"""
    console.print(Panel(description, title="[bold bright_white on magenta] 🛠 工具说明手册 [/bold bright_white on magenta]", border_style="bright_blue"))

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        show_header()
        table = Table(show_header=False, box=None)
        table.add_row("[bold bright_cyan]1[/bold bright_cyan]", "[bold bright_yellow]⏬ 批量下载[/bold bright_yellow]")
        table.add_row("[bold bright_cyan]2[/bold bright_cyan]", "[bold bright_yellow]🔄 消息转发[/bold bright_yellow]")
        table.add_row("[bold bright_cyan]3[/bold bright_cyan]", "[bold bright_yellow]🚀 下载并转发[/bold bright_yellow]")
        table.add_row("[bold bright_cyan]P[/bold bright_cyan]", "[bold bright_magenta]🌐 代理管理[/bold bright_magenta]")
        table.add_row("[bold bright_cyan]L[/bold bright_cyan]", "[bold bright_magenta]🔑 登录管理[/bold bright_magenta]")
        table.add_row("[bold bright_cyan]Q[/bold bright_cyan]", "[bold bright_red]❌ 退出程序[/bold bright_red]")
        console.print(table)

        choice = Prompt.ask("[bold bright_white on dark_magenta] 请选择功能编号 [/bold bright_white on dark_magenta]", choices=["1","2","3","P","p","L","l","Q","q"])
        if choice=="1": execute_task("dl")
        elif choice=="2": execute_task("fw")
        elif choice=="3": execute_task("both")
        elif choice.upper()=="P": proxy_manager()
        elif choice.upper()=="L": 
            subprocess.run(f'"{tdl_path}" login', shell=True)
            input("\n[dim]登录操作结束，按回车返回...[/dim]")
        elif choice.upper()=="Q": break

if __name__=="__main__":

    main()
