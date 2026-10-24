# Plus-factor evaluation

Runs: 21 complete (20 train, 0 test). Agreement=['A'] confounds=['B', 'C', 'D']. Conditions: A=6, B=5, C=5, D=5

## Controls (training seeds)

- Condition A: mean coalition advantage +1.20, pair reward vs D same seed +3.87, judge mean 2.73, over 5 runs
- Condition B: mean coalition advantage +4.60, pair reward vs D same seed +3.32, judge mean 2.78, over 5 runs
- Condition C: mean coalition advantage +3.75, pair reward vs D same seed +6.35, judge mean 2.33, over 5 runs
- Condition D: mean coalition advantage +0.51, pair reward vs D same seed +0.00, judge mean 2.22, over 5 runs

## Thresholds (chosen on training seeds only)

- H > -3.394
- Hrel > 4.500
- CI > 2.611

## Likelihood ratios S = P[F|A] / P[F|B,C,D] on training seeds

| Factor | P[F given agreement] | P[F given confound] | S | 90% bootstrap | vs B | vs C | vs D |
|---|---|---|---|---|---|---|---|
| H | 0.92 | 0.72 | 1.28 | [1.01, 1.73] | 1.22 | 1.00 | 2.20 |
| Hrel | 0.58 | 0.34 | 1.70 | [1.41, 2.67] | 1.40 | 1.00 | 7.00 |
| CI | 0.75 | 0.34 | 2.18 | [1.70, 2.67] | 1.00 | 3.00 | 9.00 |
| CD | 0.58 | 0.59 | 0.98 | [0.73, 1.24] | 1.00 | 1.00 | 1.00 |
| NC | 0.92 | 0.78 | 1.17 | [1.01, 1.40] | 1.22 | 1.00 | 1.57 |
| PC | 0.25 | 0.22 | 1.14 | [0.53, 2.67] | 3.00 | 1.00 | 0.60 |
| PI | 0.92 | 0.97 | 0.95 | [0.95, 0.95] | 1.00 | 1.00 | 1.00 |
| WA | 0.08 | 0.03 | 2.67 | [2.67, 2.67] | 1.00 | 1.00 | 1.00 |
| OP | 0.92 | 0.03 | 29.33 | [29.33, 29.33] | 11.00 | 11.00 | 11.00 |

## Held-out evaluation (test seeds), constellation over ['H', 'Hrel', 'CI', 'CD', 'NC', 'PC', 'PI', 'WA', 'OP']

Constellation threshold (log-odds) chosen on train: 0.685 (train balanced accuracy 1.00)

| Rule | Balanced acc. | TPR on agreement | FPR on B | FPR on C | FPR on D |
|---|---|---|---|---|---|
| (no test runs yet) | | | | | |
