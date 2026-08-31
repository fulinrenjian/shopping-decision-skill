# Shopping Decision Skill Design

Date: 2026-08-31  
Status: Approved design  
Initial version target: 0.1.0

## 1. Purpose

`shopping-decision` is a Chinese-first Codex Skill for personal shopping decisions in mainland China. It helps ordinary consumers choose products, evaluate a specific product, compare alternatives, verify current prices, judge purchase timing, and create an explicitly requested price-drop monitor.

The Skill is designed for open-source distribution. It must remain useful without mandatory paid services, platform credentials, or third-party API keys.

## 2. Goals

- Support automatic activation for clear shopping-decision requests and explicit invocation through `$shopping-decision`.
- Focus on mainland Chinese retail channels, initially including Taobao/Tmall, JD, Pinduoduo, Douyin Mall, and Vipshop where publicly accessible evidence is available.
- Produce recommendations grounded in the user's budget, use case, hard constraints, total cost, seller quality, after-sales support, and evidence confidence.
- Distinguish exact variants, capacities, bundles, conditions, and seller types before comparing products or prices.
- Support an optional, user-controlled local preference profile without silently collecting personal data.
- Support price-drop monitoring only after the user explicitly requests and confirms it.
- Keep token use proportionate through one public Skill entry point and progressive disclosure of mode-specific references.
- Be independently authored and suitable for publication under Apache-2.0.

## 3. Non-goals

Version 0.1.0 will not:

- Operate an e-commerce store, perform seller-side sourcing, write listings, or manage advertising.
- Log in to a marketplace, manage carts, place orders, submit personal information, or make payments.
- Require or bundle a scraper, database, browser extension, paid API, marketplace account, cookie, or credential.
- Promise complete platform coverage when pages are login-gated, blocked, stale, or unavailable.
- Give direct purchase conclusions for medicine, medical devices, financial products, real estate, whole vehicles, travel bookings, or peer-to-peer second-hand transactions. It may organize information and surface risk boundaries for these categories. Official refurbished products may remain in scope when the seller, condition, warranty, and return terms can be verified.
- Handle repair tutorials, legal disputes, after-sales arbitration, or generic product-technology explanations unless they are necessary to an active purchase decision.
- Persist full browsing history, purchase history, precise addresses, payment data, account credentials, or inferred sensitive traits.

## 4. Repository and Package Structure

The project will be a standalone Git repository named `shopping-decision-skill`.

```text
shopping-decision-skill/
|-- .codex-plugin/
|   `-- plugin.json
|-- skills/
|   `-- shopping-decision/
|       |-- SKILL.md
|       |-- agents/
|       |   `-- openai.yaml
|       |-- references/
|       |   |-- decision-modes.md
|       |   |-- price-verification.md
|       |   |-- monitoring.md
|       |   |-- preference-profile.md
|       |   `-- safety-boundaries.md
|       `-- assets/
|           `-- shopping-profile.example.md
|-- tests/
|   `-- behavior-cases/
|-- README.md
|-- README.zh-CN.md
|-- LICENSE
`-- NOTICE
```

`SKILL.md` will contain only shared routing, essential invariants, and reference-loading rules. Detailed instructions will be loaded only for the active shopping mode. The initial release will not include executable shopping or scraping scripts.

## 5. Activation and Routing

### 5.1 Automatic activation

The Skill should activate when the user clearly requests a personal purchase decision, including requests to:

- Recommend a product within a budget or use case.
- Decide whether a specific product is suitable or worth buying.
- Compare two or more concrete products.
- Find where a specific product is cheaper.
- Decide whether to buy now or wait.
- Monitor a product for a target price or price drop.

### 5.2 Explicit activation

The Skill must also support `$shopping-decision` followed by a shopping request.

### 5.3 Exclusions

The description and body must avoid attracting generic product explanations, repairs, seller-side e-commerce work, after-sales disputes, or high-risk purchase categories outside the supported scope.

### 5.4 Internal modes

The router selects one primary mode:

1. `recommend`: Generate a short list that fits the user's requirements.
2. `evaluate`: Assess one exact product and purchase context.
3. `compare`: Compare multiple exact products on decision-relevant dimensions.
4. `price-timing`: Verify channel costs and assess whether to buy now or wait.
5. `monitor`: Define and create an explicitly authorized price-drop monitor.

A request may use supporting rules from another mode without creating another public Skill. For example, a comparison may load price-verification rules while remaining a `compare` task.

