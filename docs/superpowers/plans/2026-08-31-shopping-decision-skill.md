# Shopping Decision Skill 实现计划

> **面向执行 Agent：** REQUIRED SUB-SKILL: 使用 `superpowers:subagent-driven-development`（推荐）或 `superpowers:executing-plans`，逐项执行本计划。所有步骤使用复选框（`- [ ]`）跟踪。

**目标：** 构建并验证一个中文优先、面向中国大陆个人购物决策的开源 Codex Skill，支持商品推荐、单品评估、商品比较、价格时机判断和经过明确授权的降价监控。

**架构：** 项目只暴露一个可自动或显式触发的 `shopping-decision` Skill。入口文件负责选择五种内部模式并按需加载参考文件；实时信息依赖当前 Codex 已有的网页搜索、浏览器和定时任务能力，不内置爬虫、账号系统或第三方 API。测试分为结构验证、路由用例和新对话行为观察三层。

**技术栈：** Codex 插件清单 JSON、Agent Skills Markdown/YAML frontmatter、`agents/openai.yaml`、JSON 测试夹具、Python 3 标准库验证脚本、PowerShell、Git。

**设计文档：** `docs/superpowers/specs/2026-08-31-shopping-decision-skill-design.md`

## 全局约束

- 面向中国大陆普通消费者，不包含电商卖家选品、店铺运营、Listing 或广告工作流。
- 自动触发与 `$shopping-decision` 显式触发同时启用。
- 公开信息优先；运行时不强制要求付费服务、平台账号、Cookie、第三方 API Key 或浏览器扩展。
- 只提供购物建议；不得登录、操作购物车、结算、下单、付款或索取敏感凭据。
- 首版支持 `recommend`、`evaluate`、`compare`、`price-timing`、`monitor` 五种内部模式。
- 已核验价格必须绑定准确版本、卖家类型、库存状态、查询时间和可追溯来源。
- 搜索摘要、营销页和无法访问页面只能作为线索，不能声明为已核验最低价。
- 本地偏好档案默认关闭；创建、修改和删除均需用户确认，且当前对话要求优先。
- 降价监控必须由用户明确请求，并确认准确版本、价格条件、平台或卖家限制、频率和结束日期。
- 个人对个人二手交易不在首版范围；能够核验卖家、成色、保修和退货的官方翻新商品可以纳入。
- Skill 正文中文优先；UI 元数据保持中英可发现性；公开仓库提供英文 `README.md` 和中文 `README.zh-CN.md`。
- 项目内容独立创作并使用 Apache-2.0；不复制其他购物 Skills 的提示词、代码、模板或文档。
- Runtime 不包含 MCP server、App、Hook、平台抓取脚本或数据库。
- 每个任务先建立可观察的失败，再做最小实现、验证并提交。

## 文件职责图

- `.codex-plugin/plugin.json`：插件身份、版本、公开描述、Skill 路径和 UI 元数据。
- `skills/shopping-decision/SKILL.md`：触发边界、五模式路由、公共工作流、参考文件加载规则和输出约定。
- `skills/shopping-decision/agents/openai.yaml`：Codex UI 名称、简述和默认提示；保留自动调用。
- `skills/shopping-decision/references/decision-modes.md`：五种模式的输入、关键判断和停止条件。
- `skills/shopping-decision/references/price-verification.md`：准确型号、证据分级、总成本、卖家和价格核验协议。
- `skills/shopping-decision/references/preference-profile.md`：偏好档案的开启、字段、优先级、复核、修改和删除规则。
- `skills/shopping-decision/references/monitoring.md`：监控前置条件、定时任务边界、通知格式和停止条件。
- `skills/shopping-decision/references/safety-boundaries.md`：高风险品类、敏感信息、禁止购买行为和失败降级。
- `skills/shopping-decision/assets/shopping-profile.example.md`：空值、可读、可复制的本地档案示例。
- `tests/routing-cases.json`：自动触发、显式触发、五模式选择和负向边界案例。
- `tests/content-contract.json`：运行时文件必须包含的关键结构和不变量。
- `tests/validate_fixtures.py`：使用 Python 标准库验证路由用例结构与覆盖面。
- `tests/validate_content.py`：验证文件存在、关键结构、引用路径和禁用词。
- `tests/behavior-cases/*.md`：需要在全新对话中人工观察的行为合同。
- `README.md`、`README.zh-CN.md`、`LICENSE`、`NOTICE`：安装、使用、开源和来源说明。

---

### 任务 1：建立可验证的插件外壳

