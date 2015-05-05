# -*- coding: utf-8 -*-

class IssuegrpGrid(object):

    @staticmethod
    def prj_link(r):
        res = db(
            (db.project.id==db.link_issuegrp_project.project_id) & \
            (db.link_issuegrp_project.issuegrp_id==r.id)
        ).select(db.project.ALL, distinct=True)
        url = lambda rid: URL('project', 'index', extension="",
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
        def _get_lis(row):

            def _get_li(id, slug):
                url = URL('wiki', 'index', extension='', args=('issue_%s' % id +'_'+slug,))
                return LI(A(slug, _href=url))
            
            for slug in row.slugs:
                yield _get_li(row.id, slug)
            
#         res = db(
#             (db.project.id==db.link_issuegrp_project.project_id) & \
#             (db.link_issuegrp_project.issuegrp_id==r.id)
#         ).select(db.project.ALL, distinct=True)

        lis = [l for l in _get_lis(r)]

#         for prj in res:
#             lis += [LI(_class="divider"), LI(res.title, _role="presentation", _class="dropdown-header")]
#             lis += [l for l in _get_lis(prj)]

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
    def oncreate(form):
        if request.vars.project_id:
            db.link_issuegrp_project[0] = dict(issuegrp_id=form.vars.id, project_id=request.vars.project_id)
        elif request.vars.project_ids:
            db.link_issuegrp_project.bulk_insert([
                dict(issuegrp_id=form.vars.id, project_id=i) \
            for i in request.vars.project_ids])