import numpy as np

# Functions to solve heat diffusion: 

def solve_heat2D(T,type,kappa, dt,dx,dz,nx,nz):
    dT_arr = np.zeros_like(T)
    for i in range(1, nx+1):
        for j in range(1,nz+1):
            if type[j,i] == 'a' or type[j,i] == 'b': #ignore atomsphere and boundary cells
                continue
            else:
                dTdx = (T[j,i-1] - 2*T[j,i] + T[j,i+1]) / (dx**2) # calculate T difference in  x
                dTdz = (T[j-1,i] - 2*T[j,i] + T[j+1,i]) / (dz**2) # calculate T difference in z
                
                dT_arr[j,i] = kappa[j,i]*dt*(dTdx+dTdz)

    return dT_arr

def convert_T_to_heat(T,dz,dx,cp,porosity,rho_solid,rho_water):
    mass = porosity*(dz*dx**2)*rho_water + (1-porosity)*(dz*dx**2)*rho_solid #calculate mass of whole cell
    return T*mass*cp


# Functions used to move cells during freezing:

def cart_distance(p1,p2):
    '''Calculate the cartesian distance between two points (2D)'''
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def find_closest(x,z,target_val,search_arr):
    '''Find the closest cell of target_val value to the cell at [z,x] in search_arr and the distance between them'''
    valid = np.where(search_arr == target_val)
    valid = list(zip(valid[0],valid[1]))

    d = [cart_distance((x,z),v) for v in valid]
    if len(d) != 0:
        closest_idx = valid[np.where(d==min(d))[0][0]]
        distance = min(d)
    else: #if all space is filled
        closest_idx=None
        distance=None
    return closest_idx, distance

def find_newplace(old_coord,type_arr,ds=5,dv=5):
    ''' Find new location for a cell when displaced by an ice cell'''
    z,x = old_coord
    closest_atm, d_atm = find_closest(z,x,'a',type_arr)
    closest_void, d_void = find_closest(z,x,'v',type_arr)

    if closest_void == None or d_void == None:
        new_z,new_x = closest_atm
        return new_z,new_x
    
    P_surf = max(0,1-(d_atm/ds))
    P_void = max(0,1-(d_void/dv))

    if P_surf > P_void:
        new_z,new_x = closest_atm
    else:
        new_z,new_x = closest_void

    return new_z,new_x

def replace_cell(old_coord,new_coord,type_arr,diff_arr,fine_diff,ice_diff):
    '''Replace fines cell with ice particle and move fines to new cell and change diffusivity array'''
    #change old cell to ice cell:
    type_arr[old_coord] = 'i'
    diff_arr[old_coord] = ice_diff

    #change new cell:
    type_arr[new_coord] = 'f'
    diff_arr[new_coord] = fine_diff

    return type_arr,diff_arr
    

# Functions to move cells during thawing: