# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 13:44:11 2016

@author: divakv
"""

import os
from sqlalchemy import Column, ForeignKey, Integer, String, TEXT, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import cPickle
import datetime
from DecisionTree import *



engine = create_engine('sqlite:///tutorial.db', echo = True)
Base = declarative_base()
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)


class Decision(Base):
    __tablename__ = 'decisions'
    id = Column( Integer, primary_key = True)
    name = Column(String(100), nullable = False)
    tree = Column(TEXT, nullable = False)
    in_z = Column(DATETIME, nullable = False)
    out_z = Column(DATETIME, nullable = False)

def addDecision(name, tree):
    session = DBSession()
    old_dec = session.query(Decision).filter_by(name = name, out_z = datetime.datetime.max).first()
    now = datetime.datetime.utcnow()
    if old_dec != None:
        old_dec.out_z = now
    dec = Decision( name = name, tree = cPickle.dumps(tree), in_z = now, out_z = datetime.datetime.max)
    session.add(dec)
    session.commit()

def selectDecision(name):
    session = DBSession()
    s = session.query(Decision).filter_by(name = name, out_z = datetime.datetime.max).first()
    return s

if __name__ == "__main__":
    #Base.metadata.create_all(engine)
    df = pd.read_excel('/home/vik1124/DecisionService/xor.xlsx',"Sheet1")
    tree = DecisionTree(df)
    addDecision('xor', tree)
    s = selectDecision('xor')
    print s.id, s.name, s.in_z, s.out_z
    



