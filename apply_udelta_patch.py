import re

path = "/Users/abhijith/AeroVECTOR/src/simulation/servo_lib.py"

with open(path, "r") as f:
    content = f.read()

# 1. Add history list in __init__, right after self._u = 0.
old1 = "        self._resolution = 1\n        self._u = 0.\n        # Matrices left in uppercase"
new1 = "        self._resolution = 1\n        self._u = 0.\n        self._u_delta_history = []\n        # Matrices left in uppercase"
assert content.count(old1) == 1, "init anchor not found or not unique"
content = content.replace(old1, new1)

# 2. Reset history each run inside __reset_variables
old2 = "    def __reset_variables(self):\n        # sets the variables and matrices to zero\n        self._u = 0."
new2 = "    def __reset_variables(self):\n        # sets the variables and matrices to zero\n        self._u = 0.\n        self._u_delta_history = []"
assert content.count(old2) == 1, "reset anchor not found or not unique"
content = content.replace(old2, new2)

# 3. Log _u_delta + t_current after _update() call in simulate(), and add export method
old3 = "        self._sample_time = t_current - self._t_prev\n        self._t_prev = t_current\n        self._update()\n        u_2_round = self._u"
new3 = "        self._sample_time = t_current - self._t_prev\n        self._t_prev = t_current\n        self._update()\n        self._u_delta_history.append((t_current, self._u_delta))\n        u_2_round = self._u"
assert content.count(old3) == 1, "simulate anchor not found or not unique"
content = content.replace(old3, new3)

old4 = "        self._x_s = self._x_dot_s\n        return self._out_s[0,0]\n"
new4 = "        self._x_s = self._x_dot_s\n        return self._out_s[0,0]\n\n    def export_u_delta_log(self, path):\n        with open(path, 'w') as f:\n            f.write('Time,u_delta\\n')\n            for t, ud in self._u_delta_history:\n                f.write(f'{t},{ud}\\n')\n"
assert content.count(old4) == 1, "export method anchor not found or not unique"
content = content.replace(old4, new4)

with open(path, "w") as f:
    f.write(content)

print("All 4 edits applied successfully.")
