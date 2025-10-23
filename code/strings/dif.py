import os
import sys

name = sys.argv[1]

q1 = float(os.popen(f"python3 quant-stretch.py ").read())
q2 = float(os.popen(f"python3 quant-stretch.py ").read())
