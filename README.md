# fractal-box-count
A fixed grid box-counting algorithm to determine the fractal dimension of a 3-D collection of spherical particles in a cubic box.

The function takes a 2-D array of Nx3 dimensions, where N is the number of spherical particles to be counted. The other 3 dimesions are the x, y, and z coordinates of the particles.
The radius, "rad", is a float.
The "side_L" is the length of a side of the cube containing all of the particles. 
The number of partitions for the grid are determined by the argument nb.

The returns are ints for the number of boxes at least partially occupied by a sphere, and the total number of boxes in the cube of interest.
