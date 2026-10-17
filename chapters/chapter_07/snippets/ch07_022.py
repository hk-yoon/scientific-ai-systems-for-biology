# Chapter: 7
# Section: 7.12.3 Parameterization과 Python Simulation
# Type: SNIPPET
# Status: SNIPPET_UNTESTED
# Origin: Word paragraph(s) 4147–4157
# Note: Independent execution NOT guaranteed. Original text preserved below.

mu_max = 0.7
K_s = 0.5
Y = 0.6
X0 = 0.1
S0 = 10.0
y0 = [X0, S0]
t_span = (0.0, 20.0)
t_eval = np.linspace(0.0, 20.0, 201)
