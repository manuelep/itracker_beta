# -*- coding: utf-8 -*-

if not 'plugin_shared_tools' in globals():
    import plugin_shared_tools
Populator, IssueReferences, UniqueDefault = plugin_shared_tools.Populator, plugin_shared_tools.IssueReferences, plugin_shared_tools.UniqueDefault

# Ticket Types (Problem/Bug, Enhancement, Issue)
db.define_table('issuegrp_type',
    Field('label', required=True),
    Field('description', 'text'),
    Field('is_default', 'boolean', required=True),
    format = '%(label)s'
)

db.define_table('issuegrp',
    Field('title', requires=IS_NOT_EMPTY()),
    Field('description', 'text',
        comment=XML(T("MARKMIN text syntax is accepted.").replace('MARKMIN', str(STRONG(A('MARKMIN', _href="http://web2py.com/books/default/chapter/29/05#markmin_markmin_syntax"))))),
        represent=lambda v, r: MARKMIN(v)
    ),
    Field('typology', 'reference issuegrp_type', label=T('Type')),
    Field('slugs', 'list:string', label=T("Wiki pages"), readable=False,
        represent = lambda v,r: SPAN(*map(lambda e: A(e, _href=URL('wiki', 'index', args=('issue_%s' % r.id +'_'+e,))), v))),
    auth.signature,
    format = '%(title)s'
)

####################
# Callbacks
####################

for tablename in db.tables:
    if tablename.startswith('issuegrp_') and 'is_default' in db[tablename].fields:
        db[tablename]._before_update.append(UniqueDefault(db[tablename]))

####################
# Default values
####################

Populator.bulk(
    db.issuegrp_type,
    [
        dict(label='Task', description='A generic description of something to do', is_default=True),
        dict(label='Milestone', description='A group of issue with a precise aim', is_default=False),
    ]
)
