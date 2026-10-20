"""October 2026 public reconstruction of the documented 2023 OLS workflow.

The built-in demonstration is synthetic; no internship data are distributed.
Specification comparisons use one common complete-case sample per outcome.
"""
from pathlib import Path
from itertools import combinations
from math import comb
import argparse
import json
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def prepare(frame, outcome, base, controls):
    names = [outcome] + list(base) + list(controls)
    if len(names) != len(set(names)):
        raise ValueError('Outcome and predictors must be distinct and unique.')
    missing = set(names) - set(frame.columns)
    if missing: raise ValueError('Missing columns: ' + ', '.join(sorted(missing)))
    data = frame[names].apply(pd.to_numeric, errors='raise').replace([np.inf,-np.inf],np.nan).dropna()
    if len(data) <= len(names) + 2: raise ValueError('Too few complete observations for this control set.')
    if data[outcome].std() <= 1e-12: raise ValueError('Outcome must vary.')
    return data


def compare_models(frame, outcome, base, controls, max_controls=3, max_models=256):
    if not base: raise ValueError('Supply at least one base predictor.')
    if not isinstance(max_controls, int) or not isinstance(max_models, int) or max_controls < 0 or max_models < 1: raise ValueError('Invalid search limits.')
    model_count = sum(comb(len(controls), k) for k in range(min(max_controls, len(controls)) + 1))
    if model_count > max_models: raise ValueError('Search exceeds max_models; reduce controls or max_controls.')
    data = prepare(frame,outcome,base,controls)
    specs = [list(base)+list(extra) for k in range(min(max_controls,len(controls))+1) for extra in combinations(controls,k)]
    if len(specs)>max_models: raise ValueError('Search exceeds max_models; reduce controls or max_controls.')
    rows=[]; fits={}; skipped=[]
    for i, predictors in enumerate(specs):
        key=f'model_{i:03d}'
        X=sm.add_constant(data[predictors],has_constant='add')
        if np.linalg.matrix_rank(X.to_numpy())<X.shape[1]:
            skipped.append({'model':key,'predictors':predictors,'reason':'rank deficient'}); continue
        fit=sm.OLS(data[outcome],X).fit(cov_type='HC3')
        fits[key]=(predictors,fit)
        rows.append({'model':key,'predictors':'+'.join(predictors),'n':int(fit.nobs),
            'r_squared':float(fit.rsquared),'adjusted_r_squared':float(fit.rsquared_adj),
            'aic':float(fit.aic),'bic':float(fit.bic),'predictor_count':len(predictors)})
    if not rows: raise ValueError('Every specification was rank deficient.')
    comparison=pd.DataFrame(rows).sort_values(['adjusted_r_squared','bic'],ascending=[False,True]).reset_index(drop=True)
    return data,comparison,fits,skipped


def synthetic_data(seed=20261019,n=400):
    rng=np.random.default_rng(seed)
    numeracy=rng.normal(size=n); coast=rng.normal(size=n)
    climate=rng.normal(size=n); missions=.35*numeracy+rng.normal(size=n)
    population=rng.lognormal(.5,.5,size=n)
    life=55+4*numeracy-1.8*coast+1.2*climate+rng.normal(scale=3,size=n)
    frame=pd.DataFrame({'life_expectancy':life,'numeracy':numeracy,'coast_distance':coast,
        'climate':climate,'missions':missions,'population':population})
    frame.loc[rng.choice(n,12,replace=False),'climate']=np.nan
    return frame


def run(frame,outcome,base,controls,output,synthetic=False,max_controls=3):
    output=Path(output);output.mkdir(exist_ok=True,parents=True)
    data,comparison,fits,skipped=compare_models(frame,outcome,base,controls,max_controls)
    comparison.to_csv(output/'model_comparison.csv',index=False)
    coefficients=[];vifs=[];summaries=[]
    for key in comparison.model:
        predictors,fit=fits[key]
        intervals=fit.conf_int()
        for name in fit.params.index:
            coefficients.append({'model':key,'variable':name,'coefficient':float(fit.params[name]),
                'hc3_se':float(fit.bse[name]),'p_value':float(fit.pvalues[name]),
                'ci_low':float(intervals.loc[name,0]),'ci_high':float(intervals.loc[name,1])})
        X=sm.add_constant(data[predictors],has_constant='add')
        for j,name in enumerate(X.columns):
            if name!='const':vifs.append({'model':key,'variable':name,'vif':float(variance_inflation_factor(X.to_numpy(),j))})
        if len(summaries)<10:summaries.append(key+'\n'+fit.summary().as_text())
    pd.DataFrame(coefficients).to_csv(output/'coefficients_hc3.csv',index=False)
    pd.DataFrame(vifs).to_csv(output/'vif.csv',index=False)
    (output/'top_model_summaries.txt').write_text('\n\n'.join(summaries))
    best=comparison.model.iloc[0];fit=fits[best][1]
    fig,ax=plt.subplots(figsize=(6,5));ax.scatter(data[outcome],fit.fittedvalues,s=15,alpha=.5)
    lo=min(data[outcome].min(),fit.fittedvalues.min());hi=max(data[outcome].max(),fit.fittedvalues.max())
    ax.plot([lo,hi],[lo,hi],color='black',linestyle='--')
    ax.set(title=('SYNTHETIC DEMONSTRATION: ' if synthetic else '')+'Fitted versus observed',xlabel=outcome,ylabel='Fitted value')
    fig.tight_layout();fig.savefig(output/'fit.svg');plt.close(fig)
    metadata={'synthetic':synthetic,'input_rows':len(frame),'common_complete_case_rows':len(data),
        'outcome':outcome,'base':base,'controls':controls,'models_estimated':len(comparison),'skipped':skipped,
        'inference':'Exploratory specification search. HC3 standard errors do not correct for multiple-model selection.',
        'provenance':'Public reconstruction; original institutional data and unpublished findings are excluded.'}
    (output/'run_metadata.json').write_text(json.dumps(metadata,indent=2))
    return comparison


def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--demo',action='store_true');g.add_argument('--csv',type=Path)
    p.add_argument('--outcome',default='life_expectancy');p.add_argument('--base',nargs='+',default=['numeracy'])
    p.add_argument('--controls',nargs='*',default=['coast_distance','climate','missions','population'])
    p.add_argument('--max-controls',type=int,default=3);p.add_argument('--output',default='demo_output')
    a=p.parse_args();frame=synthetic_data() if a.demo else pd.read_csv(a.csv)
    print(run(frame,a.outcome,a.base,a.controls,a.output,a.demo,a.max_controls).to_string(index=False))


if __name__=='__main__':main()
