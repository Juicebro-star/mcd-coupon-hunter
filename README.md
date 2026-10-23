# mcd-coupon-hunter 麦门领券

一句话的事：连上麦当劳官方 MCP，一键领走当前所有可领的「麦麦省」优惠券，并汇报你账户里已有的券——快过期的还会提醒你先用。

## 它解决什么问题

麦麦省的券是真金白银的羊毛，但要打开 App 一张张手动领，很容易忘、很容易漏。这个 Skill 把领券变成一句话：

> "帮我把麦当劳的券领了"

AI 就会自动查可领的券 → 全部领走 → 汇报结果。领券从"记得打开 App 点半天"变成"顺手说一句"。

## 目标用户

- 麦当劳常客：不想错过任何一张麦麦省券的人
- AI 工具玩家：想看看官方 MCP 能把多少日常小事变成一句话的人
- 羊毛党：券有有效期，领了不用等于没领——这个 Skill 会盯着快过期的券提醒你

## 工作流程

1. **查可领**：调用 `available-coupons`，看现在有哪些麦麦省券可以领
2. **一键领**：调用 `auto-bind-coupons`，把可领的券全部领到账户（官方行为即一次全领，无需逐张指定）
3. **查已有**：调用 `query-my-coupons`，列出账户里现在所有的券
4. **汇报**：这次领了几张、分别是什么、有没有 3 天内过期的券需要优先用掉

可选增强：

- 点餐前调用 `query-store-coupons`，查当前这家店能用哪些券
- 想抽奖先调用 `query-lottery-info` 看规则再决定，`draw-lottery` 会真实消耗积分，不闭眼抽

## 安装方法

### 1. 申请麦当劳 MCP Token

打开 [open.mcd.cn/mcp](https://open.mcd.cn/mcp)：

1. 点右上角，用手机号验证登录
2. 登录后点右上角
3. 点申请 Token，阅读并同意服务协议
4. Token 申请成功后一键复制

> ⚠️ Token 等同于你的麦当劳账号凭证：不要发到群聊、不要写进代码仓库、不要截图外传。

### 2. 配置 MCP 连接

在任何支持 MCP 的客户端（Cherry Studio、Cursor、TRAE、WorkBuddy 等）里添加：

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

把 `YOUR_MCP_TOKEN` 换成你自己的 Token 并保存、启用。

### 3. 安装本 Skill

把本仓库的 `SKILL.md` 放进你的 AI 客户端的 Skill 目录（或直接把内容粘贴为自定义指令），然后对 AI 说"帮我领麦当劳的券"即可。

也可以直接跑仓库里的参考脚本（Token 只从环境变量读）：

```bash
export MCD_MCP_TOKEN="你的Token"
python3 coupon_hunter.py
```

## 使用示例

| 你说 | AI 做 |
|---|---|
| "领一下麦当劳的券" | 查可领 → 全部领走 → 汇报领了什么 |
| "我现在有哪些麦当劳券？" | 列出已有券和有效期，快过期的标出来 |
| "这家店能用哪些券？" | 查当前门店可用券（需定位/门店信息） |

示例汇报：

> 领好了 ✅ 这次新领 3 张：麦辣鸡腿堡买一送一、薯条兑换券、麦乐鸡 5 块装优惠券。
> 你账户里现在共 7 张券，其中「中杯可乐兑换券」后天过期，记得先用掉。

## 安全说明

- Token 只通过环境变量 `MCD_MCP_TOKEN` 或客户端配置传入，**绝不写进仓库**
- 官方限流为每 Token 每分钟 600 次请求，日常使用碰不到
- 本项目只调用官方 MCP 提供的工具，不模拟登录、不抓取任何非公开接口

## 参赛说明

本项目参加麦当劳程序员创意开发大赛，参赛声明见 [CONTEST_DECLARATION.md](./CONTEST_DECLARATION.md)，MCP 集成说明见 [MCP_INTEGRATION.md](./MCP_INTEGRATION.md)。
