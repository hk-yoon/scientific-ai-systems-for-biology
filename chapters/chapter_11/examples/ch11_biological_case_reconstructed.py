"""Chapter 11.11 educational reconstruction, NOT original canonical source.
Reuses Chapter 11.10 Task, ToolRegistry, Reviewer, Workflow, EventStore.
"""
import argparse
import csv
import json
import math
from pathlib import Path
from scientific_agent import Task, Planner, Reviewer, Workflow, EventStore, ToolRegistry, ReviewStatus

FIELDS=('sample_id','batch','temperature','nutrient','viability')

def make_data(path):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    rows=[]
    offsets=[-.055,-.015,.025,.045]
    for b,offset in enumerate(offsets,1):
        for i in range(8):
            rows.append({'sample_id':f'S{b:02d}{i:02d}','batch':f'B{b}',
                         'temperature':round(36.5+(i%4)*.25,2), 'nutrient':round(1.2+.2*(i%3),2),
                         'viability':round(.78+offset+(i-3.5)*.013,5)})
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
    return str(path)

def load_csv(path):
    with open(path,encoding='utf-8',newline='') as f:
        reader=csv.DictReader(f)
        if not set(FIELDS).issubset(reader.fieldnames or []):raise ValueError('required columns missing')
        return {'rows':list(reader),'source_path':str(path)}

def quality_check(data):
    rows=data['rows'];seen=set();batches=set();clean=[]
    if not rows:raise ValueError('empty input')
    for row in rows:
        sid=row['sample_id'];batch=row['batch']
        if not sid or sid in seen or not batch:raise ValueError('invalid sample ID or batch')
        seen.add(sid);batches.add(batch)
        t=float(row['temperature']);n=float(row['nutrient']);v=float(row['viability'])
        if not(all(map(math.isfinite,(t,n,v))) and 30<=t<=42 and 0<=n<=5 and 0<=v<=1):
            raise ValueError('out-of-range observation')
        clean.append({'sample_id':sid,'batch':batch,'temperature':t,'nutrient':n,'viability':v})
    if len(batches)<3:raise ValueError('at least 3 batches required')
    return {'rows':clean,'count':len(clean),'batches':sorted(batches),'source_path':data['source_path']}

def analysis(data,method):
    rows=data['rows']; folds=[]
    if method=='row_split':
        train=[r['viability'] for i,r in enumerate(rows) if i%4!=0]
        test=[r['viability'] for i,r in enumerate(rows) if i%4==0]
        pred=sum(train)/len(train)
        folds=[{'batch':'row_split','rmse':math.sqrt(sum((x-pred)**2 for x in test)/len(test)),'n':len(test)}]
    elif method=='leave_one_batch_out':
        for batch in data['batches']:
            train=[r['viability'] for r in rows if r['batch']!=batch]
            test=[r['viability'] for r in rows if r['batch']==batch]
            pred=sum(train)/len(train)
            folds.append({'batch':batch,'rmse':math.sqrt(sum((x-pred)**2 for x in test)/len(test)),'n':len(test)})
    else:raise ValueError('unknown method')
    rmse=math.sqrt(sum(f['n']*f['rmse']**2 for f in folds)/sum(f['n'] for f in folds))
    return {'method':method,'rmse':rmse,'folds':folds,'count':data['count'],'batches':data['batches'],
            'overall_mean':sum(r['viability'] for r in rows)/len(rows)}

def report(analysis_result,data):
    return {'title':'Synthetic cell viability assessment','rmse':analysis_result['rmse'],
            'method':analysis_result['method'],'count':data['count'],'batches':data['batches'],
            'overall_mean':analysis_result['overall_mean'],'review_status':'ACCEPTED',
            'limitations':'Synthetic data and mean-baseline model; no biological inference.'}

class CasePlanner(Planner):
    def plan(self,path,method='row_split'):
        return [Task('T1','load',{'path':str(path)}),Task('T2','quality',dependencies=('T1',)),
                Task('T3','analyze',{'method':method},dependencies=('T2',)),Task('T4','report',dependencies=('T3',))]

class CaseReviewer(Reviewer):
    def review(self,task,result):
        if task.tool=='analyze':
            if result['method']!='leave_one_batch_out':return ReviewStatus.NEEDS_REVISION
            if not math.isfinite(result['rmse']):return ReviewStatus.REJECTED
        return ReviewStatus.ACCEPTED

class CaseWorkflow(Workflow):
    def _arguments(self,task):
        if task.tool=='quality':return {'data':self.index['T1'].result}
        if task.tool=='analyze':return {'data':self.index['T2'].result,'method':task.arguments['method']}
        if task.tool=='report':return {'analysis_result':self.index['T3'].result,'data':self.index['T2'].result}
        return task.arguments

def registry():
    r=ToolRegistry()
    for name,fn in [('load',load_csv),('quality',quality_check),('analyze',analysis),('report',report)]:r.register(name,fn)
    return r

def run_plan(path,method,output_dir,plan_name):
    output_dir=Path(output_dir);output_dir.mkdir(parents=True,exist_ok=True)
    events=EventStore();tasks=CaseWorkflow(CasePlanner().plan(path,method),registry(),CaseReviewer(),events).run()
    payload={'plan':plan_name,'method':method,'tasks':[{'id':t.task_id,'execution':t.execution_status.value,
              'review':t.review_status.value,'result':t.result,'error':t.error} for t in tasks]}
    (output_dir/f'{plan_name}_results.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    events.save(output_dir/f'{plan_name}_events.jsonl')
    return payload

def run_case(output_dir='results',approve=False):
    p=Path(output_dir);p.mkdir(parents=True,exist_ok=True)
    source=make_data(p/'synthetic_measurements.csv')
    v1=run_plan(source,'row_split',p,'plan_v1')
    v2=run_plan(source,'leave_one_batch_out',p,'plan_v2')
    approval='APPROVED' if approve else 'PENDING_APPROVAL'
    (p/'approval.json').write_text(json.dumps({'status':approval,'demonstration_only':True},indent=2),encoding='utf-8')
    return v1,v2,approval

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',default='results');parser.add_argument('--approve',action='store_true')
    args=parser.parse_args();v1,v2,status=run_case(args.output_dir,args.approve)
    print(json.dumps({'v1_T3':v1['tasks'][2]['review'],'v1_T4':v1['tasks'][3]['execution'],
                      'v2_T3':v2['tasks'][2]['review'],'v2_T4':v2['tasks'][3]['execution'],
                      'rmse':v2['tasks'][2]['result']['rmse'],'approval':status},indent=2))
