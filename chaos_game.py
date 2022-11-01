from re import T
import numpy as np
import matplotlib.pyplot as plt

class ChaosGame:
    def __init__(self, n: int, r: float = 1/2)->None:

        if isinstance(n, int) == False or isinstance(r, float) == False:
            raise TypeError()
        
        if n >= 3 and r > 0 and r < 1:
            self.n = n
            self.r = r

        else:
            raise ValueError()

        self._generate_ngon()

    def _generate_ngon(self) -> np.ndarray:
        theta = np.linspace(0, 2*np.pi, self.n + 1)
        Corners = []

        for i in theta:
            Corners.append((np.sin(i), np.cos(i)))

        return np.array(Corners)

    def _starting_point(self)->int:
        corners = self._generate_ngon()
        weights = np.random.random(self.n)
        weights = weights/sum(weights)
        
        x0 = 0
        for i in range(self.n):
            x0 += corners[i] * weights[i]      
        return x0

    def iterate(self, steps: int = 10000, discard: int = 5)->np.ndarray:
        corner = self._generate_ngon()
        x0 = self._starting_point()
        x_list = [x0]
        Indicies = [0]
        for i in range(steps-1):
            j = np.random.randint(low=0, high=self.n+1)
            x_list.append(self.r * x_list[i] + (1-self.r) * corner[j])
            Indicies.append(j)

        # Discarding starting points
        Indicies = Indicies[discard:]
        x_list = x_list[discard:]
        return np.array(x_list), np.array(Indicies)

    @property
    def gradient_color(self, steps: int = 10000, discard: int = 5)->np.ndarray:

        C = np.zeros((steps,3)) # C is the color values 
        C[0] = (0,0,0)

        r0 = np.array([1,0,0]) #red
        r1 = np.array([0,1,0]) #green
        r2 = np.array([0,0,1]) #blue
        r = [r0, r1, r2]

        for i in range(steps-1):
            j = np.random.randint(3)
            C[i+1] = (C[i] + r[j])/2
        
        return C[discard:]

    def plot_ngon(self)->None:
    
        plt.figure()
        plt.scatter(*zip(*self._generate_ngon()), c='b')
        plt.show()

    def plot(self, color=False, cmap='rainbow')->None:
        
        x_list = self.iterate()[0]

        if color == True:
            colors = self.gradient_color
        else:
            colors = 'black'
            
        
        plt.scatter(x_list[:,0], x_list[:,1], c=colors, cmap=cmap, s = 0.4, marker = '.') 
        plt.scatter(*zip(*self._generate_ngon()), c = 'b')  
        plt.axis('equal')
        plt.axis('off')
    
    def show(self, color = False, cmap='rainbow')->None:
        self.plot(color, cmap=cmap)
        plt.show()


    def savepng(self, outfile, color=False, cmap='rainbow')->None:

        if '.png' not in outfile:
            outfile = outfile + '.png'

        self.plot(color, cmap=cmap)
        plt.savefig(outfile, dpi=300, transparent=True)




if __name__ == "__main__":
    ''' Exercise 2b) 
    Tester om plot_ngon plotter figurer med n punkter og om de ser rimelig ut:
    figurene ser rimelige ut. n=3 gir trekant, n=4 gir firekant, n=5 gir femkant osv.
    Jo flere n, jo nærmere en sirkel kommer formen.

    for n in range(3, 9):
        figure = ChaosGame(n)
        figure.plot_ngon()
    '''

    '''Exercise 2c) 
    Genererer 1000 tilfeldig tall for å sjekke om startpunktet x0 er innenfor femkanten.

    pentagon = ChaosGame(5)
    for i in range(11): #1001
        x = pentagon._starting_point()
        plt.scatter(x[0], x[1], c = 'r')
        plt.scatter(*zip(*pentagon._generate_ngon()), c='b')

    plt.show()
    '''

    ''' Exercise 2e) '''
    # Without color
    rectangle = ChaosGame(n=3, r=1/2)
    rectangle.show()
    
    # With color
    rectangle_color = ChaosGame(n=3, r=1/2)
    rectangle_color.show(color = True)

        
