import falcon

from pomoccore import db
from pomoccore.middleware import dbsessionmanager

app = falcon.API(middleware=[dbsessionmanager.DBSessionManager(db.Session)])