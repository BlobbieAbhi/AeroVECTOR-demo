# AeroVECTOR-demo (OpenVector integration demo)

This is a trimmed public snapshot of my ARGUS rocket project's AeroVECTOR fork, published as a working demo for [OpenVector](https://github.com/BlobbieAbhi/OpenVector) — a tool that imports real Mach-dependent drag data from OpenRocket/RASAero exports into AeroVECTOR's 6-DOF simulation.

## What's different from stock AeroVECTOR

`src/aerodynamics/drag_data.py` (OpenVector's `DragModel`) is wired directly into the simulation loop in `src/simulation/main_simulation.py`:

```python
rocket.set_drag_model("src/aerodynamics/argus_rasaero.csv")
```

This means every simulation run in this repo automatically uses real drag data exported from my ARGUS rocket's OpenRocket simulation (`src/aerodynamics/argus_rasaero.csv`, 491 data points) instead of AeroVECTOR's default empirical drag build-up.

## Quick start

```bash
git clone https://github.com/BlobbieAbhi/AeroVECTOR-demo.git
cd AeroVECTOR-demo
pip install tkinter numpy scipy matplotlib pandas vpython
python3 AeroVECTOR.py
```

The GUI will open with `Argus.txt` — my real ARGUS rocket configuration (fin geometry, motor, and PID gains tuned via Ziegler-Nichols-style testing). Click **Run Simulation** to see the flight simulated using the imported drag data.

## See it in isolation

To see the drag model working outside the full sim GUI, check the [OpenVector repo](https://github.com/BlobbieAbhi/OpenVector)'s `examples/argus/` folder — it loads the same `argus_rasaero.csv` data and plots it directly.

---

## Original AeroVECTOR documentation follows below