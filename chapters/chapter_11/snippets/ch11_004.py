# Chapter: 11
# Section: 11.10.2 기본 Agent와 도구 인터페이스
# Type: SNIPPET
# Status: SNIPPET_UNTESTED
# Origin: Word paragraph(s) 2646–2646
# Note: Independent execution NOT guaranteed. Original text preserved below.

class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, fn):
        if name in self.tools:
            raise ValueError(f"duplicate tool: {name}")
        self.tools[name] = fn

    def execute(self, name, arguments):
        if name not in self.tools:
            raise ValueError(f"unsupported tool: {name}")
        return self.tools[name](**arguments)
