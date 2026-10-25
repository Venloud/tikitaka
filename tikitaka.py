#!/usr/bin/env python3
"""Thin entry point to the existing Vandam Route, ECC and memory implementations."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['route','skills','memory','doctor'])
    p.add_argument('args',nargs=argparse.REMAINDER)
    a=p.parse_args()
    root=Path(os.environ.get('VANDAM_ROOT',str(Path(__file__).resolve().parent.parent/'claudevandam'))).resolve()
    helper=root/'route/skill/scripts/route-state.mjs'
    ecc=root/'integrations/ecc/ecc.py'
    memory=root/'memory/memory.py'
    if a.command=='doctor':
        print(json.dumps({'vandam_root':str(root),'route_available':helper.is_file(),
                          'ecc_available':ecc.is_file(),'memory_available':memory.is_file(),
                          'harnesses':{x:shutil.which(x) is not None for x in ['node','python3','claude','codex','kimi']},
                          'runtime_authority':'Original Vandam Route state.json',
                          'model_calls_made':False,'approval_gates_bypassed':False},indent=2))
        return 0 if helper.is_file() and ecc.is_file() and memory.is_file() else 2
    if not helper.is_file() or not ecc.is_file():
        p.error('Locate the existing sibling claudevandam integration checkout or supply VANDAM_ROOT')
    if a.command=='route':cmd=['node',str(helper),*a.args]
    elif a.command=='skills':cmd=[sys.executable,str(ecc),'select','--project',str(Path(__file__).resolve().parent),'--task',' '.join(a.args)]
    else:
        if not memory.is_file():p.error('Vandam memory feature branch is required')
        if not a.args or a.args[0] not in ['recall','graph','serve']:p.error('memory supports recall, graph or serve (read-only)')
        cmd=[sys.executable,str(memory),a.args[0],'--root',str(root),*a.args[1:]]
    return subprocess.run(cmd).returncode


if __name__=='__main__':
    sys.exit(main())
