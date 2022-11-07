import numpy as np
import matplotlib.pyplot as plt
from chaos_game import ChaosGame


class Variations:
    def __init__(self, x: np.ndarray, y: np.ndarray, name: float)-> None:
        """
        Constructor for Variation
        Arguments:
            x (np.ndarray):
                x values
            y (np.ndarray):
                y values
            name (float):
                name of the variation
        """
        self.x = x
        self.y = y
        self.name = name
        self._func = getattr(Variations, name)
        
    @staticmethod
    def linear(x: np.ndarray, y: np.ndarray)->np.ndarray:
        """
        Linear transformation
        Arguments:
            x (np.ndarray):
                x values
            y (np.ndarray):
                y values
        returns:
            np.ndarray:
                New x and y values
        """
        return x, y

    @staticmethod
    def handkerchief(x: np.ndarray, y: np.ndarray)->np.ndarray:
        """
        Handkerchief transformation
        Arguments:
            x (np.ndarray):
                x values
            y (np.ndarray):
                y values
            returns:
                np.ndarray:
                    New x and y values
        """
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(x, y)
        return r*np.sin(theta + r), r*np.cos(theta - r)

    @staticmethod
    def swirl(x: np.ndarray, y: np.ndarray)->np.ndarray:
        """
        Swirl transformation
        Arguments:
            x (np.ndarray):
                x values
            y (np.ndarray):
                y values
            returns:
                np.ndarray:
                    New x and y values
        """
        r = np.sqrt(x**2 + y**2)
        return x*np.sin(r**2) - y*np.cos(r**2), x*np.cos(r**2) + y*np.sin(r**2)

    @staticmethod
    def disc(x: np.ndarray, y: np.ndarray)->np.ndarray:
        """
        Disc transformation
        Arguments:
            x (np.ndarray):
                x values
            y (np.ndarray):
                y values
            returns:
                np.ndarray:
                    New x and y values
        """
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(x, y)
        return theta/np.pi * np.sin(np.pi*r), theta/np.pi * np.cos(np.pi*r)

    @staticmethod
    def diamond(x: np.ndarray, y: np.ndarray)->np.ndarray:
        """
        Diamond transformation
        Arguments:
            x (np.ndarray):
                x values
            y (np.ndarray):
                y values
            returns:
                np.ndarray:
                    New x and y values
        """
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(x, y)
        return np.sin(theta)*np.cos(r), np.cos(theta)*np.sin(r)

    @staticmethod
    def power(x: np.ndarray, y: np.ndarray)->np.ndarray:
        """
        Power transformation
        Arguments:
            x (np.ndarray):
                x values
            y (np.ndarray):
                y values
            returns:
                np.ndarray:
                    New x and y values
        """
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(x, y)
        return r**np.sin(theta)*np.cos(theta), r**np.sin(theta)*np.sin(theta)
        

    def transform(self)-> np.ndarray:
        """
        Transforms the coordinates.
        return:
            np.ndarray:
                transformed x and y values.
        """

        x_new, y_new = self._func(self.x, self.y)
        return x_new, y_new

    @classmethod
    def from_chaos_game(cls, instance: ChaosGame, name: float):
        """
        Generating ChaosGame object to Variation.
        Arguments:
            instance(ChaosGame):
                instances of ChaosGame
            name(float):
                Name of the transformation chosen 
        """
        x = instance.X
        return cls(x[:,0], -x[:,1], name) 


if __name__=="__main__":

    #Exercise 4b)
    grid_values = np.linspace(-1, 1, 100)
    x, y = np.meshgrid(grid_values, grid_values)
    x_values = x.flatten()
    y_values = y.flatten()
    transformations = ["linear", "handkerchief", "swirl", "disc"]
    variations = [Variations(x_values, y_values, version) for version in transformations]
    fig, axs = plt.subplots(2, 2, figsize=(9, 9))
    for i, (ax, variation) in enumerate(zip(axs.flatten(), variations)):
        u, v = variation.transform()
        ax.plot(u, -v, markersize=1, marker=".", linestyle="", color="black")
        ax.scatter(u, -v, s=0.2, marker=".", color="black")
        ax.set_title(variation.name)
        ax.axis("off")
    fig.savefig("figures/variations_4b.png")

    #Exercise 4c)
    fig, axs = plt.subplots(2, 2, figsize=(9, 9))
    n_gons = ChaosGame(4, 0.3)
    n_gons.iterate()
    n_color = n_gons.gradient_color
    transformations = ["linear", "handkerchief", "swirl", "disc"]


    for i, (ax, variation) in enumerate(zip(axs.flatten(), transformations)):
        var = Variations.from_chaos_game(n_gons, variation)
        u, v = var.transform()
        ax.scatter(u, -v, s=0.2, marker=".", c=n_color)
        ax.set_title(var.name)
        ax.axis("off")
    #plt.show()

    #Exercise 4d)
    def linear_combination_wrap(V1: Variations, V2: Variations)-> tuple:
        """
        Arguments:
            V1(Variations):
                First variation
            V2(Variations):
                Second variation
        returns:
            tuple:
                weighted linear combination of the two variations.
        """
        
        u1, v1 = V1.transform()
        u2, v2 = V2.transform()
        return lambda w: (w*u1 + (1-w)*u2, w*v1 + (1-w)*v2)


    coeffs = np.linspace(0, 1, 4)
    
    variation1 = Variations.from_chaos_game(n_gons, "linear")
    variation2 = Variations.from_chaos_game(n_gons, "disc")

    variation12 = linear_combination_wrap(variation1, variation2)    
        
    fig, axs = plt.subplots(2, 2, figsize=(9, 9))
    for ax, w in zip(axs.flatten(), coeffs):
        u, v = variation12(w)
    
        ax.scatter(u, -v, s=0.2, marker=".", c=n_color)
        ax.set_title(f"weight = {w:.2f}")
        ax.axis("off")
    plt.show()


