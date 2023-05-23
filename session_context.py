from contextlib import contextmanager
from sqlite3 import IntegrityError
#from sqlalchemy.exc import IntegrityError
#import sqlite3

from flask import render_template
import sqlalchemy
from alabar.models import db
#from sqlalchemy.exc import DBAPIError

@contextmanager
def transactional_session():
    session = db.session
    try:
        yield session
        session.commit()
    except (IntegrityError,AttributeError):
    #except (IntegrityError,AttributeError,sqlalchemy.exc.IntegrityError):
    #except (IntegrityError as error_IntegrityError,AttributeError as error_AttributeError,sqlalchemy.exc.IntegrityError as error_duplicados):
    #except (IntegrityError,AttributeError,sqlite3.IntegrityError,sqlalchemy.exc.IntegrityError,DBAPIError as e):
    #except DBAPIError as DBAPIError:
        session.rollback()
        #print("Error de duplicados:", error_duplicados)
        #print("Error de la DBAPI:", DBAPIError.orig)
        #raise
    #    result = False
    #    return result
    #else:
    #    result = True
    #    return result
    finally:
        session.close()