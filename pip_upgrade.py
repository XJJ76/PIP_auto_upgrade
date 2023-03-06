import os
installed_packages_info = os.popen(f"pip list").readlines()
old_packages = {}
for i in installed_packages_info[2:]:
    x = i[:-1].split(' ')
    l = [j for j in x if j != '']
    old_packages[l[0]] = l[1]
outdate_info = os.popen( f'python -m pip list -o')
outdate_list = outdate_info.readlines()
update_packages = {}

for i in outdate_list[2:]:
    x = i[:-1].split(' ')
    l = [j for j in x if j != '']
    update_packages[l[0]] = l[2]

for i in update_packages.keys():
    if i == 'pip':
        os.system(f"python -m pip install pip --upgrade --no-cache-dir")
    else:
        os.system(f'pip install {i}=={update_packages[i]} --no-cache-dir ')

#Solve conflict
print('\nNow solve conflict!!\n')
conflict1 = os.popen('pip check').readlines()
if 'No broken requirements' in conflict1[0]:
    print('Congratulation! No conflict found!')
    exit
conflict_p = []
comp = ['>','>=','==','<','<=','~=']

def get_first_comp(s):
    l = []
    for i in comp:
        if i in s:
            l.append(s.index(i))
    return min(l)

for i in conflict1:
        if 'which is not installed' not in i:
            j = i.split('has requirement ')[-1]
            r = get_first_comp(j)
            if j[:r] not in conflict_p:
                conflict_p.append(j[:r])
        else:
            i = i.split(',')[0]
            j = i.split('requires ')[-1]
            conflict_p.append(j)
for i in conflict_p:
    p_list = [i, i.replace('-',"_"),i.capitalize()]
    for j in p_list:
        if j in old_packages.keys():
            os.system(f'pip install {j}=={old_packages[j]} --no-cache-dir ')
#Solve conflict second round
print('\nRecheck conflict!!\n')

conflict2 = os.popen('pip check').readlines()

if 'No broken requirements' in conflict2[0]:
    print('Congratulation! No conflict found!')
    exit
conflict_rep = []
for i in update_packages.keys():
    for j in conflict2:
        if i in j:
            conflict_rep.append(i)
for i in conflict_rep:
    os.system(f'pip install {i}=={old_packages[i]} --no-cache-dir ')
