# lhcb-hltflow

[![Build Status](https://travis-ci.org/kdungs/lhcb-hltflow.svg?branch=master)](https://travis-ci.org/kdungs/lhcb-hltflow)
[![Documentation Status](https://readthedocs.org/projects/lhcb-hltflow/badge/?version=latest)](https://readthedocs.org/projects/lhcb-hltflow/?badge=latest)

A tool that automatically produces TikZ-based flowcharts for HLT1 streamers. Requires Python 3.4 as it makes use of the [`enum`](https://docs.python.org/3/library/enum.html) library.

## Obtaining configuration files
In order to obtain the configurations of the HLT1 muon lines from a TCK, the following Python script can be used with Moore.

```python
#!/usr/bin/env python

import json
import TCKUtils.utils as ut

TCK = 0x00fb0051
FILENAME = 'hlt1streamers2015.json'
STREAMERS = [
    'Hlt1TrackMuonUnit',
    'Hlt1DiMuonHighMassStreamer',
    'Hlt1DiMuonLowMassStreamer',
    'Hlt1SingleMuonHighPTStreamer',
    'Hlt1SingleMuonNoIPStreamer'
]

tree = ut.getConfigTree(TCK)
codes = [{'name': streamer.replace('Streamer', ''),
          'code': tree.leafs()[streamer].props['Code']}
         for streamer in STREAMERS]

with open(FILENAME, 'w') as jsonfile:
    json.dump(codes, jsonfile)
```

save it as (for example) `streamers.py` and run it via

```
lb-run Moore v23r7p5 python streamers.py
```

The resulting file is used with this program via

```
python3 hltflow.py -c hlt1streamers.json test > latex/flowchart.tex
```

To compile the LaTeX file do

```
cd latex
make
```

and open `build/flowchart.pdf` (`make open` on a Mac).
