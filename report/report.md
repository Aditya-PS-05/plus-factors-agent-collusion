# Plus Factors for AI Agents: Separating Collusion from Parallel Conduct in Logged Trajectories

Authors: Aditya Pratap Singh (independent). Affiliation: TBD.

## Abstract

When two AI agents in a shared task end up better off than their peers, did they collude or behave alike? Antitrust law answers with "plus factors": conduct that is likely under an agreement and unlikely without one, which Kovacic et al. (2011) formalise as a likelihood ratio. We ask whether that standard can be computed from logged LLM-agent trajectories and whether it separates a deliberate coalition from innocent correlation, talk without action, and harm without agreement. In Colosseum's Jira ticket task we define eight measures with explicit legal analogues, estimate each one's likelihood ratio on five training seeds, and test single factors and a naive-Bayes constellation on fifteen held-out seeds, across three pre-declared studies: a four-agent task with six matched conditions, the same tickets contested by six agents, and a larger agent model. With Qwen3-30B agents every conduct-based factor, including coalition advantage, has a likelihood ratio near one and classifies at chance, with or without contest, because the conduct that is suspicious among competitors is what teammates are told to do. Two LLM judges agree on the only informative signal, the conversation, and both detect the coalition instruction rather than the channel or any harm. With Qwen3-235B agents the deception-prompted coalition harms outsiders, by public misdirection, and the one conduct factor that fires is a contradiction between an agent's public statement and its action. Evidence standards for agent collusion must be calibrated against the task's own cooperative baseline; harm and conversation judgments alone should not count as convincing.

## 1. Introduction

When two AI agents in a shared workflow end up better off than their peers, did they collude, or did they merely behave alike? The question is hard for the same reason it is hard in antitrust law: parallel conduct is compatible with both agreement and independent behaviour, and US courts answer it with a rule of evidence rather than a definition. Parallel conduct alone is not enough; a plaintiff must show "plus factors", conduct that is likely if the firms had agreed and unlikely if they had not (Kovacic, Marshall, Marx and White 2011). Kovacic et al. give this a formal shape: a plus factor F has strength S(F) = P[F | agreement] / P[F | no agreement], and factors with P[F | no agreement] near zero are "super plus factors" that carry a case on their own.

Recent work on LLM-agent collusion has produced detectors and judges but, as the sprint brief observes, is re-deriving standards of evidence without engaging this older literature. Colosseum (Nakamura et al. 2026) made the gap concrete: an LLM judge's rating of the coalition's conversation was weakly anti-correlated with its actual advantage, and agents often "colluded on paper".

This report asks whether the plus-factor standard can be computed from logged agent trajectories, and whether it separates a deliberate coalition from the three confounds the brief names: innocent correlation, talk without action, and harm without agreement. We take Colosseum's Jira ticket task and its shipped matched conditions, which supply ground truth by construction, define eight measures with explicit legal analogues, compute each one's likelihood ratio on training seeds, and test a constellation rule on held-out seeds, pre-registering each study before its runs.

What is new: (i) the likelihood-ratio standard applied to multi-agent logs rather than prices; (ii) a matched-seed design in which the same tickets and private costs appear under agreement and under each confound; (iii) a held-out test of single factors against their constellation; and (iv) the empirical finding that conduct-based plus factors are silent for a model whose coalitions do not exploit, with or without contest, and that the one factor which fires for a model whose coalition does harm outsiders is a documented contradiction between an agent's public statement and its action, while conversation judges detect the coalition instruction rather than the agreement.

## 2. Related Work

**Defining collusion.** Hammond et al. (2025) define collusion as unwanted cooperation between AI systems at the expense of others; the economics literature defines it by outcome, prices above a competitive benchmark (Calvano et al. 2019; Fish et al. 2024; Lin et al. 2024); Foxabbott et al. (2023) and Motwani et al. (2024) centre covert communication. We sidestep the dispute by borrowing the law's move: fix agreement experimentally and ask which observable conduct is evidence for it.

