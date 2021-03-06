import os,sys, glob
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import time

from stl import mesh, Mesh


import numpy as np
from Support_finder import support_45deg_rule
from Support_finder import needed_support_Bridge_rule
from Support_Generator import AreasWithSameAngle
from Support_Generator import FindContour
from Support_Generator import Projection
from Support_Shape import line_support
from Support_Shape import Rectangular_simple_support
from Support_Shape import thetraedral_simple_support
from Support_Shape import gridxy
from Support_Shape import ZigZag
from Support_Shape import plot
from Support_Shape import plot_mesh
from Locate_STL import ShapeChoice



print("----------------------------------------\n")
print("            SUPPORT GENERATOR              \n")
print("by Thomas Heissel and Thomas Girerd       ")
print("----------------------------------------\n")
print("You need to choose the STL file you want to generate supports with.")

from Locate_STL import FindSTL
STL = FindSTL()
my_mesh= mesh.Mesh.from_file(STL)
normal=my_mesh.normals
vertices= my_mesh.points
support_angle=support_45deg_rule(normal,vertices,45)
support_bridge=needed_support_Bridge_rule(normal,vertices,5)
i=0
p=len(support_bridge)
k=0
while i<p:
    if all(support_bridge[k][0,0:9]== 0):
        del support_bridge[k]
    else:
        k=k+1
    p=p-1
liste_support=[]
liste_support=support_bridge+support_angle
ListeContour=[]
for i in range(len(liste_support)):
    A=AreasWithSameAngle(liste_support[i])
    ListeContour.append(FindContour(A))
ListeProjete=Projection(ListeContour)
ListeProjete_shape=np.shape(ListeProjete)

if len(ListeProjete)==0:
    print("you do not need any support")
else:
    n=0
    Faces=np.zeros((0,12))
    if ListeProjete_shape[2]==3:
        while n <ListeProjete_shape[0]:
            The=thetraedral_simple_support(ListeProjete[:][n][:][:])
            Faces= np.append(Faces,The,axis=0)
            n+=1
        plot(Faces,my_mesh,-50,50,0,80)
    else:
        Choice=ShapeChoice()
        if Choice==1:
            while n <ListeProjete_shape[0]:
                Rec=Rectangular_simple_support(ListeProjete[:][n][:][:])
                Faces= np.append(Faces,Rec,axis=0)
                n+=1
        elif Choice==2:
            while n <ListeProjete_shape[0]:
                Grid=gridxy(ListeProjete[:][n][:][:],1)
                Faces= np.append(Faces,Grid,axis=0)
                n+=1
        elif Choice==3:
            while n <ListeProjete_shape[0]:
                ZZ=ZigZag(ListeProjete[:][n][:][:],1)
                Faces= np.append(Faces,ZZ,axis=0)
                n+=1
        plot(Faces,my_mesh,-30,30,0,50)



