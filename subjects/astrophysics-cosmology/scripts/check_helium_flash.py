"""Independent mesh-convergence check for the two PS5.3 heat-capacity conventions."""

import json
from pathlib import Path

import numpy as np
from scipy.integrate import simpson

ROOT = Path(__file__).resolve().parents[1]
rho = 2.0e5  # g cm^-3
t_start = 1.5e8  # K
t_stop = (rho / 1e-8) ** (2 / 3)
x = (rho / 2e6) ** (1 / 3)
boltzmann_cgs = 1.380649e-16
proton_g = 1.67262192369e-24


def dt_dT(temp, corrected):
    ionic_cv = 3 * boltzmann_cgs / ((8 if corrected else 4) * proton_g)
    electronic_cv = 1.35e5 * temp * x * np.sqrt(1 + x * x) / rho
    t9 = temp / 1e9
    heating = 5.1e8 * rho**2 * t9**-3 * np.exp(-4.4027 / t9)
    return (ionic_cv + electronic_cv) / heating


rows = []
for corrected, target in [(False, 667284.2), (True, 489384.3)]:
    estimates = []
    for n in [2001, 4001, 8001, 16001]:
        temp = np.geomspace(t_start, t_stop, n)
        estimates.append(float(simpson(dt_dT(temp, corrected), x=temp)))
    assert abs(estimates[-1] - target) < 1.0
    rows.append(
        {
            "model": "corrected monatomic ion cv" if corrected else "original printed ion cv",
            "seconds_by_geometric_simpson_grids": estimates,
            "relative_8001_to_16001": abs(estimates[-1] - estimates[-2]) / estimates[-1],
        }
    )

receipt = {
    "method": "Composite Simpson on four independently spaced temperature meshes; integral of Cv(T)/epsilon(T)",
    "T_stop_K": t_stop,
    "results": rows,
    "asserted_against_worked_solution_seconds": [667284.2, 489384.3],
}
out = ROOT / "qa/helium-flash-independent-convergence.json"
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(receipt, ensure_ascii=False))