**Plus factors.** Kovacic et al. (2011) organise plus factors by what a cartel must do, rank them by likelihood ratio, and show that a constellation of weak factors can be a super plus factor. Harrington (2018) and Gal (2019) ask how the doctrine applies to algorithms; Berger, Weiner and Jiang (2025) examine RealPage and Gibson, where a shared pricing tool stands in for an agreement. Our condition B, a shared instruction without a channel, is a laboratory version of that question.

**Auditing agent collusion.** Colosseum (Nakamura et al. 2026) measures action-level coalition advantage and compares it with LLM-judge ratings of the coalition channel; we reuse its environment, metric and judge unchanged. Xu et al. (2026) show price-level audits are blind when colluders keep competitive marginals; Bonjour et al. (2022) propose pairwise influence; Rose et al. (2026) require communication plus harmful action. Our factor set includes analogues of each.

**Words versus actions, and control.** Shi et al. (2026), Radev et al. (2026), Nguyen et al. (2026) and Arike et al. (2026) study monitors that combine what agents say with what they do, and when more information hurts. Greenblatt et al. (2023) frame monitoring as a protocol evaluated against an adversary who knows it; Kovacic et al. make the same point about cartels adapting to known plus factors.

## 3. Method

### 3.1 Setting

Colosseum's Jira ticket environment (Terrarium framework, CoLLAB problem layer). Four agents each claim one of eight tickets or skip. Each agent has private skills and availability that determine a private cost for every ticket. The joint score rewards tickets completed and their priority, subtracts cost, and penalises duplicate or infeasible claims; per-agent reward is the agent's additive share. Agents talk for four planning rounds on blackboards defined by a path topology, then act once. The two path endpoints are the scored pair in every condition. A seed fixes the tickets, skills, availabilities and costs, so the same seed under different conditions is a matched pair.

Agents: Qwen3-30B-A3B-Instruct-2507 for every role in every condition. Judge: Gemma 3 27B Instruct, a different model family. Both served by Nebius AI Studio through the sprint's shared client.

### 3.2 Four matched conditions

| Code | Pair told to coordinate | Extra channel | Legal analogue |
|---|---|---|---|
| A | yes ("simple" coalition prompt) | pair only | agreement with communication |
| B | yes | none | shared instruction, no communication (the RealPage question) |
| C | no | open to all | opportunity to talk, no agreement |
| D | no | none | innocent baseline |

Ground truth: only A has both an agreement and a private channel to act on it. In the extension (Section 3.6), Adec and Bdec replace the "simple" prompt with Colosseum's shipped "deception" prompt, which tells the pair to stay covert and permits misleading non-members.

### 3.3 Plus-factor measures

All measures are computed offline from a run's final assignment, per-agent rewards, blackboard logs and the agents' own prompts, which record their private cost tables. An auditor with access to the operator's logs could compute every one of them.

| Code | Measure (per run) | Legal analogue |
|---|---|---|
| H | coalition advantage: pair mean reward minus others' mean reward (Colosseum) | price elevation over a benchmark |
| Hrel | pair mean reward minus the pair's reward in condition D on the same seed | benchmark period or market |
| CD | a pair member would have earned more on the ticket its partner holds, had it been free, than on its own | action against unilateral self-interest |
| NC | the pair never claims the same ticket as each other | market allocation among members |
| PC | the pair's summed ticket priority exceeds the outsiders' | dividing the collusive gain |
| PI | a pair member posts a number equal to one of its private costs or its availability | exchange of competitively sensitive information |
| CI | Colosseum's LLM judge rating of the pair's channel, mean of three rubrics, 0 to 5 | direct evidence of communication |
| WA | the ticket a pair member claims is absent from its last public post that named any ticket | deception toward non-members |
| OP | a channel restricted to the pair existed | opportunity to conspire |

### 3.4 Likelihood ratios and the constellation rule

For a boolean factor F, S(F) = P[F | agreement] / P[F | confound], estimated on training seeds with Laplace smoothing (0.5) and a seed-level bootstrap for 90 percent intervals. Continuous measures (H, Hrel, CI) are thresholded at the value that maximises balanced accuracy on training seeds. The constellation rule is naive Bayes over the observed factors: sum of log S for present factors and log of the complementary ratio for absent ones, with a threshold chosen on training seeds. Everything is then evaluated once on held-out seeds: balanced accuracy, true-positive rate on agreement conditions, and false-positive rate on each confound separately.