**文件：**
- 创建：`.gitignore`
- 创建：`.codex-plugin/plugin.json`
- 创建：`LICENSE`
- 创建：`NOTICE`

**接口：**
- 输入：已批准设计文档和现有独立 Git 仓库。
- 输出：名称为 `shopping-decision-skill`、版本为 `0.1.0` 的有效插件外壳，供后续 Skill 文件填充。

- [ ] **步骤 1：验证缺少插件清单时会失败**

运行：

```powershell
& 'C:\Users\tian\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'C:\Users\tian\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py' 'C:\Users\tian\OneDrive\Desktop\work space\shopping-decision-skill'
```

预期：失败，并指出 `.codex-plugin/plugin.json` 不存在。

- [ ] **步骤 2：创建仓库忽略规则**

创建 `.gitignore`：

```gitignore
.superpowers/
.worktrees/
__pycache__/
*.pyc
.env
*.local.md
```

不要忽略设计文档、测试夹具或示例偏好档案。

- [ ] **步骤 3：创建插件清单**

创建 `.codex-plugin/plugin.json`：

```json
{
  "name": "shopping-decision-skill",
  "version": "0.1.0",
  "description": "Chinese-first personal shopping decisions for recommendations, comparisons, price verification, purchase timing, and authorized price monitoring.",
  "author": {
    "name": "fulinrenjian"
  },
  "license": "Apache-2.0",
  "keywords": ["shopping", "product-comparison", "price", "consumer", "chinese"],
  "skills": "./skills/",
  "interface": {
    "displayName": "购物决策",
    "shortDescription": "面向中国大陆消费者的商品推荐、对比与比价",
    "longDescription": "根据预算、使用场景、准确型号、总成本、卖家和售后证据，提供个人购物建议并支持经授权的降价监控。",
    "developerName": "fulinrenjian",
    "category": "Productivity",
    "capabilities": ["Interactive"],
    "defaultPrompt": [
      "使用 $shopping-decision：预算 3000 元，帮我推荐适合长辈使用的手机。",
      "使用 $shopping-decision：比较这两款商品，并告诉我现在是否值得买。",
      "使用 $shopping-decision：低于我的目标价时提醒我。"
    ],
    "brandColor": "#C85A3A"
  }
}
```

不得添加 `mcpServers`、`apps`、`hooks` 或需要额外权限的字段。

- [ ] **步骤 4：加入许可证和来源声明**

把 Apache License 2.0 标准全文写入 `LICENSE`。创建 `NOTICE`：

```text
Shopping Decision Skill
Copyright 2026 fulinrenjian and contributors

This project is an independent implementation of a personal shopping
decision workflow. It is not affiliated with, endorsed by, or derived from
any shopping platform, price-comparison service, or third-party Agent Skill.
Third-party names may appear in documentation only for factual ecosystem
reference and interoperability discussion.
```

- [ ] **步骤 5：验证插件外壳通过**

再次运行 `validate_plugin.py`。

预期：插件清单验证通过；没有不支持的能力字段。

- [ ] **步骤 6：提交**

```powershell
git add .gitignore .codex-plugin LICENSE NOTICE
git commit -m "chore: scaffold shopping decision plugin"
```

---

### 任务 2：建立结构化测试合同

**文件：**
- 创建：`tests/routing-cases.json`
- 创建：`tests/content-contract.json`
- 创建：`tests/validate_fixtures.py`
- 创建：`tests/validate_content.py`

**接口：**
- 输入：五个固定模式名称和全局约束。
- 输出：后续每个实现任务都能扩展并运行的零运行时依赖验证器。

- [ ] **步骤 1：先创建一个不完整的路由夹具**

创建 `tests/routing-cases.json`：

```json
{
  "schema_version": 1,
  "cases": [
    {
      "id": "invalid-missing-request",
      "should_trigger": true,
      "expected_mode": "recommend"
    }
  ]
}
```

- [ ] **步骤 2：创建夹具验证器并确认失败**

创建 `tests/validate_fixtures.py`：

