#!/usr/bin/env python3
"""
Patches src/simulation/servo_lib.py to log self._u_delta (the amplitude-
dependent servo position error that drives the K/J lookup tables) to a CSV
file, so we can check whether ZN test runs stayed in the small-signal
regime or pushed the servo into its softened large-error dynamics.

Run once from inside the AeroVECTOR repo root:
    python3 patch_servo.py
"""
import re

path = "src/simulation/servo_lib.py"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

original = content

# 1. Initialize the history list right after self._u_delta = 0 in __init__
anchor1 = "        self._u_delta = 0\n        self._t_prev = -0.0001"
if anchor1 not in content:
    print("ERROR: anchor1 not found -- file may differ from expected. "
          "No changes made.")
    raise SystemExit(1)
replacement1 = (
    "        self._u_delta = 0\n"
    "        self._u_delta_history = []  # [instrumentation]\n"
    "        self._t_prev = -0.0001"
)
content = content.replace(anchor1, replacement1, 1)

# 2. Log u_delta every time it's computed in _update()
anchor2 = (
    "        self._u_delta = abs(self._u-self._out_s[0,0]) "
    "* self._actuator_weight_compensation\n"
    "        K = self.K(self._u_delta)"
)
if anchor2 not in content:
    print("ERROR: anchor2 not found -- file may differ from expected. "
          "No changes made.")
    raise SystemExit(1)
replacement2 = (
    "        self._u_delta = abs(self._u-self._out_s[0,0]) "
    "* self._actuator_weight_compensation\n"
    "        self._u_delta_history.append((self._t_prev, self._u_delta))  "
    "# [instrumentation]\n"
    "        K = self.K(self._u_delta)"
)
content = content.replace(anchor2, replacement2, 1)

# 3. Add an export method right before def test(self, u_deg):
anchor3 = "    def test(self, u_deg):"
if anchor3 not in content:
    print("ERROR: anchor3 not found -- file may differ from expected. "
          "No changes made.")
    raise SystemExit(1)
replacement3 = (
    "    def export_u_delta_log(self, path='u_delta_log.csv'):\n"
    "        \"\"\"[instrumentation] Dump logged u_delta history to CSV.\"\"\"\n"
    "        with open(path, 'w', encoding='utf-8') as f:\n"
    "            f.write('Time,u_delta_rad,u_delta_deg\\n')\n"
    "            for t, ud in self._u_delta_history:\n"
    "                f.write(f'{t},{ud},{ud*RAD2DEG}\\n')\n"
    "        print(f'Exported {len(self._u_delta_history)} u_delta samples '\n"
    "              f'to {path}')\n\n"
    "    def test(self, u_deg):"
)
content = content.replace(anchor3, replacement3, 1)

if content == original:
    print("No changes made (unexpected) -- check anchors.")
    raise SystemExit(1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Patched successfully:")
print("  - self._u_delta_history initialized in __init__")
print("  - logging added to _update()")
print("  - export_u_delta_log() method added")
print("\nNext: after running a sim, call sim.controller.servo"
      ".export_u_delta_log() from a Python console, OR I can show you"
      " where to auto-call it after run_simulation() completes.")
