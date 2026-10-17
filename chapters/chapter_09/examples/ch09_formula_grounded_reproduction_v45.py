"""Chapter 9, sections 9.9 and 9.10: NEW reconstruction, NOT recovered original.
Synthetic educational response, not experimentally calibrated. CPU only.
"""
import itertools
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy.optimize import minimize

SEED = 20261010
ALPHA = (2**3)**0.25
FORMULA = 'response ~ A+B+C+I(A**2)+I(B**2)+I(C**2)+A:B+A:C+B:C'

def generate_ccd():
    factorial = np.array(list(itertools.product((-1.0,1.0),repeat=3)))
    axial = []
    for j in range(3):
        for sign in (-1.,1.):
            v = np.zeros(3)
            v[j] = sign * ALPHA
            axial.append(v)
    pts = np.vstack((factorial, np.array(axial), np.zeros((5,3))))
    return pd.DataFrame(pts,columns=['A','B','C'])

def synthetic_mean(df):
    """Coefficients transcribed from Word 9.9 OMML equation."""
    a,b,c=(df[t].to_numpy() for t in ('A','B','C'))
    return (18 + 1.4*a + 0.9*b + 1.1*c - 2.3*a*a - 1.8*b*b - 1.5*c*c + 0.8*a*b - 0.5*a*c + 0.4*b*c)

def make_data():
    df=generate_ccd()
    rng=np.random.default_rng(SEED)
    df['response']=synthetic_mean(df)+rng.normal(0,0.35,len(df))
    return df

def fit_model(data):
    return smf.ols(FORMULA,data=data).fit()

def predict_biomass(model,x):
    return float(model.predict(pd.DataFrame([dict(zip('ABC',x))])).iloc[0])

def predict_viability(x):
    a,b,c=x
    return 96.0-2*(a-.05)**2-2*(b+.15)**2-1.5*(c+.1)**2-.8*a*c

def predict_byproduct(x):
    """Function transcribed from 9.10 Word paragraph 4099."""
    a,b,c=x
    return 1.5 + .65*c + .35*a*a + .30*b*b

def desirability_max(y,lower,target):
    return float(np.clip((y-lower)/(target-lower),0,1))

def desirability_min(y,target,upper):
    return float(np.clip((upper-y)/(upper-target),0,1))

def overall_desirability(x,model):
    d1=desirability_max(predict_biomass(model,x),15,18.5)
    d2=desirability_max(predict_viability(x),90,96)
    d3=desirability_min(predict_byproduct(x),1,2.5)
    return float((d1*d2*d3)**(1/3))  # equal weights: explicit book convention

def main():
    data=make_data()
    model=fit_model(data)
    bounds=[(-1,1)]*3
    constraint={'type':'ineq','fun':lambda x: .6-x[0]-x[1]}
    res=minimize(lambda x:-overall_desirability(x,model),np.zeros(3),method='SLSQP',bounds=bounds,constraints=[constraint])
    assert res.success
    print('CCD runs:',len(data),'unique:',len(data[['A','B','C']].drop_duplicates()))
    print('R2:',round(model.rsquared,6))
    print('Multiresponse x:',res.x.round(6))
    print('Overall desirability:',round(overall_desirability(res.x,model),6))
    return data,model,res

if __name__=='__main__':main()
