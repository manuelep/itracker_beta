# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    db.issue.description.readable = 'view' in request.args or 'edit' in request.args
    if 'new' in request.args:
        db.issue.closed.writable = False
    grid = SQLFORM.smartgrid(db.issue,
        csv = False
    )
    return locals()

@auth.requires_login()
def customize():
    return _customize()