```python
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "tests" / "routing-cases.json"
REQUIRED = {"id", "request", "invocation", "should_trigger", "expected_mode", "must_not", "rationale"}
MODES = {"recommend", "evaluate", "compare", "price-timing", "monitor", "none"}


def main() -> None:
    payload = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    assert payload["schema_version"] == 1
    cases = payload["cases"]
    assert cases, "cases must not be empty"
    ids: set[str] = set()
    covered: set[str] = set()
    has_positive = False
    has_negative = False
    has_explicit = False
    for case in cases:
        missing = REQUIRED - set(case)
        assert not missing, f"{case.get('id', '<unknown>')} missing {sorted(missing)}"
        assert case["id"] not in ids, f"duplicate id: {case['id']}"
        ids.add(case["id"])
        assert case["invocation"] in {"implicit", "explicit"}
        assert isinstance(case["should_trigger"], bool)
        assert case["expected_mode"] in MODES
        assert isinstance(case["must_not"], list)
        assert case["rationale"].strip()
        has_positive |= case["should_trigger"]
        has_negative |= not case["should_trigger"]
        has_explicit |= case["invocation"] == "explicit"
        if case["should_trigger"]:
            assert case["expected_mode"] != "none"
            covered.add(case["expected_mode"])
        else:
            assert case["expected_mode"] == "none"
    assert covered == MODES - {"none"}, f"missing modes: {sorted((MODES - {'none'}) - covered)}"
    assert has_positive and has_negative and has_explicit
    print(f"PASS: {len(cases)} routing cases")


if __name__ == "__main__":
    main()
```

运行：

```powershell
python tests/validate_fixtures.py
```

预期：失败，指出 `invalid-missing-request` 缺少 `request`、`invocation`、`must_not` 和 `rationale`。

- [ ] **步骤 3：替换为完整路由用例**

把 `routing-cases.json` 替换为以下十条实际案例：

```json
{
  "schema_version": 1,
  "cases": [
    {
      "id": "recommend-phone-for-parent",
      "request": "预算3000元，推荐一部字体大、续航好、适合长辈使用的手机。",
      "invocation": "implicit",
      "should_trigger": true,
      "expected_mode": "recommend",
      "must_not": ["seller-workflow"],
      "rationale": "预算、使用人群和购买目标明确。"
    },
    {
      "id": "evaluate-air-fryer",
      "request": "这款具体型号的空气炸锅值得买吗？我主要给两个人做饭。",
      "invocation": "implicit",
      "should_trigger": true,
      "expected_mode": "evaluate",
      "must_not": ["generic-explanation"],
      "rationale": "用户要评估一个具体商品是否适合。"
    },
    {
      "id": "compare-two-vacuums",
      "request": "追觅A型号和石头B型号哪个更适合有猫家庭？",
      "invocation": "implicit",
      "should_trigger": true,
      "expected_mode": "compare",
      "must_not": ["price-only"],
      "rationale": "用户要在两个具体候选之间进行场景化比较。"
    },
    {
      "id": "price-and-timing",
      "request": "这款耳机现在在哪里买比较便宜，还是等双十一？",
      "invocation": "implicit",
      "should_trigger": true,
      "expected_mode": "price-timing",
      "must_not": ["unverified-lowest-price"],
      "rationale": "核心问题是渠道总价和购买时机。"
    },
    {
      "id": "monitor-explicit",
      "request": "使用 $shopping-decision：这款16GB+512GB手机低于3500元时提醒我。",
      "invocation": "explicit",
      "should_trigger": true,
      "expected_mode": "monitor",
      "must_not": ["auto-purchase"],
      "rationale": "显式调用并明确提出降价监控。"
    },
    {
      "id": "negative-oled-explanation",
      "request": "OLED和LCD的发光原理有什么区别？",
      "invocation": "implicit",
      "should_trigger": false,
      "expected_mode": "none",
      "must_not": ["shopping-decision"],
      "rationale": "这是产品原理解释，不是购买决策。"
    },
    {
      "id": "negative-repair",
      "request": "我的电饭煲加热盘坏了，怎么拆开维修？",
      "invocation": "implicit",
      "should_trigger": false,
      "expected_mode": "none",
      "must_not": ["shopping-decision"],
      "rationale": "维修教程不在购物决策范围。"
    },
    {
      "id": "negative-seller-selection",
      "request": "帮我找适合在拼多多开店销售的高利润商品。",
      "invocation": "implicit",
      "should_trigger": false,
      "expected_mode": "none",
      "must_not": ["shopping-decision"],
      "rationale": "这是卖家选品。"
    },
    {
      "id": "negative-medical-device",
      "request": "根据我的症状直接推荐一台家用医疗器械并告诉我买哪款。",
      "invocation": "implicit",
      "should_trigger": false,
      "expected_mode": "none",
      "must_not": ["direct-medical-purchase"],
      "rationale": "医疗器械直接购买结论属于首版高风险排除范围。"
    },
    {
      "id": "negative-peer-used-phone",
      "request": "帮我判断这个个人卖家的二手手机能不能直接买。",
      "invocation": "implicit",
      "should_trigger": false,
      "expected_mode": "none",
      "must_not": ["peer-to-peer-approval"],
      "rationale": "个人对个人二手交易不在首版范围。"
    }
  ]
}
```

