from stl import mesh
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.pyplot import autoscale
import numpy as np
import Support_Generator

def extremity_creation_triangle(axe,List):
    '''
        determined 2 faces exterimities of the support along x or y axis
    '''
    Shape_listfinal=np.shape(List)
    if axe=='xy':
        Faces=np.zeros((3,12))
        for j in range (0,3):
            for i in range(0,2):
                if j==0 or j==1:
                    #First line is the face 1254 (j=0) and 2nd face is the face 2365 (j=1)
                    Faces[j,3*i]= List[0][i+j][0]
                    Faces[j,3*i+1]= List[0][i+j][1]
                    Faces[j,3*i+2]= List[0][i+j][2]
                    Faces[j,6+3*i]= List[1][1-i+j][0]
                    Faces[j,6+3*i+1]= List[1][1-i+j][1]
                    Faces[j,6+3*i+2]= List[1][1-i+j][2]
                else:
                    Faces[j,3*i]= List[0][i*2][0]
                    Faces[j,3*i+1]= List[0][i*2][1]
                    Faces[j,3*i+2]= List[0][i*2][2]
                    Faces[j,6+3*i]= List[1][2-2*i][0]
                    Faces[j,6+3*i+1]= List[1][2-2*i][1]
                    Faces[j,6+3*i+2]= List[1][2-2*i][2]
    elif axe=='z':
        Faces=np.zeros((2,12))
        for j in range (0,2):
            for i in range(0,2):
                #First is the face 1231 and 2nd face 4564
                Faces[j,3*i]= List[j][i][0]
                Faces[j,3*i+1]= List[j][i][1]
                Faces[j,3*i+2]= List[j][i][2]
                Faces[j,6+3*i]= List[j][2-2*i][0]
                Faces[j,6+3*i+1]= List[j][2-2*i][1]
                Faces[j,6+3*i+2]= List[j][2-2*i][2]
    else:
        return "axe is not well define"
            # we need to cross the upper points to have a face (Face is point [1265] and not [1256]), that's why we have 1-i in the indices of ListFinal
    return Faces

def extremity_creation(axe,List):
    '''
        determined 2 faces exterimities of the support along x or y axis
    '''
    Shape_listfinal=np.shape(List)
    Faces=np.zeros((Shape_listfinal[0],Shape_listfinal[2]*2))
    if axe=='x':
        for j in range (0,Shape_listfinal[0]):
            for i in range(0,np.int(Shape_listfinal[1]/2)):
                #First line is the face 1265 (j=0) and 2nd face is the face 3487 (j=1)
                Faces[j,3*i]= List[0][i+j*2][0]
                Faces[j,3*i+1]= List[0][i+j*2][1]
                Faces[j,3*i+2]= List[0][i+j*2][2]
                Faces[j,6+3*i]= List[1][1+j*2-i][0]
                Faces[j,6+3*i+1]= List[1][1+j*2-i][1]
                Faces[j,6+3*i+2]= List[1][1+j*2-i][2]
    elif axe=='y':
        for i in range(0,np.int(Shape_listfinal[1]/2)):
            #First is the face 2376
            Faces[0,3*i]= List[0][i+1][0]
            Faces[0,3*i+1]= List[0][i+1][1]
            Faces[0,3*i+2]= List[0][i+1][2]
            Faces[0,6+3*i]= List[1][2-i][0]
            Faces[0,6+3*i+1]= List[1][2-i][1]
            Faces[0,6+3*i+2]= List[1][2-i][2]
            #2nd face is 1485
            Faces[1,3*i]= List[0][i*3][0]
            Faces[1,3*i+1]= List[0][i*3][1]
            Faces[1,3*i+2]= List[0][i*3][2]
            Faces[1,6+3*i]= List[1][3-3*i][0]
            Faces[1,6+3*i+1]= List[1][3-3*i][1]
            Faces[1,6+3*i+2]= List[1][3-3*i][2]
    elif axe=='z':
        for j in range (0,Shape_listfinal[0]):
            for i in range(0,np.int(Shape_listfinal[1]/2)):
                #First line is the face 1234 (j=0) and 2nd face is the face 5678(j=1)
                Faces[j,3*i]= List[j][i][0]
                Faces[j,3*i+1]= List[j][i][1]
                Faces[j,3*i+2]= List[j][i][2]
                Faces[j,6+3*i]= List[j][i+2][0]
                Faces[j,6+3*i+1]= List[j][2+i][1]
                Faces[j,6+3*i+2]= List[j][2+i][2]

    else:
        return "axe is not well define"
            # we need to cross the upper points to have a face (Face is point [1265] and not [1256]), that's why we have 1-i in the indices of ListFinal
    return Faces

