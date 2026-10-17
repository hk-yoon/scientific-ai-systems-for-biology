"""Chapter 11.10 rule-based Scientific AI Agent (Python 3.10+, stdlib only).
Reconstructed from Chapter_11_FINAL.md; not a recovered original source.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import statistics
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path

class ExecutionStatus(str, Enum):
    PENDING='PENDING'; READY='READY'; RUNNING='RUNNING'; COMPLETED='COMPLETED'; FAILED='FAILED'; CANCELLED='CANCELLED'

class ReviewStatus(str, Enum):
    NOT_REVIEWED='NOT_REVIEWED'; ACCEPTED='ACCEPTED'; NEEDS_REVISION='NEEDS_REVISION'; INCONCLUSIVE='INCONCLUSIVE'; REJECTED='REJECTED'

@dataclass
class Task:
    task_id: str
    tool: str
    arguments: dict = field(default_factory=dict)
    dependencies: tuple[str, ...] = ()
    max_attempts: int = 2
    execution_status: ExecutionStatus = ExecutionStatus.PENDING
    review_status: ReviewStatus = ReviewStatus.NOT_REVIEWED
    attempts: int = 0
    result: dict | None = None
    error: str | None = None

class ToolRegistry:
    def __init__(self): self.tools={}
    def register(self,name,fn):
        if name in self.tools: raise ValueError(f'duplicate tool: {name}')
        self.tools[name]=fn
    def execute(self,name,arguments):
        if name not in self.tools: raise ValueError(f'unsupported tool: {name}')
        return self.tools[name](**arguments)

def validate_measurements(values,unit='relative'):
    if unit != 'relative': raise ValueError('expected relative unit')
    if not isinstance(values,(list,tuple)) or len(values)<3: raise ValueError('at least 3 observations required')
    if any(isinstance(v,bool) or not isinstance(v,(float,int)) or not math.isfinite(v) or not 0<=v<=1 for v in values):
        raise ValueError('observations must be finite numbers in [0,1]')
    normalized=[float(v) for v in values]
    canonical=json.dumps({'unit':unit,'values':normalized},sort_keys=True,separators=(',',':'))
    return {'values':normalized,'unit':unit,'count':len(normalized),'sha256':hashlib.sha256(canonical.encode()).hexdigest()}

def summarize_measurements(values,unit='relative'):
    return {'mean':statistics.mean(values),'sample_std':statistics.stdev(values),'count':len(values),'unit':unit}

def generate_report(summary,validation):
    return {'title':'Cell viability measurement report','summary':summary,'source_sha256':validation['sha256']}

class Planner:
    def plan(self,values):
        return [Task('T1','validate',{'values':values}),Task('T2','summarize',dependencies=('T1',)),Task('T3','report',dependencies=('T2',))]

class Reviewer:
    def review(self,task,result):
        if task.tool=='validate': return ReviewStatus.ACCEPTED
        if task.tool=='summarize':
            if result['count']<3 or not 0<=result['mean']<=1 or result['sample_std']<0: return ReviewStatus.REJECTED
            return ReviewStatus.INCONCLUSIVE if result['sample_std']>0.10 else ReviewStatus.ACCEPTED
        return ReviewStatus.ACCEPTED

class EventStore:
    def __init__(self): self.events=[]
    def append(self,event_type,task_id,details=None):
        self.events.append({'timestamp':datetime.now(timezone.utc).isoformat(),'event_type':event_type,'task_id':task_id,'details':details or {}})
    def save(self,path):
        with open(path,'w',encoding='utf-8') as f:
            for item in self.events: f.write(json.dumps(item,ensure_ascii=False)+'\n')

class Workflow:
    def __init__(self,tasks,registry,reviewer=None,event_store=None):
        self.tasks=list(tasks); self.index={t.task_id:t for t in self.tasks}
        if len(self.index)!=len(self.tasks): raise ValueError('duplicate task ID')
        self.registry=registry; self.reviewer=reviewer or Reviewer();self.events=event_store or EventStore()
        self._validate_graph()
    def _validate_graph(self):
        visited=set();active=set()
        def visit(tid):
            if tid not in self.index: raise ValueError(f'unknown dependency: {tid}')
            if tid in active: raise ValueError('cyclic dependency')
            if tid in visited: return
            active.add(tid)
            for dependency in self.index[tid].dependencies:visit(dependency)
            active.remove(tid);visited.add(tid)
        for tid in self.index:visit(tid)
    def _arguments(self,task):
        if task.tool=='summarize':
            prior=self.index['T1'].result
            return {'values':prior['values'],'unit':prior['unit']}
        if task.tool=='report':return {'summary':self.index['T2'].result,'validation':self.index['T1'].result}
        return task.arguments
    def run(self):
        # Ordered educational execution: reject plans that list a child before its parent.
        completed=set()
        for task in self.tasks:
            if any(dep not in completed for dep in task.dependencies):
                raise ValueError('tasks must be in dependency order')
            completed.add(task.task_id)
            if any(self.index[dep].execution_status!=ExecutionStatus.COMPLETED or self.index[dep].review_status!=ReviewStatus.ACCEPTED for dep in task.dependencies):
                task.execution_status=ExecutionStatus.CANCELLED
                self.events.append('TASK_BLOCKED',task.task_id,{'dependencies':list(task.dependencies)})
                continue
            task.execution_status=ExecutionStatus.READY;self.events.append('TASK_READY',task.task_id)
            for attempt in range(1,task.max_attempts+1):
                task.attempts=attempt;task.execution_status=ExecutionStatus.RUNNING
                self.events.append('TASK_STARTED',task.task_id,{'attempt':attempt})
                try:
                    task.result=self.registry.execute(task.tool,self._arguments(task))
                except (OSError,ValueError,TypeError) as exc:
                    task.error=f'{type(exc).__name__}: {exc}'
                    self.events.append('TASK_FAILED',task.task_id,{'attempt':attempt,'error':task.error})
                    if isinstance(exc,OSError) and attempt<task.max_attempts:continue
                    task.execution_status=ExecutionStatus.FAILED;break
                else:
                    task.execution_status=ExecutionStatus.COMPLETED
                    self.events.append('TASK_COMPLETED',task.task_id)
                    task.review_status=self.reviewer.review(task,task.result)
                    self.events.append('TASK_REVIEWED',task.task_id,{'review_status':task.review_status.value})
                    break
        return self.tasks

def build_registry():
    registry=ToolRegistry();registry.register('validate',validate_measurements)
    registry.register('summarize',summarize_measurements);registry.register('report',generate_report)
    return registry

def run_case(case='normal',output_dir='results'):
    cases={'normal':[0.82,0.79,0.85,0.81], 'inconclusive':[0.45,0.65,0.85,0.95], 'invalid':[0.82,-0.10,0.85,0.81]}
    if case not in cases:raise ValueError(f'unknown case: {case}')
    events=EventStore();tasks=Workflow(Planner().plan(cases[case]),build_registry(),event_store=events).run()
    path=Path(output_dir);path.mkdir(parents=True,exist_ok=True)
    payload={'case':case,'tasks':[{'task_id':t.task_id,'execution_status':t.execution_status.value,'review_status':t.review_status.value,'attempts':t.attempts,'result':t.result,'error':t.error} for t in tasks]}
    (path/f'{case}_results.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    events.save(path/f'{case}_events.jsonl')
    return payload

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--case',choices=['normal','inconclusive','invalid'],default='normal');parser.add_argument('--output-dir',default='results')
    args=parser.parse_args();print(json.dumps(run_case(args.case,args.output_dir),ensure_ascii=False,indent=2))
