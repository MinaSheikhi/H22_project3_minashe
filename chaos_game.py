import numpy as np
import matplotlib.pyplot as plt

class ChaosGame:
    def __init__(self, n: int, r: float = 1/2)->None:
        """
        Constructor for ChaosGame
        Arguments:
            n(int):
                number of corners for the n-gon.
            r(float):
                ratio between two points.  
        """
        if isinstance(n, int) == False or isinstance(r, float) == False:
            raise TypeError()
        
        if n >= 3 and r > 0 and r < 1:
            self.n = n
            self.r = r

        else:
            raise ValueError()

        self._generate_ngon()

    def _generate_ngon(self) -> np.ndarray:
        """
        Generating corners of the n-gon.
        returns:
            np.ndarray:
                corner points
        """
        theta = np.linspace(0, 2*np.pi, self.n + 1)
        Corners = []

        for i in theta:
            Corners.append((np.sin(i), np.cos(i)))

        return np.array(Corners)

    def _starting_point(self)->np.ndarray:
        """
        Picking a random starting point within the n-gon.
        returns:
            np.ndarray:
                Starting point x0

        """
        corners = self._generate_ngon()
        weights = np.random.random(self.n)
        weights = weights/sum(weights)
        
        x0 = 0
        for i in range(self.n):
            x0 += corners[i] * weights[i]      
        return x0

    def iterate(self, steps: int = 10000, discard: int = 5)->np.ndarray:
        """
        Generating points from randomly picked corner, storing generated points and the indicies.
        Arguments:
            steps(int): 
                number of iterations
            discard(int):
                number of first values we want to ignore
        """
        corner = self._generate_ngon()
        x0 = self._starting_point()
        x_list = [x0]
        Indicies = [0]
        for i in range(steps-1):
            j = np.random.randint(low=0, high=self.n)
            x_list.append(self.r * x_list[i] + (1-self.r) * corner[j])
            Indicies.append(j)

        # Discarding starting points
        Indicies = Indicies[discard:]
        x_list = x_list[discard:]
        self.Indicies = np.array(Indicies)
        self.X = np.array(x_list)

    @property
    def gradient_color(self)->np.ndarray:
        """
        Defining colors for the plot by computing individual RGB color value for each point.
        return:
            np.ndarray:
                Array of the color values 
        """
        self.iterate()
        C = np.zeros(len(self.X))
        C[0] = self.Indicies[0]
        for i in range(len(self.X)-1):
            C[i+1] =(C[i] + self.Indicies[i+1])/2
        
        return C

    def plot_ngon(self)->None:
        """
        Plotting corner points of n-gon.
        """
    
        plt.figure()
        plt.scatter(*zip(*self._generate_ngon()), c='b')
        plt.show()

    def plot(self, color: bool =False, cmap: str ='rainbow')->None:
        """
        Plotting the generated points with a choice to have them colored or not.
        Arguments:
            color(bool):
                colored plot or not
            cmap(str):
                registered colormap name
        """
        self.iterate()

        if color == True:
            colors = self.gradient_color
        else:
            colors = 'black'
            
        
        plt.scatter(self.X[:,0], self.X[:,1], c=colors, cmap=cmap, s = .4, marker = '.') 
        plt.scatter(*zip(*self._generate_ngon()), c = 'b')  
        plt.axis('equal')
        plt.axis('off')
    
    def show(self, color: bool = False, cmap: str ='rainbow')->None:
        """
        Shows the plot.
        Arguments:
            color(bool):
                colored plot or not
            cmap(str):
                registered colormap name
        """
        self.plot(color, cmap=cmap)
        plt.show()


    def savepng(self, outfile: str, color: bool = False, cmap: str ='rainbow')->None:
        """
        Saves the plot.
        Arguments:
            outfile(str):
                Name we want the file to be saved as
            color(bool):
                colored plot or not
            cmap(str):
                registered colormap name
        """
        if '.png' not in outfile:
            outfile = outfile + '.png'
        self.plot(color, cmap=cmap)
        plt.savefig(outfile, dpi=300, transparent=False)
        plt.clf() #clears figure after each figure




if __name__ == "__main__":
    ''' Exercise 2b) 
    Tester om plot_ngon plotter figurer med n punkter og om de ser rimelig ut:
    figurene ser rimelige ut. n=3 gir trekant, n=4 gir firekant, n=5 gir femkant osv.
    Jo flere n, jo nærmere en sirkel kommer formen.'''

    for n in range(3, 9):
        figure = ChaosGame(n)
        figure.plot_ngon()


    '''Exercise 2c) 
    Genererer 1000 tilfeldig tall for å sjekke om startpunktet x0 er innenfor femkanten.'''

    pentagon = ChaosGame(5)
    for i in range(11): #1001
        x = pentagon._starting_point()
        plt.scatter(x[0], x[1], c = 'r')
        plt.scatter(*zip(*pentagon._generate_ngon()), c='b')

    plt.show()
    

    ''' Exercise 2e)''' 
    # Without color
    rectangle = ChaosGame(n=3, r=1/2)
    rectangle.show()
    
    # With color
    rectangle_color = ChaosGame(n=3, r=1/2)
    rectangle_color.show(color = True)

    '''Exercise 2i)'''

    threegon = ChaosGame(n=3, r=1/2)
    threegon.savepng("chaos1")

    fourgon = ChaosGame(n=4, r=1/3)
    fourgon.savepng("chaos2")

    fivegon = ChaosGame(n=5, r=1/3)
    fivegon.savepng("chaos3")

    five2gon = ChaosGame(n=5, r=3/8)
    five2gon.savepng("chaos4")

    sixgon = ChaosGame(n=6, r=1/3)
    sixgon.savepng("chaos5")
