# -*- coding: utf-8 -*-

from gluon.utils import web2py_uuid

if myconf.take('app.development', cast=bool):
    from gluon.custom_import import track_changes; track_changes(True)

random_password = web2py_uuid()[:8]

guest_user = auth.get_or_create_user(
    keys = dict(
#         email = "manuele@inventati.org",
        first_name = "Guest",
        username = "guest",
        password = db.auth_user.password.validate(random_password)[0]
    ),
    update_fields = [],
    login = myconf.take('app.development', cast=bool)
)

if myconf.take('app.development', cast=bool) and auth.user_id is None:
    auth.login_user(guest_user)
