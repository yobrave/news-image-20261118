import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
shutil.copyfile(os.path.join(here, "entry.png"), os.path.join(out_dir, "entry.png"))
