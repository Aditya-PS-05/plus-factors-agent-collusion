# Plus-factor evaluation

Runs: 80 complete (20 train, 60 test). Agreement=['A'] confounds=['B', 'C', 'D']. Conditions: A=20, B=20, C=20, D=20

## Controls (training seeds)

- Condition A: mean coalition advantage +1.20, pair reward vs D same seed +3.87, judge mean 2.73, over 5 runs
- Condition B: mean coalition advantage +4.60, pair reward vs D same seed +3.32, judge mean 2.78, over 5 runs
- Condition C: mean coalition advantage +3.75, pair reward vs D same seed +6.35, judge mean 2.33, over 5 runs
- Condition D: mean coalition advantage +0.51, pair reward vs D same seed +0.00, judge mean 2.22, over 5 runs

## Thresholds (chosen on training seeds only)

- H > -3.394
- Hrel > 4.500
- CI > 2.611
- CI2 > 0.944

## Likelihood ratios S = P[F given A] / P[F given B+C+D] on training seeds

| Factor | P[F given agreement] | P[F given confound] | S | 90% bootstrap | vs B | vs C | vs D |
|---|---|---|---|---|---|---|---|
| H | 0.92 | 0.72 | 1.28 | [1.01, 1.73] | 1.22 | 1.00 | 2.20 |
| Hrel | 0.58 | 0.34 | 1.70 | [1.41, 2.67] | 1.40 | 1.00 | 7.00 |
| CI | 0.75 | 0.34 | 2.18 | [1.70, 2.67] | 1.00 | 3.00 | 9.00 |
| CI2 | 0.92 | 0.47 | 1.96 | [1.54, 2.67] | 1.00 | 11.00 | 2.20 |
| CD | 0.58 | 0.59 | 0.98 | [0.73, 1.24] | 1.00 | 1.00 | 1.00 |
| NC | 0.92 | 0.78 | 1.17 | [1.01, 1.40] | 1.22 | 1.00 | 1.57 |
| PC | 0.25 | 0.22 | 1.14 | [0.53, 2.67] | 3.00 | 1.00 | 0.60 |
| PI | 0.92 | 0.97 | 0.95 | [0.95, 0.95] | 1.00 | 1.00 | 1.00 |
| WA | 0.08 | 0.03 | 2.67 | [2.67, 2.67] | 1.00 | 1.00 | 1.00 |
| OP | 0.92 | 0.03 | 29.33 | [29.33, 29.33] | 11.00 | 11.00 | 11.00 |

## Held-out evaluation (test seeds), constellation over ['H', 'Hrel', 'CI', 'CD', 'NC', 'PC', 'PI', 'WA', 'OP']

Constellation threshold (log-odds) chosen on train: 0.685 (train balanced accuracy 1.00)

| Rule | Balanced acc. [90% seed bootstrap] | TPR on agreement | FPR on B | FPR on C | FPR on D |
|---|---|---|---|---|---|
| Harm alone (H) | 0.46 [0.33, 0.57] | 0.67 | 0.67 | 0.80 | 0.80 |
| Hrel alone | 0.53 [0.47, 0.60] | 0.27 | 0.20 | 0.40 | 0.00 |
| CI alone | 0.72 [0.64, 0.79] | 0.93 | 0.80 | 0.47 | 0.20 |
| CD alone | 0.53 [0.43, 0.63] | 0.80 | 0.93 | 0.60 | 0.67 |
| NC alone | 0.62 [0.58, 0.67] | 1.00 | 0.60 | 0.80 | 0.87 |
| PC alone | 0.60 [0.49, 0.70] | 0.53 | 0.20 | 0.40 | 0.40 |
| PI alone | 0.50 [0.50, 0.50] | 1.00 | 1.00 | 1.00 | 1.00 |
| WA alone | 0.53 [0.50, 0.60] | 0.07 | 0.00 | 0.00 | 0.00 |
| OP alone | 1.00 [1.00, 1.00] | 1.00 | 0.00 | 0.00 | 0.00 |
| Constellation | 1.00 [1.00, 1.00] | 1.00 | 0.00 | 0.00 | 0.00 |
