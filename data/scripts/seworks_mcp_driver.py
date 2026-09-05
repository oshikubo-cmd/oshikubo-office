# SEWorks MCP driver: mcp-bridge.exe とstdioでMCP JSON-RPCを話す。
# Claude DesktopにしかSEWorksコネクタが登録されていないため、
# Claude Codeセッションからはこのドライバ経由でツールを呼ぶ。
#
# 使い方:
#   python seworks_mcp_driver.py tools/list
#   python seworks_mcp_driver.py tools/call <tool-name> <args.json のパス | インラインJSON>
#
# APIキーは Claude Desktop の設定ファイルから読む（ハードコードしない）。
import json, os, subprocess, sys, threading

BRIDGE = r"C:\Users\020168\seworks-mcp\mcp-bridge.exe"
URL = "https://seintra.g1.shoeisha.co.jp/mcp"
ARGS = ["--name", "seworks-mcp", "--url", URL, "--label", "SEWorks"]
CONFIG = os.path.join(os.environ["APPDATA"], "Claude", "claude_desktop_config.json")

with open(CONFIG, encoding="utf-8") as f:
    key = json.load(f)["mcpServers"]["seworks-mcp"]["env"]["SEWORKS_MCP_API_KEY"]

env = os.environ.copy()
env["SEWORKS_MCP_API_KEY"] = key

proc = subprocess.Popen([BRIDGE] + ARGS, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, env=env)

def drain_stderr():
    for line in proc.stderr:
        sys.stderr.write("[bridge] " + line.decode("utf-8", "replace"))
threading.Thread(target=drain_stderr, daemon=True).start()

def send(msg):
    proc.stdin.write((json.dumps(msg) + "\n").encode())
    proc.stdin.flush()

def recv(expect_id):
    while True:
        line = proc.stdout.readline()
        if not line:
            raise RuntimeError("bridge closed stdout")
        line = line.strip()
        if not line:
            continue
        msg = json.loads(line)
        if msg.get("id") == expect_id:
            return msg

send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
    "protocolVersion": "2024-11-05", "capabilities": {},
    "clientInfo": {"name": "claude-code", "version": "1.0"}}})
recv(1)
send({"jsonrpc": "2.0", "method": "notifications/initialized"})

cmd = sys.argv[1] if len(sys.argv) > 1 else "tools/list"
if cmd == "tools/list":
    send({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    res = recv(2)
    for t in res.get("result", {}).get("tools", []):
        print("### " + t["name"])
        print(t.get("description", "")[:500])
        print("input:", json.dumps(t.get("inputSchema", {}), ensure_ascii=False)[:1000])
        print()
elif cmd == "tools/call":
    name = sys.argv[2]
    if len(sys.argv) > 3:
        arg = sys.argv[3]
        if os.path.isfile(arg):
            with open(arg, encoding="utf-8-sig") as f:
                args = json.load(f)
        else:
            args = json.loads(arg)
    else:
        args = {}
    send({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
          "params": {"name": name, "arguments": args}})
    res = recv(2)
    out = json.dumps(res, ensure_ascii=False, indent=1)
    limit = int(os.environ.get("OUT_LIMIT", "30000"))
    print(out[:limit])
    if len(out) > limit:
        print(f"\n...[truncated {len(out)-limit} chars]")

proc.stdin.close()
proc.terminate()
