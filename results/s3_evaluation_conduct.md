# Plus-factor evaluation

Runs: 60 complete (15 train, 45 test). Agreement=['Adecq', 'Aq'] confounds=['Dq']. Conditions: Adecq=20, Aq=20, Dq=20

## Controls (training seeds)

- Condition Aq: mean coalition advantage +5.57, pair reward vs D same seed +4.51, judge mean 3.00, over 5 runs
- Condition Dq: mean coalition advantage -1.73, pair reward vs D same seed +0.00, judge mean 2.47, over 5 runs
- Condition Adecq: mean coalition advantage +3.00, pair reward vs D same seed +1.02, judge mean 4.13, over 5 runs

## Thresholds (chosen on training seeds only)

- H > -0.328
- Hrel > 0.110
- CI > 2.611
- CI2 > 1.222

## Likelihood ratios S = P[F given Adecq+Aq] / P[F given Dq] on training seeds

| Factor | P[F given agreement] | P[F given confound] | S | 90% bootstrap | vs Dq |
|---|---|---|---|---|---|
| H | 0.95 | 0.25 | 3.82 | [1.64, 11.45] | 3.82 |
| Hrel | 0.77 | 0.08 | 9.27 | [7.09, 11.45] | 9.27 |
| CI | 0.95 | 0.25 | 3.82 | [1.64, 11.45] | 3.82 |
| CI2 | 0.95 | 0.25 | 3.82 | [1.64, 11.45] | 3.82 |
| CD | 0.50 | 0.58 | 0.86 | [0.55, 1.03] | 0.86 |
| NC | 0.95 | 0.58 | 1.64 | [1.04, 3.82] | 1.64 |
| PC | 0.50 | 0.25 | 2.00 | [0.98, 7.09] | 2.00 |
| PI | 0.95 | 0.92 | 1.04 | [1.04, 1.04] | 1.04 |
| WA | 0.23 | 0.08 | 2.73 | [0.55, 4.91] | 2.73 |
| OP | 0.95 | 0.08 | 11.45 | [11.45, 11.45] | 11.45 |

## Held-out evaluation (test seeds), constellation over ['H', 'Hrel', 'CD', 'NC', 'PC', 'PI', 'WA']

Constellation threshold (log-odds) chosen on train: -2.156 (train balanced accuracy 0.90)

| Rule | Balanced acc. [90% seed bootstrap] | TPR on agreement | FPR on Dq |
|---|---|---|---|
| Harm alone (H) | 0.52 [0.38, 0.65] | 0.57 | 0.53 |
| Hrel alone | 0.65 [0.57, 0.73] | 0.30 | 0.00 |
| CD alone | 0.55 [0.47, 0.63] | 0.83 | 0.73 |
| NC alone | 0.62 [0.52, 0.72] | 0.97 | 0.73 |
| PC alone | 0.53 [0.45, 0.62] | 0.40 | 0.33 |
| PI alone | 0.47 [0.43, 0.50] | 0.93 | 1.00 |
| WA alone | 0.70 [0.63, 0.77] | 0.40 | 0.00 |
| Constellation | 0.55 [0.40, 0.70] | 0.63 | 0.53 |
