list_of_followers = []
path = 'My_followers.txt'
with open(path, 'r') as f:
    my_list = f.readlines()
for i in my_list:
    list_of_followers.append(i.replace('\n', ''))

list_of_followers_1 = []
path_1 = 'My_followers_1.txt'
with open(path_1, 'r') as f:
    my_list = f.readlines()
for i in my_list:
    list_of_followers_1.append(i.replace('\n', ''))

for i in list_of_followers:
    if i not in list_of_followers_1:
        print(i)
