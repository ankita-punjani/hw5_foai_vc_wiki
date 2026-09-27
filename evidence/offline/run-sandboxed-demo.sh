#!/bin/bash
# Same offline demo, but with network access denied by the macOS kernel sandbox
# (sandbox-exec) for this script and every process it starts. Used when Wi-Fi
# could not be turned off; the rest of the Mac stays online.
cd "$(dirname "$0")/../.." || exit 1
export DEMO_MODE='network denied to every process by macOS sandbox-exec profile "(deny network*)" (Wi-Fi itself still on)'
export DEMO_LOG=evidence/offline/terminal-log-sandboxed.txt
exec sandbox-exec -p '(version 1)(allow default)(deny network*)' /bin/bash evidence/offline/run-offline-demo.sh
