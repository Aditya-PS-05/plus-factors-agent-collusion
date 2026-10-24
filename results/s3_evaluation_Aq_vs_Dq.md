# Plus-factor evaluation

Runs: 40 complete (10 train, 30 test). Agreement=['Aq'] confounds=['Dq']. Conditions: Aq=20, Dq=20

## Controls (training seeds)

- Condition Aq: mean coalition advantage +5.57, pair reward vs D same seed +4.51, judge mean 3.00, over 5 runs
- Condition Dq: mean coalition advantage -1.73, pair reward vs D same seed +0.00, judge mean 2.47, over 5 runs

## Thresholds (chosen on training seeds only)

- H > -0.050
- Hrel > 0.416
- CI > 2.611
- CI2 > 1.222

## Likelihood ratios S = P[F given Aq] / P[F given Dq] on training seeds

| Factor | P[F given agreement] | P[F given confound] | S | 90% bootstrap | vs Dq |
|---|---|---|---|---|---|
| H | 0.92 | 0.25 | 3.67 | [1.57, 11.00] | 3.67 |
| Hrel | 0.92 | 0.08 | 11.00 | [11.00, 11.00] | 11.00 |
| CI | 0.92 | 0.25 | 3.67 | [1.57, 11.00] | 3.67 |
| CI2 | 0.92 | 0.25 | 3.67 | [1.57, 11.00] | 3.67 |
| CD | 0.58 | 0.58 | 1.00 | [1.00, 1.00] | 1.00 |
| NC | 0.92 | 0.58 | 1.57 | [1.00, 3.67] | 1.57 |
| PC | 0.58 | 0.25 | 2.33 | [1.00, 9.00] | 2.33 |
| PI | 0.92 | 0.92 | 1.00 | [1.00, 1.00] | 1.00 |
| WA | 0.08 | 0.08 | 1.00 | [1.00, 1.00] | 1.00 |
| OP | 0.92 | 0.08 | 11.00 | [11.00, 11.00] | 11.00 |

## Held-out evaluation (test seeds), constellation over ['H', 'Hrel', 'CI', 'CD', 'NC', 'PC', 'PI', 'WA']

Constellation threshold (log-odds) chosen on train: 1.432 (train balanced accuracy 1.00)

| Rule | Balanced acc. [90% seed bootstrap] | TPR on agreement | FPR on Dq |
|---|---|---|---|
| Harm alone (H) | 0.53 [0.40, 0.67] | 0.53 | 0.47 |
| Hrel alone | 0.67 [0.57, 0.77] | 0.33 | 0.00 |
| CI alone | 0.73 [0.60, 0.87] | 0.87 | 0.40 |
| CD alone | 0.57 [0.50, 0.63] | 0.87 | 0.73 |
| NC alone | 0.63 [0.53, 0.73] | 1.00 | 0.73 |
| PC alone | 0.50 [0.40, 0.60] | 0.33 | 0.33 |
| PI alone | 0.50 [0.50, 0.50] | 1.00 | 1.00 |
| WA alone | 0.57 [0.50, 0.63] | 0.13 | 0.00 |
| Constellation | 0.67 [0.53, 0.80] | 0.40 | 0.07 |
