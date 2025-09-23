import sys

a1 = "default"
a2 = 5
a3 = 3.14

for inp in sys.argv[1:]:
    if (inp[0] == '-'):
        match inp[1:3]:
            case "2=":
                a2 = int(inp[3:])
            case "3=":
                a3 = float(inp[3:])
    else:
        a1 = inp
