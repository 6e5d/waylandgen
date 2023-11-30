from pathlib import Path
from subprocess import run

def gen(proj, protocol):
	name = protocol.stem
	run(["wayland-scanner", "client-header"],
		stdin = open(protocol),
		stdout = open(proj / f"include/{name}.external.h", "w"),
		text = True,
		check = True,
	)
	f = open(proj / f"src/{name}.external.c", "w")
	print(f'#include "../include/{name}.external.h"', file = f)
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
gen(Path(), wproot / "unstable/xdg-decoration/xdg-decoration-unstable-v1.xml")
gen(Path(), wproot /
	"unstable/pointer-gestures/pointer-gestures-unstable-v1.xml")
