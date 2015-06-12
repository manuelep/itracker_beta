# -*- coding: utf-8 -*-

from pydal.objects import Table

if not 'plugin_shared_tools' in globals():
    import plugin_shared_tools
Populator, IssueReferences, UniqueDefault = plugin_shared_tools.Populator, plugin_shared_tools.IssueReferences, plugin_shared_tools.UniqueDefault

from datetime import datetime, date
from gluon.tools import prettydate

####################
# Model
####################

# Issue
# =====

# Ticket Types (Problem/Bug, Enhancement, Issue)
db.define_table('issue_type',
    Field('label', required=True),
    Field('description', 'text'),
    Field('is_default', 'boolean', required=True),
    format = '%(label)s'
)

weight_table_template = Table(db, 'weight_table_template',
    Field('label', required=True),
    Field('sort_order', 'integer', required=True),
    Field('is_default', 'boolean', required=True)
)

# Ticket Priorities (Highest, High, Normal, Low, Lowest)
db.define_table('issue_priority',
    weight_table_template,
    Field('color', represent=lambda v,r: SPAN(v, _class="label", _style="background-color: %s" % v)),
    format = lambda r: XML(SPAN(r.label, _class="label", _style="background-color: %(color)s" % r))
)

# Ticket Severities (Blocker, Critical, Major, Normal, Minor, Trivial)
db.define_table('issue_severity',
    weight_table_template,
    Field('color', represent=lambda v,r: SPAN(v, _class="label", _style="background-color: %s" % v)),
    format = lambda r: XML(SPAN(r.label, _class="label", _style="background-color: %(color)s" % r))
)

# Ticket Status (New, Assigned, Fixed, Rejected, Invalid, Re-opened, Could Not Replicate, Duplicated)
db.define_table('issue_state',
    weight_table_template,
    format = '%(label)s'
)

class IssueWeight(object):
    @staticmethod
    def _get_weight(pid, sid):
        pw = db.issue_priority[pid].sort_order
        sw = db.issue_severity[sid].sort_order
        return pw*sw
    @classmethod
    def run(cls, r):
        return cls._get_weight(r.priority, r.severity)
        

db.define_table('issue',
    Field('title', requires=IS_NOT_EMPTY()),
    Field('description', 'text',
        comment=XML(T("MARKMIN text syntax is accepted.").replace('MARKMIN', str(STRONG(A('MARKMIN', _href="http://web2py.com/books/default/chapter/29/05#markmin_markmin_syntax"))))),
        represent=lambda v, r: MARKMIN(v)
    ),
    Field('typology', 'reference issue_type', label=T('Type')),
    Field('priority', 'reference issue_priority'),
    Field('severity', 'reference issue_severity'),
    Field('weigth', 'integer', compute=IssueWeight.run),
    Field('status', 'reference issue_state', label=T('State')),
    Field('tags', 'list:string'),
#     Field('assigned_to', 'list:reference auth_group', comment="DEPRECATED"), # DEPRECATED
    Field('assignedto', 'reference auth_group', label=T("Assigned to"),
        default = auth.user_id
    ),
    Field('dead_line', 'date', represent=lambda v,r: prettydate(v)),
    Field('time_spent', 'integer', label=T("Time spent"), comment=T("in hours")),
    Field('closed', 'boolean', default=False),
    Field('closed_on', 'datetime', writable=False),
    Field('slugs', 'list:string', label=T("Wiki pages"),
        readable = False,
        represent=lambda v,r: SPAN(*map(lambda e: A(e, _href=URL('wiki', 'index', args=('issue_%s' % r.id +'_'+e,))), v))),
    auth.signature,
    format = '%(title)s',
)

db.issue.modified_on.represent=lambda v,r: prettydate(v)
db.issue.modified_on.label = T("Last modified")

IssueReferences(db.issue).assign()

class AuthGroupSet(object):
    """
    I want to list all groups but when groups got only one member I want to show
    just this memeber
    """

    @staticmethod
    def _get_label(id):
        n = db(db.auth_membership.group_id==id).count()
        if n == 1:
            row = db(
                (db.auth_membership.user_id==db.auth_user.id) & \
                (db.auth_membership.group_id==id)
            ).select(db.auth_user.ALL).first()
            format = db.auth_user._format
            if isinstance(format, basestring):
                return format % row
            else:
                return format(row)
        else:
            return None

    @classmethod
    def _loop(cls):
        for row in db(db.auth_group>0).select(db.auth_group.ALL):
            value = row.id
            label = cls._get_label(row.id) or row.role
            yield value, label

    @classmethod
    def get(cls):
        return dict([(v, l) for v,l in cls._loop()])

    @classmethod
    def represent(cls, value, row):
        return ', '.join((cls._get_label(id) for id in value))

    @classmethod
    def represent1(cls, value, row):
        return cls._get_label(value)


