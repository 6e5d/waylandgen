from pathlib import Path
from subprocess import run

def gen(proj, protocol):
	name = protocol.stem
	run(["wayland-scanner", "client-header"],
		stdin = open(protocol),
		stdout = open(proj / f"include/{name}-client-header.h", "w"),
		text = True,
		check = True,
	)
	f = open(proj / f"src/{name}-private-code.c", "w")
	print(f'#include "../include/{name}-client-header.h"', file = f)
	f.flush()
	run(["wayland-scanner", "private-code"],
		stdin = open(protocol),
		stdout = f,
		text = True,
		check = True,
	)
	f.close()

wproot = Path("/usr/share/wayland-protocols")
gen(Path(), wproot / "stable/xdg-shell/xdg-shell.xml")
gen(Path(), wproot / "unstable/tablet/tablet-unstable-v2.xml")