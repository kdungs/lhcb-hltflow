#!/usr/bin/env python

prefix = 'hltdimuon'
code = """
VeloCandidates
>>  MatchVeloMuon
>>  tee  ( monitor( TC_SIZE > 0, '# pass match', LoKi.Monitoring.ContextSvc ) )
>>  tee  ( monitor( TC_SIZE    , 'nMatched' , LoKi.Monitoring.ContextSvc ) )
>>  LooseForward
>>  tee  ( monitor( TC_SIZE > 0, '# pass forward', LoKi.Monitoring.ContextSvc ) )
>>  tee  ( monitor( TC_SIZE , 'nForward' , LoKi.Monitoring.ContextSvc ) )
>>  ( ( TrPT > %(PT)s * MeV ) & ( TrP  > %(P)s  * MeV ) )
>>  IsMuon
>>  tee  ( monitor( TC_SIZE > 0, '# pass IsMuon', LoKi.Monitoring.ContextSvc ) )
>>  tee  ( monitor( TC_SIZE , 'nIsMuon' , LoKi.Monitoring.ContextSvc ) )
>>  FitTrack
>>  tee  ( monitor( TC_SIZE > 0, '# pass fit', LoKi.Monitoring.ContextSvc ) )
>>  tee  ( monitor( TC_SIZE , 'nFitted' , LoKi.Monitoring.ContextSvc ) )
>>  ( TrCHI2PDOF < %(TrChi2)s )
>>  MakeDiMuons
>>  tee  ( monitor( TC_SIZE > 0, '# pass vertex', LoKi.Monitoring.ContextSvc ) )
>>  tee  ( monitor( TC_SIZE , 'nVertices' , LoKi.Monitoring.ContextSvc ) )
>>  ( RV_MASS ( 'mu+' , 'mu-' ) > %(M)s * MeV )
>>  tee  ( monitor( TC_SIZE > 0, '# pass mass', LoKi.Monitoring.ContextSvc ) )
>>  tee  ( monitor( TC_SIZE , 'nDiMuons' , LoKi.Monitoring.ContextSvc ) )
>>  SINK( 'Hlt1%(name)sDecision' )
>> ~TC_EMPTY
"""

def latex_sanitise(s):
    from functools import reduce
    escape = '%_&~'
    replacers = (lambda s: s.replace(e, '\{}'.format(e)) for e in escape)
    return reduce(lambda s, f: f(s), replacers, s)

def is_cut(op):
    return op.startswith('(')

def is_sink(op):
    return op.startswith('SINK')

def make_tikz_node(op, _id):
    _class = 'block'
    if _id == 0:
        return '\\node [start] ({prefix}-{id}) {{{op}}};'.format(**{'prefix': prefix, 'id': _id, 'op': op})
    if is_cut(op):
        _class += ', cut'
        op = 'Cut: ' + op
    if is_sink(op):
        _class += ', sink'
    return '\\node [{_class}, below=of {prefix}-{prev}] ({prefix}-{id}) {{{op}}};'.format(**{'_class': _class, 'prefix': prefix, 'prev': _id - 1, 'id': _id, 'op': op})


import re
operations = [line for line in code.split('\n') if line]
operations = [op for op in operations if 'tee' not in op]
operations = [re.sub('>>\s+', '', op) for op in operations]
operations = [make_tikz_node(op, i) for i, op in enumerate(operations)]
lines = ['\\path [line] ({prefix}-{a}) -- ({prefix}-{b});'.format(prefix=prefix, a=a, b=b)
        for a, b in zip(range(len(operations)), range(1, len(operations)))]
tikzstring = latex_sanitise('\n'.join(operations))
tikzstring += '\n'.join(lines)


def write_to_file():
    import shutil as sh
    sh.copytree('template/', 'result/')
    with open('result/flowchart.tex') as f:
       template = f.read()
    with open('result/flowchart.tex', 'w') as f:
       f.write(template.replace('{{ STREAMER }}', tikzstring))


write_to_file()