# db.issue.assigned_to.requires = IS_IN_SET(
#     theset = AuthGroupSet.get(),
#     multiple = True
# )
db.issue.assignedto.requires = IS_IN_SET(
    theset = AuthGroupSet.get(),
    multiple = False
)

# db.issue.assigned_to.represent = AuthGroupSet.represent
db.issue.assignedto.represent = AuthGroupSet.represent1

# Thread
# ======

db.define_table('thread',
    Field('issue_id', 'reference issue'),
    Field('reply_to', 'reference thread'),
    Field('reply', 'text', length=255,
        comment=XML(T("MARKMIN text syntax is accepted. Max length is 255.")\
            .replace('MARKMIN', str(STRONG(A('MARKMIN', _href="http://web2py.com/books/default/chapter/29/05#markmin_markmin_syntax"))))\
            .replace('255', str(STRONG('255')))
        ),
        represent=lambda v, r: MARKMIN(v)
    ),
    auth.signature,
    format = '%(reply)s'
)

db.thread.reply_to.requires = IS_EMPTY_OR(IS_IN_DB(db, 'thread.id', '%(reply)s'))

####################
# Callbacks
####################



for tablename in db.tables:
    if tablename.startswith('issue_') and 'is_default' in db[tablename].fields:
        db[tablename]._before_update.append(UniqueDefault(db[tablename]))

class ClosedOn(object):
    """ Register in the db the last time the issue had been closed """

    @staticmethod
    def before_update(s, f):
        if f.get('closed')==True:
            session.closed_issues = [i[0] for i in db.executesql(s(db.issue.closed!=True)._select(db.issue.id))]

    @classmethod
    def after_update(cls, s, f):
        if not session.closed_issues is None:
            s(db.issue.id.belongs(session.closed_issues)).update_naive(closed_on=datetime.now())
            del session.closed_issues

db.issue._before_update.append(ClosedOn.before_update)
db.issue._after_update.append(ClosedOn.after_update)

####################
# Default values
####################

Populator.bulk(
    db.issue_type,
    [
        dict(label='Bug', description='An error, flaw, failure, or fault in a computer program or system that causes it to produce an incorrect or unexpected result, or to behave in unintended ways', is_default=False),
        dict(label='Enhancement', description='A proposed or newly added software feature', is_default=False),
        dict(label='Issue', description='A unit of work to accomplish an improvement in a data system', is_default=True),
    ]
)

Populator.bulk(
    db.issue_priority,
    [
        dict(label='Highest', sort_order=1, is_default=False, color='#BF0100'),
        dict(label='High', sort_order=2, is_default=False, color='#C86500'),
        dict(label='Normal', sort_order=3, is_default=True, color='#D0D200'),
        dict(label='Low', sort_order=4, is_default=False, color='#6DDB00'),
        dict(label='Lowest', sort_order=5, is_default=False, color='#00E500'),
    ]
)

# Blocker, Critical, Major, Normal, Minor, Trivial
Populator.bulk(
    db.issue_severity,
    [
        dict(label='Blocker', sort_order=1, is_default=False, color='#BF0100'),
        dict(label='Critical', sort_order=2, is_default=False, color='#C6009D'),
        dict(label='Major', sort_order=3, is_default=False, color='#5300CE'),
        dict(label='Normal', sort_order=4, is_default=True, color='#0054D5'),
        dict(label='Minor', sort_order=5, is_default=False, color='#00DDB1'),
        dict(label='Trivial', sort_order=6, is_default=False, color='#00E500'),
    ]
)

# New, Assigned, Fixed, Rejected, Invalid, Re-opened, Could Not Replicate, Duplicated
Populator.bulk(
    db.issue_state,
    [
        dict(label='New', sort_order=0, is_default=True),
        dict(label='Work in progress', sort_order=1, is_default=False),
        dict(label='Fixed', sort_order=2, is_default=False),
        dict(label='Rejected', sort_order=3, is_default=False),
        dict(label='Invalid', sort_order=4, is_default=False),
        dict(label='Re-opened', sort_order=5, is_default=False),
        dict(label='Could Not Replicate', sort_order=6, is_default=False),
        dict(label='Duplicated', sort_order=7, is_default=False),
    ]
)
