#!/bin/bash
# Offline demonstration. Turn Wi-Fi OFF first, then run from anywhere:
#     ~/vc-wiki/evidence/offline/run-offline-demo.sh
# Every command is a fresh process (the CLI is "restarted" for each step).
# Everything printed is also saved to evidence/offline/terminal-log.txt.

cd "$(dirname "$0")/../.." || exit 1
LOG=${DEMO_LOG:-evidence/offline/terminal-log.txt}
exec > >(tee "$LOG") 2>&1
echo "offline mode: ${DEMO_MODE:-Wi-Fi turned off by the user}"

step() { printf '\n\n########## %s ##########\n$ %s\n' "$1" "$2"; }

step "0. Proof the internet is unreachable" "date; networksetup -getairportpower en0; ping / curl"
date
networksetup -getairportpower en0 2>/dev/null || true
ping -c 1 -t 3 1.1.1.1 >/dev/null 2>&1 && echo "ping 1.1.1.1: REACHABLE (still online!)" || echo "ping 1.1.1.1: unreachable"
curl -sS -m 8 -o /dev/null https://huggingface.co && echo "curl huggingface.co: REACHABLE (still online!)" || echo "curl huggingface.co: failed -> offline"

step "1. Help" "./wiki --help"
./wiki --help

step "2. Status (model cached locally, index, wiki, links)" "./wiki status"
./wiki status

step "3. Ingest one source offline (re-index + Gemma redrafts into data/drafts/, reviewed notes untouched)" \
     "./wiki ingest 'vault/raw/Harlem Capital - Return the Fund.pdf' --redraft"
echo "wiki notes before: $(find vault/wiki -name '*.md' | wc -l | tr -d ' ')"
/usr/bin/time -l ./wiki ingest "vault/raw/Harlem Capital - Return the Fund.pdf" --redraft
echo "wiki notes after:  $(find vault/wiki -name '*.md' | wc -l | tr -d ' ')  (same count = no duplicates)"

step "4. Search mode: original passages only, no model" "./wiki search 'return the fund'"
./wiki search "return the fund" -k 3
step "4b. Search a topic before asking about it" "./wiki search 'how much ownership do founders give up at seed'"
./wiki search "how much ownership do founders give up at seed" -k 3

step "5. The four ask-mode tests (writes evidence/ask/T1-T4.md)" "./wiki eval"
/usr/bin/time -l ./wiki eval

step "6. Chat mode-boundary checks" "./wiki chat --script tests/chat_checks.txt"
./wiki chat --script tests/chat_checks.txt

step "7. Ask must not treat the chat-only claim (5% fee) as evidence" "./wiki ask \"What management fee do venture capital partners usually charge?\""
./wiki ask "What management fee do venture capital partners usually charge?"

step "7b. Extended beginner questions (writes evidence/ask/B1-B8.md)" "./wiki eval --tests tests/beginner_questions.yml"
./wiki eval --tests tests/beginner_questions.yml

step "7b-2. Follow-up (not a pre-registered test): B8 rephrased in the sources' own words" "./wiki ask \"Why can't traditional valuation methods be used for a VC-funded company?\""
./wiki ask "Why can't traditional valuation methods be used for a VC-funded company?"

step "7c. Audit every number in every wiki note against its cited source" "./wiki verify"
./wiki verify

step "8. Useful errors" "./wiki ask 'x' --mode online ; ./wiki ingest missing.pdf"
./wiki ask "x" --mode online
./wiki ingest missing.pdf

step "9. Still offline at the end" "ping / curl"
date
ping -c 1 -t 3 1.1.1.1 >/dev/null 2>&1 && echo "ping 1.1.1.1: REACHABLE" || echo "ping 1.1.1.1: unreachable"
curl -sS -m 8 -o /dev/null https://huggingface.co && echo "curl huggingface.co: REACHABLE" || echo "curl huggingface.co: failed -> offline"
echo; echo "Done. Log saved to $LOG"
