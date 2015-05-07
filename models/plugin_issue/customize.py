# -*- coding: utf-8 -*-

def _customize():
    tabname = request.args(0)
    grid = SQLFORM.grid(db[tabname], args=request.args[:1], csv = False)
    return dict(grid=grid)