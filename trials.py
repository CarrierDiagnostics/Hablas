list = ['--je', 'vais', 'voir', 'ma', 'mère-grand']
sentence = "--je vais voir ma mère-grand"
#stripped_sentence = sentence.strip("-")
sentence2 = sentence.replace("-"," ").strip()
stripped_list = []

for i in range(len(list)):
    #stripped_list[i]=list[i].strip("-") #it doesnt work because pos[0] doesnt exist so it crashes
    stripped_list.append(list[i].strip("-"))
#for item in string_list:
       #stripped_list.append(item.strip())

print(stripped_list)
print(sentence2)