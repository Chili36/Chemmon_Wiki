# Page selector: Jev 1.13.0 vs Claude Haiku 5.5 (2026-10-18)

Issue #44. Jev selector ported from the FoodEx2 wiki; its ChemMon prompt was
fixed (commit 7a41f04) before this run and not changed after. Both selectors
used the same catalogue (hints), the same 16 cases in `evals/cases.json`
(10 development, 6 held-out) and each case's page limit. Three repeats per
model; raw reports `development-r*.json`, `held-out-r*.json`.

| Metric (48 selections each) | Haiku 5.5 | Jev 1.13.0 |
|---|---:|---:|
| Required-page recall | 97.6% | 95.2% |
| All required pages selected | 41/42 | 40/42 |
| Wrong-domain picks | 0 | 0 |
| Empty selection when expected | 3/3 | 3/3 |
| Mean pages selected | 3.6 | 3.6 |
| Median selection time | 1.30 s | 0.64 s |
| 95th percentile time | 2.62 s | 0.88 s |
| Median input tokens | 6,234 | 24,106 |
| Estimated cost per selection | $0.00070 | $0.00101 |
| Errors | 0 | 0 |

Misses: both missed `ambiguous-facet` once (picked FoodEx2 facet pages, not the
required page); Jev also missed `pre-implicit` once. One selection in 48 is the
whole recall difference, within run-to-run noise on 16 draft-labelled cases.

Reading: on ChemMon, Jev matches Haiku's selection quality and halves selection
time, but is not cheaper. Its request is about four times larger (every page
question repeats the instructions and the four levels), which outweighs its
lower price per token. FoodEx2's large saving was measured against Sonnet 5,
not Haiku. Costs are estimates from returned usage and the prices in
`prices.json`; Jev output tokens are free.

Limits: draft labels; 16 cases; provider-default sampling. Not evidence of
general superiority either way.
