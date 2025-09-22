import os

t = os.popen("echo 1").read()
if (int(t) == 1):
    print("worked")
else:
    print("didn't work")
