import math
import numpy as np

def reconstruction(e,s):

	# e = a list of lists of edges in each path [[],[],[]]
	# s = a list of sums paired with each list of edges in the paths

	all_edges = []

	for edges in e:
		for i in range(0, len(edges)):
			all_edges.append(edges[i])

	all_edges = list(set(all_edges))

	# as long as all the entries in all_edges are strings or integers, set will do the work

	matrix = np.zeros((len(s),len(all_edges)), dtype = np.int)

	for path in range(0, len(s)):	
		for j in range(0, len(all_edges)):
			for i in range(0, len(e[path])):
				if e[path][i] == all_edges[j]:
					matrix[path][j] += 1

	answer = np.linalg.lstsq(matrix,s)[0]
	print(all_edges,answer)

	return (all_edges,answer)

reconstruction([[1,2,3],[3,4,5],[2,5,6]], [3,4,5])
reconstruction([["1.1", "1.2", "1.3"],["1.1","1.2"],["1.2","1.3","1.2"],["1.1","1.6","1.3","1.4"],["1.2","1.4"]],[2,3,4,5,6])