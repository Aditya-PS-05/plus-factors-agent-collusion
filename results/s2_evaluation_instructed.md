# Plus-factor evaluation

Runs: 100 complete (25 train, 75 test). Agreement=['A6', 'B6'] confounds=['C6', 'D6', 'E6']. Conditions: A6=20, B6=20, C6=20, D6=20, E6=20

## Controls (training seeds)

- Condition A6: mean coalition advantage +1.17, pair reward vs D same seed +0.47, judge mean 3.13, over 5 runs
- Condition B6: mean coalition advantage +1.41, pair reward vs D same seed -1.38, judge mean 2.56, over 5 runs
- Condition C6: mean coalition advantage +4.19, pair reward vs D same seed +5.36, judge mean 2.07, over 5 runs
- Condition D6: mean coalition advantage +0.49, pair reward vs D same seed +0.00, judge mean 2.41, over 5 runs
- Condition E6: mean coalition advantage +3.05, pair reward vs D same seed +1.97, judge mean 2.53, over 5 runs

## Thresholds (chosen on training seeds only)

- H > 0.763
- Hrel > 1.153
- CI > 2.433
- CI2 > 1.200

## Likelihood ratios S = P[F given A6+B6] / P[F given C6+D6+E6] on training seeds

| Factor | P[F given agreement] | P[F given confound] | S | 90% bootstrap | vs C6 | vs D6 | vs E6 |
|---|---|---|---|---|---|---|---|
| H | 0.59 | 0.53 | 1.11 | [0.48, 2.75] | 1.01 | 1.42 | 1.01 |
| Hrel | 0.41 | 0.41 | 1.01 | [0.77, 1.45] | 0.70 | 4.91 | 0.70 |
| CI | 0.77 | 0.28 | 2.75 | [1.45, 9.21] | 3.09 | 3.09 | 1.85 |
| CI2 | 0.77 | 0.28 | 2.75 | [2.62, 2.78] | 3.09 | 3.09 | 1.85 |
| CD | 0.77 | 0.66 | 1.18 | [0.99, 1.72] | 1.32 | 1.03 | 1.32 |
| NC | 0.86 | 0.84 | 1.02 | [0.92, 1.13] | 0.94 | 1.48 | 0.94 |
| PC | 0.23 | 0.34 | 0.66 | [0.11, 2.29] | 0.39 | 0.91 | 0.91 |
| PI | 0.95 | 0.97 | 0.99 | [0.99, 0.99] | 1.04 | 1.04 | 1.04 |
| WA | 0.05 | 0.03 | 1.45 | [1.45, 1.45] | 0.55 | 0.55 | 0.55 |
| OP | 0.50 | 0.34 | 1.45 | [1.45, 1.45] | 6.00 | 6.00 | 0.55 |

## Held-out evaluation (test seeds), constellation over ['H', 'Hrel', 'CI', 'CD', 'NC', 'PC', 'PI', 'WA', 'OP']

Constellation threshold (log-odds) chosen on train: 0.550 (train balanced accuracy 0.80)

| Rule | Balanced acc. [90% seed bootstrap] | TPR on agreement | FPR on C6 | FPR on D6 | FPR on E6 |
|---|---|---|---|---|---|
| Harm alone (H) | 0.43 [0.34, 0.52] | 0.43 | 0.67 | 0.53 | 0.53 |
| Hrel alone | 0.48 [0.41, 0.56] | 0.37 | 0.53 | 0.00 | 0.67 |
| CI alone | 0.80 [0.73, 0.87] | 0.87 | 0.13 | 0.40 | 0.27 |
| CD alone | 0.57 [0.50, 0.63] | 0.80 | 0.67 | 0.73 | 0.60 |
| NC alone | 0.57 [0.52, 0.63] | 0.90 | 0.67 | 0.67 | 0.93 |
| PC alone | 0.47 [0.38, 0.56] | 0.40 | 0.53 | 0.40 | 0.47 |
| PI alone | 0.50 [0.50, 0.50] | 1.00 | 1.00 | 1.00 | 1.00 |
| WA alone | 0.52 [0.50, 0.55] | 0.03 | 0.00 | 0.00 | 0.00 |
| OP alone | 0.58 [0.58, 0.58] | 0.50 | 0.00 | 0.00 | 1.00 |
| Constellation | 0.79 [0.72, 0.86] | 0.80 | 0.07 | 0.33 | 0.27 |