以上十条案例已经覆盖五种模式、自动触发、显式触发和五类负向边界；按该结构写入，不增加空案例或占位字段。

- [ ] **步骤 4：创建内容合同和验证器**

创建初始 `tests/content-contract.json`：

```json
{
  "schema_version": 1,
  "files": {}
}
```

创建 `tests/validate_content.py`：

```python
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "tests" / "content-contract.json"


def main() -> None:
    payload = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert payload["schema_version"] == 1
    for relative, rule in payload["files"].items():
        path = ROOT / relative
        assert path.is_file(), f"missing file: {relative}"
        text = path.read_text(encoding="utf-8")
        for required in rule.get("required", []):
            assert required in text, f"{relative} missing required text: {required}"
        for forbidden in rule.get("forbidden", []):
            assert forbidden not in text, f"{relative} contains forbidden text: {forbidden}"
    print(f"PASS: {len(payload['files'])} content contracts")


if __name__ == "__main__":
    main()
```

- [ ] **步骤 5：运行验证并提交**

```powershell
python tests/validate_fixtures.py
python tests/validate_content.py
git add tests
git commit -m "test: define shopping skill contracts"
```

预期：两个验证器均输出 `PASS`。

---

### 任务 3：实现 Skill 入口和 UI 元数据

**文件：**
- 创建：`skills/shopping-decision/SKILL.md`
- 创建：`skills/shopping-decision/agents/openai.yaml`
- 修改：`tests/content-contract.json`

**接口：**
- 输入：`routing-cases.json` 的五模式名称和负向边界。
- 输出：一个支持自动与显式触发、只加载相关参考文件的公开 Skill 入口。

- [ ] **步骤 1：先扩展内容合同并确认失败**

向 `content-contract.json` 的 `files` 添加：

```json
"skills/shopping-decision/SKILL.md": {
  "required": [
    "name: shopping-decision",
    "## 选择一个主要模式",
    "recommend",
    "evaluate",
    "compare",
    "price-timing",
    "monitor",
    "references/decision-modes.md",
    "references/price-verification.md",
    "references/preference-profile.md",
    "references/monitoring.md",
    "references/safety-boundaries.md"
  ],
  "forbidden": [
    "自动下单",
    "代替用户付款"
  ]
},
"skills/shopping-decision/agents/openai.yaml": {
  "required": [
    "display_name: 购物决策",
    "short_description:",
    "$shopping-decision"
  ],
  "forbidden": [
    "allow_implicit_invocation: false"
  ]
}
```

运行 `python tests/validate_content.py`。

预期：失败，指出 `skills/shopping-decision/SKILL.md` 不存在。

- [ ] **步骤 2：创建 `SKILL.md` frontmatter 和路由骨架**

使用以下 frontmatter：

```yaml
---
name: shopping-decision
description: Use for personal shopping decisions in mainland China when a user wants product recommendations, evaluation of a specific product, comparison between products, current price and purchase-timing analysis, or explicitly requested price-drop monitoring. Also supports direct invocation with $shopping-decision. Do not use for generic product explanations, repairs, after-sales disputes, seller-side e-commerce, peer-to-peer used goods, or direct purchase conclusions for medical, financial, real-estate, whole-vehicle, or travel products. 当用户需要个人购物推荐、单品值不值得买、多商品比较、比价、购买时机判断或明确要求降价监控时使用。
---
```

正文必须包含：

```markdown
# 个人购物决策

只帮助用户做购买决定；不登录、不操作购物车、不结算、不下单、不付款。

## 选择一个主要模式

| 模式 | 触发信号 | 读取资料 |
| --- | --- | --- |
| `recommend` | 按预算、用途或人群推荐候选 | `references/decision-modes.md` |
| `evaluate` | 判断一个准确商品是否适合、是否值得买 | `references/decision-modes.md`、`references/price-verification.md` |
| `compare` | 比较两个或多个准确商品 | `references/decision-modes.md`、`references/price-verification.md` |
| `price-timing` | 查询渠道总价、历史价或现在是否该买 | `references/price-verification.md` |
| `monitor` | 用户明确要求持续关注或降价提醒 | `references/monitoring.md`、`references/price-verification.md` |

一次只确定一个主要模式。需要价格证据时可以补读价格核验资料，不再触发第二个 Skill。

## 公共工作流

1. 读取本次预算、用途、硬性条件和准确商品信息。
2. 只有已启用且与本次任务相关时，才按 `references/preference-profile.md` 读取本地偏好档案。
3. 只询问会改变推荐结果的缺失信息。
4. 搜索前锁定品牌、型号、代际、容量、尺寸、套装、成色和卖家类型。
5. 通过当前可用的网页搜索或浏览器收集公开证据；不要求账号、Cookie 或 API Key。
6. 按证据强度给出结论，并明确覆盖缺口和未核验事项。

## 必须停止或转交的情况

遇到敏感信息、购买操作、高风险品类、个人对个人二手交易或售后纠纷时，读取 `references/safety-boundaries.md` 并遵守其停止条件。

## 默认输出

先给结论，再说明匹配原因、关键差异、价格与渠道证据、风险和下一步。简单商品保持简洁；昂贵或复杂商品才展开完整对比。
```

