name = "a-10_b-2.7"

def get_list(s):
    s += '_'
    mode = 0
    out_n = []
    out_v = []
    cur = ''
    for c in s:
        match mode:
            case 0:
                if (c == '-'):
                    out_n.append(cur)
                    cur = ''
                    mode = 1
                    continue
                else:
                    cur += c
            case 1:
                if (c == '_'):
                    out_v.append(cur)
                    cur = ''
                    mode = 0
                    continue
                else:
                    cur += c
    l = len(out_n)
    return [[out_n[i], float(out_v[i])] for i in range(l)]

print(get_list(name))