def thetraedral_simple_support(List):
    Facesxy=extremity_creation_triangle('xy',List)
    Facesz=extremity_creation_triangle('z',List)
    Faces= np.concatenate((Facesxy,Facesz),axis=0)
    return Faces

def Rectangular_simple_support(List):
    Facesx=extremity_creation('x',List)
    Facesy=extremity_creation('y',List)
    Facesz=extremity_creation('z',List)
    Faces= np.concatenate((Facesx,Facesy,Facesz),axis=0)
    return Faces

def line_support(axes,List,p):
    '''
        Creation of a line support
        with p the gap between each face of the grid
    '''
    Faces= extremity_creation(axes, List)
    #Coefficient i1 i2 i3 and d1 d2 d3 d4 aim to manage the surface creations when top and bottom are not parallel
    i1=i2=i3=i4=d1=d2=d3=d4=0
    m=np.zeros((1,1))
    if Faces[0,2]>Faces[1,2]:
        i1=-1
        d1=np.int(np.abs(Faces[0,2]-Faces[1,2]))
        m=np.append(m,np.array([[2]]),axis=0)
    elif Faces[0,2]<Faces[1,2]:
        i1=1
        d1=np.int(np.abs(Faces[0,2]-Faces[1,2]))
        m=np.append(m,np.array([[2]]),axis=0)
    else:
        i1=0
    if Faces[0,5]>Faces[1,5]:
        i2=-1
        d2=np.int(np.abs(Faces[0,5]-Faces[1,5]))
        m=np.append(m,np.array([[5]]),axis=0)
    elif Faces[0,5]<Faces[1,5]:
        i2=1
        d2=np.int(np.abs(Faces[0,5]-Faces[1,5]))
        m=np.append(m,np.array([[5]]),axis=0)
    else:
        i2=0
    if Faces[0,8]>Faces[1,8]:
        i3=-1
        d3=np.int(np.abs(Faces[0,8]-Faces[1,8]))
        m=np.append(m,np.array([[8]]),axis=0)
    elif Faces[0,8]<Faces[1,8]:
        i3=1
        d3=np.int(np.abs(Faces[0,8]-Faces[1,8]))
        m=np.append(m,np.array([[8]]),axis=0)
    else:
        i3=0
    if Faces[0,11]>Faces[1,11]:
        i4=-1
        d4=np.int(np.abs(Faces[0,11]-Faces[1,11]))
        m=np.append(m,np.array([[11]]),axis=0)
    elif Faces[0,11]<Faces[1,11]:
        i4=1
        d4=np.int(np.abs(Faces[0,11]-Faces[1,11]))
        m=np.append(m,np.array([[11]]),axis=0)
    else:
        i4=0
    if axes!='z':
        if i1==i2==i3==i4==0:
            pass
        else:
            a=m[1,0]
            b=m[2,0]
            if Faces[0,np.int(a)]!=Faces[0,np.int(b)]:
                i1=i2=i3=i4=0
        if axes == 'x':
            nx=np.int(np.abs(Faces[0,1]-Faces[1,4])*(1/p))-1
            l=2
            while nx == -1:
                nx=np.int(np.abs(Faces[0,0]-Faces[1,3*l+1])*(1/p))-1
                l+=1
            a=np.zeros((nx,12))
            if Faces[0,1]>Faces[1,1]:
                for i in range(1, nx+1):
                    a[i-1,:]=np.array([Faces[0,0],Faces[0,1]-i*p,Faces[0,2]+(i*d1*i1)/nx,Faces[0,3],Faces[0,4]-i*p,Faces[0,5]+(i*d2*i2)/nx,Faces[0,6],Faces[0,7]-i*p,Faces[0,8]+(i*d3*i3)/nx,Faces[0,9],Faces[0,10]-i*p,Faces[0,11]+(i*d4*i4)/nx])
            elif Faces[0,1]<Faces[1,1]:
                for i in range(1, nx+1):
                    a[i-1,:]=np.array([Faces[0,0],Faces[0,1]+i*p,Faces[0,2]+(i*d1*i1)/nx,Faces[0,3],Faces[0,4]+i*p,Faces[0,5]+(i*d2*i2)/nx,Faces[0,6],Faces[0,7]+i*p,Faces[0,8]+(i*d3*i3)/nx,Faces[0,9],Faces[0,10]+i*p,Faces[0,11]+(i*d4*i4)/nx])
            Faces= np.insert(Faces,1, a, axis=0)

        #elif Faces[0,1]!= Faces[0,4] or Faces[0,1]!= Faces[0,7] or Faces[0,1]!= Faces[0,10]:
        elif axes == 'y':
            ny=np.int(np.abs(Faces[0,0]-Faces[1,3])*(1/p))-1
            l=2
            while ny == -1:
                ny=np.int(np.abs(Faces[0,1]-Faces[1,3*l])*(1/p))-1
                l+=1
            a=np.zeros((ny,12))
            if Faces[0,0]>Faces[1,0]:
                for i in range(1, ny+1):
                    a[i-1,:]=np.array([Faces[0,0]-i*p,Faces[0,1],Faces[0,2]+(i*d1*i1)/ny,Faces[0,3]-i*p,Faces[0,4],Faces[0,5]+(i*d2*i2)/ny,Faces[0,6]-i*p,Faces[0,7],Faces[0,8]+(i*d3*i3)/ny,Faces[0,9]-i*p,Faces[0,10],Faces[0,11]+(i*d4*i4)/ny])
            elif Faces[0,0]<Faces[1,0]:
                for i in range(1, ny+1):
                    a[i-1,:]=np.array([Faces[0,0]+i*p,Faces[0,1],Faces[0,2]+(i*d1*i1)/ny,Faces[0,3]+i*p,Faces[0,4],Faces[0,5]+(i*d2*i2)/ny,Faces[0,6]+i*p,Faces[0,7],Faces[0,8]+(i*d3*i3)/ny,Faces[0,9]+i*p,Faces[0,10],Faces[0,11]+(i*d4*i4)/ny])
            Faces= np.insert(Faces,1, a, axis=0)

    elif axes=='z':
        nz=np.int(np.abs(Faces[0,2]-Faces[1,2])*(1/p))-1
        a=np.zeros((nz,12))
        if Faces[0,2]>Faces[1,2]:
            for i in range(1, nz+1):
                a[i-1,:]=np.array([Faces[0,0],Faces[0,1],Faces[0,2]+(i*d1*i1)/nz,Faces[0,3],Faces[0,4],Faces[0,5]+(i*d2*i2)/nz,Faces[0,6],Faces[0,7],Faces[0,8]+(i*d3*i3)/nz,Faces[0,9],Faces[0,10],Faces[0,11]+(i*d4*i4)/nz])
        elif Faces[0,2]<Faces[1,2]:
            for i in range(1, nz+1):
                a[i-1,:]=np.array([Faces[0,0],Faces[0,1],Faces[0,2]+(i*d1*i1)/nz,Faces[0,3],Faces[0,4],Faces[0,5]+(i*d2*i2)/nz,Faces[0,6],Faces[0,7],Faces[0,8]+(i*d3*i3)/nz,Faces[0,9],Faces[0,10],Faces[0,11]+(i*d4*i4)/nz])
        Faces= np.insert(Faces,1, a, axis=0)

    return Faces