- [ ] **步骤 3：创建 UI 元数据**

创建 `agents/openai.yaml`：

```yaml
interface:
  display_name: 购物决策
  short_description: 面向中国大陆消费者的商品推荐、对比、比价与降价监控
  default_prompt: 使用 $shopping-decision：根据我的预算和用途推荐商品，并核验关键价格与风险。
```

不要设置 `allow_implicit_invocation: false`。

- [ ] **步骤 4：验证入口**

```powershell
python tests/validate_content.py
& 'C:\Users\tian\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'C:\Users\tian\.codex\skills\.system\skill-creator\scripts\quick_validate.py' 'C:\Users\tian\OneDrive\Desktop\work space\shopping-decision-skill\skills\shopping-decision'
```

预期：内容合同和 Skill 快速验证均通过。

- [ ] **步骤 5：提交**

```powershell
git add skills/shopping-decision tests/content-contract.json
git commit -m "feat: add shopping decision router"
```

---

### 任务 4：实现决策模式和价格核验

**文件：**
- 创建：`skills/shopping-decision/references/decision-modes.md`
- 创建：`skills/shopping-decision/references/price-verification.md`
- 修改：`tests/content-contract.json`
- 创建：`tests/behavior-cases/decision-and-price.md`

**接口：**
- 输入：`SKILL.md` 选择出的主要模式、用户本次约束和公开网页证据。
- 输出：模式专用步骤、准确商品标识、证据等级、总成本和带时间戳价格结论。

- [ ] **步骤 1：增加失败内容合同**

为两个参考文件增加合同：

```json
"skills/shopping-decision/references/decision-modes.md": {
  "required": ["## recommend", "## evaluate", "## compare", "## price-timing", "## monitor", "停止条件"],
  "forbidden": ["统一综合评分"]
},
"skills/shopping-decision/references/price-verification.md": {
  "required": ["准确版本", "A级", "B级", "C级", "D级", "总成本", "查询时间", "卖家类型", "覆盖缺口"],
  "forbidden": ["搜索摘要就是最低价", "无法访问时猜测价格"]
}
```

运行内容验证，预期因文件缺失而失败。

- [ ] **步骤 2：编写五模式合同**

`decision-modes.md` 的每个模式都必须明确：

```markdown
## recommend
- 必要输入：预算、用途、硬性条件。
- 核心动作：先硬筛，再保留 2 至 4 个真正不同的候选。
- 输出：首选、备选、各自适用人群和仍需确认的信息。
- 停止条件：预算或硬性条件缺失且会改变候选范围时，只问一个合并问题。
```

其余模式采用同样字段，但必须落实以下差异：

- `evaluate`：先确认准确版本和卖家，再判断适配性与购买风险。
- `compare`：只比较同一购买问题下可替代的准确候选；版本不一致时先拆分。
- `price-timing`：区分无条件价、条件优惠和历史参考；不能根据促销日名称推断必然降价。
- `monitor`：只负责确认监控合同并转入 `monitoring.md`，不在此处创建定时任务。

- [ ] **步骤 3：编写价格核验协议**

`price-verification.md` 必须定义：

```markdown
## 商品身份键
`品牌 | 型号 | 代际 | 容量/尺寸 | 套装 | 成色 | 卖家`

## 已核验价格最小字段
- `variant_key`
- `seller_name`
- `seller_type`: `brand-official`、`platform-self-operated`、`marketplace-third-party`
- `stock_state`
- `base_price`
- `conditional_discount`
- `shipping_cost`
- `verified_total`
- `observed_at`
- `source`
- `evidence_grade`
```

同时写清 A 至 D 级证据、总成本计算、条件优惠拆分、价格冲突重查、平台覆盖缺口和“无法核验时降低结论强度”的规则。

