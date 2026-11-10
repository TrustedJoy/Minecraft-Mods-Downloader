def logUnable(reason, mod):
    with open('mods/.unable.txt', 'a+') as f:
        f.write(f"{mod}, {reason}\n")

def logAble(mod):
    with open('mods/.able.txt', 'a+') as f:
        f.write(f"mod\n")
