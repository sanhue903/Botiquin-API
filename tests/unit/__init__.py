from app.models import Session
from app.extensions import db

class TestBase:
    def __init__(self):
        self.query = db.select(Session)    

    def run(self, test_sessions, filter = ModuleNotFoundError):
        items = db.session.scalars(self.query).all()
        

        if filter is not None:
            sessions = [session for session in test_sessions if filter(session)]
        else:
            sessions = test_sessions
    
        assert len(items) == len(sessions)
