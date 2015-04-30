# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    if request.vars.issuegrp_id:
        sq = db(
            (db.issue.id==db.link_issue_issuegrp.issue_id) & \
            (db.link_issue_issuegrp.issuegrp_id==request.vars.issuegrp_id)
        )._select(db.link_issue_issuegrp.issue_id)
        query = db.issue.id.belongs(sq)
    elif request.vars.project_id:
        sq1 = db(
            (db.link_issue_issuegrp.issuegrp_id==db.link_issuegrp_project.issuegrp_id) & \
            (db.link_issuegrp_project.project_id==request.vars.project_id)
        )._select(db.link_issue_issuegrp.issue_id)
        
        sq2 = db(
            (db.issue.id==db.link_issue_project.issue_id) & \
            (db.link_issue_project.project_id==request.vars.project_id)
        )._select(db.link_issue_project.issue_id)

        query = db.issue.id.belongs(sq1)|db.issue.id.belongs(sq2)
    else:
        query = db.issue.id>0

    db.project.title.label = T("Project")
    db.project.title.represent = lambda v,r: v or ''
    
    fields = [db.issue.id, db.issue.title,
        db.issue.typology, db.issue.priority,
        db.issue.severity, db.issue.weigth, db.issue.status,
        db.issue.dead_line, db.issue.assigned_to, db.issue.closed,
    ]

    grid = SQLFORM.grid(query,
        field_id = db.issue.id,
        fields = fields,
        orderby = db.issue.weigth,
        links = [
            dict(header='Projects', body=IssueGrid.prj_link),
            dict(header='Tasks', body=IssueGrid.tsk_link),
            dict(header='Wikis', body=IssueGrid.doc_link),
            dict(header='Comments', body=IssueGrid.add_new_comment),
        ],
        links_in_grid = False,
        oncreate = IssueGrid.oncreate,
        csv = False,
        formname = 'issue'
    )
    return locals()

@auth.requires_login()
def new():
    return new_record('issue')


@auth.requires_login()
def new_comment():
    issue_id = request.args(0, cast=int)
    reply_to = request.args(1, cast=int, default=None)
    
    db.thread.issue_id.writable = False
    
    db.thread.issue_id.represent = lambda v,r: db.issue[issue_id].title
    db.thread.issue_id.label = T("Issue")

    db.thread.reply_to.writable = False
    db.thread.reply_to.readable = False
    form = SQLFORM(db.thread, hidden=dict(issue_id=issue_id, reply_to=reply_to))
    form.vars.issue_id = request.vars.issue_id
    form.vars.reply_to = request.vars.reply_to
    if form.process().accepted:
        if not request.vars.redirect_url is None:
            redirect(request.vars.redirect_url)
    
    return dict(form=form)