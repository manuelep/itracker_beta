# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello! And welcome to my own issue tracker.")
    return dict()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@auth.requires_login()
def access():

    db.auth_membership.user_id.represent = lambda v,_: "%(first_name)s %(last_name)s" % db.auth_user[v]
    db.auth_membership.group_id.represent = lambda v,_: db.auth_group[v].role

    db.auth_user.registration_key.writable = True
    db.auth_user.registration_key.requires = IS_IN_SET([
        ("pending", "Pending",),
        ("blocked", "Blocked",),
        ("", "Accepted",)
    ])
    db.auth_user.registration_key.default = "pending"
    grid = SQLFORM.smartgrid(db['auth_'+request.args(0)],
        args = request.args[:1],
        linked_tables = [db.auth_membership],
        csv = False,
    )
    return locals()

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


