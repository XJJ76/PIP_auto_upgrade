import os
from datetime import date
date_s = str(date.today())

# full backup
try:
    os.mkdir('D:\\Whl_list_backup') # The backup path can be changed by yourself.

except:
      None
os.chdir('D:\\Whl_list_backup')
os.popen(f'pip freeze > {date_s}_fullbackup.txt')

# Get the outdated packages
outdate_list = os.popen( f'python -m pip list -o')
info = outdate_list.readlines()
update_dic = {'Package': [], 'Old_version': [], 'Latest_version': []}

for i in info[2:]:
    i = i.rstrip('\n')
    l = i.split(' ')
    l = [j for j in l if j!='']
    update_dic['Package'].append(l[0])
    update_dic['Old_version'].append(l[1])
    update_dic['Latest_version'].append(l[2])
# backup old version
backup = []
n = len(update_dic['Package'])
for i in range(n):
    item = update_dic['Package'][i] + '\t' + update_dic['Old_version'][i] + '\n'
    backup.append(item)

with open(f'{date_s}_old_version.txt', 'w') as file:
    file.writelines(backup)

# Update package

##pip upgrade
if 'pip' in update_dic['Package']:
    os.system('python -m pip install pip --upgrade')
    n = update_dic['Package'].index('pip')
    update_dic['Package'].remove('pip')
    upddate_dic['Old_version'].remove(upddate_dic['Old_version'][n])
    update_dic['Latest_version'].remove(update_dic['Latest_version'][n])

##Update other packages
for i in update_dic['Package']:
    os.system(f'pip install {i} --upgrade --no-cache-dir ')

#Solve packages version conflict
conflict = os.popen('pip check').readlines()
if 'No broken requirements' in conflict[0]:
    exit
for i in conflict:
    j = i.split('you have ')[-1]
    j = j.split(' ')[0]
    if f'{j}==' in i:
        s = i.split('requirement ')[-1]
        s = s.split(' ')[0]
        s = s.rstrip(',')
        s = s.rstrip(';')
        os.system(f"pip install {s}")
    else:
        m = update_dic['Package'].index(j)
        os.system(f"pip install  {j}=={update_dic['Old_version'][m]}")
