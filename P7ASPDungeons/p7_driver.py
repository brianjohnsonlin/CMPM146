import p7_helper

def main(argv):
	design = p7_helper.solve("level-core.lp", "level-style.lp", "level-sim.lp","level-shortcuts.lp","--parallel-mode=4")
	print p7_helper.side_by_side(p7_helper.render_ascii_dungeon(design), p7_helper.render_ascii_touch(design, 1))
	print p7_helper.side_by_side(*[p7_helper.render_ascii_touch(design,i) for i in range(2,4)])

if __name__ == '__main__':
	import sys
	main(sys.argv)
