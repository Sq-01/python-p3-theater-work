from importlib.metadata import MetadataPathFinder
from pkg_resources import _MetadataType
from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, create_engine, Sequence
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetadataPathFinder(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, Sequence('role_id_seq'), primary_key=True)
    character_name = Column(String(), nullable=False)
    
    auditions = relationship('Audition', backref='role')

    def actors(self):
        return [audition.actor for audition in self.auditions]

    def locations(self):
        return [audition.location for audition in self.auditions]

    def lead(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        if hired_auditions:
            return hired_auditions[0]
        else:
            return 'no actor has been hired for this role'

    def understudy(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        if len(hired_auditions) > 1:
            return hired_auditions[1]
        else:
            return 'no actor has been hired for understudy for this role'

class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(Integer, Sequence('audition_id_seq'), primary_key=True)
    actor = Column(String(), nullable=False)
    location = Column(String(), nullable=False)
    phone = Column(Integer())
    hired = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)

    def call_back(self):
        self.hired = True

# Add this to create the database
engine = create_engine('sqlite:///auditions.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Sample usage:
if __name__ == '__main__':
    role = Role(character_name='Main Character')
    audition1 = Audition(actor='Actor1', location='Location1', role=role)
    audition2 = Audition(actor='Actor2', location='Location2', role=role)
    
    session.add(role)
    session.add(audition1)
    session.add(audition2)
    session.commit()
    role.lead()  # Returns 'no actor has been hired for this role'
    audition1.call_back()
    role.lead()  # Returns audition1
    role.understudy()  # Returns 'no actor has been hired for understudy for this role'
