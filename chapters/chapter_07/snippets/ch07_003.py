# Chapter: 7
# Section: 7.7.2 Numerical Integration과 Euler Method
# Type: SNIPPET
# Status: SNIPPET_UNTESTED
# Origin: Word paragraph(s) 2095–2101
# Note: Independent execution NOT guaranteed. Original text preserved below.

plt.plot(time, C, label="Euler")
plt.plot(time, C_exact, "--", label="Analytical")
plt.xlabel("Time")
plt.ylabel("Concentration")
plt.legend()
plt.show()
