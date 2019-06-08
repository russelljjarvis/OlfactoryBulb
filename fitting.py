
# coding: utf-8

# In[1]:


from prev_ob_models.Birgiolas2020.fitting import *


# In[15]:


import sys
mc_id = sys.argv[1]


# In[2]:


fitter = FitterMC("prev_ob_models.Birgiolas2020.isolated_cells.MC"+mc_id)


# In[ ]:


fitter.fit(35, 30)


# In[14]:


fitter.pop


# In[ ]:


fitter.pretty_pop()

