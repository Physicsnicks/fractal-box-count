#================================================#
# A fixed-grid box counting algorithm that could #
# be used to help determine the fractal dimension#
# of a group of sperical particles in a cubic    #
# container. The return froma a call to this     #
# function might be taken for the calculation    #
# S = ln(N)/ln(1/e)                              #

def intersect(sx,sy,sz,rad,bx,by,bz,l):
    """
    Determine if a sphere and a box overlap
    Args:
        sx: float for the x postion of the center of the sphere
        sy: float for the y postion of the center of the sphere
        sz: float for the z postion of the center of the sphere
        rad: a float with the raidus of the sphere
        bx: a float with the smallest x value of the box
        by: a float with the smallest y value of the box
        bz: a float with the smallest z value of the box
        l: a float with the side length
    Returns:
        a boolean indicating if they overlap
    """
    # check intersection with the planes that define the box

    xs = (sx <= bx) & ((sx + rad) >= bx)
    xl = (sx >= (bx+l)) & ((sx - rad) <= (bx+l))
    ys = (sy <= by) & ((sy + rad) >= by)
    yl = (sy >= (by+l)) & ((sy - rad) <= (by+l))
    zs = (sz <= bz) & ((sz + rad) >= bz)
    zl = (sz >= (bz+l)) & ((sz - rad) <= (bz+l))

    # check if within a face
    fz = (bx <= sx <= (bx+l)) & (by <= sy <= (by+l))
    fx = (bz <= sz <= (bz+l)) & (by <= sy <= (by+l))
    fy = (bx <= sx <= (bx+l)) & (bz <= sz <= (bz+l))

    # now do some logic
    # if within a face and intersecting a plane return true

    if ((fx & (xs or xl)) or (fy & (ys or yl)) or (fz & (zs or zl))):
        return True
        
    # if within two planes and intersecting two orthogonal planes
    if ((bx <= sx <= (bx+l)) & 
        ((yl & zl) or (yl & zs) or (ys & zl) or (ys & zs))):
        return True
    if ((by <= sy <= (by+l)) & 
        ((xl & zl) or (xl & zs) or (xs & zl) or (xs & zs))):
        return True
    if ((bz <= sz <= (bz+l)) & 
        ((yl & xl) or (yl & xs) or (ys & xl) or (ys & xs))):
        return True

    # if intersecting three planes return true
    if (xs or xl) & (ys or yl) & (zs or zl):
        return True 

    # we got here, the sphere must be outside the box
    return False

    

def box_counting(pos, rad, side_L, nb=10):
    """
    Calculate the box counting dimension for a fractal-like object using a fixed
    grid scheme. 
    Args:
        pos: an array of float coordinates for the particles (dimension [N][3]  
          where N is the number of particles)
        rad: a float defining the radius of the particles
        side_L: a float with the length of the bounding box 
        nb: integer for the number of boxes per length inside the bounding box
    Returns:
        a float with the box counting dimension
    """
    tot = 0 # the total number of boxes
    count = 0 # the number of boxes occupied
    dis = side_L/nb   # the length of each box to be counted

    #iterate over the three dimensions
    for i in range(0,nb):
        for j in range(0,nb):
            for k in range(0,nb):
                tot += 1
                #iterate over all of the particles
                for p in range(len(pos)):
                    if ((i*dis <= pos[p][0] < (i+1)*dis) &
                        (j*dis <= pos[p][1] < (j+1)*dis) & 
                        (k*dis <= pos[p][2] < (k+1)*dis)):  
                        # first determine if the center of the particle is in the box
                        count += 1
                        break # we only need to add 1 particle / box

                    # check if the edge of the box intersects the sphere
                    # this is slower so we separate it    
                    elif intersect(pos[p][0],
                                   pos[p][1],
                                   pos[p][2],
                                   rad,
                                   i*dis,
                                   j*dis,
                                   k*dis,dis):
                        count += 1
                        break
    return count, tot

