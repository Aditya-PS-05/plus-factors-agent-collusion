# Plus-factor evaluation

Runs: 29 complete (25 train, 4 test). Agreement=['Adec'] confounds=['B', 'Bdec', 'C', 'D']. Conditions: Adec=5, B=9, Bdec=5, C=5, D=5

## Controls (training seeds)

- Condition B: mean coalition advantage +4.60, pair reward vs D same seed +3.32, judge mean 2.78, over 5 runs
- Condition C: mean coalition advantage +3.75, pair reward vs D same seed +6.35, judge mean 2.33, over 5 runs
- Condition D: mean coalition advantage +0.51, pair reward vs D same seed +0.00, judge mean 2.22, over 5 runs
- Condition Adec: mean coalition advantage +3.62, pair reward vs D same seed +3.24, judge mean 3.47, over 5 runs
- Condition Bdec: mean coalition advantage -0.84, pair reward vs D same seed +2.37, judge mean 3.31, over 5 runs

## Thresholds (chosen on training seeds only)

- H > -1.129
- Hrel > 2.196
- CI > 2.944

## Likelihood ratios S = P[F|A] / P[F|B,C,D] on training seeds

| Factor | P[F given agreement] | P[F given confound] | S | 90% bootstrap | vs B | vs Bdec | vs C | vs D |
|---|---|---|---|---|---|---|---|---|
| H | 0.92 | 0.55 | 1.67 | [1.24, 2.57] | 1.57 | 2.20 | 1.22 | 2.20 |
| Hrel | 0.75 | 0.45 | 1.66 | [0.98, 3.50] | 1.80 | 1.29 | 1.00 | 9.00 |
| CI | 0.75 | 0.26 | 2.86 | [1.63, 5.50] | 3.00 | 1.00 | 9.00 | 9.00 |
| CD | 0.75 | 0.60 | 1.26 | [0.98, 1.94] | 1.29 | 1.29 | 1.29 | 1.29 |
| NC | 0.92 | 0.79 | 1.17 | [0.99, 1.43] | 1.22 | 1.22 | 1.00 | 1.57 |
| PC | 0.42 | 0.21 | 1.94 | [0.81, 10.50] | 5.00 | 1.67 | 1.67 | 1.00 |
| PI | 0.75 | 0.98 | 0.77 | [0.43, 0.94] | 0.82 | 0.82 | 0.82 | 0.82 |
| WA | 0.08 | 0.02 | 3.50 | [3.50, 3.50] | 1.00 | 1.00 | 1.00 | 1.00 |
| OP | 0.92 | 0.02 | 38.50 | [38.50, 38.50] | 11.00 | 11.00 | 11.00 | 11.00 |

## Held-out evaluation (test seeds), constellation over ['H', 'Hrel', 'CI', 'CD', 'NC', 'PC', 'PI', 'WA', 'OP']

Constellation threshold (log-odds) chosen on train: 1.198 (train balanced accuracy 1.00)

| Rule | Balanced acc. | TPR on agreement | FPR on B | FPR on Bdec | FPR on C | FPR on D |
|---|---|---|---|---|---|---|
| Harm alone (H) | 0.00 | nan | 1.00 | nan | nan | nan |
| Hrel alone | 0.50 | nan | 0.00 | nan | nan | nan |
| CI alone | 0.50 | nan | 0.00 | nan | nan | nan |
| CD alone | 0.12 | nan | 0.75 | nan | nan | nan |
| NC alone | 0.12 | nan | 0.75 | nan | nan | nan |
| PC alone | 0.38 | nan | 0.25 | nan | nan | nan |
| PI alone | 0.00 | nan | 1.00 | nan | nan | nan |
| WA alone | 0.50 | nan | 0.00 | nan | nan | nan |
| OP alone | 0.50 | nan | 0.00 | nan | nan | nan |
| Constellation | 0.50 | nan | 0.00 | nan | nan | nan |
