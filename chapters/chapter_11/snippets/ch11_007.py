# Chapter: 11
# Section: 11.10.4 Reviewer를 이용한 결과 검토
# Type: SNIPPET
# Status: SNIPPET_UNTESTED
# Origin: Word paragraph(s) 2710–2710
# Note: Independent execution NOT guaranteed. Original text preserved below.

from enum import Enum

class ReviewStatus(str, Enum):
    NOT_REVIEWED = "NOT_REVIEWED"
    ACCEPTED = "ACCEPTED"
    NEEDS_REVISION = "NEEDS_REVISION"
    INCONCLUSIVE = "INCONCLUSIVE"
    REJECTED = "REJECTED"