- [ ] **步骤 4：编写行为合同**

`tests/behavior-cases/decision-and-price.md` 至少包含三个全新对话案例：

1. 不同容量手机不能合并比价。
2. 搜索摘要中的促销价不能被称为实时最低价。
3. 简单日用品推荐不应输出冗长研究报告。

每个案例记录：调用方式、用户请求、必须行为、禁止行为、停止条件、无 Skill 基线观察和启用 Skill 后观察。

- [ ] **步骤 5：验证并提交**

```powershell
python tests/validate_content.py
python tests/validate_fixtures.py
git diff --check
git add skills/shopping-decision/references tests
git commit -m "feat: add shopping decision and price protocols"
```

---

### 任务 5：实现偏好档案、安全边界和降价监控

**文件：**
- 创建：`skills/shopping-decision/references/preference-profile.md`
- 创建：`skills/shopping-decision/references/monitoring.md`
- 创建：`skills/shopping-decision/references/safety-boundaries.md`
- 创建：`skills/shopping-decision/assets/shopping-profile.example.md`
- 修改：`tests/content-contract.json`
- 创建：`tests/behavior-cases/privacy-and-monitoring.md`

**接口：**
- 输入：用户对档案或监控的明确请求，以及当前购物任务。
- 输出：用户控制的偏好读写合同、安全停止条件和可撤销的监控定义；不输出购买动作。

- [ ] **步骤 1：增加失败内容合同**

为三个参考文件和示例档案增加必需内容：

```json
"skills/shopping-decision/references/preference-profile.md": {
  "required": ["默认关闭", "创建前确认", "修改前确认", "删除前确认", "当前对话优先", "最后确认日期"],
  "forbidden": ["自动记录购买历史", "保存完整地址", "保存账号密码"]
},
"skills/shopping-decision/references/monitoring.md": {
  "required": ["明确授权", "准确版本", "目标价格", "检查频率", "结束日期", "不得自动下单"],
  "forbidden": ["无限期监控", "默认购买"]
},
"skills/shopping-decision/references/safety-boundaries.md": {
  "required": ["敏感信息", "高风险品类", "个人对个人二手交易", "官方翻新", "停止"],
  "forbidden": ["代填支付信息"]
},
"skills/shopping-decision/assets/shopping-profile.example.md": {
  "required": ["schema_version: 1", "region: null", "preferred: []", "excluded: []", "updated_at: null"],
  "forbidden": ["password:", "payment:", "full_address:"]
}
```

运行内容验证，预期因文件缺失而失败。

- [ ] **步骤 2：实现偏好档案规则**

`preference-profile.md` 必须规定：

- 默认关闭；用户主动开启并选择本地路径。
- 创建、修改和删除分别确认，不能把一次购买自动永久化。
- 允许字段：地区到省市、品类预算、品牌和平台偏好、官方翻新接受度、第三方卖家接受度、决策权重、用户主动保存的尺码信息、最后确认日期。
- 禁止字段：账号、密码、Token、支付数据、完整地址、身份证明、完整浏览或购买历史、后台推断的敏感信息。
- 当前对话覆盖档案默认值；昂贵购买使用长期未确认偏好前先复核。

- [ ] **步骤 3：创建空值示例档案**

`shopping-profile.example.md` 使用真实可解析但不含个人数据的 YAML frontmatter：

```markdown
---
schema_version: 1
updated_at: null
region: null
category_budgets: {}
brands:
  preferred: []
  excluded: []
marketplaces:
  preferred: []
  excluded: []
seller_policy:
  official_or_self_operated_only: false
  allow_official_refurbished: false
  allow_marketplace_third_party: false
priorities:
  price: null
  performance: null
  reliability: null
  after_sales: null
  appearance: null
  portability: null
size_and_fit: {}
preference_confirmed_at: {}
---

# 本地购物偏好档案

只有在你明确开启后，购物决策 Skill 才能读取或建议修改本文件。不要在这里填写账号、密码、支付信息、身份证件号码或完整地址。
```

- [ ] **步骤 4：实现监控合同**

`monitoring.md` 必须要求完整监控定义：

```text
product_variant
target_condition
eligible_platforms
eligible_seller_types
check_frequency
end_date
notification_fields
```

当环境支持定时任务时，使用环境提供的原生定时机制；不输出自制原始调度指令。创建前向用户复述完整条件并取得确认。可以建议 30 天，但不能默认采用。通知必须含价格、库存、卖家类型、查询时间、来源和是否满足全部条件。停止、删除和修改监控也必须可由用户控制。

- [ ] **步骤 5：实现安全停止边界**

