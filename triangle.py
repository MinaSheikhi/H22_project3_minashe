from array import array
from calendar import c
import numpy as np
import matplotlib.pyplot as plt


def triangle_corners (points: tuple)->np.ndarray:
    """
    Defining three corners of a equilateral triangle.

    Arguments:
        points (tuple):
            two choosen corners
    
    Returns:
        np.ndarray:
            The 3 corners        
    """
    c0, c1 = points 
    c0 = np.array(c0)
    c1 = np.array(c1)
    x = (c0[0] + c1[0])/2
    y = abs(c0[0] - c1[0])
    c2 = (x, y)
    return np.array([c0, c1, c2])



def starting_point(points: np.ndarray)->np.ndarray:

    """
    Picking a starting point randomly within the triangle.

    Arguments:
        points (np.ndarray):
            The 3 corners of the rectangle
    returns: 
        np.ndarray:
            Random starting point
    """
    c0, c1, c2 = points
    weights = np.random.random(3) # np.random.random() returns random floats in the half-open interval [0.0, 1.0)
    weights = weights/sum(weights)
    w0, w1, w2 = weights
    return c0*w0 + c1*w1 + c2*w2

    

def plot_triangle(N: int)->None:

    """
    Plotting the triangle corners

    Arguments:
        N(int):
            Number of points that are going to be generated
    """

    corners = triangle_corners(([0,0], [1,0]))
    plt.figure()
    
    # Generating N points to plot figure resembling Sierpinski Triangle.
    for _ in range(N):
        x = starting_point(corners)
        plt.scatter(x[0], x[1], c='r')


def list_of_points_on_triangle()->None:
    """
    Generating a list with start value x0 and array with triangle corners.
    returns:
        corners(np.ndarray):
            Triangle corners
        x_list(list):
            list including startvalue x0
    """
    corners = triangle_corners(([0,0], [1,0]))
    plt.figure()
    x = starting_point(corners)
    x_list = [x]
    return corners, x_list

def plot_Sierpinski_Triangle_1d(N: int)->None:
    """
    Generating N points, ignoring first 5, to plot figure resembling Sierpinski Triangle.
    Argument:
        N(int):
            Number of points.
    """

    corners, x_list = list_of_points_on_triangle()

    for i in range(N):
        x_list.append((x_list[i] + corners[np.random.randint(low=0, high = 3)])/2) #random.randint velger tilfeldig heltall fra 0 til og med 2

    # Turning x_list to an array 
    x_list = np.array(x_list[6:])
    print(len(x_list))
    plt.scatter(*zip(*corners), c='b')
    plt.scatter(x_list[:,0], x_list[:,1], s = 0.1, marker = '.', c='g')
    plt.axis('equal')
    plt.axis('off')
    plt.show()


def plot_alt_1e(N: int)->None:
    """
    Generating N points to plot figure resembling Sierpinski Triangle and adding 
    color relative to which corner was picked for each point.
    Argument:
            N(int):
                Number of points.
    """
    corners, x_list = list_of_points_on_triangle()
    colors = [0]
    for i in range(N):
        j = np.random.randint(low=0, high=3)#random.randint velger tilfeldig heltall fra 0 til og med 2
        x_list.append((x_list[i] + corners[j])/2) 
        colors.append(j)

    # Turning x_list to an array 
    x_list = np.array(x_list[6:]) #blir en liste med punkter
    colors = np.array(colors[6:]) #en liste med corner index (altså hvilken corner det er)

    red = x_list[colors == 0]  #colors == 0 gir en liste med True og False og deretter drar ut liste med punkter som korresponderer True.
    green = x_list[colors == 1]
    blue = x_list[colors == 2]
  
    plt.scatter(*zip(*corners), c='b')
    plt.scatter(red[:,0], red[:,1], s = 0.1, marker = '.', color = 'red')
    plt.scatter(green[:,0], green[:,1], s = 0.1, marker = '.', color = 'green')
    plt.scatter(blue[:,0], blue[:,1], s = 0.1, marker = '.', color = 'blue')
    plt.axis('equal')
    plt.axis('off')
    plt.show()


def Alternative_iteration_func(N: int)->np.ndarray:
    """
    Defining colors for the plot by computing individual RGB color value for each point.
    Argument:
        N(int):
            Number of points.
    returns:
        np.ndarray:
            RGB values
    """
    C = np.zeros((N, 3))
    C[0] = (0,0,0)
    corners = list_of_points_on_triangle()[0]
    x_list = np.zeros((N, 2))

    r0 = np.array([1,0,0]) #red
    r1 = np.array([0,1,0]) #green
    r2 = np.array([0,0,1]) #blue
    r = [r0, r1, r2]

    for i in range(N-1):
        j = np.random.randint(3)
        C[i+1] = (C[i] + r[j])/2
        x_list[i+1] = ((x_list[i] + corners[j])/2) # the corners get the same index as the color list C

    return C[5:], x_list[5:]

def Alernative_plot_color_Sierpinski(N: int)->None:
    """
    Plotting Sierpinski Triangle with colors using RGB values.
    Argument:
        N(int):
            Number of points.
    """

    colors, x = Alternative_iteration_func(N)

    plt.scatter(*zip(*x), c=colors, s=0.2)
    plt.axis('equal')
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    plot_triangle(1001)
    plot_Sierpinski_Triangle_1d(10000)
    plot_alt_1e(10000)
    Alernative_plot_color_Sierpinski(10000)