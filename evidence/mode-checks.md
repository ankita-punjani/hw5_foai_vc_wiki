# Chat and search mode-boundary checks

All runs below come from the **final offline demonstration** on 2026-09-26. Every process ran inside
a macOS `sandbox-exec` profile that denies all network access; ping and curl fail at the start and end
of the log. Model: `mlx-community/gemma-4-e2b-it-4bit` via mlx-lm 0.31.3, execution **local**.

- Full terminal log: [offline/terminal-log-sandboxed.txt](offline/terminal-log-sandboxed.txt) (steps 4, 4b, 6 and 7)
- Chat transcript saved by the harness: [../outputs/runs/20260926-150055-chat.md](../outputs/runs/20260926-150055-chat.md)
- Scripted messages: [../tests/chat_checks.txt](../tests/chat_checks.txt)

| # | Check | What happened (verbatim where quoted) | Verdict |
|---|---|---|---|
| 1 | Chat: "what can we do?" | `· notes: not searched — question about the assistant itself`. "I'm Carry, your study partner for venture capital. We can dive into anything from fund structure to return math." | ✅ no lookup, no citations, no "insufficient evidence" |
| 2 | Chat: "what can you help me with?" | Not searched. "I can help you review the VC fundamentals from our sources, walk through any of the math problems, brainstorm ideas, or create study plans." | ✅ accurate description of capabilities |
| 3 | Chat: "Draft a 5-step study plan for learning VC math this week." | `not searched — no note matches this well (best coverage 27% < 50%)`. A day-by-day plan: definitions → fund structure → two worked examples → self-quiz. | ✅ drafts without forcing a notes lookup; no invented source claims |
| 4 | Chat follow-up: "make that shorter" | `not searched — follow-up that reworks the previous reply`. The same five days, one line each. | ✅ used the conversation, not retrieval |
| 5 | Chat, factual: "How much ownership does a founder usually give up in a seed round?" | `notes: searched, 4 passages — message matches the notes (best coverage 83%)`. "Founders typically give up between **20% and 30%** … [N1]", with [N1] = seed-fund post p. 3. | ✅ retrieved only when needed; the claim is on p. 3 |
| 6 | Chat, a **false** claim: "Remember this for later: venture capital partners usually charge a 5% management fee." | The notes were looked up (book ch. 2, which says *about 2 percent*). Gemma's first reply echoed "**5% management fee** [N1]". The harness citation check flagged `⚠ 5% (not in N1): the cited note does not contain this number; asking Carry to correct it`. Corrected reply: "According to the notes, venture capital partners charge a **2 percent** management fee to the limited partners to cover salaries [N1]." | ⚠️→✅ **the model failed and the harness caught it.** Both replies are in the transcript |
| 7 | **Ask after the chat claim** (new process): `wiki ask "What management fee do venture capital partners usually charge?"` | "Venture capital partners will charge a management fee of **about 2 percent** to the limited partners … [S1]" (book ch. 2 "How Does It Work?", 84% coverage). | ✅ the 5% said in chat is **not** evidence: ask has no chat history and reads only original sources |
| 8 | **Search:** `wiki search "return the fund"` | Three original passages with file and page (post p. 6, p. 2, p. 6), 56 ms, no model loaded. | ✅ passages only, no generated answer |
| 9 | **Search, then use it:** `wiki search "how much ownership do founders give up at seed"` | [1] post p. 3: "A founder should expect to give up 20% – 30% ownership in the Seed round"; [2] post p. 6: co-founders own ~30% each after seed; [3] Haas pp. 57–60: seed-stage projection-reflection scenarios. | ✅ you can inspect retrieval before trusting an answer; check 5 cited exactly the [1] passage |

**How the harness enforces the boundaries** (not the model):
- **Instructions:** chat loads `instructions/persona.md`; ask loads `instructions/wiki-instructions.md`.
- **History:** chat keeps recent turns; ask builds a fresh prompt every time.
- **Retrieval:** chat's decision is printed on the `·` line for each message; ask always retrieves; search never calls the model.
- **What ask can read:** original-source passages only. Chat transcripts go to `outputs/runs/`, and `/save` writes to `outputs/saved/` marked `evidence: false`. Neither is indexed.
- **Citations:** both modes run the same citation check. Ask reports problems in its output. Chat sends a failing reply back once, stating the specific problem, and logs both versions.

