
# coding: utf-8

# In[1]:


import pymongo
from pymongo import MongoClient
import tqdm
from collections import defaultdict, Counter
import json

client = MongoClient('localhost', 27017)
db = client.istex
cambridge = db.cambridge
springer = db.springer
total = springer.find({'categories': {'$exists': True}, 'abstract': {'$exists': True}, 'title': {'$exists': True}}).count() + cambridge.find({'categories': {'$exists': True}, 'abstract': {'$exists': True}, 'title': {'$exists': True}}).count()
categories = defaultdict(set)

cnt = Counter()

with open('springer_cambridge.txt', 'a') as outfile:
    for col in [springer, cambridge]:
        for i in tqdm.tqdm(col.find({'categories': {'$exists': True}, 'abstract': {'$exists': True}, 'title': {'$exists': True}, 'language': 'eng'})):
            for ar, v in i['categories'].iteritems():
                if ar == 'scopus':
                    cat = set()
                    for el in v:
                        if '1 -' in el:
                            cat.add(el)
                    cat = list(cat)
                    json.dump({'abstract': i['abstract'], 'label': ','.join(cat), 'id': i['id'], 'title': i['title']}, outfile)
                    outfile.write('\n')


# In[27]:


import pandas as pd

d = pd.read_json("springer_cambridge.txt", orient='records', lines=True)
d = d[d.label != '']


# In[28]:


d.count()


# In[29]:


d.labels = d.label.apply(lambda x: x.split(','))
d.labels[0]


# In[42]:


import numpy as np
d['health_sciences'] = np.full((d.shape[0],), 0)
d['life_sciences'] = np.full((d.shape[0],), 0)
d['physical_sciences'] = np.full((d.shape[0],), 0)
d['social_sciences'] = np.full((d.shape[0],), 0)

health_mask = d.label.str.contains('1 - Health Sciences')
physical_mask = d.label.str.contains('1 - Physical Sciences')
life_mask = d.label.str.contains('1 - Life Sciences')
social_mask = d.label.str.contains('1 - Social Sciences')

d['health_sciences'][health_mask] = 1
d['life_sciences'][life_mask] = 1
d['social_sciences'][social_mask] = 1
d['physical_sciences'][physical_mask] = 1
d


# In[43]:


d = d.drop("label", axis=1)


# In[44]:


d.to_csv('scopus.csv', encoding='utf-8', index=False)


# In[64]:


from sklearn.model_selection import train_test_split


train, test = train_test_split(d, test_size=0.2)


# In[65]:


train.to_csv('scopus_train.csv', encoding='utf-8', index=False)
test.to_csv('scopus_test.csv', encoding='utf-8', index=False)

print train.shape
print test.shape


# In[66]:


test.to_json('scopus_test.json', orient='records', lines=True)


# In[69]:


train[train.abstract.str.contains('fiscal policy')]

