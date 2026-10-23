#!/usr/bin/env python3
"""麦门领券参考脚本：通过麦当劳官方 MCP 完成 查可领 → 一键领 → 查已有。

Token 只从环境变量 MCD_MCP_TOKEN 读取，绝不硬编码、绝不写进仓库。
用法：
    export MCD_MCP_TOKEN="你的Token"
    python3 coupon_hunter.py
依赖：Python 3.9+ 标准库（urllib），无需第三方包。
"""

import json
import os
import sys
import urllib.request
import urllib.error

MCP_URL = "https://mcp.mcd.cn"


def call_tool(token: str, tool_name: str, arguments: dict | None = None) -> dict:
    """通过 Streamable HTTP 调用一个 MCP Tool（JSON-RPC 2.0 tools/call）。"""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments or {}},
    }
    req = urllib.request.Request(
        MCP_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        if e.code == 401:
            sys.exit("401：Token 无效或已过期，请去 open.mcd.cn/mcp 控制台重新激活。")
        if e.code == 429:
            sys.exit("429：触发限流（600 次/分钟），稍后再试。")
        raise
    # Streamable HTTP 可能返回 SSE 流，取其中 data: 行的 JSON
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("data:"):
            return json.loads(line[5:])
    return json.loads(body)


def main() -> None:
    token = os.environ.get("MCD_MCP_TOKEN", "").strip()
    if not token:
        sys.exit("未设置环境变量 MCD_MCP_TOKEN，请先 export 你的麦当劳 MCP Token。")

    print("1/3 查询当前可领的麦麦省券…")
    available = call_tool(token, "available-coupons")
    print(json.dumps(available, ensure_ascii=False, indent=2))

    print("2/3 一键领取全部可领券…")
    bound = call_tool(token, "auto-bind-coupons")
    print(json.dumps(bound, ensure_ascii=False, indent=2))

    print("3/3 查询账户已有券（领后核对）…")
    mine = call_tool(token, "query-my-coupons")
    print(json.dumps(mine, ensure_ascii=False, indent=2))

    print("完成。请结合 query-my-coupons 的结果核对到账情况，并留意 3 天内到期的券。")


if __name__ == "__main__":
    main()