## 6. Decision Workflow

The shared workflow is:

1. Identify the purchase goal and primary mode.
2. Read current-turn requirements and, only if enabled, the user-controlled preference profile.
3. Ask only for missing information that can materially change the recommendation.
4. Pin the exact product identity: brand, model, generation, capacity, size, color when price-relevant, bundle, condition, and seller type.
5. Collect current public evidence using available web search and browser capabilities.
6. Verify product facts, price, stock, shipping, discounts, warranty, return terms, and seller identity as far as accessible.
7. Apply hard constraints before comparing softer preferences.
8. Compare total acquisition and ownership cost rather than headline price alone.
9. Surface quality, after-sales, compatibility, counterfeit, return, and evidence risks.
10. Produce a conclusion calibrated to the strength and completeness of the evidence.
11. Offer monitoring only when it would serve the request; create it only after explicit user authorization.

## 7. Evidence and Price Verification

### 7.1 Evidence grades

- Grade A: Manufacturer pages, current marketplace product pages, official flagship stores, and first-party/self-operated retailer pages.
- Grade B: Authoritative reviews, certification records, official manuals, and official after-sales policies.
- Grade C: Corroborated user reviews, forums, and credible long-term ownership reports.
- Grade D: Search snippets, comparison sites, marketing articles, inaccessible pages, and uncorroborated claims. These are leads, not decisive evidence.

### 7.2 Price requirements

A price may be presented as verified only when the response can identify:

- The exact product variant.
- The seller or store type.
- In-stock or applicable availability state.
- The observation time and timezone.
- The source page or traceable source.

Search snippets and promotional claims must not be described as the verified lowest price. Discounts that require cart, membership, trade-in, financing, livestream participation, coupon collection, or uncertain cashback must be separated from an unconditional price.

### 7.3 Total cost

Where relevant, comparisons should account for product price, shipping, required accessories or consumables, warranty, likely maintenance, and clearly applicable discounts. The Skill must not manufacture precision when taxes, regional subsidies, membership terms, or checkout-only discounts are unknown.

### 7.4 Recommendation strength

The Skill will use hard filters and category-specific decision criteria rather than a universal numeric score. It should not invent a precise score that implies unsupported measurement. Missing or conflicting evidence must weaken the conclusion and appear in the final answer.

## 8. Default Output Contract

Outputs scale with purchase complexity and cost. A simple request should stay concise; an expensive or technically complex purchase may use the full structure:

1. Conclusion: recommended option and the main reason.
2. Fit: why it matches the user's stated requirements.
3. Alternatives: material differences, trade-offs, and best-fit user for each.
4. Price and channel evidence: exact variant, store type, total price when calculable, stock, observation time, and source.
5. Risks and uncertainty: unresolved facts, seller or after-sales concerns, and checkout items the user must confirm.
6. Next action: buy now, wait, choose another variant, inspect in person, or set a price monitor.

The Skill must not fill tables with irrelevant specifications or declare a winner solely because it has the highest specifications.

## 9. Optional Local Preference Profile

### 9.1 Default behavior

The Skill uses the current conversation by default and does not create persistent memory automatically.

### 9.2 Opt-in behavior

The user may explicitly enable a local preference profile in a user-controlled location outside the installed Skill directory. Creation, modification, and deletion require confirmation. The example asset documents a portable schema rather than containing real user data.

### 9.3 Allowed fields

The profile may include:

- Typical budget ranges by category.
- Province or city, without a full address.
- Preferred or excluded brands and marketplaces.
- Acceptance of official refurbished products or third-party marketplace sellers. Peer-to-peer used-goods transactions remain outside the initial scope.
- Relative preference for price, performance, reliability, after-sales support, appearance, or portability.
- User-provided size or fit information when they explicitly choose to store it.
- A last-confirmed date for each preference.

### 9.4 Prohibited fields

The profile must not contain account passwords, tokens, payment data, government identifiers, full addresses, or silently inferred sensitive information. It must not become a comprehensive browsing or purchase-history database.

### 9.5 Precedence and freshness

Current-turn requirements override profile defaults. Stale preferences should be re-confirmed before materially influencing an expensive purchase.

## 10. Price-drop Monitoring

Monitoring is an explicit, separate action. Before creating a monitor, the Skill must confirm:

