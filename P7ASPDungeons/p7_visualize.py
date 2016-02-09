import p7_helper
	
def main(argv):
	prog, filename = argv
	design = p7_helper.parse_json_result(open(filename).read())
	print p7_helper.side_by_side(p7_helper.render_ascii_dungeon(design), p7_helper.render_ascii_touch(design, 1))
	print p7_helper.side_by_side(*[p7_helper.render_ascii_touch(design,i) for i in range(2,4)])

if __name__ == '__main__':
	import sys
	main(sys.argv)
 