from bitdeli.insight import insight
from bitdeli.widgets import Text, Bar, Table
from discodb.query import Q, Literal, Clause

COLORS = {'least active': 'rgb(255, 36, 0)',
          'barely active': 'rgb(255, 197, 11)',
          'moderately active': 'rgb(179, 220, 108)',
          'very active': 'rgb(0, 163, 89)',
          'most active': 'rgb(118, 192, 255)'}

def keys(model):
    for i, key in enumerate(sorted(model.keys(), key=lambda x: int(x.split('-')[0]))):
        yield 'c%d' % i, key.split(' ', 2)

def columns(model):
    for col, (counts, perc, label) in keys(model):
        yield {'name': col,
               'label': label.capitalize(),
               'width': perc}
    
def rows(model):
    def streak():
        for col, (counts, perc, label) in keys(model):
            yield col, {'label': perc, 'background': COLORS[label]}
    def legend():
        for col, (counts, perc, label) in keys(model):
            mi, ma = counts.split('-')
            if mi == ma:
                counts = mi
            txt = counts + (' event' if counts == '1' else ' events')
            yield col, {'label': txt,
                        'background': COLORS[label]}
    yield dict(streak())
    yield dict(legend())

@insight
def view(model, params):
    yield Table(size=(12, 3),
                fixed_width=False,
                data={'columns': list(columns(model)),
                      'rows': list(rows(model))})