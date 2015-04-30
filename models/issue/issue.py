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