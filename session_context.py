from contextlib import contextmanager
from sqlite3 import IntegrityError

from flask import render_template
from alabar.models import db

@contextmanager
def transactional_session():
    session = db.session
    try:
        yield session
        session.commit()
    except (IntegrityError,AttributeError):
        session.rollback()
        #raise
    finally:
        session.close()