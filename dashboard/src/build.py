#!/usr/bin/env python3
"""Builds the single-file dashboard: python3 build.py <three.min.js> <OrbitControls.js> <out.html>"""
import sys, pathlib
here = pathlib.Path(__file__).parent
three, orbit, out = sys.argv[1:4]
t = (here / "template.html").read_text(encoding="utf-8")
d = (here / "data.json").read_text(encoding="utf-8")
t = t.replace("__DATA__", d.replace("</", "<\\/"))
t = t.replace("__MESHES__", (here / "meshes.json").read_text(encoding="utf-8"))
t = t.replace("__THREE__", pathlib.Path(three).read_text(encoding="utf-8"))
t = t.replace("__ORBIT__", pathlib.Path(orbit).read_text(encoding="utf-8"))
t = t.replace("__MW__", (here / "vendor" / "material-web.min.js").read_text(encoding="utf-8"))
pathlib.Path(out).write_text(t, encoding="utf-8")
print("built", out, len(t))
