print("Starting main.py \n\n")

#--------------------------------------------
# Solving the maze
#--------------------------------------------
import Maze

#sample only stuff
sampleMaze5bin =[
	[ 6, 10, 10, 10, 12],
	[ 7, 14, 12,  6, 13],
	[ 5,  5,  1,  5,  5],
	[ 5,  3, 10,  9,  5],
	[ 3, 10, 10, 10,  9]
]
sampleMaze5Target = [2, 2]

print "Maze binary:"
for i in range(5):
	print sampleMaze5bin[i]
print " "

Maze.solve(sampleMaze5bin, sampleMaze5Target)

print " "
print " "
print " "

sampleMaze8bin = [
	[6, 10, 14, 12, 6, 14, 10, 8],
	[7, 12, 1, 5, 5, 3, 10, 12],
	[5, 5, 6, 11, 11, 10, 12, 5],
	[5, 5, 7, 14, 12, 6, 13, 5],
	[5, 3, 9, 3, 9, 5, 1, 5],
	[3, 12, 6, 10, 10, 11, 10, 13],
	[6, 9, 3, 14, 10, 14, 8, 1],
	[3, 10, 10, 9, 2, 11, 10, 8]
]
sampleMaze8Target = [3, 3]

print "Maze binary:"
for i in range(8):
	print sampleMaze8bin[i]
print " "

Maze.solve(sampleMaze8bin, sampleMaze8Target)