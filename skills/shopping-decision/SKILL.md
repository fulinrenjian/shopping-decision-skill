---
name: shopping-decision
description: Use for personal shopping decisions in mainland China when a user wants product recommendations, evaluation of a specific product, comparison between products, current price and purchase-timing analysis, or explicitly requested price-drop monitoring. Also supports direct invocation with $shopping-decision. Do not use for generic product explanations, repairs, after-sales disputes, seller-side e-commerce, peer-to-peer used goods, or direct purchase conclusions for medical, financial, real-estate, whole-vehicle, or travel products. 当用户需要个人购物推荐、单品值不值得买、多商品比较、比价、购买时机判断或明确要求降价监控时使用。
---

# 个人购物决策

只帮助用户做购买决定；不登录、不操作购物车、不结算、不下单、不付款。

## 选择一个主要模式

| 模式 | 触发信号 | 读取资料 |
| --- | --- | --- |
| `recommend` | 按预算、用途或人群推荐候选 | `references/decision-modes.md` |
| `evaluate` | 判断一个准确商品是否适合、是否值得买 | `references/decision-modes.md`、`references/price-verification.md` |
| `compare` | 比较两个或多个准确商品 | `references/decision-modes.md`、`references/price-verification.md` |
| `price-timing` | 查询渠道总价、历史价或现在是否该买 | `references/decision-modes.md`、`references/price-verification.md` |
| `monitor` | 用户明确要求持续关注或降价提醒 | `references/decision-modes.md`、`references/monitoring.md`、`references/price-verification.md` |

一次只确定一个主要模式。需要价格证据时可以补读价格核验资料，不再触发第二个 Skill。

## 公共工作流

1. 读取本次预算、用途、硬性条件和准确商品信息。
2. 只有已启用且与本次任务相关时，才按 `references/preference-profile.md` 读取本地偏好档案。
3. 只询问会改变推荐结果的缺失信息。
4. 搜索前锁定品牌、型号、代际、容量、尺寸、会影响价格的颜色、套装、成色和卖家类型；监控复用这一准确变体，不能把颜色不同的商品当作同一监控对象。
5. 通过当前可用的网页搜索或浏览器收集公开证据；不要求账号、Cookie 或 API Key。
6. 按证据强度给出结论，并明确覆盖缺口和未核验事项。

## 必须停止或转交的情况

遇到敏感信息、购买操作、高风险品类、个人对个人二手交易或售后纠纷时，读取 `references/safety-boundaries.md` 并遵守其停止条件。

## 默认输出

先给结论，再说明匹配原因、关键差异、价格与渠道证据、风险和下一步。简单商品保持简洁；昂贵或复杂商品才展开完整对比。
