path = "/Users/abhijith/AeroVECTOR/src/simulation/servo_lib.py"

with open(path, "r") as f:
    content = f.read()

# 1. Change the logging line to store commanded + actual instead of the scaled abs error
old1 = "        self._u_delta_history.append((t_current, self._u_delta))"
new1 = "        self._u_delta_history.append((t_current, self._u, self._out_s[0,0]))"
assert content.count(old1) == 1, "logging line not found or not unique"
content = content.replace(old1, new1)

# 2. Update export_u_delta_log to write 3 columns instead of 2
old2 = "    def export_u_delta_log(self, path):\n        with open(path, 'w') as f:\n            f.write('Time,u_delta\\n')\n            for t, ud in self._u_delta_history:\n                f.write(f'{t},{ud}\\n')\n"
new2 = "    def export_u_delta_log(self, path):\n        with open(path, 'w') as f:\n            f.write('Time,Commanded,Actual\\n')\n            for t, cmd, act in self._u_delta_history:\n                f.write(f'{t},{cmd},{act}\\n')\n"
assert content.count(old2) == 1, "export method not found or not unique"
content = content.replace(old2, new2)

with open(path, "w") as f:
    f.write(content)

print("Both edits applied successfully.")
