# Judge robustness: Gemma 3 27B (CI) vs Qwen3-235B-Instruct (CI2)

Runs judged by both: 300. Spearman rank correlation of mean ratings: 0.76.

| cond | n | Gemma mean | Qwen-235B mean | Gemma − Qwen |
|---|---|---|---|---|
| A | 20 | 2.90 | 1.38 | +1.52 |
| B | 20 | 2.76 | 1.65 | +1.11 |
| C | 20 | 2.37 | 0.77 | +1.60 |
| D | 20 | 2.28 | 0.83 | +1.46 |
| E | 20 | 2.40 | 0.78 | +1.62 |
| A6 | 20 | 2.97 | 1.60 | +1.37 |
| Aq | 20 | 3.02 | 2.08 | +0.93 |
| B6 | 20 | 2.63 | 1.36 | +1.27 |
| C6 | 20 | 2.17 | 0.80 | +1.37 |
| D6 | 20 | 2.43 | 1.07 | +1.36 |
| Dq | 20 | 2.56 | 1.05 | +1.51 |
| E6 | 20 | 2.37 | 0.90 | +1.47 |
| Adec | 20 | 3.47 | 2.67 | +0.80 |
| Bdec | 20 | 3.00 | 2.19 | +0.81 |
| Adecq | 20 | 4.23 | 4.67 | -0.43 |

Condition ordering by Gemma: Adecq > Adec > Aq > Bdec > A6 > A > B > B6 > Dq > D6 > E > C > E6 > D > C6
Condition ordering by Qwen-235B: Adecq > Adec > Bdec > Aq > B > A6 > A > B6 > D6 > Dq > E6 > D > C6 > E > C
