# MCP 集成说明

## 使用的 MCP Server

- **名称**：麦当劳中国官方 MCP Server
- **地址**：`https://mcp.mcd.cn`
- **传输协议**：Streamable HTTP
- **鉴权方式**：请求头 `Authorization: Bearer <MCP_TOKEN>`，Token 在 [open.mcd.cn/mcp](https://open.mcd.cn/mcp) 登录后于控制台激活申请
- **限流**：每 Token 每分钟最多 600 次请求；Token 无效/过期/未提供时返回 401

配置示例：

```json
{
  "mcpServers": {
    "mcd-mcp": {
      "type": "streamablehttp",
      "url": "https://mcp.mcd.cn",
      "headers": {
        "Authorization": "Bearer YOUR_MCP_TOKEN"
      }
    }
  }
}
```

## 实际使用的 Tool

本 Skill 使用以下 4 个官方 Tool（核心 3 个 + 可选 1 个）：

| Tool | 用途 | 在本项目中的角色 |
|---|---|---|
| `available-coupons` | 查询当前可领取的麦麦省券列表 | 第一步：先看有什么可领，避免空领 |
| `auto-bind-coupons` | 一键领取所有当前可用的麦麦省券（无需指定 couponId） | 第二步：核心动作，一次全领 |
| `query-my-coupons` | 查询账户下已有的全部优惠券 | 第三步：领后核对 + 找快过期的券 |
| `query-store-coupons` | 查询当前门店下可用的优惠券列表 | 可选：点餐前查这家店能用哪些券 |

## 调用流程

```text
用户："帮我把麦当劳的券领了"
   │
   ├─ 1. available-coupons ──→ 当前可领券列表
   │        └─ 若为空：直接汇报"暂时没有可领的券"，结束
   │
   ├─ 2. auto-bind-coupons ──→ 一键领取全部可领券
   │
   ├─ 3. query-my-coupons ───→ 账户现有全部券（含有效期）
   │
   └─ 4. 汇总汇报：新领张数与名称、现有总数、3 天内过期提醒
```

设计要点：

- **先查后领**：先用 `available-coupons` 确认有券可领再调领券接口，汇报时能说清"这次新领了什么"，而不是只报一个总数。
- **领后核对**：用 `query-my-coupons` 做闭环验证——领券接口返回成功不等于券真的到账，以账户实际列表为准。
- **过期提醒**：从 `query-my-coupons` 的结果里筛出 3 天内到期的券单独提醒，避免"领了却过期"的浪费。

## 业务价值

1. **对用户**：麦麦省券从"要记得手动领"变成"一句话领完"，不漏领、不过期，羊毛真正落袋。
2. **对场景**：领券是高频、低决策成本的动作，天然适合被 AI Agent 托管——这是 MCP 把"App 里的功能"变成"对话里的能力"的最小完整样本。
3. **对生态**：展示了官方 MCP 在优惠权益场景的完整链路（查询 → 执行 → 核对 → 提醒），可复用到积分、活动、点餐等其他日常场景。
