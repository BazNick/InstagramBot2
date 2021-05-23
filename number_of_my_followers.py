new_list = []
# specify full path to your subscribes file
# for example C:/Users/Unfollow/my_subscribes.txt
with open('...', 'r') as f:
    my_list = f.readlines()

for i in my_list:
    new_list.append(i.replace('\n', ''))
# print(new_list)
print(len(new_list))

