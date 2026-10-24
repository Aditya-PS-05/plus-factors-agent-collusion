# Plus-factor evaluation

Runs: 120 complete (30 train, 90 test). Agreement=['A', 'Adec'] confounds=['B', 'Bdec', 'C', 'D']. Conditions: A=20, Adec=20, B=20, Bdec=20, C=20, D=20

## Controls (training seeds)

- Condition A: mean coalition advantage +1.20, pair reward vs D same seed +3.87, judge mean 2.73, over 5 runs
- Condition B: mean coalition advantage +4.60, pair reward vs D same seed +3.32, judge mean 2.78, over 5 runs
- Condition C: mean coalition advantage +3.75, pair reward vs D same seed +6.35, judge mean 2.33, over 5 runs
- Condition D: mean coalition advantage +0.51, pair reward vs D same seed +0.00, judge mean 2.22, over 5 runs
- Condition Adec: mean coalition advantage +3.62, pair reward vs D same seed +3.24, judge mean 3.47, over 5 runs
- Condition Bdec: mean coalition advantage -0.84, pair reward vs D same seed +2.37, judge mean 3.31, over 5 runs

## Thresholds (chosen on training seeds only)

- H > -1.293
- Hrel > 2.196
- CI > 2.944
- CI2 > 0.944

## Likelihood ratios S = P[F given A+Adec] / P[F given B+Bdec+C+D] on training seeds

| Factor | P[F given agreement] | P[F given confound] | S | 90% bootstrap | vs B | vs Bdec | vs C | vs D |
|---|---|---|---|---|---|---|---|---|
| H | 0.86 | 0.55 | 1.58 | [1.20, 2.42] | 1.48 | 2.07 | 1.15 | 2.07 |
| Hrel | 0.68 | 0.45 | 1.51 | [0.92, 2.50] | 1.64 | 1.17 | 0.91 | 8.18 |
| CI | 0.59 | 0.26 | 2.26 | [1.91, 3.00] | 2.36 | 0.79 | 7.09 | 7.09 |
| CI2 | 0.86 | 0.60 | 1.45 | [1.25, 1.74] | 0.94 | 0.94 | 10.36 | 2.07 |
| CD | 0.68 | 0.60 | 1.15 | [0.99, 1.40] | 1.17 | 1.17 | 1.17 | 1.17 |
| NC | 0.95 | 0.79 | 1.21 | [1.03, 1.48] | 1.27 | 1.27 | 1.04 | 1.64 |
| PC | 0.32 | 0.21 | 1.48 | [0.64, 5.73] | 3.82 | 1.27 | 1.27 | 0.76 |
| PI | 0.86 | 0.98 | 0.88 | [0.70, 0.98] | 0.94 | 0.94 | 0.94 | 0.94 |
| WA | 0.05 | 0.02 | 1.91 | [1.91, 1.91] | 0.55 | 0.55 | 0.55 | 0.55 |
| OP | 0.95 | 0.02 | 40.09 | [40.09, 40.09] | 11.45 | 11.45 | 11.45 | 11.45 |

## Held-out evaluation (test seeds), constellation over ['H', 'Hrel', 'CD', 'NC', 'PC', 'PI', 'WA']

Constellation threshold (log-odds) chosen on train: 0.721 (train balanced accuracy 0.70)

| Rule | Balanced acc. [90% seed bootstrap] | TPR on agreement | FPR on B | FPR on Bdec | FPR on C | FPR on D |
|---|---|---|---|---|---|---|
| Harm alone (H) | 0.49 [0.40, 0.57] | 0.67 | 0.67 | 0.53 | 0.73 | 0.80 |
| Hrel alone | 0.51 [0.45, 0.57] | 0.23 | 0.20 | 0.27 | 0.40 | 0.00 |
| CD alone | 0.57 [0.50, 0.64] | 0.90 | 0.93 | 0.87 | 0.60 | 0.67 |
| NC alone | 0.62 [0.57, 0.68] | 1.00 | 0.60 | 0.73 | 0.80 | 0.87 |
| PC alone | 0.55 [0.49, 0.61] | 0.43 | 0.20 | 0.33 | 0.40 | 0.40 |
| PI alone | 0.45 [0.40, 0.48] | 0.90 | 1.00 | 1.00 | 1.00 | 1.00 |
| WA alone | 0.54 [0.50, 0.59] | 0.10 | 0.00 | 0.07 | 0.00 | 0.00 |
| Constellation | 0.54 [0.48, 0.60] | 0.27 | 0.20 | 0.20 | 0.33 | 0.00 |
