
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


# In[2]:


import pandas as pd

d = pd.read_json("springer_cambridge.txt", orient='records', lines=True)
d = d[d.label != '']


# In[3]:


d.count()


# In[4]:


d.labels = d.label.apply(lambda x: x.split(','))


# In[5]:


from collections import Counter
r = []
di = set()

for l in d.labels:
    lab_di = {'Health Sciences':0, 'Life Sciences':0, 'Physical Sciences':0, 'Social Sciences':0}
    for i in l:
        lab_di[i[4:]] += 1
    r.append(lab_di)
d['labels_dict'] = pd.Series(r)


# In[6]:


d_nonan = d.dropna(axis=0, how='any')


# In[7]:


hs = []
ls = []
ps = []
ss = []

nd = {'Health Sciences': hs, 'Life Sciences': ls, 'Physical Sciences': ps, 'Social Sciences': ss}

for l in d_nonan.labels_dict.tolist():
    nd['Health Sciences'].append(l['Health Sciences'])
    nd['Life Sciences'].append(l['Life Sciences'])
    nd['Physical Sciences'].append(l['Physical Sciences'])
    nd['Social Sciences'].append(l['Social Sciences'])
nd


# In[8]:


d_nonan['health_sciences'] = nd['Health Sciences']
d_nonan['life_sciences'] = nd['Life Sciences']
d_nonan['physical_sciences'] = nd['Physical Sciences']
d_nonan['social_sciences'] = nd['Social Sciences']

d_nonan.head()


# In[9]:


d_nonan = d_nonan.drop("labels_dict", axis=1)


# In[10]:


d_nonan.to_csv('scopus.csv', encoding='utf-8', index=False)


# In[11]:


from sklearn.model_selection import train_test_split


train, test = train_test_split(d_nonan, test_size=0.2)


# In[12]:


train.to_csv('scopus_train.csv', encoding='utf-8', index=False)
test.to_csv('scopus_test.csv', encoding='utf-8', index=False)

print train.shape
print test.shape


# In[13]:


test.to_json('scopus_test.json', orient='records', lines=True)

