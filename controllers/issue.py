# -*- coding: utf-8 -*-

from plugin_shared_tools import CheckTextLength

@auth.requires_login()
def index():

    if 'assigned_to_user' in request.args:
        query = db.issue.assignedto.belongs(auth.user_groups)
    else:
        query = db.issue.id>0

    if 'active_only' in request.args:
        query &= db.issue.closed!=True

    if request.vars.issuegrp_id:
        sq = db(
            (db.issue.id==db.link_issue_issuegrp.issue_id) & \
            (db.link_issue_issuegrp.issuegrp_id==request.vars.issuegrp_id)
        )._select(db.link_issue_issuegrp.issue_id)
        query &= db.issue.id.belongs(sq)
    elif request.vars.project_id:
        sq1 = db(
            (db.link_issue_issuegrp.issuegrp_id==db.link_issuegrp_project.issuegrp_id) & \
            (db.link_issuegrp_project.project_id==request.vars.project_id)
        )._select(db.link_issue_issuegrp.issue_id)
        
        sq2 = db(
            (db.issue.id==db.link_issue_project.issue_id) & \
            (db.link_issue_project.project_id==request.vars.project_id)
        )._select(db.link_issue_project.issue_id)

        query &= db.issue.id.belongs(sq1)|db.issue.id.belongs(sq2)

    db.project.title.label = T("Project")
    db.project.title.represent = lambda v,r: v or ''
    
    # PRIORITY
    db.issue.priority.readable = False
    db.issue_priority.sort_order.label = db.issue.priority.label
    db.issue_priority.sort_order.readable = False
#     db.issue_priority.sort_order.represent = lambda v,r: db.issue_priority._format(db.issue_priority[r.issue.priority])
    
    # SEVERITY
    db.issue.severity.readable = False
    db.issue_severity.sort_order.label = db.issue.severity.label
    db.issue_severity.sort_order.readable = False
#     db.issue_severity.sort_order.represent = lambda v,r: db.issue_severity._format(db.issue_severity[r.issue.severity])

    db.issue.id.label = T("Issue id")
    db.issue.id.represent = IssueGrid.render
    if not any([i in request.args for i in ('view', 'edit',)]):
        db.issue.title.readable = False
        db.issue.typology.readable = False
        db.issue.weigth.readable = False
        db.issue.closed.readable = False
        db.issue.dead_line.readable = False
        db.issue.status.readable = False
        db.issue.description.readable = False

    fields = [db.issue.id, db.issue.title, db.issue.description, db.issue.typology,
        db.issue.priority, db.issue_priority.sort_order,
        db.issue.severity, db.issue_severity.sort_order,
        db.issue.weigth, db.issue.status,
        db.issue.dead_line, db.issue.assignedto,
        db.issue.modified_on, db.issue.closed,
    ]
    db.issue.modified_on.readable = True

    grid = SQLFORM.grid(query & (db.issue.priority==db.issue_priority.id) & (db.issue.severity==db.issue_severity.id),
        field_id = db.issue.id,
        fields = fields,
        orderby = db.issue.closed|db.issue.status|db.issue.weigth|db.issue.modified_on,
        args = request.args,
        links = [
            dict(header='Projects', body=IssueGrid.prj_link),
            dict(header='Tasks', body=IssueGrid.tsk_link),
            dict(header='Wikis', body=IssueGrid.doc_link),
            dict(header='Comments', body=lambda r: IssueGrid.add_new_comment(r.id)),
        ],
        links_in_grid = False,
        oncreate = IssueGrid.oncreate,
        csv = False,
        formname = 'issue'
    )
    return locals()

# @auth.requires_login()
# def new():
#     """ DEPRECATED """
#     return new_record('issue')

def onclick_hideModal(e):
    """ data-dismiss="modal"
    WARNING: problema noto: questo chiude il form aperto in modal prima della validazione
    se qualcosa non passa la validazione si viene avvertiti via flash ma oramai il form è chiuso.
    Per ora ho limitato via js la digitazione di più di 255 caratteri mediante widget dedicato.
    """
    e.attributes['_onclick'] = "$('.modal').modal('hide');"
    return e

@auth.requires_login()
def _new_comment():
    issue_id = request.args(0, cast=int)
    reply_to = request.args(1, cast=int, default=None)
    
    db.thread.issue_id.writable = False
    
    db.thread.issue_id.represent = lambda v,r: db.issue[issue_id].title
    db.thread.issue_id.label = T("Issue")

    db.thread.reply_to.writable = False
    db.thread.reply_to.readable = False
    db.thread.reply.widget = CheckTextLength.widget
    form = SQLFORM(db.thread, hidden=dict(issue_id=issue_id, reply_to=reply_to))
    form.vars.issue_id = request.vars.issue_id
    form.vars.reply_to = request.vars.reply_to
    if form.process().accepted:
        pass

    form.elements('input[type=submit]', replace=onclick_hideModal)
    
    return dict(form=form)

@auth.requires_login()
def _comments():
    return IssueGrid.threads(request.args(0, cast=int))