- Exact product and variant.
- Target price or qualifying drop condition.
- Eligible platforms or store types.
- Whether only official or self-operated sellers qualify.
- Check frequency.
- End date.

When the current Codex environment provides recurring automations, the Skill may create a manageable scheduled monitor after authorization. Otherwise, it should provide a manual monitoring plan. A 30-day duration may be suggested but must not be assumed without confirmation.

A notification must include the verified price, stock state, seller type, observation time, source, and whether every user condition was met. Uncertain coupon, cashback, membership, or checkout-only claims must not silently satisfy the target.

Monitoring never authorizes login, cart mutation, checkout, purchase, or payment.

## 11. Safety and Privacy Boundaries

- Never request, store, or transmit a marketplace password, payment credential, identity number, or full address.
- Never claim to have placed an order or reserved stock.
- Never perform a purchase or payment action.
- Do not treat a marketplace domain as proof that the seller is the platform or brand.
- Do not compare different variants as if they were identical.
- Do not hide missing platform coverage, login barriers, blocked pages, or stale evidence.
- Do not turn an unavailable price into an estimate unless clearly labeled and useful.
- Stop and hand off when a task requires legal, medical, financial, or other specialized high-stakes advice.

## 12. Failure Handling

If live pages are inaccessible, the Skill should continue with accessible public evidence only when that evidence can still support a useful, qualified answer. It must state which channels were not checked and which claims remain unverified.

If exact variants cannot be established, the Skill should ask one targeted question or provide a conditional comparison rather than merging products.

If price sources disagree across observation times, the Skill should re-check when practical and otherwise surface the disagreement rather than average the prices.

If a requested monitor lacks an exact variant, threshold, cadence, seller constraint, or end date, the Skill must collect the missing condition before creating the automation.

## 13. Testing Strategy

Tests will validate behavior and invariants, not volatile market prices.

### 13.1 Trigger tests

- Positive automatic-trigger examples for recommendation, evaluation, comparison, price timing, and monitoring.
- Explicit `$shopping-decision` invocation.
- Negative examples for generic explanations, repairs, seller-side work, disputes, and unsupported high-risk categories.

### 13.2 Behavioral cases

- Ask only decision-changing questions.
- Reject comparisons between mismatched variants.
- Do not promote snippet prices to verified current prices.
- Include source and timestamp for verified prices.
- Prefer current-turn requirements over profile defaults.
- Require authorization before profile changes.
- Require explicit monitoring intent and complete monitor conditions.
- Avoid login, cart, checkout, payment, and sensitive-data collection.
- State coverage gaps and evidence uncertainty.
- Keep simple purchases concise and expand only when warranted.

### 13.3 Structural validation

The package will be checked for valid Skill frontmatter, consistent naming, discoverable references, plugin metadata, unresolved placeholders, and installability from GitHub.

## 14. Open-source and Provenance Policy

- License original project content under Apache-2.0.
- Maintain a `NOTICE` file stating that the project is an independent implementation.
- Do not copy prompts, code, templates, or documentation from existing shopping Skills.
- The README may list related projects for ecosystem context without implying affiliation, endorsement, or collaboration.
- Do not commit credentials, cookies, API keys, user profiles, or real shopping records.
- Provide Chinese-first documentation and an English README for international discoverability.

## 15. Acceptance Criteria for Version 0.1.0

Version 0.1.0 is complete when:

1. Codex can select the Skill automatically for clear shopping decisions and explicitly through `$shopping-decision`.
2. All five modes route to the correct references without loading unrelated modules.
3. Product identity, price evidence, seller type, timestamp, and uncertainty rules are enforced in realistic cases.
4. The optional profile workflow preserves user control and does not store prohibited data.
5. Monitoring requires explicit authorization and complete conditions.
6. No workflow logs in, buys, checks out, pays, or requests sensitive credentials.
7. Behavior cases and structural validation pass.
8. The repository includes complete installation, usage, license, and provenance documentation.
9. The Skill remains useful without a mandatory external API key or paid service.

## 16. Deferred Work

The following may be evaluated after real-world use of version 0.1.0:

- Optional adapters for reputable price-history or shopping data providers.
- Additional platform-specific guidance when it can be maintained reliably.
- User-controlled import or export of preference profiles.
- Category-specific modules where generic rules prove insufficient.
- Privacy-preserving local price-history storage.

Deferred features must not weaken the authorization, privacy, evidence, or no-purchase boundaries established here.
