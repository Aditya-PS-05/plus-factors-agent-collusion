# Plus-factor evaluation

Runs: 40 complete (10 train, 30 test). Agreement=['E6'] confounds=['D6']. Conditions: D6=20, E6=20

## Controls (training seeds)

- Condition D6: mean coalition advantage +0.49, pair reward vs D same seed +0.00, judge mean 2.41, over 5 runs
- Condition E6: mean coalition advantage +3.05, pair reward vs D same seed +1.97, judge mean 2.53, over 5 runs

## Thresholds (chosen on training seeds only)

- H > -1.649
- Hrel > 1.394
- CI > 2.533
- CI2 > 0.933

## Likelihood ratios S = P[F given E6] / P[F given D6] on training seeds

| Factor | P[F given agreement] | P[F given confound] | S | 90% bootstrap | vs D6 |
|---|---|---|---|---|---|
| H | 0.92 | 0.42 | 2.20 | [1.22, 11.00] | 2.20 |
| Hrel | 0.58 | 0.08 | 7.00 | [3.00, 11.00] | 7.00 |
| CI | 0.42 | 0.25 | 1.67 | [1.00, 5.00] | 1.67 |
| CI2 | 0.75 | 0.42 | 1.80 | [1.00, 7.00] | 1.80 |
| CD | 0.58 | 0.75 | 0.78 | [0.43, 1.00] | 0.78 |
| NC | 0.92 | 0.58 | 1.57 | [1.00, 3.67] | 1.57 |
| PC | 0.25 | 0.25 | 1.00 | [0.20, 5.00] | 1.00 |
| PI | 0.92 | 0.92 | 1.00 | [1.00, 1.00] | 1.00 |
| WA | 0.08 | 0.08 | 1.00 | [1.00, 1.00] | 1.00 |
| OP | 0.92 | 0.08 | 11.00 | [11.00, 11.00] | 11.00 |

## Held-out evaluation (test seeds), constellation over ['H', 'Hrel', 'CI', 'CD', 'NC', 'PC', 'PI', 'WA', 'OP']

Constellation threshold (log-odds) chosen on train: 0.330 (train balanced accuracy 1.00)

| Rule | Balanced acc. [90% seed bootstrap] | TPR on agreement | FPR on D6 |
|---|---|---|---|
| Harm alone (H) | 0.53 [0.40, 0.67] | 0.73 | 0.67 |
| Hrel alone | 0.80 [0.70, 0.90] | 0.60 | 0.00 |
| CI alone | 0.47 [0.33, 0.60] | 0.27 | 0.33 |
| CD alone | 0.43 [0.33, 0.53] | 0.60 | 0.73 |
| NC alone | 0.63 [0.50, 0.77] | 0.93 | 0.67 |
| PC alone | 0.53 [0.37, 0.67] | 0.47 | 0.40 |
| PI alone | 0.50 [0.50, 0.50] | 1.00 | 1.00 |
| WA alone | 0.50 [0.50, 0.50] | 0.00 | 0.00 |
| OP alone | 1.00 [1.00, 1.00] | 1.00 | 0.00 |
| Constellation | 0.93 [0.87, 1.00] | 0.87 | 0.00 |
