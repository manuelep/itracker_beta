# -*- coding: utf-8 -*-

# from plugin_shared_tools import Populator

####################
# Model
####################

# weight_table_template = Table(db, 'weight_table_template',
#     Field('label', required=True),
#     Field('sort_order', 'integer', required=True),
#     Field('is_default', 'boolean', required=True)
# )

# Ticket Status (Open, Closed, Suspended)
db.define_table('project_state',
    weight_table_template,
    format = '%(label)s'
)

db.define_table('project',
    Field('title', requires=IS_NOT_EMPTY()),
    Field('description', 'text',
        comment=XML(T("MARKMIN text syntax is accepted.").replace('MARKMIN', str(STRONG(A('MARKMIN', _href="http://web2py.com/books/default/chapter/29/05#markmin_markmin_syntax"))))),
        represent=lambda v, r: MARKMIN(v)
    ),
    Field('project_version'),
    Field('status', 'reference project_state', label=T('State')),
    Field('project_id', 'reference project', label=T("Parent project")),
    format = '%(title)s'
)

IssueReferences(db.project).assign()

####################
# Default values
####################

Populator.bulk(
    db.project_state,
    [
        dict(label='Open', sort_order=1, is_default=True),
        dict(label='Suspended', sort_order=2, is_default=False),
        dict(label='Closed', sort_order=3, is_default=False),
    ]
)
