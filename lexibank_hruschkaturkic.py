# coding=utf-8
from __future__ import unicode_literals, print_function
from itertools import groupby

import attr
import lingpy
from pycldf.sources import Source
from clldutils.path import Path
from clldutils.misc import slug
from pylexibank.dataset import Dataset as BaseDataset

from pylexibank.dataset import Metadata, Concept
from pylexibank.util import pb

class Dataset(BaseDataset):
    dir = Path(__file__).parent

    def cmd_install(self, **kw):
        with self.cldf as ds:
            data = {}
            for taxon, string in pb(
                    self.raw.read_tsv('TurkicFullBoundaries.txt')):
                out = []
                for char in string:
                    if char == '-':
                        out += ['-']
                    else:
                        out += [char]
                out = ' '.join(out)
                data[taxon] = [''.join(x).strip() for x in out.split(':')]


