# -*- coding: utf-8 -*-

class IssueGrid(object):

    @staticmethod
    def render(v, r):
        """ To be used as id represent function """

        def _rf(name):
            """ Render field value accordingly to their represent function """
            return db.issue[name].represent(r.issue[name], r)

        def _closed():
            if r.issue.closed:
                return SPAN(ICON('exclamation-sign', _title=T("Closed"), **{"_data-toggle": "tooltip", "_data-placement": "top"}), _class="text-success")
            else:
                return SPAN(ICON('paperclip', _title=T("Open"), **{"_data-toggle": "tooltip", "_data-placement": "top"}), _class="text-warning")

        def _dl():
            """ Dead line """
            if r.issue.dead_line is None:
                return SPAN(ICON('sunglasses', _title=T("Relax! No deadline fixed."), **{"_data-toggle": "tooltip", "_data-placement": "top"}), _class="text-primary")
            elif r.issue.closed:
                return SPAN(ICON('flag'), _class="text-success")
            
            today = date.today()
            if r.issue.dead_line >= today:
                return SPAN(ICON('flag'), _class="text-warning")
            elif r.issue.dead_line < today:
                return SPAN(ICON('fire', _title=T("Fired! Deadline passed and issue still open!"), **{"_data-toggle": "tooltip", "_data-placement": "top"}), _class="text-danger")

        def _cc():
            """ Comments """
            c = db(db.thread.issue_id==v).count()
            return SPAN(ICON("comment"), " ", c, _class="label label-default")

        return DIV(
            DIV(
                DIV(_closed(), " ", _rf('status'), _class="col-md-2"), # status
                DIV(_rf('typology'), _class="col-md-1"), # priority
                DIV(TAG.abbr("P", _title=T("Priority")), ": ", _rf('priority'), _class="col-md-2"), # priority
                DIV(TAG.abbr("S", _title=T("Severity")), ": ", _rf('severity'), _class="col-md-2"), # severity
                DIV(_dl(), " ", _rf('dead_line'), _class="col-md-4"), # deadline
                DIV(_cc(), _class="col-md-1"), # comments
                _class = "row"
            ), # header row with meta data
            # TODO: USE CSS!!!
            DIV(" ", _class="col-md-12"), DIV(" ", _class="col-md-12"), # BRUTTURA per distanziare meta info da titolo
            DIV(
                DIV(
                    DIV(
                        DIV(
                            DIV(
                                H4(
                                    A(
                                        "issue #", r.issue.id,
                                        _class="collapsed", _href="#collapse%s" % r.issue.id,
                                        **{
                                            '_data-toggle': "collapse",
                                            '_data-parent': "#accordion",
                                            '_aria-expanded': "true",
                                            '_aria-controls': "collapse%s" % r.issue.id
                                        } 
                                    ),
                                    ": ", r.issue.title,
                                    _class="panel-title"
                                ),
                                DIV(
                                    DIV(
                                        MARKMIN(r.issue.description),
                                        _class="panel-body"
                                    ),
                                    _id="collapse%s" % r.issue.id, _class="panel-collapse collapse", _role="tabpanel",
                                    **{'_aria-labelledby': "heading%s" % r.issue.id}
                                ),
                                _class="panel-heading", _role="tab", _id="headingOne"
                            ),
                            _class="panel panel-default"
                        ),
                        _class="panel-group", _id="accordion%s" % r.issue.id, _role="tablist",
                        **{'aria-multiselectable': "true"}
                    ),
                    _class = "col-md-12"
                ),
                _class = "row"
            ), # body row with title and description
            _class = "container-fluid"
        )

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
            extension = 'html',
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
        url = lambda rid: URL('issuegrp', 'index', extension="html",
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
                url = URL('wiki', 'index', extension='html', args=('issue-%s' % id +'-'+slug,))
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
    def add_new_comment_old(r, label="Add comment"):
        redirect_url = URL(args=request.args, vars=request.vars, user_signature=True)
        return A(
            T(label),
            _href=URL('issue', '_new_comment', args=(r.id,), vars=dict(redirect_url=redirect_url)),
            _class = "btn btn-default"
        )

    @staticmethod
    def add_new_comment(*args):
        """
        <!-- Small modal -->
        <button type="button" class="btn btn-primary" data-toggle="modal" data-target=".bs-example-modal-sm">Small modal</button>
        
        <div class="modal fade bs-example-modal-sm" tabindex="-1" role="dialog" aria-labelledby="mySmallModalLabel" aria-hidden="true">
          <div class="modal-dialog modal-sm">
            <div class="modal-content">
              ...
            </div>
          </div>
        </div>
        """
        label = T("Replay") if len(args)>1 else T("Add new comment")
        modal_id = 'modal-' + '-'.join([str(i) for i in args])
        load_url = URL('issue', '_new_comment.load', args=args)
        button = BUTTON(ICON("comment"), " ", label, _type="button",
            _onclick = "jQuery('#%(modal_id)s').html('loading...');jQuery.web2py.component('%(load_url)s', '%(modal_id)s');jQuery('.modal').on('hidden.bs.modal', function (e) {jQuery('#comments').get(0).reload();});" % locals(),
            _class="button btn btn-default btn-sm",
            **{
                '_data-toggle': 'modal',
                '_data-target': '.' + modal_id
            }
        )
        div = DIV(
            DIV(
                DIV(
                    # <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                    #BUTTON("x", _type="button", _class="close", **{'_data-dismiss': 'modal', '_aria-label': 'Close'}),
                    DIV(_id=modal_id),
                    _class = "modal-content"
                ),
                _class = "modal-dialog modal-lg"
            ),
            _id = "MyModal",
            _class = "modal fade " + modal_id,
            _tabindex="-1", _role="dialog",
            **{
                '_aria-labelledby': 'Comment on ' + modal_id,
                '_aria-hidden': "true"
            }
        )
        return SPAN(button, div)

    @staticmethod
    def _colors(c):
        n = len(c) or 1
        white = int("FF7171", 16)
        first = white/n
        return dict([(i.id, '#{0:06X}'.format(first*(n+1))) for n,i in enumerate(c)])

    @classmethod
    def threads(cls, issue_id):
        """
        """

        all_comments = db(db.thread.issue_id==issue_id).select(orderby=db.thread.reply_to|~db.thread.created_on)
        cols = cls._colors(all_comments)
        def _walker(comment_id):
            for comment in all_comments.find(lambda row: row.reply_to==comment_id):
                yield comment
                for reply in _walker(comment.id):
                    yield reply

        rows = []
        
        for comment in all_comments.find(lambda row: row.reply_to==None):
            main = TR(
                TD(
                    SPAN("#", comment.id, _class="label", _style="background-color: %s" % cols[comment.id]),
                    _class="info"
#                     _class="col-md-1"
                ),
                TD(ICON("user"), BR(), db.auth_user[comment.created_by].username),
                TD(MARKMIN(comment.reply), _style="width: 80%"),
                TD(
                    cls.add_new_comment(issue_id, comment.id),
#                     _class="col-md-2"
                ),
#                 _class="row"
            )
            subs = [TR(
                TD(
                    SPAN("#", reply.reply_to, _class="label", _style="background-color: %s" % cols[reply.reply_to]),
                    " ", ICON("chevron-right"), " ",
                    SPAN("#", reply.id, _class="label", _style="background-color: %s" % cols[reply.id]),
#                     _class="col-md-2"
                ),
                TD(ICON("user"), BR(), db.auth_user[reply.created_by].username),
                TD(MARKMIN(reply.reply), _style="width: 80%"),
#                 DIV(
#                     T("In reply to: "),
#                     reply.reply_to,
#                     _class="col-md-1"
#                 ),
#                 DIV(, _class="col-md-8 alert alert-warning"),
                DIV(
                    cls.add_new_comment(issue_id, reply.id),
#                     _class="col-md-2"
                ),
#                 _class = "row"
            ) for reply in _walker(comment.id)]
            rows += [main]
            rows += subs

        return TABLE(TBODY(*rows), _class="table table-striped")

    @staticmethod
    def oncreate(form):
        if request.vars.issuegrp_id:
            db.link_issue_issuegrp[0] = dict(issue_id=form.vars.id, issuegrp_id=request.vars.issuegrp_id)
        elif request.vars.issuegrp_ids:
            db.link_issue_issuegrp.bulk_insert([
                dict(issue_id=form.vars.id, issuegrp_id=i) \
            for i in request.vars.issuegrp_ids])
        elif request.vars.project_id:
            db.link_issue_project[0] = dict(issue_id=form.vars.id, project_id=request.vars.project_id)
        elif request.vars.project_ids:
            db.link_issue_project.bulk_insert([
                dict(issue_id=form.vars.id, project_id=i) \
            for i in request.vars.project_ids])