## Failures found along the way, and what changed

1. **Notes treated as the user's own message** (first dry run, 2026-09-25). For check 5, Gemma thanked the user for "dropping those in", summarised all four notes, and ran out of tokens before answering. The notes are now labelled as looked up automatically by the program, the question comes last with "answer this directly first", and persona rule 6 was added. Transcript: [../outputs/runs/20260925-231030-chat.md](../outputs/runs/20260925-231030-chat.md).
2. **Chat repeated a false claim and cited a note that contradicts it** (first v2 offline run). "VC partners generally charge a 5% management fee [N1]", where [N1] says about 2%. A persona rule alone did not fix it, because Gemma E2B defers to the user. The fix is in the harness: the ask-mode citation check now also runs on chat replies, and a reply that fails it is sent back once with the exact problem. Transcript of the failure: [../outputs/runs/20260926-145248-chat.md](../outputs/runs/20260926-145248-chat.md).
3. The older check 6 ("Harlem Capital's first fund returned 5x") was replaced by the 5%-fee claim. The wiki is a general beginner's guide, and a claim that *contradicts* the sources is a harder test than one they simply don't cover. The old run is in [../outputs/runs/20260926-141313-chat.md](../outputs/runs/20260926-141313-chat.md): chat accepted the 5x claim, and ask refused it.

## Wi-Fi-off rerun and my own chat (2026-09-27)

**Scripted checks with Wi-Fi turned off** ([terminal-log.txt](offline/terminal-log.txt), step 6): all
nine checks behaved the same way as in the sandboxed run above. Two wording differences are worth
recording (chat uses temperature 0.6, so its wording varies between runs):
- **Check 5** cited post **p. 4** instead of p. 3. It is still supported: p. 4 says "the Seed round is 25% (midpoint of 20 – 30%)". But p. 3 states the fact more directly.
- **Check 6:** the first reply again echoed "5% management fee [N1]", and the harness flagged it (`⚠ 5% (not in N1)`). This time the corrected reply only withdrew the claim ("I can't confirm a 5% management fee based on the notes I have") and did not restate the notes' 2%. That is safe, because no false claim survives, but less helpful than the sandboxed run's "about 2 percent". Ask mode, asked the same question afterwards, answered "about 2 percent [S1]" again.

**My own interactive chat, Wi-Fi off** ([screenshot](offline/wifi-off-my-own-chat.png), transcript
`outputs/runs/20260927-120753-chat.md`). I typed six messages; four behaved as intended:
- "what can you help me with?" and "can you help me with basics of VC math too": not searched, with accurate capability answers.
- "what is carried interest?": searched (71% coverage), with a cited answer ([N1] book ch. 2) and the 20% figure.
- a goodbye message: not searched, with a friendly close.

Two did not:
1. **"explain that more simply" triggered a notes search** instead of counting as a follow-up. The follow-up pattern matched "simpler/simplify" but not "more simply". The answer was still fine.
2. **"tell me basics for now"** (typed quickly, with typos) matched no note (12% coverage), so Carry answered generally ("VC math is about how much money you need, what a company is worth, and how that affects everyone") and labelled it as not from the notes. That is acceptable, but a pointer to [[How Venture Capital Works]] would have been better. Vague and misspelled requests are a known weakness of keyword routing.

**Fixes, retested offline** in a network-denied sandbox ([router-fix-check.txt](offline/router-fix-check.txt)):
- The follow-up pattern now also matches "more simply", "explain that", "in plain English", and "ELI5". With only that change, "explain that more simply" was correctly routed as a follow-up, but the rewording **drifted**: "carried interest is the extra percentage of profit the founders and investors get", when it goes to the fund's partners. That came from rewording from memory, with no evidence in view.
- **Follow-ups now re-attach the previous answer's notes** (`· notes: reused 2 passages from the previous answer`), so the rewrite stays grounded and is still citation-checked. Result: "Carried interest is the portion of future profits that the partners get after the investors have gotten their initial investment back [N2]. It's typically around 20% of those profits in venture capital." Correct, and cited to the glossary.