`safety-boundaries.md` 必须区分：

- 可以继续：普通实物商品、可核验的官方翻新商品、公开信息整理。
- 只能做信息整理和风险提示：药品、医疗器械、金融产品、房产、汽车整车、旅游预订。
- 必须退出购买结论：个人对个人二手交易、需要敏感凭据、要求登录或付款、售后法律纠纷。

- [ ] **步骤 6：编写行为合同、验证并提交**

`privacy-and-monitoring.md` 至少覆盖：未经同意不创建档案、当前预算覆盖历史偏好、监控缺少结束日期时只询问缺失条件、满足目标价也不自动下单、高风险品类退出。

运行：

```powershell
python tests/validate_content.py
git diff --check
git add skills/shopping-decision tests
git commit -m "feat: add shopping privacy and monitoring safeguards"
```

---

### 任务 6：补全触发和行为评估集

**文件：**
- 创建：`tests/behavior-cases/README.md`
- 创建：`tests/behavior-cases/routing.md`
- 修改：`tests/routing-cases.json`

**接口：**
- 输入：已实现的 Skill 和参考模块。
- 输出：覆盖触发、误触发、五模式、证据、隐私、监控和停止边界的可复现实验集。

- [ ] **步骤 1：定义统一行为案例格式**

创建 `tests/behavior-cases/README.md`：

```markdown
# 行为案例格式

每个案例必须记录：

1. 调用方式：自动或 `$shopping-decision` 显式调用。
2. 在全新对话中使用的用户请求。
3. 必须观察到的行为。
4. 禁止出现的行为。
5. 停止条件。
6. 未启用 Skill 的基线观察。
7. 启用 Skill 后的观察。

评价行为、证据和边界，不比较固定措辞。每次测试都使用全新对话，避免先前案例或期望答案污染结果。
```

- [ ] **步骤 2：补齐路由案例**

保留任务 2 的十条基础案例，再添加以下两条显式调用案例：

```json
{
  "id": "explicit-recommend-laptop",
  "request": "使用 $shopping-decision：预算6000元，推荐适合出差和写代码的轻薄本。",
  "invocation": "explicit",
  "should_trigger": true,
  "expected_mode": "recommend",
  "must_not": ["seller-workflow"],
  "rationale": "显式调用，目标是按预算和使用场景推荐商品。"
},
{
  "id": "explicit-compare-routers",
  "request": "使用 $shopping-decision：比较这三款路由器，但先确认是不是同一规格。",
  "invocation": "explicit",
  "should_trigger": true,
  "expected_mode": "compare",
  "must_not": ["merge-mismatched-variants"],
  "rationale": "显式调用，且用户要求先执行商品身份核对。"
}
```

每条案例保留 `id`、`request`、`invocation`、`should_trigger`、`expected_mode`、`must_not`、`rationale` 七个字段。添加后共有十二条路由案例。

- [ ] **步骤 3：编写路由行为合同**

`routing.md` 至少包含以下全新对话请求：

```text
预算800元，推荐适合租房使用的小型洗衣机。
这款显示器的HDR原理是什么？
使用 $shopping-decision：比较这三款路由器，但先确认是不是同一规格。
帮我找适合在抖音商城销售的爆款商品。
官方翻新的这款平板是否值得买？
帮我直接判断闲鱼个人卖家的这台电脑能不能付款。
```

- [ ] **步骤 4：运行自动验证并进行小规模人工前测**

```powershell
python tests/validate_fixtures.py
python tests/validate_content.py
```

然后在全新 Codex 对话中抽测一条正向、一条负向、一条价格证据和一条监控案例，记录实际观察。预期：四条案例都满足必须行为且不出现禁止行为；发现偏差时只修改能够解释该偏差的最小规则。

- [ ] **步骤 5：提交**

```powershell
git add tests
git commit -m "test: add shopping decision behavior suite"
```

---

### 任务 7：完成中英文开源文档

**文件：**
- 创建：`README.md`
- 创建：`README.zh-CN.md`
- 修改：`tests/content-contract.json`

**接口：**
- 输入：完成的 Skill 结构、调用方式、安全边界和开源政策。
- 输出：可以被普通 Codex 用户理解、安装和安全使用的公开说明。

- [ ] **步骤 1：增加文档内容合同并确认失败**

增加：

