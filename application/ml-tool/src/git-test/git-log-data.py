#!/usr/bin/env python
# coding: utf-8

# In[1]:


import subprocess
from dateutil.parser import parse
from tqdm.auto import tqdm
import os, psutil


# In[2]:


# Clone example repo and add it to git ignore
subprocess.run(['git', 'clone', 'git@github.com:cambolbro/Ludii.git', 'gitrepo'])

data_directory = 'data'
# Create the folder for the data
if not os.path.exists(data_directory):
    os.mkdir(data_directory)

# Add the repo folder to a git ignore folder
with open('.gitignore', 'w') as f:
    f.write("gitrepo")


# In[3]:


get_ipython().run_line_magic('cd', 'gitrepo')


# In[4]:


result = subprocess.run(['git', 'log', '--pretty=%H,%cn,%cd'], stdout=subprocess.PIPE)


# In[5]:


commit_data = str(result.stdout, 'utf8').split('\n')
commit_data = list(filter(lambda line: len(line) != 0, commit_data))
commit_data = list(map(lambda line: line.split(','), commit_data))

for feature_list in tqdm(commit_data):
    feature_list[2] = parse(feature_list[2]).strftime("%Y%m%d-%H%M%S")


# In[6]:


print(f'Amount of Commits: {len(commit_data)}')
process = psutil.Process(os.getpid())
print(f'Memory Usage: {process.memory_info().rss / 1024 ** 2}mb')
print('Example Data:')
print(f'\tCommit   id: {commit_data[0][0]}')
print(f'\tCommit name: {commit_data[0][1]}')
print(f'\tCommit date: {commit_data[0][2]}')


# In[7]:


date_1 = parse(commit_data[-1][2])
date_2 = parse(commit_data[-65][2])

print((date_2 - date_1).days)
print(str(date_1.strftime("%Y%m%d-%H%M%S")))


# In[8]:


start_date = parse(commit_data[-1][2])

curr_file_list = []

for data in tqdm(commit_data[::-1]):

    result = subprocess.run(['git', 'diff-tree', '--no-commit-id', '--name-status', '-r', data[0]], stdout=subprocess.PIPE)
    file_list = list(map(lambda line: line.split('\t'), filter(len, str(result.stdout, 'utf8').split('\n'))))
    curr_file_list += list(map(lambda line: line + list(map(str, data[1:])), file_list))
    curr_date = parse(data[2])

    if (curr_date - start_date).days > 1 and len(curr_file_list) != 0:

        file_data = '\n'.join(map(lambda element: ','.join(element), curr_file_list))

        with open(f'../data/{curr_date.strftime("%Y%m%d-%H%M%S")}', 'w') as f:
            f.write(file_data)

        curr_file_list.clear()
        start_date = curr_date


# In[26]:




