# Plus-factor evaluation

Runs: 80 complete (20 train, 60 test). Agreement=['A6'] confounds=['B6', 'C6', 'D6']. Conditions: A6=20, B6=20, C6=20, D6=20

## Controls (training seeds)

- Condition A6: mean coalition advantage +1.17, pair reward vs D same seed +0.47, judge mean 3.13, over 5 runs
- Condition B6: mean coalition advantage +1.41, pair reward vs D same seed -1.38, judge mean 2.56, over 5 runs
- Condition C6: mean coalition advantage +4.19, pair reward vs D same seed +5.36, judge mean 2.07, over 5 runs
- Condition D6: mean coalition advantage +0.49, pair reward vs D same seed +0.00, judge mean 2.41, over 5 runs

## Thresholds (chosen on training seeds only)

- H > -2.745
- Hrel > 1.153
- CI > 2.567
- CI2 > 1.533

## Likelihood ratios S = P[F given A6] / P[F given B6+C6+D6] on training seeds

| Factor | P[F given agreement] | P[F given confound] | S | 90% bootstrap | vs B6 | vs C6 | vs D6 |
|---|---|---|---|---|---|---|---|
| H | 0.92 | 0.72 | 1.28 | [0.95, 1.96] | 1.57 | 1.00 | 1.57 |
| Hrel | 0.58 | 0.28 | 2.07 | [1.60, 2.67] | 2.33 | 1.00 | 7.00 |
| CI | 0.92 | 0.28 | 3.26 | [1.96, 9.78] | 2.20 | 3.67 | 3.67 |
| CI2 | 0.75 | 0.22 | 3.43 | [1.85, 18.67] | 3.00 | 3.00 | 3.00 |
| CD | 0.75 | 0.72 | 1.04 | [0.81, 1.28] | 1.00 | 1.29 | 1.00 |
| NC | 0.92 | 0.78 | 1.17 | [0.95, 1.54] | 1.22 | 1.00 | 1.57 |
| PC | 0.42 | 0.28 | 1.48 | [0.30, 4.80] | 5.00 | 0.71 | 1.67 |
| PI | 0.92 | 0.97 | 0.95 | [0.95, 0.95] | 1.00 | 1.00 | 1.00 |
| WA | 0.08 | 0.03 | 2.67 | [2.67, 2.67] | 1.00 | 1.00 | 1.00 |
| OP | 0.92 | 0.03 | 29.33 | [29.33, 29.33] | 11.00 | 11.00 | 11.00 |

## Held-out evaluation (test seeds), constellation over ['H', 'Hrel', 'CD', 'NC', 'PC', 'PI', 'WA']

Constellation threshold (log-odds) chosen on train: 0.103 (train balanced accuracy 0.77)

| Rule | Balanced acc. [90% seed bootstrap] | TPR on agreement | FPR on B6 | FPR on C6 | FPR on D6 |
|---|---|---|---|---|---|
| Harm alone (H) | 0.49 [0.38, 0.59] | 0.73 | 0.73 | 0.80 | 0.73 |
| Hrel alone | 0.56 [0.46, 0.66] | 0.40 | 0.33 | 0.53 | 0.00 |
| CD alone | 0.53 [0.46, 0.61] | 0.80 | 0.80 | 0.67 | 0.73 |
| NC alone | 0.64 [0.59, 0.70] | 1.00 | 0.80 | 0.67 | 0.67 |
| PC alone | 0.48 [0.36, 0.60] | 0.40 | 0.40 | 0.53 | 0.40 |
| PI alone | 0.50 [0.50, 0.50] | 1.00 | 1.00 | 1.00 | 1.00 |
| WA alone | 0.53 [0.50, 0.60] | 0.07 | 0.00 | 0.00 | 0.00 |
| Constellation | 0.59 [0.48, 0.70] | 0.53 | 0.33 | 0.53 | 0.20 |
