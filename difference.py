with open("result(79995480000-79995489999).txt") as oldfile:
    old = oldfile.read()
old_list = old.split("\n")


with open("79995480000-79995485000.txt") as newfile:
    new = newfile.read()
new_list = new.split("\n")


difference = list(set(old_list) - set(new_list))
print(difference)