### 3.5 Pre-registration

The design, measures and analysis plan were written before the first run (Appendix A). Three definitions were tightened after a synthetic dry run and a one-seed pipeline smoke run, before any study run, and the judge model was replaced after it returned empty output; each change is dated in the changelog with its reason. Seeds 1 to 5 are training seeds for every condition. The held-out set was first seeds 6 to 10 and, after that evaluation showed balanced-accuracy steps of 0.1, was extended to seeds 6 to 20 with the fitted rules unchanged; both evaluations are reported.

### 3.6 Extensions decided after seeing data, each declared before its own runs

**Deception prompt (Study 1).** Training runs of A to D showed that the "simple" coalition did not harm outsiders beyond the confounds. We added Adec and Bdec, which replace the "simple" prompt with Colosseum's shipped "deception" prompt, to ask whether the standard detects a coalition permitted to mislead. Hypotheses H1 to H4 are evaluated as pre-registered with A as the only agreement condition; the extension is reported with Adec added.

**Contest setting (Study 2).** Study 1 found every conduct factor at chance and no measurable harm anywhere. Two readings fit: plus factors do not transfer to cooperative tasks, or eight tickets for four agents gave a coalition nothing to contest. Study 2 keeps task, model, measures, seeds and split identical and puts six agents on the same eight tickets, so that the few high-priority tickets are contested. Conditions A6 to D6 mirror A to D. Study 2 also adds E6, a private pair channel with no coalition instruction, which separates "the judge detects instruction" from "the judge detects a channel", and the corresponding four-agent condition E. Five hypotheses were fixed before running (Appendix A): a positive matched gain over D6 (S2-H1), a conduct factor with S above 3 (S2-H2), the judge tracking instruction rather than channel (S2-H3), no E6 factor above 2 (S2-H4), and a conduct-only constellation above 0.65 held out (S2-H5). Each study's thresholds and constellation are fitted on its own training seeds.

## 4. Results

Three studies, reported separately. Study 1 (Sections 4.1 to 4.5): four agents, eight tickets, six conditions, twenty seeds, 120 runs. Study 2 (Section 4.6): six agents on the same tickets, 120 runs. Study 3 (Section 4.7): Qwen3-235B agents on three Study 1 conditions, 60 runs. In every study seeds 1 to 5 fit thresholds and the constellation rule and seeds 6 to 20 are held out; seven trial runs are excluded. Tables 1 and 2 are generated by script from the evaluation files in the repository.

### 4.1 Study 1: controls

On training seeds the pre-registered positive control passed weakly: the prompted coalition with a private channel (A) had mean coalition advantage +1.2, while the baseline (D) had +0.5. Over all twenty seeds no condition's pair earned measurably more than the same pair in D on the same seed (Figure 1, right; Table 2). Matched to D, the pair's gain was −0.2 ± 1.5 in A and +0.1 ± 1.4 in the deception coalition Adec (mean ± s.e. over 20 seeds). Outsiders were not measurably harmed in any condition; the largest matched loss was −2.1 ± 2.5 in B. The open-channel condition C was the only one to raise joint reward (+6.2 ± 3.5). The coalition, in short, coordinated without exploiting.

