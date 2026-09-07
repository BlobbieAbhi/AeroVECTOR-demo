path = "/Users/abhijith/AeroVECTOR/Argus.txt"

with open(path, "r") as f:
    content = f.read()

old = "Fins_s\n0.485,0.08\n0.035,0.03\n0.06\n0.003\n"
new = "Fins_s\n0.485,0.056\n0.035,0.021\n0.042\n0.003\n"

assert content.count(old) == 1, "fin block not found or not unique — check exact formatting"
content = content.replace(old, new)

with open(path, "w") as f:
    f.write(content)

print("Fin dimensions updated (30% smaller chord/span).")
