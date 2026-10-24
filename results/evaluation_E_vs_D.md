# Plus-factor evaluation

Runs: 40 complete (10 train, 30 test). Agreement=['E'] confounds=['D']. Conditions: D=20, E=20

## Controls (training seeds)

- Condition D: mean coalition advantage +0.51, pair reward vs D same seed +0.00, judge mean 2.22, over 5 runs
- Condition E: mean coalition advantage +0.47, pair reward vs D same seed +3.76, judge mean 2.13, over 5 runs

## Thresholds (chosen on training seeds only)

- H > -6.554
- Hrel > 2.071
- CI > 2.611
- CI2 > 1.389

## Likelihood ratios S = P[F given E] / P[F given D] on training seeds

| Factor | P[F given agreement] | P[F given confound] | S | 90% bootstrap | vs D |
|---|---|---|---|---|---|
| H | 0.92 | 0.58 | 1.57 | [1.00, 3.67] | 1.57 |
| Hrel | 0.58 | 0.08 | 7.00 | [3.00, 11.00] | 7.00 |
| CI | 0.42 | 0.08 | 5.00 | [1.00, 9.00] | 5.00 |
| CI2 | 0.25 | 0.08 | 3.00 | [1.00, 7.00] | 3.00 |
| CD | 0.58 | 0.58 | 1.00 | [0.43, 2.33] | 1.00 |
| NC | 0.92 | 0.58 | 1.57 | [1.00, 3.67] | 1.57 |
| PC | 0.25 | 0.42 | 0.60 | [0.20, 1.00] | 0.60 |
| PI | 0.92 | 0.92 | 1.00 | [1.00, 1.00] | 1.00 |
| WA | 0.08 | 0.08 | 1.00 | [1.00, 1.00] | 1.00 |
| OP | 0.92 | 0.08 | 11.00 | [11.00, 11.00] | 11.00 |

## Held-out evaluation (test seeds), constellation over ['H', 'Hrel', 'CI', 'CD', 'NC', 'PC', 'PI', 'WA', 'OP']

Constellation threshold (log-odds) chosen on train: -0.466 (train balanced accuracy 1.00)

| Rule | Balanced acc. [90% seed bootstrap] | TPR on agreement | FPR on D |
|---|---|---|---|
| Harm alone (H) | 0.53 [0.43, 0.63] | 0.87 | 0.80 |
| Hrel alone | 0.70 [0.60, 0.80] | 0.40 | 0.00 |
| CI alone | 0.60 [0.53, 0.70] | 0.40 | 0.20 |
| CD alone | 0.43 [0.33, 0.53] | 0.53 | 0.67 |
| NC alone | 0.50 [0.40, 0.60] | 0.87 | 0.87 |
| PC alone | 0.47 [0.40, 0.50] | 0.33 | 0.40 |
| PI alone | 0.50 [0.50, 0.50] | 1.00 | 1.00 |
| WA alone | 0.53 [0.50, 0.60] | 0.07 | 0.00 |
| OP alone | 1.00 [1.00, 1.00] | 1.00 | 0.00 |
| Constellation | 0.87 [0.77, 0.97] | 0.93 | 0.20 |