def gridxy(List,p):
    '''
        Creation a grid along x and y axis
    '''
    Faces_x=line_support('x',List,p)
    Faces_y=line_support('y',List,p)
    Faces=np.concatenate((Faces_x,Faces_y),axis=0)
    return Faces

def grid3D(List,p):
    '''
        Creation of a grid along x, y and z-axis
    '''
    Faces_x=line_support('x',List,p)
    Faces_y=line_support('y',List,p)
    Faces_z=line_support('z',List,p)
    Faces=np.concatenate((Faces_x,Faces_y,Faces_z),axis=0)
    return Faces

def ZigZag(List,p):
    '''
        Creation of the ZigZag shape
    '''
    Facesx=line_support('x',List,p)
    Facesx= np.delete(Facesx,0,0)
    Facesx_shape=Facesx.shape
    Facesx= np.delete(Facesx,Facesx_shape[0]-1,0)
    Faces_all_y=extremity_creation('y',List)
    i1=i2=d1=d2=0
    m=np.zeros((1,1))
    if (Faces_all_y[0,2]>Faces_all_y[0,5] and np.abs(Faces_all_y[0,1])>np.abs(Faces_all_y[0,4])) or (Faces_all_y[0,2]<Faces_all_y[0,5]and np.abs(Faces_all_y[0,1])<np.abs(Faces_all_y[0,4])):
        i1=-1
        d1=np.int(np.abs(Faces_all_y[0,2]-Faces_all_y[0,5]))
        m=np.append(m,np.array([[2]]),axis=0)
    elif Faces_all_y[0,2]<Faces_all_y[0,5] and np.abs(Faces_all_y[0,1])>np.abs(Faces_all_y[0,4]):
        i1=1
        d1=np.int(np.abs(Faces_all_y[0,2]-Faces_all_y[0,5]))
        m=np.append(m,np.array([[2]]),axis=0)
    else:
        i1=0
    if Faces_all_y[0,8]>Faces_all_y[0,11]:
        i2=-1
        d2=np.int(np.abs(Faces_all_y[0,8]-Faces_all_y[0,11]))
        m=np.append(m,np.array([[5]]),axis=0)
    elif Faces_all_y[0,8]<Faces_all_y[0,11]:
        i2=1
        d2=np.int(np.abs(Faces_all_y[0,8]-Faces_all_y[0,11]))
        m=np.append(m,np.array([[5]]),axis=0)
    else:
        i2=0
    ny=np.int(np.abs(Faces_all_y[0,1]-Faces_all_y[0,4])*(1/(p*2)))
    a1=np.zeros((ny,12))
    a2=np.zeros((ny,12))
    if Faces_all_y[0,1]>Faces_all_y[0,4]:
        p=-p
    else:
        pass
    for i in range(0, ny):
        if i==0:
            a1[i,:]=np.array([Faces_all_y[0,0],Faces_all_y[0,1]+i*(p*2),Faces_all_y[0,2],Faces_all_y[0,3],Faces_all_y[0,1]+p,Faces_all_y[0,5]+d1+(i1*d1)/ny,Faces_all_y[0,6],Faces_all_y[0,1]+p,Faces_all_y[0,8],Faces_all_y[0,9],Faces_all_y[0,10]+i*(p*2),Faces_all_y[0,11]+d2+(i2*d2)/ny])
            a2[i,:]=np.array([Faces_all_y[1,0],Faces_all_y[1,1]+p,Faces_all_y[1,2],Faces_all_y[1,3],Faces_all_y[1,1]+2*p,Faces_all_y[1,5]+d1+(i1*d1)/ny,Faces_all_y[1,6],Faces_all_y[1,1]+2*p,Faces_all_y[1,8],Faces_all_y[1,9],Faces_all_y[1,10]+p,Faces_all_y[1,11]+d2+(i2*d2)/ny])
        else:
            a1[i,:]= np.array([Faces_all_y[0,0],Faces_all_y[0,1]+i*(p*2),a1[i-1,2]+(i1*d1)/ny,Faces_all_y[0,3],a1[i-1,1]+3*p,a1[i-1,5]+(i1*d1)/ny,Faces_all_y[0,6],a1[i-1,1]+3*p,a1[i-1,8]+(i2*d2)/ny,Faces_all_y[0,9],Faces_all_y[0,10]+i*(p*2),a1[i-1,11]+(i2*d2)/ny])
            a2[i,:]=np.array([Faces_all_y[1,0],a2[i-1,1]+p*2,a2[i-1,2]+(i1*d1)/ny,Faces_all_y[1,3],a2[i-1,1]+3*p,a2[i-1,5]+(i1*d1)/ny,Faces_all_y[1,6],a2[i-1,1]+3*p,a2[i-1,8]+(i2*d2)/ny,Faces_all_y[1,9],a2[i-1,10]+p*2,a2[i-1,11]+(i2*d2)/ny])
    a= np.concatenate((a1,a2),axis=0)
    Faces=np.concatenate((Facesx,a),axis=0)
    return Faces


