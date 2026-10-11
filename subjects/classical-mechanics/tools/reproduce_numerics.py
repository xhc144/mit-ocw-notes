#!/usr/bin/env python3
"""Recompute all course-model data; no source notebook is executed."""
from pathlib import Path
import subprocess
import sys
HERE=Path(__file__).resolve().parent
if __name__=='__main__':
 subprocess.run([sys.executable,str(HERE/'project_check.py')],check=True,cwd=HERE)
 from project_check import export_course_plot
 print(export_course_plot())
 for filename in ['nonlinear_check.py','verify_nonlinear_cases.py','periodic_orbit_scan.py','export_phase_plots.py','prepare_plot_data.py']:
  subprocess.run([sys.executable,str(HERE/filename)],check=True,cwd=HERE)
