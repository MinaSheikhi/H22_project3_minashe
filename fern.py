import numpy as np
import matplotlib.pyplot as plt

class AffineTransform:
    def __init__(self, a: int = 0, b: int = 0, c: int = 0, d: int = 0, e: int = 0, f: int = 0)->None:  
        """
        AffineTransform constructor.
        Arguments:
            a,b,c,d,e,f (int): 
                free parameters
        """
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f

    def __call__(self, x: int, y: int)-> list:
        """
        Arguments:
            x(int):
                x value of the point
            y(int):
                y value of the point
        Returns:
            list:
                point resulting from transformation f(x,y)
        """
        x = self.a*x + self.b*y + self.e
        y = self.c*x + self.d*y + self.f
        return [x, y]




if __name__ == "__main__":
    
    f1 = AffineTransform(d=0.16)
    f2 = AffineTransform(a=0.85, b=0.04, c=-0.04, d=0.85, f=1.60)
    f3 = AffineTransform(a=0.2, b=-0.26, c=0.23, d=0.22, f=1.6)
    f4 = AffineTransform(a=-0.15, b=0.28, c=0.26, d=0.24, f=0.44)

    def non_uniform(x:int , y:int)-> AffineTransform:

        """
        Picking one of four functions at random given probabilities for each function.
        Arguments:
            x(int):
                 x value of the point
            y(int):
                y value of the point
        Returns:
            AffineTransform:
                Transformed point
        """

        functions = np.array([f1, f2, f3, f4])
        p_functions = np.array([0.01, 0.85, 0.07, 0.07])
        assert(np.sum(p_functions) == 1)

        p_cumulative = np.cumsum(p_functions, axis = 0) # cumulative sum of the probabilities.
        
        #Check that probabilities sums up to 1

        #picking one of 4 probabilities at random
        # r is the random point. interval: [0,1)
        r = np.random.random()
        for j, p in enumerate(p_cumulative):
            if r < p:
                return functions[j](x,y)

    def iterating(x0: int = 0, y0: int = 0, N: int = 50000)-> np.ndarray:
        """
        Iterating new points by picking one of four functions randomly according
        to their probability.
        Arguments:
            x0(int):
                x value of startpoint
            y0(int):
                y value of Startpoint
            N(int):
                Number of iterations
        returns:
            np.ndarray:
                list of generated points.
        """
        x_list = np.zeros((N, 2))
        x_list[0] = [x0, y0]
        for i in range(N-1):
            x_list[i+1] = non_uniform(x_list[i][0], x_list[i][1])
        return x_list

    def plot()->None:
        """
        Plotting the the generated points.
        """
        x_list = iterating()
        plt.scatter(*zip(*x_list), c='forestgreen', s=0.1)
        plt.axis('equal')
        plt.axis('off')

    def savepng(outfile: str)->None:
        """
        Saving the plot to a file.
        Arguments:
            outfile(str):
                Chosen name to the file.
        """
        if '.png' not in outfile:
            outfile + '.png'
        plot()
        plt.savefig(outfile, dpi=300, transparent=False)
        plt.clf()
    
    savepng('barnsley_fern.png')
    