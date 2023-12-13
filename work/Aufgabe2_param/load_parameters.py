import minitopsim.parameters as par
import os
import sys

sys.path.insert(0, os.getcwd())


cfg_file = sys.argv[1]
out_file = cfg_file.replace(".cfg", ".out")
cfg_file = os.path.join(os.path.dirname(__file__), cfg_file)
out_file = os.path.join(os.path.dirname(__file__), out_file)

try:
    par.load_parameters(cfg_file)

    file_content = ""
    for key in dir(par):
        if key.isupper() and not key.startswith("_"):
            file_content = f'{file_content}{key} = {getattr(par, key)}\n'

except Exception as e:
    file_content = e.__str__()

with open(out_file, "w") as f:
    f.write(file_content)
