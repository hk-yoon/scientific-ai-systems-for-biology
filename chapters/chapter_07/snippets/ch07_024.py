# Chapter: 7
# Section: 7.12.3 Parameterization과 Python Simulation
# Type: SNIPPET
# Status: SNIPPET_UNTESTED
# Origin: Word paragraph(s) 4172–4178
# Note: Independent execution NOT guaranteed. Original text preserved below.

plt.plot(solution.t, X, label="Biomass")
plt.plot(solution.t, S, label="Substrate")
plt.xlabel("Time")
plt.ylabel("State")
plt.legend()
plt.show()
