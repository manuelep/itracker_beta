#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *

class Populator(object):

    @staticmethod
    def bulk(table, recs):
        #table.truncate()
        db = table._db
        if db(table.id>0).count()==0:
            table.bulk_insert(recs)

class IssueReferences(object):

    def __init__(self, tab):
        self.tab = tab
        self.db = tab._db

    def _loop(self):
        for field in self.tab.fields:
            if self.tab[field].type.startswith('reference'):
                tablename = self.tab[field].type.split()[1]
                if 'is_default' in self.db[tablename].fields:
                    yield field, tablename #, value
                else:
                    continue

    def _assign_default(self, f, t):
        res = self.db(self.db[t].is_default==True).select(self.db[t].id).first()
        if not res is None:
            self.tab[f].default = res.id

    def _assign_represent(self, f, t):
        if callable(self.db[t]._format):
            self.tab[f].represent = lambda v,r: self.db[t]._format(self.db[t][v])
        elif isinstance(self.db[t]._format, basestring):
            self.tab[f].represent = lambda v,r: self.db[t]._format % self.db[t][v]
        else:
            # WHATELSE?
            pass

    def assign(self):
        for f, t in self._loop():
            self._assign_default(f, t)
            self._assign_represent(f, t)

class UniqueDefault(object):
    """ is_default field values should be set to True just for only one record
    so I set up a callback method for the tables that got this field that turn
    all other values to False if a True value is inserted
    """

    def __init__(self, tab):
        self.tab = tab

    def __call__(self, s, f):
        """ Before update callback """
        # TODO: dicide what to do if the passed set referes to more than one record and
        # is_default is set to True
        if f['is_default']==True:
            db(self.tab.is_default==True).update_naive(is_default=False)
