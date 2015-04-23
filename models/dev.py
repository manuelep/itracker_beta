# -*- coding: utf-8 -*-

if myconf.take('app.development', cast=bool):
    from gluon.custom_import import track_changes; track_changes(True)

guest_user = auth.get_or_create_user(
    keys = dict(
        email = "manuele@inventati.org",
        first_name = "manuele",
        password = db.auth_user.password.validate('password')[0]
    ),
    update_fields = [],
    login = myconf.take('app.development', cast=bool)
)

if myconf.take('app.development', cast=bool) and auth.user_id is None:
    auth.login_user(guest_user)
