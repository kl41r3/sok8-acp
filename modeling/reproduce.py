#!/usr/bin/env python3
"""Regenerate deterministic data/plots in a separate clean output copy; no API."""
from pathlib import Path
import argparse,os,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--plots',action='store_true');args=p.parse_args()
    output=args.output.resolve();assert not output.exists(),'Choose a new output directory; existing files are never overwritten.'
    assert ROOT not in output.parents,'Output must be outside modeling/ to avoid recursive copying.'
    shutil.copytree(ROOT,output,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1';env['MPLCONFIGDIR']=str(output/'.mpl-cache')
    commands=[['case-a/compute.py'],['case-b/compute.py'],['replay.py','--output','replay-receipt.json']]
    if args.plots:commands.extend([['case-a/plot.py'],['case-b/plot.py'],['case-a/supplemental/optimized-cap/plot.py']])
    for cmd in commands:
        result=subprocess.run([sys.executable,'-B',*cmd],cwd=output,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        if result.returncode:print(result.stdout);print(result.stderr,file=sys.stderr);raise SystemExit(result.returncode)
        print('Passed: '+' '.join(cmd))
    print('Saved regenerated output copy: '+str(output))
if __name__=='__main__':main()
