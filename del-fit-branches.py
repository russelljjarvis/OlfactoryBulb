import os
branches = os.popen("git branch -r --list '*fit*'").read()
print(branches)

branches = branches.split('\n')

commands = ["git push --delete "+b.strip().replace("/"," ") for b in branches if len(b) > 0]

for c in commands:
    print(c)
    os.system(c)




