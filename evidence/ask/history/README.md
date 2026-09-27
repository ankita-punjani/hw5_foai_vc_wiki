# Earlier ask-mode runs (kept, not replaced)

`wiki eval` never overwrites a card: the previous card is moved here. **The timestamp in each filename
is when the card was *replaced*, not when it ran.** Runs whose answers were byte-identical to the
next run were removed as duplicates (generation is greedy, temperature 0).

| Files | What run it was | Network | Harness / rules | What it shows |
|---|---|---|---|---|
| `T*-20260925-230834…230851` | test set **v1**, first dry run | online | research rules v1 | T3 used only the glossary definition and gave no worked examples |
| `T*-20260926-141206…141229` | v1, second dry run | online | + "include the passages' numbers", "walk through worked examples" | T3 now uses both sources; T1 and T4 unchanged |
| `T*-20260926-144237…144309` | v1, offline (sandboxed) | offline | same | identical answers offline; v1 T1/T4 were Harlem-specific questions |
| `T*-20260926-145144…145207`, `B*-20260926-145312…145407` | test set **v2** + beginner set, first offline run | offline | same | **T4 v2 FAILED**: an invented "hurdle rate" definition, cited (assessment written in the card). B8 gave a grounded but partial answer |

The current cards in `../` come from the final offline run: test set v2, plus the unknown-term
signal added after the T4 failure. That signal fixed T4 and correctly refuses B7. Its cost is that
B8 became a cautious refusal. Each current card's assessment explains this.
