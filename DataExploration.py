
# coding: utf-8

# In[66]:


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,inspect, func

import pandas as pd

import numpy as np


# In[67]:


# Create engine using the `demographics.sqlite` database file
engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()


# In[68]:


# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)


# In[69]:


# Print all of the classes mapped to the Base
Base.classes.keys()


# In[70]:



Otu = Base.classes.otu
Samples = Base.classes.samples
Samples_Metadata = Base.classes.samples_metadata


# In[71]:


# Create our session (link) from Python to the DB
session = Session(engine)


# In[72]:


results = engine.execute('SELECT* FROM samples LIMIT 1')

for row in results:
    colnames = (row.keys())

ColDict = {k for k in colnames}
print(ColDict)