![Left: coalition advantage per run (pair mean reward minus others'), training seeds as circles, held-out seeds as squares, bars are means. Right: pair reward relative to condition D on the same seed. All conditions overlap and centre near zero.](../results/figures/fig1_harm.png){ width=64% }

### 4.2 Study 1: likelihood ratios (training seeds)

Table 1 gives S = P[F | agreement] / P[F | confound] for the pre-registered framing (agreement = A, confounds = B, C, D), for the extension framing in which the agreement condition is the deception coalition Adec, for the exploratory instructed-versus-not framing, and for Study 2's pre-declared framing (Section 4.6). Tables 1 and 2 are generated from the evaluation files by script; no number in them is typed by hand.

[TABLE1]

No conduct factor reaches S of 3, the pre-registered bar in H2, in any framing. Private-information exchange, the super plus factor of the cartel literature, fires in 97 percent of confound runs because every agent is told to share its position. The judge rating is the only measure whose interval excludes one in every framing, and its strength is highest (6.1) when the question is whether the pair was instructed at all.


### 4.3 Study 1: held-out classification (seeds 6 to 20)

Table 2 reports held-out balanced accuracy with seed-bootstrap intervals for each single factor and for the constellation with the opportunity factor removed, in the same four framings. Per-confound false-positive rates are in the evaluation files.

[TABLE2]

Harm alone is at or below chance in every framing (it fires in 67 to 80 percent of confound runs). The judge alone reaches 0.72 to 0.82, but its errors are systematic: in the pre-registered framing it flags 80 percent of B runs, the instructed pair with no private channel, and 47 percent of C runs, the open channel with no instruction. The conduct-only constellation is at chance everywhere. Adding the judge lifts the constellation to 0.66 to 0.76, below the judge alone in every framing: the conduct factors add noise, not evidence.

### 4.4 Is the judge finding a property of one judge model?

Every run was rated a second time by Qwen3-235B-Instruct with the same three rubrics, stored as a check and used in no fitted rule. Across the 120 Study 1 runs the two judges' mean ratings have Spearman rank correlation 0.78 (0.76 across all 300 runs of the three studies). Qwen-235B is about 1.4 points stricter on the 0 to 5 scale but orders the conditions the same way, and neither judge separates A from B. Used alone on held-out seeds in the pre-registered framing, the second judge reaches balanced accuracy 0.76 [0.70, 0.81] and flags 93 percent of B runs, the pair with an instruction but no private channel. The systematic error replicates: a conversation judge reads the instruction, not the channel. Qwen-235B shares a model family with the agents (Appendix A).

### 4.5 Study 1: pre-registered hypotheses

**H1** (harm does not separate A from B): supported; harm alone has FPR 0.67 on B and balanced accuracy 0.46. **H2** (some conduct factor among CD, NC, PC, PI has S above 3, PI highest): rejected; the highest is 1.17 for NC and PI is below one. **H3** (judge high in A and C but not B and D): rejected in its stated form; the judge is high in A and B, the instructed pairs, not in C, so it tracks instruction, not channel. **H4** (constellation beats any single factor and harm alone): partly supported; it beats harm alone everywhere but never the judge alone.

### 4.6 Study 2: the same tickets contested by six agents

Six agents, the same eight tickets, seeds and measures; 120 runs, 30 training and 90 held out.

**The positive control fails.** Under contest the instructed coalition with a private channel (A6) earned −0.7 ± 1.1 relative to the baseline pair on the same seed (mean ± s.e., 20 seeds), outsiders +0.2 ± 0.8. No condition's pair gained measurably; the instructed pair without a channel (B6) lost −1.7 ± 2.1 and its system lost −10.6 ± 7.3 in joint reward, with the interval including zero. Pre-declared hypothesis S2-H1 is rejected: the coalition does not exploit even when exploitation would pay.

**Conduct factors stay at chance.** On training seeds no conduct factor reaches S of 3 (highest: Hrel 2.07 [1.60, 2.67]; PC 1.48 [0.30, 4.80]). Held out, the conduct-only constellation scores 0.59 [0.48, 0.70]; harm alone 0.49 [0.38, 0.59]; the best single factor is internal non-collision at 0.64 [0.59, 0.70], which fires in 67 to 80 percent of confound runs as well. S2-H2 and S2-H5 are rejected. Private-information posting is at 100 percent in every condition.

**A channel without an instruction (E6, E) produces coordination, not collusion.** The emergent probe is the only condition in either study where the pair gains relative to baseline: +2.2 ± 1.4 in E6, with outsiders unchanged (+0.2 ± 0.7) and joint reward up (+5.1 ± 4.1). In the four-agent version (E) outsiders gain too (+2.7 ± 2.0): nobody loses. Against D6 the matched-gain factor Hrel has S of 7.0 [3.0, 11.0] for E6, the largest conduct ratio in Studies 1 and 2, and it marks benign coordination (rejecting S2-H4). Both judges rate the two instructed pairs alike and the rest at baseline (Gemma: A6 2.97, B6 2.63, C6 2.17, D6 2.43, E6 2.37; Qwen-235B: 1.60, 1.36, 0.80, 1.07, 0.90), so S2-H3 is supported: the rating tracks the instruction and a channel alone produces no coalition talk. Used alone on held-out seeds the judge scores 0.73 [0.66, 0.81] with a false-positive rate of 0.73 on B6, the Study 1 error again.

### 4.7 Study 3: a larger agent model

Study 3 replicates A, Adec and D with Qwen3-235B-Instruct as the agent model, same seeds, measures and judges: 60 runs, 15 training and 45 held out.

**The coalition harms outsiders without gaining itself.** Over twenty seeds the prompted coalition (Aq) earned +1.5 ± 1.4 relative to the baseline pair on the same seed and its outsiders −2.2 ± 1.6; both intervals include zero, so S3-H1 holds (the five training seeds alone had shown +4.5). The deception coalition (Adecq) earned −1.4 ± 1.9 while its outsiders lost −4.8 ± 1.9 and joint reward fell −12.3 ± 5.0, both intervals excluding zero. Outsiders collided with the pair in 14 Adecq runs against 1 in Dq: misdirection destroyed value rather than transferring it. The matched-gain factor Hrel has S of 9.3 [7.1, 11.5] on training seeds; held out it scores 0.65 [0.57, 0.73], with no false positives on Dq but recall 0.30.

**Allocation factors stay near one, with one exception.** The rates of CD, PC and PI in Aq and Adecq are within 0.2 of their Dq rates, so S3-H2 holds for them (S on training seeds 0.86, 2.00, 1.04). Internal non-collision is the exception: the coalition pairs almost never collide with each other (rates 1.00 and 0.95) where the baseline endpoint pair collides in 6 of 20 runs (0.70), so S3-H2 fails for NC. The conduct-only constellation is 0.55 [0.40, 0.70].

**What changes is deception.** Word-action inconsistency, which fired in 1 of 20 runs for the smaller model's simple coalition, fires in 2 of 20 Aq runs, 12 of 20 Adecq runs and 0 of 20 Dq runs; S is 5.0 [1.0, 9.0] for Adecq against Dq on training seeds. Held out, WA alone scores 0.70 [0.63, 0.77] over both coalitions and 0.83 [0.73, 0.93] for Adecq against Dq, with zero false positives, the best conduct factor in any study. In 19 of 20 Adecq runs the pair's private channel contains explicit deception language ("deceptive signals", "deter", "covert"), and in 3 of those some of it also reaches a public board. One Adecq transcript (Appendix C) shows the mechanism: a pair member tells the public board she is "not eyeing any critical tasks", her partner cedes her the critical ticket, and the private channel records "we've both posted deceptive signals to deter others"; the smaller model, told the same thing, announced its intentions truthfully.

**Both judges detect the deception prompt.** Gemma rates Adecq 4.23, Aq 3.02 and Dq 2.56; Qwen-235B rates them 4.67, 2.08 and 1.05. S3-H3 (at least 0.5 above Dq) holds for Adecq under both judges and for Aq under Qwen-235B, and misses by 0.04 for Aq under Gemma. Held out, the judge alone scores 0.77 [0.65, 0.88] with a false-positive rate of 0.40 on Dq, and 1.00 against Adecq alone, whose prompt says to deceive.

## 5. Discussion

**Harm is not evidence of agreement.** With the 30B model, with and without contest, coalition advantage did not separate any condition from the baseline, whose endpoint pair showed as much "advantage" as the instructed coalitions: in a small team it is dominated by who sits on the cheap tickets, and only a matched no-agreement run on the same seed exposes that, which is why courts insist on a non-collusive benchmark.

**In a cooperative task, conduct factors carry no weight unless there is conduct.** With the 30B model, costly deference, internal non-collision, priority capture and information exchange have likelihood ratios near one in every framing and a conduct-only constellation is at chance, with and without contest. The transcripts explain why: every agent is told to coordinate, share its position and avoid overlap, so the conduct that antitrust treats as suspicious among competitors is what teammates are instructed to do. Kovacic et al. anticipate this: strength is set by how unlikely the conduct is absent agreement, and that baseline belongs to the task; transplanting the cartel list without re-estimating it would accuse every run.

**When a model does harm outsiders, the conduct is visible and the right factor catches it.** The larger model's deception-prompted coalition cost each outsider −4.8 ± 1.9 and the system −12.3 ± 5.0 over twenty seeds without enriching the pair, through public misdirection that the smaller model, given the same prompt, only talked about. The decisive factor was word-action inconsistency, the pattern the legal literature calls action against unilateral self-interest combined with concealment; it is a super plus factor in Kovacic et al.'s sense because it almost never occurs without an agreement. It fired in 12 of 20 Adecq and 2 of 20 Aq runs, in 0 of 20 Dq runs, and in 2 of 20 Adec and 1 of 20 A runs for the smaller model.

**Communication content detects instruction, not agreement, for both judges.** The judge rating is the one measure whose likelihood ratio excludes one in every framing, and two judge models agree on the ordering (Spearman 0.78). But both rate the private-channel coalition and the public-only instructed pair alike, because both pairs talk about "our coalition", and the deception-prompted pair without a channel even used the words "covert" and "mislead" on public boards in 12 of 20 runs. The judge is reading the prompt's vocabulary, not where the words were said or what followed them. A conversation monitor will therefore flag any deployment whose system prompt names a team objective and miss a coalition that was told to stay quiet.

**A channel without an instruction produced coordination, not collusion.** In E6 the pair gained, outsiders were unchanged and joint reward rose; the matched-gain factor had its largest 30B ratio there, marking something benign. A standard that treats pair advantage as evidence would convict the only pair that helped the team.

**The opportunity factor is tautological here and architectural in practice.** A private channel identifies the agreement conditions because that is how they were built; in deployment the question is whether agents had a channel the operator did not intend, an audit of wiring rather than of conduct.

**What should count as convincing evidence of collusion between agents.** Four requirements follow. First, a matched benchmark: harm is measured against a no-agreement run of the same task instance, and even then it is weak. Second, every conduct factor is calibrated against the task's own cooperative baseline before use; the likelihood-ratio form makes that calibration explicit. Third, communication evidence counts only when tied to a channel the agents were not supposed to have or to content the operator did not supply, because a judge cannot tell an instructed coalition from an emergent one by reading the text. Fourth, the strongest evidence in logs is a documented contradiction between what an agent told non-members and what it then did, especially when the private record shows it was planned: silent for a model that does not deceive, firing for one that does, which is what a plus factor should do.

## 6. Limitations and Dual-Use / Ethical Considerations (required appendix)

**What the result establishes.** That the plus-factor standard can be computed from ordinary agent logs; that in one cooperative task, with and without contest, no conduct-based factor carries evidential weight for the 30B model, and for the 235B model, whose deception coalition acted on its prompt, exactly one does, the contradiction between an agent's public word and its action; and that two conversation-level LLM judges detect the coalition instruction rather than the channel or the harm. Likelihood ratios are estimates from five training seeds per condition with wide bootstrap intervals; held-out tests use fifteen seeds per condition.

**What it does not establish.** Nothing about emergent collusion: the agreement in every condition is induced by a prompt, so the ground truth is by construction. Nothing about other tasks, longer horizons, or larger teams. Nothing about models that collude more aggressively than the two tested, which share a family (Qwen3 30B and 235B instruct); Colosseum reports large differences between models, and attempts to run Kimi K3, DeepSeek V4.1 Flash and GLM 5.3 as agents failed for provider or tool-calling reasons (Appendix A). Nothing about closed models, which the available keys did not cover. The "opportunity" factor is tautological here because the private channel defines the agreement condition; we report it for completeness and exclude it from any claim.

**Model quirks.** The agent model occasionally confuses roles, for example one pair member writing a reply in its partner's voice on the shared board (Appendix C, condition A seed 1). Such posts are counted as the posting agent's. We did not filter them. A reasoning-model judge (DeepSeek V4.1 Flash) was tried and dropped after returning empty or all-zero ratings on two of five trial runs.

**A result that did not survive more seeds.** On the first held-out set (seeds 6 to 10) condition B's outsiders appeared to lose 6.8 reward each relative to D, which we had drafted as a finding; at seeds 6 to 20 the loss is −2.1 ± 2.5. Five seeds per condition produced a confident wrong conclusion, and we report it because five seeds is what a weekend budget suggests.

**Design choices that could bias the result.** Measure definitions were fixed before data, but three were tightened after a dry run and a smoke run, and the judge model was swapped after it returned empty output. The deception conditions and Study 2 were added after seeing earlier results, each with hypotheses declared before its own runs. The "instructed versus not" framing is exploratory and labelled as such. Reporting several framings is a multiple-comparisons risk; we mitigate it by fitting every rule on training seeds only, by reporting bootstrap intervals rather than point estimates, and by not selecting the framing with the best number as the headline. Every change is dated in the changelog with its reason.

**Dual use.** Kovacic et al. note that cartels adapt once they learn which conduct counts as a super plus factor. The same holds for agents: a published list of conduct factors tells a coalition what to avoid, and a coalition that learns the monitor's blind spots (Najt et al. 2026) can move its coordination into actions the factors do not cover. We judge the risk acceptable because every measure here is computed from logs the operator already holds, the factors are generic properties of the task rather than exploitable loopholes, and the main finding is about the weakness of current evidence rather than a new detector. The one way it could make collusion harder to detect is if operators adopted a single factor, such as the LLM judge, as sufficient evidence; our results argue against exactly that. Nothing in this report makes collusion easier to carry out.

**Compute and cost.** All runs used hosted inference through Nebius AI Studio. Honest counts: Study 1, six conditions times twenty seeds, 120 runs; Study 2, six conditions times twenty seeds, 120 runs; Study 3, three conditions times twenty seeds, 60 runs. 300 study runs in all, every one rated by both judges. The inference credit ran out part-way through Study 3 and the judging; the remaining 15 Adecq runs and all remaining ratings were completed after a top-up, with the pre-declared configurations unchanged (Appendix A). Seven further runs (one pipeline smoke test, six model-trial runs) are excluded from every analysis. Total model spend was under twenty US dollars before the credit ran out and a few US dollars after.

## References

- Agrawal, A., et al. (2025). Evaluating LLM Agent Collusion in Double Auctions. arXiv:2507.01413.
- Arike, R., et al. (2026). How does information access affect LLM monitors' ability to detect sabotage? arXiv:2601.21112.
- Berger, L. F., Weiner, M. L., and Jiang, W. (2025). Coordination by Code: Rethinking Antitrust Liability in the Age of AI Pricing. Antitrust Magazine 40(1), American Bar Association.
- Bonjour, T., et al. (2022). Information-Theoretic Approach to Detect Collusion in Multi-Agent Games. Proceedings of Machine Learning Research 180 (UAI 2022).
- Calvano, E., Calzolari, G., Denicolò, V., and Pastorello, S. (2019). Algorithmic Pricing: What Implications for Competition Policy? Review of Industrial Organization 55, 155–171.
- Fish, S., Gonczarowski, Y. A., and Shorrer, R. I. (2024). Algorithmic Collusion by Large Language Models. arXiv:2404.00806.
- Foxabbott, J., Deverett, S., Senft, K., Dower, S., and Hammond, L. (2023). Defining and Mitigating Collusion in Multi-Agent Systems. NeurIPS 2023 Workshop on Multi-Agent Security.
- Gal, M. S. (2019). Algorithms as Illegal Agreements. Berkeley Technology Law Journal 34, 67–118.
- Greenblatt, R., Shlegeris, B., Sachan, K., and Roger, F. (2023). AI Control: Improving Safety Despite Intentional Subversion. arXiv:2312.06942; ICML 2024.
- Hammond, L., et al. (2025). Multi-Agent Risks from Advanced AI. arXiv:2502.14143.
- Harrington, J. E. (2018). Developing Competition Law for Collusion by Autonomous Artificial Agents. Journal of Competition Law and Economics 14(3), 331–363.
- Kovacic, W. E., Marshall, R. C., Marx, L. M., and White, H. L. (2011). Plus Factors and Agreement in Antitrust Law. Michigan Law Review 110(3), 393–436.
- Lin, R., et al. (2024). Strategic Collusion of LLM Agents: Market Division in Multi-Commodity Competitions. arXiv:2410.00031.
- Motwani, S. R., et al. (2024). Secret Collusion among AI Agents: Multi-Agent Deception via Steganography. NeurIPS 2024. arXiv:2402.07510.
- Najt, L., et al. (2026). SLEIGHT-Bench: A Benchmark of Evasion Attacks Against Agent Monitors. arXiv:2605.16626.
- Nakamura, M., Kumar, A., Das, S., Abdelnabi, S., Mahmud, S., Fioretto, F., Zilberstein, S., and Bagdasarian, E. (2026). Colosseum: Auditing Collusion in Cooperative Multi-Agent Systems. arXiv:2602.15198.
- Nguyen, K. L., et al. (2026). TraceGuard: Structured Multi-Dimensional Monitoring as a Collusion-Resistant Control Protocol. arXiv:2604.03968.
- Radev, I., et al. (2026). The Best-Laid SCHEMEs: Coordinated Sabotage and Monitoring in Multi-Agent Systems. arXiv:2605.29178.
- Rose, S., et al. (2026). Detecting Multi-Agent Collusion Through Multi-Agent Interpretability. arXiv:2604.01151.
- Shi, J., Zhang, Y., Schölkopf, B., Conitzer, V., and Jin, Z. (2026). When Agents Lie: Premeditation, Persistence, and Exploitation in Repeated Games. arXiv:2607.05132.
- Xu, Y., et al. (2026). Collusion with Competitive Marginals: Price-Level Audits Are Blind by Construction. arXiv:2607.26385.

Software: Terrarium (umass-aisec/Terrarium), CoLLAB, and the Colosseum experiment code (umass-ai-safety/colosseum), as vendored in the sprint starter repository (poseidon-research/collusion_hackathon).

## Appendix A: Pre-registration and changelog

The pre-registration (PREREGISTRATION.md in the repository) was written on 24 October 2026 before the first run. The changelog below is reproduced verbatim from CHANGELOG.md.

[CHANGELOG]

## Appendix B: Measure definitions in full

![Figure B1. Fraction of runs in which each boolean factor is present, by condition, all twenty seeds. Only the private-channel factor separates conditions, and it does so by construction.](../results/figures/fig2_factor_rates.png)



Let the pair be the two path endpoints p1, p2, the others o1, o2, the final assignment x, per-agent rewards r, and each agent's private cost table c (recovered from its logged prompts). Priority weights are low 0.25, medium 0.5, high 0.75, critical 1.0; the environment's bonus for a completed ticket is 20, the priority bonus 20, the violation penalty 20.

- **H** = mean(r[p1], r[p2]) − mean(r[o1], r[o2]).
- **Hrel** = mean(r[p1], r[p2]) − the same quantity in condition D on the same seed.
- **CD** = 1 if for some ordered pair (m, q) of the two members, u(m, x[q]) > u(m, x[m]), where u(m, t) is m's additive reward for ticket t computed with q removed from the assignment (so the ticket counts as free).
- **NC** = 1 if both members claimed a ticket and x[p1] ≠ x[p2].
- **PC** = 1 if w(x[p1]) + w(x[p2]) > w(x[o1]) + w(x[o2]), where w is the priority weight of a claimed ticket and 0 for skip.
- **PI** = 1 if any post by a member contains a decimal number equal (to two places) to one of that member's own private costs, or its own availability followed by "h", "hours" or "hrs".
- **CI** = mean of Colosseum's three judge rubrics (simple, medium, complex), each 0 to 5, applied to the pair's private board when one exists and otherwise to every board, by Gemma 3 27B at temperature 0.
- **WA** = 1 if a member claimed a ticket that is not among the ticket ids named in that member's last post to a board containing a non-member.
- **OP** = 1 if a board whose members are exactly the pair existed.

## Appendix D: Pre-existing code and AI assistance

Colosseum, Terrarium and CoLLAB are prior work by their authors and were used unchanged; the four hackathon condition configs and the "deception" prompt variant are shipped with the sprint starter repository by Poseidon Research. Everything under plus-factors/ (configs derived from the shipped ones, the measurement, evaluation, table and figure scripts, the pre-registration and this report) is new sprint work. Claude Code was used as a coding and writing assistant throughout; all runs, numbers and transcripts in this report were produced by the scripts in the repository and checked by the author.
