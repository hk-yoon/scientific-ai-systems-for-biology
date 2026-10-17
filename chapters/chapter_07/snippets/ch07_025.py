# Chapter: 7
# Section: 7.12.4 Simulation Result와 Conservation Check
# Type: SNIPPET
# Status: SNIPPET_UNTESTED
# Origin: Word paragraph(s) 4209–4212
# Note: Independent execution NOT guaranteed. Original text preserved below.

print("Initial conserved quantity:", conserved[0])
print("Final conserved quantity:", conserved[-1])
print("Maximum deviation:",
np.max(np.abs(conserved - conserved[0])))
