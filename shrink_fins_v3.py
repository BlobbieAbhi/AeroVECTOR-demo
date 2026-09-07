import shutil

savefile = '/Users/abhijith/AeroVECTOR/Argus.txt'
backup = '/Users/abhijith/AeroVECTOR/Argus_backup4.txt'
shutil.copy(savefile, backup)
print(f"Backed up to {backup}")

with open(savefile) as f:
    content = f.read()

# Current (20%-further-shrunk) fin dims -> target dims from quadratic fit
old_c_root, old_c_tip, old_wingspan = 0.0448, 0.0168, 0.0336
new_c_root, new_c_tip, new_wingspan = 0.05085, 0.01907, 0.03814

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
