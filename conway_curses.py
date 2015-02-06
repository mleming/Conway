from time import sleep, clock
import random
import os,sys
import signal
import curses

#Determines whether or not to initially fill the board with random squares. If you don't do this, I made a glider that initially goes onto the board; I didn't make much else yet, however.
rand_choice = True

#The dimensions of the board you will be using. Note that, because of ASCII widths and lengths, it will not appear to be square if you make the width and length equal. Currently, to get a square box, you need about a 30:13 ratio.
(rows, columns)=map(lambda k: int(k), os.popen('stty size', 'r').read().split())
window_width = columns
window_length = rows

#In seconds, the sleep delay between each frame
frame_rate = 0.00

#Enter '0' for neverending iterations; just hit CTRL-C to exit the program
number_of_iterations = 0


#The particular numbers; as they are (live_cell_min=2; live_cell_max=3; dead_cell_reproduction=3), they go by the standard rules of Conway's Game of Life)
live_cell_min = 2
live_cell_max = 3
dead_cell_reproduction = 3

# Some sample shapes. Set one of these to "select_shape" and turn rand_choice off if you want to use one of these shapes
shape_offset = (window_length/2,window_width/2)
glider = [(0,1), (0,2), (0,3), (1,4), (2,1)]
gosper_glider_gun = [(5, 1), (5, 2), (6, 1), (6, 2), (5, 11), (6, 11), (7, 11), (4, 12), (8, 12), (3, 13), (9, 13), (3, 14), (9, 14), (6, 15), (4, 16), (8, 16), (5, 17), (6, 17), (7, 17), (6, 18), (3, 21), (4, 21), (5, 21), (3, 22), (4, 22), (5, 22), (2, 23), (6, 23), (1, 25), (2, 25), (6, 25), (7, 25), (3, 35), (4, 35), (3, 36), (4, 36)]
infinite_growth_1 = [(6,1),(5,3),(6,3),(2,5),(3,5),(4,5),(1,7),(2,7),(3,7),(2,8)]
horizontal_glider = [(1,2),(3,2),(4,3),(4,4),(1,5),(4,5),(2,6),(3,6),(4,6)]
r_pentomino = [(2,1),(1,2),(2,2),(3,2),(1,3)]

# This is the one that fills in if it is not random
select_shape = horizontal_glider

def fill_grid(mg, ra):
	tempgrid = [[0 for x in xrange(len(mg[0]))] for x in xrange(len(mg))]
	for x in range(len(tempgrid)):
		for y in range(len(tempgrid[x])):
			if ra:
				tempgrid[x][y] = random.choice([True,False])
			else:
				tempgrid[x][y] = False
	if not ra:
		for (x, y) in select_shape:
			tempgrid[x+len(mg)/2][y+len(mg[0])/2] = True
	for x in range(len(mg)):
		mg[x] = tempgrid[x];

def calculate_change(mg,x_pos,y_pos):
	surrounding_count = 0;
	for x_add in range(3):
		for y_add in range(3):
			if (mg[(x_pos + (x_add - 1))%len(mg)][(y_pos+(y_add - 1))%len(mg[0])] and ((x_add - 1) != 0 or (y_add - 1) !=0)):
				surrounding_count+=1;
	return surrounding_count;
	#return sum(mg[(x_pos-1):(x_pos+2)][(y_pos-1):(y_pos+2)],[]).count(True) - (1 if mg[x_pos][y_pos] else 0);
	
def apply_change(mg):
	tempgrid = [[0 for x in xrange(len(mg[0]))] for x in xrange(len(mg))]
	for i in range(len(mg)):
		for j in range(len(mg[i])):
			temp = calculate_change(mg,i,j)
			tempgrid[i][j] = (mg[i][j] and temp >= live_cell_min and temp <= live_cell_max) or (not mg[i][j] and temp == dead_cell_reproduction)

	for i in range(len(mg)):
		mg[i] = tempgrid[i]

def signal_handler(signal, frame):
	curses.echo();
	curses.nocbreak();
	curses.endwin();
	print "Program ended";
	sys.exit(0)


##########CURSES STUFF

def print_grid(mg):
	fill_grid(mg, rand_choice)
	stdscr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	#	signal.signal(signal.SIGQUIT, signal_handler)
	#	signal.signal(signal.SIGTERM, signal_handler)
	try:
		frame_count = 0
		i=0
		while number_of_iterations == 0 or frame_count < number_of_iterations:
			for x in mg:
				try:
					stdscr.addstr(i,0, "".join(["0" if y else " " for y in x ]))
				except curses.error:
					continue
				i+=1
			stdscr.refresh()
			if frame_rate > 0:
				sleep(frame_rate)
			i=0
			apply_change(mg)
			frame_count+=1
	finally:
		curses.echo()
		curses.nocbreak()
		curses.endwin()
		return

if __name__ == "__main__":
	memgrid = [[0 for x in xrange(window_width)] for x in xrange(window_length)]
	signal.signal(signal.SIGINT, signal_handler)
	start = clock()
	print_grid(memgrid)
	print clock() - start