```json
"README.md": {
  "required": ["Shopping Decision Skill", "README.zh-CN.md", "$shopping-decision", "Apache-2.0", "does not log in", "does not purchase"],
  "forbidden": ["official partner", "guaranteed lowest price"]
},
"README.zh-CN.md": {
  "required": ["个人购物决策", "$shopping-decision", "自动触发", "降价监控", "Apache-2.0", "不登录", "不下单", "来源"],
  "forbidden": ["保证全网最低价", "自动付款"]
}
```

运行内容验证，预期因 README 缺失而失败。

- [ ] **步骤 2：编写中文说明**

`README.zh-CN.md` 按以下顺序编写：

1. 一句话定位和适用人群。
2. 五种能力及不支持的范围。
3. 自动触发和显式调用示例。
4. GitHub 直接安装和 Codex 插件安装说明。
5. 本地偏好档案的开启、数据字段和删除方式。
6. 降价监控所需条件和通知内容。
7. 价格证据、时间戳和覆盖缺口说明。
8. 隐私与不购买边界。
9. 测试命令。
10. 许可证、来源和独立实现声明。

GitHub 直接安装示例使用预期仓库地址：

```powershell
python "$HOME/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py" --repo fulinrenjian/shopping-decision-skill --path skills/shopping-decision --method git
```

明确说明：仓库尚未推送前，该命令只作为发布后的安装格式。

- [ ] **步骤 3：编写英文说明**

`README.md` 与中文说明保持功能、限制、安装方式和许可证一致，顶部提供 `[简体中文](README.zh-CN.md)` 链接。英文版不得增加中文版本未承诺的平台覆盖或自动购买能力。

- [ ] **步骤 4：验证并提交**

```powershell
python tests/validate_content.py
git diff --check
git add README.md README.zh-CN.md tests/content-contract.json
git commit -m "docs: add shopping skill usage guides"
```

---

### 任务 8：完整验证、隔离安装检查和发布准备

**文件：**
- 修改：仅修改前面验证暴露出的最小问题。
- 检查：全部运行时、测试和文档文件。

**接口：**
- 输入：任务 1 至 7 的全部产物。
- 输出：结构通过、行为合同完整、无敏感信息、工作区干净的 0.1.0 候选版本。

- [ ] **步骤 1：运行所有静态验证**

```powershell
python tests/validate_fixtures.py
python tests/validate_content.py
& 'C:\Users\tian\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'C:\Users\tian\.codex\skills\.system\skill-creator\scripts\quick_validate.py' 'C:\Users\tian\OneDrive\Desktop\work space\shopping-decision-skill\skills\shopping-decision'
& 'C:\Users\tian\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'C:\Users\tian\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py' 'C:\Users\tian\OneDrive\Desktop\work space\shopping-decision-skill'
git diff --check
```

预期：全部通过，`git diff --check` 无输出。

- [ ] **步骤 2：执行敏感信息与边界扫描**

```powershell
rg -n -i "password|secret|api[_-]?key|cookie|token|银行卡|身份证|完整地址" . -g '!docs/superpowers/**' -g '!tests/**'
```

逐条检查命中：只允许安全说明、禁止字段名和示例空值；不得包含真实凭据或用户数据。

- [ ] **步骤 3：隔离复制并验证安装形态**

```powershell
$installProbe = Join-Path ([System.IO.Path]::GetTempPath()) ('shopping-decision-install-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Force -Path $installProbe
Copy-Item -Recurse -LiteralPath 'skills\shopping-decision' -Destination $installProbe
& 'C:\Users\tian\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'C:\Users\tian\.codex\skills\.system\skill-creator\scripts\quick_validate.py' (Join-Path $installProbe 'shopping-decision')
```

预期：隔离副本通过验证，且不依赖仓库外文件。

- [ ] **步骤 4：执行完整行为前测**

在全新对话中运行所有 `tests/behavior-cases/*.md` 案例。对每个案例记录基线与启用 Skill 后的观察。验收条件：

- 正向请求选择正确模式。
- 负向请求不误触发。
- 没有可靠证据时不编造价格。
- 偏好和监控操作均在授权边界内。
- 所有回答停在购物建议，不发生购买动作。

- [ ] **步骤 5：核对版本和发布状态**

```powershell
git status --short --branch
git log --oneline --decorate -10
```

确认 `.codex-plugin/plugin.json` 版本为 `0.1.0`，工作区没有未提交文件，README 不声称仓库已经发布或保证最低价。

- [ ] **步骤 6：提交最终修正**

只有前述验证产生必要修正时才创建此提交：

```powershell
git add .
git commit -m "test: verify shopping decision release"
```

如果没有文件变化，不创建空提交。不要在此任务中创建 GitHub 远程、推送仓库或发布 Release；这些外部操作必须由用户另行明确授权。
