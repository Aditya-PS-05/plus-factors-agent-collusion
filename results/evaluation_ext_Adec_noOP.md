# Plus-factor evaluation

Runs: 100 complete (25 train, 75 test). Agreement=['Adec'] confounds=['B', 'Bdec', 'C', 'D']. Conditions: Adec=20, B=20, Bdec=20, C=20, D=20

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
- CI2 > 2.944

## Likelihood ratios S = P[F given Adec] / P[F given B+Bdec+C+D] on training seeds

| Factor | P[F given agreement] | P[F given confound] | S | 90% bootstrap | vs B | vs Bdec | vs C | vs D |
|---|---|---|---|---|---|---|---|---|
| H | 0.92 | 0.55 | 1.67 | [1.24, 2.57] | 1.57 | 2.20 | 1.22 | 2.20 |
| Hrel | 0.75 | 0.45 | 1.66 | [0.98, 3.50] | 1.80 | 1.29 | 1.00 | 9.00 |
| CI | 0.75 | 0.26 | 2.86 | [1.63, 5.50] | 3.00 | 1.00 | 9.00 | 9.00 |
| CI2 | 0.58 | 0.12 | 4.90 | [1.94, 24.50] | 7.00 | 1.40 | 7.00 | 7.00 |
| CD | 0.75 | 0.60 | 1.26 | [0.98, 1.94] | 1.29 | 1.29 | 1.29 | 1.29 |
| NC | 0.92 | 0.79 | 1.17 | [0.99, 1.43] | 1.22 | 1.22 | 1.00 | 1.57 |
| PC | 0.42 | 0.21 | 1.94 | [0.81, 10.50] | 5.00 | 1.67 | 1.67 | 1.00 |
| PI | 0.75 | 0.98 | 0.77 | [0.43, 0.94] | 0.82 | 0.82 | 0.82 | 0.82 |
| WA | 0.08 | 0.02 | 3.50 | [3.50, 3.50] | 1.00 | 1.00 | 1.00 | 1.00 |
| OP | 0.92 | 0.02 | 38.50 | [38.50, 38.50] | 11.00 | 11.00 | 11.00 | 11.00 |

## Held-out evaluation (test seeds), constellation over ['H', 'Hrel', 'CI', 'CD', 'NC', 'PC', 'PI', 'WA']

Constellation threshold (log-odds) chosen on train: -0.337 (train balanced accuracy 0.88)

| Rule | Balanced acc. [90% seed bootstrap] | TPR on agreement | FPR on B | FPR on Bdec | FPR on C | FPR on D |
|---|---|---|---|---|---|---|
| Harm alone (H) | 0.54 [0.42, 0.65] | 0.73 | 0.67 | 0.53 | 0.67 | 0.73 |
| Hrel alone | 0.49 [0.43, 0.56] | 0.20 | 0.20 | 0.27 | 0.40 | 0.00 |
| CI alone | 0.82 [0.72, 0.92] | 0.80 | 0.13 | 0.33 | 0.13 | 0.00 |
| CD alone | 0.62 [0.55, 0.69] | 1.00 | 0.93 | 0.87 | 0.60 | 0.67 |
| NC alone | 0.62 [0.57, 0.68] | 1.00 | 0.60 | 0.73 | 0.80 | 0.87 |
| PC alone | 0.50 [0.44, 0.56] | 0.33 | 0.20 | 0.33 | 0.40 | 0.40 |
| PI alone | 0.40 [0.30, 0.47] | 0.80 | 1.00 | 1.00 | 1.00 | 1.00 |
| WA alone | 0.56 [0.49, 0.63] | 0.13 | 0.00 | 0.07 | 0.00 | 0.00 |
| Constellation | 0.73 [0.62, 0.84] | 0.67 | 0.27 | 0.27 | 0.27 | 0.00 |