def plot(FacesMatrix,my_mesh,xy_limmin,xy_limmax,z_limmin,z_limmax):
    FacesMatrix_shape=np.shape(FacesMatrix)
    figure2 = plt.figure()
    ax2 = figure2.add_subplot(111, projection='3d')
    verts=[[FacesMatrix[i,j*3:j*3+3] for j in range(4)] for i in range(FacesMatrix_shape[0])]
    ax2.add_collection3d(Poly3DCollection(verts, alpha=0.25, facecolors='#800000', edgecolors='brown'))
    ax2.add_collection3d(mplot3d.art3d.Poly3DCollection(my_mesh.vectors, edgecolors='navy'))
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')
    ax2.set_xlim(xy_limmin,xy_limmax)
    ax2.set_ylim(xy_limmin,xy_limmax)
    ax2.set_zlim(z_limmin,z_limmax)
    plt.show()
    return

def plot_mesh(my_mesh):
    figure2 = plt.figure()
    ax2 = figure2.add_subplot(111, projection='3d')
    ax2.add_collection3d(mplot3d.art3d.Poly3DCollection(my_mesh.vectors, edgecolors='navy'))
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')
    ax2.set_xlim(-30,30)
    ax2.set_ylim(-30,30)
    ax2.set_zlim(0,60)
    plt.show()
    return
