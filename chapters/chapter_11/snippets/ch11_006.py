# Chapter: 11
# Section: 11.10.3 연구 작업 계획과 실행
# Type: SNIPPET
# Status: SNIPPET_UNTESTED
# Origin: Word paragraph(s) 2675–2675
# Note: Independent execution NOT guaranteed. Original text preserved below.

class Planner:
    def plan(self, values):
        return [
            Task("T1", "validate", {"values": values}),
            Task("T2", "summarize", dependencies=("T1",)),
            Task("T3", "report", dependencies=("T2",)),
        ]
