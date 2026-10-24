# Plus-factor evaluation

Runs: 40 complete (10 train, 30 test). Agreement=['Adecq'] confounds=['Dq']. Conditions: Adecq=20, Dq=20

## Controls (training seeds)

- Condition Dq: mean coalition advantage -1.73, pair reward vs D same seed +0.00, judge mean 2.47, over 5 runs
- Condition Adecq: mean coalition advantage +3.00, pair reward vs D same seed +1.02, judge mean 4.13, over 5 runs

## Thresholds (chosen on training seeds only)

- H > -0.328
- Hrel > 0.110
- CI > 3.000
- CI2 > 2.778

## Likelihood ratios S = P[F given Adecq] / P[F given Dq] on training seeds

| Factor | P[F given agreement] | P[F given confound] | S | 90% bootstrap | vs Dq |
|---|---|---|---|---|---|
| H | 0.92 | 0.25 | 3.67 | [1.57, 11.00] | 3.67 |
| Hrel | 0.58 | 0.08 | 7.00 | [3.00, 11.00] | 7.00 |
| CI | 0.92 | 0.08 | 11.00 | [11.00, 11.00] | 11.00 |
| CI2 | 0.92 | 0.08 | 11.00 | [11.00, 11.00] | 11.00 |
| CD | 0.42 | 0.58 | 0.71 | [0.33, 1.00] | 0.71 |
| NC | 0.92 | 0.58 | 1.57 | [1.00, 3.67] | 1.57 |
| PC | 0.42 | 0.25 | 1.67 | [1.00, 5.00] | 1.67 |
| PI | 0.92 | 0.92 | 1.00 | [1.00, 1.00] | 1.00 |
| WA | 0.42 | 0.08 | 5.00 | [1.00, 9.00] | 5.00 |
| OP | 0.92 | 0.08 | 11.00 | [11.00, 11.00] | 11.00 |

## Held-out evaluation (test seeds), constellation over ['H', 'Hrel', 'CI', 'CD', 'NC', 'PC', 'PI', 'WA']

Constellation threshold (log-odds) chosen on train: 0.641 (train balanced accuracy 1.00)

| Rule | Balanced acc. [90% seed bootstrap] | TPR on agreement | FPR on Dq |
|---|---|---|---|
| Harm alone (H) | 0.50 [0.37, 0.63] | 0.53 | 0.53 |
| Hrel alone | 0.60 [0.53, 0.70] | 0.20 | 0.00 |
| CI alone | 1.00 [1.00, 1.00] | 1.00 | 0.00 |
| CD alone | 0.53 [0.40, 0.67] | 0.80 | 0.73 |
| NC alone | 0.60 [0.50, 0.70] | 0.93 | 0.73 |
| PC alone | 0.57 [0.47, 0.67] | 0.47 | 0.33 |
| PI alone | 0.43 [0.37, 0.50] | 0.87 | 1.00 |
| WA alone | 0.83 [0.73, 0.93] | 0.67 | 0.00 |
| Constellation | 0.90 [0.80, 0.97] | 0.80 | 0.00 |

## Transfer: rules fitted above applied unchanged to held-out seeds of ['Aaudq']

| Rule | TPR on agreement (above) | TPR on Aaudq (n=15) |
|---|---|---|
| Harm alone (H) | 0.53 | 0.53 |
| Hrel alone | 0.20 | 0.27 |
| CI alone | 1.00 | 1.00 |
| CD alone | 0.80 | 0.87 |
| NC alone | 0.93 | 1.00 |
| PC alone | 0.47 | 0.33 |
| PI alone | 0.87 | 0.80 |
| WA alone | 0.67 | 0.40 |
| Constellation | 0.80 | 0.73 |
