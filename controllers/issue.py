# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    query = (db.issue.id==db.link_issue_project.issue_id) & \
        (db.link_issue_project.project_id==db.project.id)

    db.project.title.label = T("Project")

    grid = SQLFORM.grid(query,
        field_id = db.issue.id,
        fields = [db.issue.id, db.issue.title, db.project.title,
            db.issue.typology, db.issue.priority,
            db.issue.severity, db.issue.weigth, db.issue.status,
            db.issue.dead_line, db.issue.assigned_to, db.issue.closed,
            db.thread.issue_id, db.thread.replay, db.thread.replay_to
        ],
        orderby = db.issue.weigth,
        links = [
            dict(header='Projects', body=IssueGrid.prj_link),
            dict(header='Tasks', body=IssueGrid.tsk_link),
            dict(header='Wikis', body=IssueGrid.doc_link),
        ],
        links_in_grid = False,
        csv = False,
        formname = 'issue'
    )
    return locals()

@auth.requires_login()
def new():
    return new_record('issue')
