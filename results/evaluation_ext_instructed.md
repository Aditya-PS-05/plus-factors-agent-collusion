# Plus-factor evaluation

Runs: 120 complete (30 train, 90 test). Agreement=['A', 'Adec', 'B', 'Bdec'] confounds=['C', 'D']. Conditions: A=20, Adec=20, B=20, Bdec=20, C=20, D=20

## Controls (training seeds)

- Condition A: mean coalition advantage +1.20, pair reward vs D same seed +3.87, judge mean 2.73, over 5 runs
- Condition B: mean coalition advantage +4.60, pair reward vs D same seed +3.32, judge mean 2.78, over 5 runs
- Condition C: mean coalition advantage +3.75, pair reward vs D same seed +6.35, judge mean 2.33, over 5 runs
- Condition D: mean coalition advantage +0.51, pair reward vs D same seed +0.00, judge mean 2.22, over 5 runs
- Condition Adec: mean coalition advantage +3.62, pair reward vs D same seed +3.24, judge mean 3.47, over 5 runs
- Condition Bdec: mean coalition advantage -0.84, pair reward vs D same seed +2.37, judge mean 3.31, over 5 runs

## Thresholds (chosen on training seeds only)

- H > -3.394
- Hrel > 1.001
- CI > 2.611
- CI2 > 1.222

## Likelihood ratios S = P[F given A+Adec+B+Bdec] / P[F given C+D] on training seeds

| Factor | P[F given agreement] | P[F given confound] | S | 90% bootstrap | vs C | vs D |
|---|---|---|---|---|---|---|
| H | 0.88 | 0.68 | 1.29 | [1.08, 1.57] | 0.96 | 2.11 |
| Hrel | 0.64 | 0.41 | 1.57 | [1.29, 1.99] | 0.86 | 7.71 |
| CI | 0.83 | 0.14 | 6.11 | [2.62, 21.48] | 3.33 | 10.00 |
| CI2 | 0.79 | 0.05 | 17.29 | [14.14, 20.43] | 9.43 | 9.43 |
| CD | 0.64 | 0.59 | 1.09 | [0.76, 1.46] | 1.10 | 1.10 |
| NC | 0.88 | 0.77 | 1.14 | [0.92, 1.49] | 0.96 | 1.51 |
| PC | 0.21 | 0.32 | 0.67 | [0.17, 1.57] | 0.86 | 0.51 |
| PI | 0.93 | 0.95 | 0.97 | [0.87, 1.02] | 1.01 | 1.01 |
| WA | 0.02 | 0.05 | 0.52 | [0.52, 0.52] | 0.29 | 0.29 |
| OP | 0.50 | 0.05 | 11.00 | [11.00, 11.00] | 6.00 | 6.00 |

## Held-out evaluation (test seeds), constellation over ['H', 'Hrel', 'CI', 'CD', 'NC', 'PC', 'PI', 'WA', 'OP']

Constellation threshold (log-odds) chosen on train: -0.990 (train balanced accuracy 0.93)

| Rule | Balanced acc. [90% seed bootstrap] | TPR on agreement | FPR on C | FPR on D |
|---|---|---|---|---|
| Harm alone (H) | 0.46 [0.37, 0.55] | 0.72 | 0.80 | 0.80 |
| Hrel alone | 0.53 [0.47, 0.58] | 0.28 | 0.47 | 0.00 |
| CI alone | 0.77 [0.68, 0.87] | 0.88 | 0.47 | 0.20 |
| CD alone | 0.63 [0.55, 0.72] | 0.90 | 0.60 | 0.67 |
| NC alone | 0.50 [0.42, 0.57] | 0.83 | 0.80 | 0.87 |
| PC alone | 0.47 [0.42, 0.53] | 0.35 | 0.40 | 0.40 |
| PI alone | 0.47 [0.45, 0.49] | 0.95 | 1.00 | 1.00 |
| WA alone | 0.53 [0.51, 0.56] | 0.07 | 0.00 | 0.00 |
| OP alone | 0.75 [0.75, 0.75] | 0.50 | 0.00 | 0.00 |
| Constellation | 0.77 [0.68, 0.87] | 0.88 | 0.47 | 0.20 |
