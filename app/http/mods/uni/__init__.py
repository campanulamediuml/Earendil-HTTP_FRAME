from app.http.mods.uni.handlers.uni_basehandler import get_example, post_example, db_example_find, db_example_select, \
    db_example_update, db_example_insert, sync

route_list = [
    ('/uni/postexample',post_example),
    ('/uni/getexample',get_example),
    ('/uni/dbexamplefind',db_example_find),
    ('/uni/dbexampleselect',db_example_select),
    ('/uni/dbexampleupdate',db_example_update),
    ('/uni/dbexampleinsert',db_example_insert),
    ('/uni/sync',sync),
]