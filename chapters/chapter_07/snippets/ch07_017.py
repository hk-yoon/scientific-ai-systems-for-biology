# Chapter: 7
# Section: 7.7.5 다중 상태 ODE의 Python 구현 (Python Implementation of Multi-State ODE Systems)
# Type: SNIPPET
# Status: SNIPPET_UNTESTED
# Origin: Word paragraph(s) 2256–2262
# Note: Independent execution NOT guaranteed. Original text preserved below.

plt.plot(solution.t, X, label="Biomass")
plt.plot(solution.t, S, label="Substrate")
plt.xlabel("Time")
plt.ylabel("State")
plt.legend()
plt.show()
