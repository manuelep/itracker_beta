# -*- coding: utf-8 -*-

class IssueGrid(object):

    @staticmethod
    def prj_link(r):
        if not hasattr(r, 'title'): return ''
        res_s = db(
            (db.project.id==db.link_issue_project.project_id) & \
            (db.link_issue_project.issue_id==db.issue.id) & \
            (db.issue.id==r.id)
        ).select(db.project.ALL, distinct=True, orderby=db.project.title)
        
        res_l = db(
            (db.project.id==db.link_issuegrp_project.project_id) & \
            (db.link_issuegrp_project.issuegrp_id==db.issuegrp.id) & \
            (db.issuegrp.id==db.link_issue_issuegrp.issuegrp_id) & \
            (db.link_issue_issuegrp.issue_id==db.issue.id) & \
            (db.issue.id==r.id)
        ).select(db.project.ALL, distinct=True, orderby=db.project.title)

        # WARNING! verificare nel tempo il comportamento dell'operatore
        res = res_s or res_l
        res = res.sort(lambda r: r.title)

        url = lambda rid: URL('project', 'index',
            args = ('project', 'view', 'project', rid,),
            user_signature=True
        )
        return DIV(
            BUTTON(
                I(_class="glyphicon glyphicon-folder-open"), ' ',
                T("Projects"), SPAN(_class="caret"),
                _type="button",
                _class="btn btn-primary btn-sm dropdown-toggle",
                **{'_data-toggle': "dropdown", '_aria-expanded': "false"}
            ),
            UL(
                *[LI(A(rec.title, _href=url(rec.id))) \
                for rec in res],
                _class="dropdown-menu", _role="menu"
            ),
            _class="btn-group"
        )

    @staticmethod
    def tsk_link(r):
        if not hasattr(r, 'title'): return ''
        res = db(
            (db.issuegrp.id==db.link_issue_issuegrp.issuegrp_id) & \
            (db.link_issue_issuegrp.issue_id==r.id)
        ).select(db.issuegrp.ALL)
        url = lambda rid: URL('issuegrp', 'index',
            args = ('issuegrp', 'view', 'issuegrp', rid,),
            user_signature=True
        )
        return DIV(
            BUTTON(
                I(_class="glyphicon glyphicon-folder-open"), ' ',
                T("Tasks"), SPAN(_class="caret"),
                _type="button",
                _class="btn btn-primary btn-sm dropdown-toggle",
                **{'_data-toggle': "dropdown", '_aria-expanded': "false"}
            ),
            UL(
                *[LI(A(rec.title, _href=url(rec.id))) \
                for rec in res],
                _class="dropdown-menu", _role="menu"
            ),
            _class="btn-group"
        )

    @staticmethod
    def doc_link(r):
        """
        <!-- Single button -->
        <div class="btn-group">
          <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-expanded="false">
            Action <span class="caret"></span>
          </button>
          <ul class="dropdown-menu" role="menu">
            <li><a href="#">Action</a></li>
            <li><a href="#">Another action</a></li>
            <li><a href="#">Something else here</a></li>
            <li class="divider"></li>
            <li role="presentation" class="dropdown-header">Dropdown header</li>
            <li><a href="#">Separated link</a></li>
            ...
          </ul>
        </div>
        """
        if not hasattr(r, 'slugs'): return ''
        def _get_lis(row):

            def _get_li(id, slug):
                url = URL('wiki', 'index', args=('issue_%s' % id +'_'+slug,))
                return LI(A(slug, _href=url))
            
            for slug in row.slugs:
                yield _get_li(row.id, slug)
            
        res = db(
            (db.issuegrp.id==db.link_issue_issuegrp.issuegrp_id) & \
            (db.link_issue_issuegrp.issue_id==r.id)
        ).select(db.issuegrp.ALL)

        lis = [l for l in _get_lis(r)]

        for grp in res:
            lis += [LI(_class="divider"), LI(grp.title, _role="presentation", _class="dropdown-header")]
            lis += [l for l in _get_lis(grp)]

        return DIV(
            BUTTON(T("Wiki pages"), SPAN(_class="caret"),
                _type = "button",
                _class = "btn btn-info btn-sm dropdown-toggle",
                **{
                    '_data-toggle': 'dropdown',
                    '_aria-expanded': 'false'
                }
            ),
            UL(
                *lis,
                _class = 'dropdown-menu',
                _role = 'menu'
            ),
            _class = "btn-group"
        )

    @staticmethod
    def add_new_comment(r, label="Add comment"):
        redirect_url = URL(args=request.args, vars=request.vars, user_signature=True)
        return A(
            T(label),
            _href=URL('issue', 'new_comment', args=(r.id,), vars=dict(redirect_url=redirect_url)),
            _class = "btn btn-default"
        )

    @classmethod
    def threads(cls, issue_id):
        """
        db.item.total_price = Field.Virtual(
    'total_price',
    lambda row: row.item.unit_price*row.item.quantity)
        """

#         def _btn(c):
#             return A(
#                 T("Replay"),
#                 _href = URL('issue', 'new_comment',
#                     args=(issue_id, c.id,),
#                     vars=dict(redirect_url=URL())
#                 ),
#                 _class = "btn btn-default btn-xs"
#             )

        all_comments = db(db.thread.issue_id==issue_id).select(orderby=db.thread.reply_to|~db.thread.created_on)
        def _walker(comment_id):
            for comment in all_comments.find(lambda row: row.reply_to==comment_id):
                yield comment
                for reply in _walker(comment.id):
                    yield reply

        rows = []
        
        for comment in all_comments.find(lambda row: row.reply_to==None):
            main = DIV(
                DIV(
                    T("Comment id: "), comment.id,
                    _class="col-md-1"
                ),
                DIV(comment.reply, _class="col-md-9 alert alert-info"),
                DIV(cls.add_new_comment(comment, "Reply"), _class="col-md-2"),
                _class="row"
            )
            subs = [DIV(
                DIV(
                    T("Comment id: "), reply.id,
                    _class="col-md-1"
                ),
                DIV(
                    T("In reply to: "),
                    reply.reply_to,
                    _class="col-md-1"
                ),
                DIV(reply.reply, _class="col-md-8 alert alert-warning"),
                DIV(cls.add_new_comment(reply, "Reply"), _class="col-md-2"),
                _class = "row"
            ) for reply in _walker(comment.id)]
            rows += [main]
            rows += subs

        return DIV(DIV(*rows, _class="container-fluid"))