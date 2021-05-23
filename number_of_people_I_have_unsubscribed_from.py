new_list = []
# specify full path to your unsubscribtions file
# for example C:/Users/Unfollow/List of people I have unsubscribed from.txt
with open('...', 'r') as f:
    my_list = f.readlines()

for i in my_list:
    new_list.append(i.replace('\n', ''))
# print(new_list)
# print(len(new_list))

unique_list = set(new_list)
print(len(unique_list))
