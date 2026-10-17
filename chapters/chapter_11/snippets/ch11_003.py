# Chapter: 11
# Section: 11.10.2 기본 Agent와 도구 인터페이스
# Type: SNIPPET
# Status: SNIPPET_UNTESTED
# Origin: Word paragraph(s) 2636–2636
# Note: Independent execution NOT guaranteed. Original text preserved below.

from dataclasses import dataclass, field

@dataclass
class Task:
    task_id: str
    tool: str
    arguments: dict = field(default_factory=dict)
    dependencies: tuple[str, ...] = ()
    max_attempts: int = 2
