import re, shutil

savefile = '/Users/abhijith/AeroVECTOR/Argus.txt'
backup = '/Users/abhijith/AeroVECTOR/Argus_backup3.txt'
shutil.copy(savefile, backup)
print(f"Backed up to {backup}")

with open(savefile) as f:
    content = f.read()

# Current (30%-shrunk) fin dims
old_c_root, old_c_tip, old_wingspan = 0.056, 0.021, 0.042

# Shrink chords/wingspan another 20% (positions x_root/x_tip_offset unchanged)
shrink = 0.80
new_c_root = round(old_c_root * shrink, 5)
new_c_tip = round(old_c_tip * shrink, 5)
new_wingspan = round(old_wingspan * shrink, 5)

old_block = f"0.485,{old_c_root}\n0.035,{old_c_tip}\n{old_wingspan}\n0.003"
new_block = f"0.485,{new_c_root}\n0.035,{new_c_tip}\n{new_wingspan}\n0.003"

print(f"New fin dims: c_root={new_c_root}, c_tip={new_c_tip}, wingspan={new_wingspan}")

if old_block not in content:
    print("WARNING: exact fin block not found — check Argus.txt formatting manually.")
else:
    content = content.replace(old_block, new_block)
    with open(savefile, 'w') as f:
        f.write(content)
    print("Argus.txt patched successfully.")
