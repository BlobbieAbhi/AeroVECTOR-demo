#!/usr/bin/env python3
"""
Adds an automatic call to servo.export_u_delta_log() inside export_plots(),
so the u_delta instrumentation CSV gets written every time you click
Export Plots in the GUI -- no extra manual step needed.

Run once from inside the AeroVECTOR repo root, AFTER patch_servo.py:
    python3 patch_export.py
"""
path = "src/simulation/main_simulation.py"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

original = content

anchor = "    files.export_plots(file_name, filepath, names_to_csv, plots_to_csv, export_T)"
if anchor not in content:
    print("ERROR: anchor not found -- export_plots() may look different "
          "than expected. No changes made.")
    raise SystemExit(1)

replacement = (
    anchor + "\n"
    "    servo.export_u_delta_log(filepath + 'u_delta_log.csv')  "
    "# [instrumentation]"
)
content = content.replace(anchor, replacement, 1)

if content == original:
    print("No changes made (unexpected) -- check anchor.")
    raise SystemExit(1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Patched successfully: export_plots() now also writes "
      "u_delta_log.csv to the same export folder.")
