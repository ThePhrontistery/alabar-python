from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker 
from alabar.models import Topic_item

# Set up the database connection (NO ES IGUAL A FLASK. NO ESTAMOS EN UN PROCESO DE FLASK AHORA!!!!)
engine = create_engine('sqlite:///./instance/alabar.db')
Session = sessionmaker(bind=engine)
session = Session()

#--------------------------------------------------------------------------
print(f"SQLAlchemy example using SQL style select and not the deprecated Query interface")

# Retrieve the user with the name "john" and ID 1
#john = session.execute(select(User).where((User.name == 'john') & (User.id == 1))).scalar_one()
id_topic = '4'
id_order_max =  session.query(func.max(Topic_item.id_order)
           .filter(Topic_item.id_topic == id_topic)).scalar()
print('id_order_max: ', id_order_max)

db.session.execute(db.update(Topic).where(Topic.end_date < current_date)
                              .where(Topic.status == True)
                              .values(status=False,end_date=datetime.datetime.now()))
