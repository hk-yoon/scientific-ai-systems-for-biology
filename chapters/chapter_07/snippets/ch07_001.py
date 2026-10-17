# Chapter: 7
# Section: 7.7.2 Numerical Integration과 Euler Method
# Type: SNIPPET
# Status: SNIPPET_UNTESTED
# Origin: Word paragraph(s) 2075–2086
# Note: Independent execution NOT guaranteed. Original text preserved below.

import numpy as np
import matplotlib.pyplot as plt
k = 0.2
C0 = 10.0
dt = 0.5
t_end = 20.0
time = np.arange(0, t_end + dt, dt)
C = np.zeros(len(time))
