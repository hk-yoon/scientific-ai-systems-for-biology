"""Scientific AI Systems for Biology — Chapter 9 integrated DOE/RSM lab.
Synthetic educational data only. CPU-first. No biological validity implied.
"""
import itertools
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats
from scipy.optimize import minimize

SEED=911
NOISE_STD=0.25
FACTORS=list('ABCDEF')
PRIMARY=list('ABC')

def synthetic_experiment(x, rng, sd=NOISE_STD):
    """A hidden educational simulator: analysis must only use returned measurements."""
    arr=np.atleast_2d(np.asarray(x,dtype=float))
    A,B,C,D,E,F=arr.T
    mean=(17.8+1.3*A+0.8*B+1.1*C+0.12*D-0.10*E+0.07*F
          -2.1*A*A-1.65*B*B-1.35*C*C+0.65*A*B-0.35*A*C
          +0.25*B*C+0.12*D*E)
    return mean+rng.normal(0,sd,len(arr))

def screening_design():
    base=np.array(list(itertools.product([-1.,1.],repeat=4)))
    A,B,C,D=base.T
    design=np.column_stack((base,A*B*C,A*B*D))
    out=pd.DataFrame(design,columns=FACTORS)
    assert np.all(out.E==out.A*out.B*out.C)
    assert np.all(out.F==out.A*out.B*out.D)
    assert np.all(out.A*out.B*out.C*out.E==1)
    assert np.all(out.C*out.D*out.E*out.F==1)
    return out

def ccd_design(k=3,n_center=5):
    alpha=(2**k)**.25
    factorial=np.array(list(itertools.product([-1.,1.],repeat=k)))
    axial=[]
    for j in range(k):
        for sign in (-1.,1.):
            a=np.zeros(k);a[j]=sign*alpha;axial.append(a)
    pts=np.vstack((factorial,axial,np.zeros((n_center,k))))
    df=pd.DataFrame(pts,columns=PRIMARY)
    df['point_id']=pd.factorize(pd.Series(list(map(tuple,pts))))[0]+1
    return df

def fit_rsm(df):
    formula='response ~ A+B+C+I(A**2)+I(B**2)+I(C**2)+A:B+A:C+B:C'
    return smf.ols(formula,data=df).fit()

def lack_of_fit(df,fit):
    n=len(df);m=df.point_id.nunique();p=len(fit.params)
    groupmean=df.groupby('point_id').response.transform('mean')
    sspe=float(((df.response-groupmean)**2).sum())
    sse=float((fit.resid**2).sum());sslof=sse-sspe
    dfpe=n-m;dflof=m-p
    assert dfpe>0 and dflof>0
    f=(sslof/dflof)/(sspe/dfpe)
    return {'ss_pure_error':sspe,'ss_lack_of_fit':sslof,
            'df_pure_error':dfpe,'df_lack_of_fit':dflof,
            'F':f,'p_value':float(stats.f.sf(f,dflof,dfpe))}

def stationary_point(fit):
    p=fit.params;b=np.array([p[t] for t in PRIMARY])
    H=np.array([[2*p['I(A ** 2)'],p['A:B'],p['A:C']],
                [p['A:B'],2*p['I(B ** 2)'],p['B:C']],
                [p['A:C'],p['B:C'],2*p['I(C ** 2)']]])
    return np.linalg.solve(H,-b),np.linalg.eigvalsh(H)

def predict(fit,x):
    return float(fit.predict(pd.DataFrame([dict(zip(PRIMARY,x))])).iloc[0])

def physical_conditions(x):
    a,b,c=x
    return {'temperature_C':35+5*a,'pH':7+b,'glucose_g_L':10+5*c,
            'nitrogen_g_L':3.0,'agitation_rpm':200.,'inoculum_g_L':0.125}

def main():
    rng=np.random.default_rng(SEED)
    screening=screening_design()
    screening['response']=synthetic_experiment(screening[FACTORS],rng)
    screening['run_order']=rng.permutation(len(screening))+1
    screen_fit=smf.ols('response ~ A+B+C+D+E+F',data=screening).fit()
    effects=pd.DataFrame({'factor':FACTORS,'coefficient':screen_fit.params[FACTORS].to_numpy(),
        'effect':(2*screen_fit.params[FACTORS]).to_numpy(),
        'exploratory_p_value':screen_fit.pvalues[FACTORS].to_numpy()})
    rsm=ccd_design()
    full=np.column_stack((rsm[PRIMARY],np.zeros((len(rsm),3))))
    rsm['response']=synthetic_experiment(full,rng)
    fit=fit_rsm(rsm);lof=lack_of_fit(rsm,fit)
    stationary,eigenvalues=stationary_point(fit)
    bounds=[(-1.,1.)]*3
    result=minimize(lambda x:-predict(fit,x),np.zeros(3),bounds=bounds,method='L-BFGS-B')
    assert result.success
    optimum=result.x
    validation_points=np.array([[-.6,.4,-.3],[.4,-.5,.6],[.1,.3,-.5],[-.2,-.4,.2]])
    valfull=np.column_stack((validation_points,np.zeros((4,3))))
    observed=synthetic_experiment(valfull,rng)
    predicted=np.array([predict(fit,x) for x in validation_points])
    validation_rmse=float(np.sqrt(np.mean((observed-predicted)**2)))
    nconf=5
    confirmed=synthetic_experiment(np.tile(np.r_[optimum,[0.,0.,0.]],(nconf,1)),rng)
    reference=synthetic_experiment(np.zeros((nconf,6)),rng)
    # Confirm two independent samples, using unequal-variance Welch inference.
    delta=float(confirmed.mean()-reference.mean())
    s1=float(confirmed.var(ddof=1));s2=float(reference.var(ddof=1))
    se=float(np.sqrt(s1/nconf+s2/nconf))
    degrees=(s1/nconf+s2/nconf)**2/((s1/nconf)**2/(nconf-1)+(s2/nconf)**2/(nconf-1))
    tstat=delta/se
    pval=float(2*stats.t.sf(abs(tstat),degrees))
    ci=stats.t.interval(.95,degrees,loc=delta,scale=se)
    summary={
      'screening_runs':len(screening),'ccd_runs':len(rsm),'ccd_unique':rsm.point_id.nunique(),
      'screening_effects':effects.round(5).to_dict('records'),
      'rsm_r2':float(fit.rsquared),
      'rsm_train_rmse':float(np.sqrt(np.mean(fit.resid**2))),
      'lack_of_fit':lof,'stationary':stationary.tolist(),
      'hessian_eigenvalues':eigenvalues.tolist(),
      'optimum':optimum.tolist(),'predicted_optimum':predict(fit,optimum),
      'physical_conditions':physical_conditions(optimum),'validation_rmse':validation_rmse,
      'confirmation_mean':float(confirmed.mean()),'reference_mean':float(reference.mean()),
      'confirmation_delta':delta,'confirmation_relative_pct':100*delta/float(reference.mean()),
      'welch_t':float(tstat),'welch_df':float(degrees),'welch_p':pval,
      'welch_ci95':[float(ci[0]),float(ci[1])]
    }
    assert len(screening)==16 and len(rsm)==19 and rsm.point_id.nunique()==15
    assert len(fit.params)==10 and lof['df_pure_error']==4 and lof['df_lack_of_fit']==5
    assert np.all(eigenvalues<0) and np.all(np.abs(optimum)<=1)
    return summary

if __name__=='__main__':
    import json
    result=main()
    print(json.dumps(result,ensure_ascii=False,indent=2))
