# Shopping Decision Skill

[简体中文](README.zh-CN.md)

A Codex Skill for personal consumers in mainland China that turns “what should I buy, is this worthwhile, how do these compare, when should I buy, and should I watch the price?” into explainable, publicly verifiable guidance based on budget, use case, and evidence.

## 1. Positioning and audience

This Codex Skill is for personal consumers in mainland China who want explainable, publicly verifiable help deciding what to buy, whether it is worthwhile, how items compare, when to buy, or whether to watch a price.

## 2. Five capabilities and unsupported scope

The Skill selects one primary mode per request:

| Mode | Purpose |
| --- | --- |
| `recommend` | Recommend 2–4 candidates from a budget, use case, and hard constraints |
| `evaluate` | Assess whether one exact product and seller fit the user |
| `compare` | Compare exact products that can substitute for one another |
| `price-timing` | Verify current total cost, use historical references, and offer conditional timing guidance |
| `monitor` | Set up a price-monitoring contract after complete authorization |

It does not handle generic product explainers, repairs, after-sales disputes, seller-side e-commerce, or peer-to-peer used transactions. For medicines, medical devices, financial products, real estate, whole vehicles, and travel bookings, it only organizes public information and risks; it does not give a purchase conclusion. It does not guarantee the lowest price across the web, and it does not treat search snippets or marketing pages as verified prices.

## 3. Automatic and explicit invocation

The Skill can trigger automatically when a conversation clearly asks for recommendations, whether a particular item is worthwhile, product comparison, current prices or purchase timing, or ongoing price watching. It can also be called explicitly:

```text
$shopping-decision: Recommend a phone for an older family member with a CNY 3,000 budget.
$shopping-decision: Compare these two products and tell me whether buying now makes sense.
$shopping-decision: Notify me if the total cost falls below my target.
```

Automatic invocation and explicit `$shopping-decision` invocation follow the same boundaries; each task has exactly one primary mode.

## 4. Installation

### Install the Skill directly

After this repository is pushed and published, use this GitHub installation format:

```powershell
python "$HOME/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py" --repo fulinrenjian/shopping-decision-skill --path skills/shopping-decision --method git
```

Before the repository has been pushed, this command does not work; it is only the post-publication installation format. Start a new Codex conversation after installation to use automatic triggering or `$shopping-decision`.

### Install as a Codex plugin

The repository includes `.codex-plugin/plugin.json` and can be published as a Codex plugin package. After publication, add the GitHub repository through Codex plugin management (or add it to your personal plugin marketplace first), then enable `shopping-decision-skill`. Codex’s plugin-management flow handles the plugin installation path; the direct Skill command above does not publish or install the plugin.

## 5. Local preference profile

The preference profile is opt-in and off by default. It is created or read only after you select a local path and confirm. It may contain only province/city-level region, category budgets, preferred or excluded brands/platforms, acceptance of verifiable official refurbishment or third-party sellers, decision weights, user-saved sizing/fit information, and a last-confirmed date for each preference.

Creation, changes, and deletion all show the path or field scope first and require confirmation; information in the current conversation takes precedence. You may ask to delete selected fields or the entire local profile at any time, with a final confirmation before deletion. The Skill does not automatically record browsing or purchase history, and it does not store account credentials, tokens, payment data, identity documents, precise addresses, or full addresses.

## 6. Price monitoring

Price monitoring requires your explicit authorization and confirmation of all seven fields before creation: exact product variant, target condition (including target price), eligible platforms, eligible seller types, check frequency, end date, and notification fields. If any field is missing, monitoring is not created or continued.

Only when the complete conditions are confirmed and the environment supports it may the Skill use the environment’s native scheduling/automation mechanism; this repository contains no scheduler scripts or substitute scheduling text. A notification includes at least price, stock, seller type, observed time, source, and whether every condition is met. Monitoring stops at the end date, when authorization is withdrawn, or when conditions become incomplete. It does not log in, add to cart, check out, place orders, or make payments.

## 7. Price evidence and coverage

Price verification first locks the brand, model, generation, capacity/size, bundle, condition, and seller. Each verified record identifies seller type, stock, base price, conditional discounts, shipping, total cost, evidence grade, source, and an observed timestamp in China Standard Time. Only publicly reviewable, no-login A/B-grade pages support a current-price or total-cost conclusion; historical prices are reference only.

The output names coverage gaps such as unvisited channels, login walls, regional differences, unavailable stock/shipping data, unverified discount eligibility, non-comparable variants, and time differences. Conclusions therefore apply only to the verified channels and pages, never to the whole web.

## 8. Privacy and no-purchase boundary

The Skill supports decisions only: it does not log in, operate a cart, check out, place orders, make payments, and does not purchase. It does not request or handle sensitive credentials. It stops a purchase assessment and offers a safe next step when a request needs login, payment, ordering, a peer-to-peer used transaction, after-sales dispute, or legal dispute. High-risk categories receive only public-information organization and risk guidance.

## 9. Tests

From the repository root, run:

```powershell
python tests/validate_content.py
python tests/validate_fixtures.py
git diff --check
```

## 10. License, sources, and independent implementation

This project is released under [Apache-2.0](LICENSE); see [LICENSE](LICENSE) and [NOTICE](NOTICE). Its sources are the public Skill, reference materials, and tests in this repository. It is an independent implementation: it is not affiliated with, endorsed by, or derived from any shopping platform, price-comparison service, or third-party Agent Skill. Third-party names appear only for factual ecosystem and interoperability discussion.
