#!/usr/bin/env python3
"""
Ziegler-Nichols tuning helper for ARGUS TVC.

Usage:
    python3 analyze_zn.py Argus_0.csv [Kp_used_for_this_run]

What it does:
  1. Reads the pitch-rate / pitch-angle log exported from AeroVECTOR.
  2. Finds the powered-flight window (Thrust > 0) since that's the only
     phase where TVC can actually influence pitch.
  3. Detects oscillation peaks in Pitch Angle during that window and
     measures whether amplitude is growing (unstable), shrinking
     (stable/damped), or roughly constant (marginally stable = the
     Z-N "critical gain" condition you're looking for).
  4. If oscillation looks sustained/marginal, estimates Tu (oscillation
     period) and prints the full Ziegler-Nichols gain table using
     Ku = Kp_used_for_this_run.

Workflow:
  - Run the sim with a given Kp (Ki=0, Kd=0 -- pure P control) and note
    that Kp value.
  - Export/save the CSV, then run:
        python3 analyze_zn.py Argus_0.csv 0.4
  - The script tells you whether to raise or lower Kp for the next run.
  - Repeat until it reports "marginal / sustained oscillation" -- that
    Kp is your Ku. It then prints the Z-N table directly.

NOTE: This needs a fine-grained export (set "Export T [s] =" in the
Sim Setup tab to ~0.002 or smaller) -- the default 0.102s export
interval is too coarse to resolve fast pitch oscillation.
"""
import csv
import sys
from statistics import mean

def load(path):
    with open(path) as f:
        rows = list(csv.DictReader(f))
    t = [float(r['Time']) for r in rows]
    pitch = [float(r['Pitch Angle [º]']) for r in rows]
    setpoint = [float(r['Setpoint [º]']) for r in rows]
    thrust = [float(r['Thrust [N]']) for r in rows]
    return t, pitch, setpoint, thrust

def powered_window(t, thrust):
    idx = [i for i, th in enumerate(thrust) if th > 0.5]
    if not idx:
        return 0, len(t) - 1
    return idx[0], idx[-1]

def find_peaks(signal, t):
    """Return (time, value) of local extrema (both peaks and troughs)."""
    peaks = []
    for i in range(1, len(signal) - 1):
        if (signal[i] > signal[i-1] and signal[i] > signal[i+1]) or \
           (signal[i] < signal[i-1] and signal[i] < signal[i+1]):
            peaks.append((t[i], signal[i]))
    return peaks

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_zn.py <csv_file> [Kp_used]")
        sys.exit(1)

    path = sys.argv[1]
    kp_used = float(sys.argv[2]) if len(sys.argv) > 2 else None

    t, pitch, setpoint, thrust = load(path)
    i0, i1 = powered_window(t, thrust)
    print(f"Powered flight window: t={t[i0]:.3f}s to t={t[i1]:.3f}s "
          f"({i1 - i0 + 1} samples)\n")

    err = [pitch[i] - setpoint[i] for i in range(i0, i1 + 1)]
    tw = t[i0:i1 + 1]

    peaks = find_peaks(err, tw)
    if len(peaks) < 4:
        print("Not enough oscillation peaks detected in powered flight "
              "to analyze. Either the response is overdamped (good -- "
              "lower Kd slightly and retest), the Export T is still too "
              "coarse, or the window is too short.")
        return

    amps = [abs(v) for _, v in peaks]
    times = [tm for tm, _ in peaks]

    half = len(amps) // 2
    early_avg = mean(amps[:half])
    late_avg = mean(amps[half:])
    ratio = late_avg / early_avg if early_avg > 0 else float('inf')

    periods = [times[i+2] - times[i] for i in range(len(times) - 2)]
    tu_est = mean(periods) if periods else None

    print(f"Detected {len(peaks)} extrema in error signal during powered flight.")
    print(f"Early-run avg |error| peak: {early_avg:.2f}º")
    print(f"Late-run avg |error| peak:  {late_avg:.2f}º")
    print(f"Amplitude ratio (late/early): {ratio:.2f}\n")

    if ratio > 1.15:
        print("=> GROWING oscillation: system is UNSTABLE at this Kp.")
        print("   Lower Kp for the next test run.")
    elif ratio < 0.7:
        print("=> DAMPING oscillation: system is stable/overdamped-ish at this Kp.")
        print("   Raise Kp slightly for the next test run to approach the")
        print("   critical (sustained-oscillation) point.")
    else:
        print("=> Roughly SUSTAINED oscillation -- this looks like the Z-N")
        print("   critical point (Ku).")
        if tu_est:
            print(f"   Estimated oscillation period Tu ~= {tu_est:.3f} s")
        if kp_used is not None and tu_est:
            ku = kp_used
            print(f"\n   Using Ku = {ku} (the Kp you ran this test with):\n")
            print(f"   {'Controller':<12}{'Kp':>10}{'Ki':>10}{'Kd':>10}")
            print(f"   {'P':<12}{0.5*ku:>10.4f}{'-':>10}{'-':>10}")
            print(f"   {'PI':<12}{0.45*ku:>10.4f}{(0.54*ku/tu_est):>10.4f}{'-':>10}")
            print(f"   {'PID (classic)':<12}{0.6*ku:>10.4f}"
                  f"{(1.2*ku/tu_est):>10.4f}{(0.075*ku*tu_est):>10.4f}")
            print(f"   {'PID (Pessen)':<12}{0.7*ku:>10.4f}"
                  f"{(1.75*ku/tu_est):>10.4f}{(0.105*ku*tu_est):>10.4f}")
            print(f"   {'PID (some overshoot)':<21}{0.33*ku:>7.4f}"
                  f"{(0.66*ku/tu_est):>10.4f}{(0.11*ku*tu_est):>10.4f}")
        else:
            print("   Re-run this script with the Kp value as the 2nd "
                  "argument to get the full gain table, e.g.:")
            print(f"       python3 analyze_zn.py {path} <Kp_you_used>")

    print(f"\nPeak times/values (first 10):")
    for tm, v in peaks[:10]:
        print(f"   t={tm:6.3f}s  error={v:8.2f}º")

if __name__ == "__main__":
    main()
