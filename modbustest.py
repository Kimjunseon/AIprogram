#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# In[7]:


from pymodbus.client import ModbusTcpClient
from pymodbus.transaction import *


# In[8]:


client = ModbusTcpClient('192.168.0.63', 502)
for n in range(0, 3):
    result = client.read_coils(n, 1)
    print(result.bits)
client.write_coil(0, True)

