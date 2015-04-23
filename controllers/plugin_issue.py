# -*- coding: utf-8 -*-

def index():
    db.issue.description.readable = 'view' in request.args or 'edit' in request.args
    if 'new' in request.args:
        db.issue.closed.writable = False
    grid = SQLFORM.smartgrid(db.issue,
        csv = False
    )
    return locals()

def _customize():
    return customize()
