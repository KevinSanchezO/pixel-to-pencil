import random
from genetic import Genetic
import numpy as np
import time
import matplotlib.pyplot as plt
import io

class GeneticAlgorithm:
    def __init__(self, population_size, genes_sizeX, genes_sizeY, objective, noChange, parents, max_generation, mutation, crossover_num, color_obtainer, with_pallete, queue):
        self.first_gen = Genetic()             #esta clase se encarga de procesar las imagenes random iniciales
        self.color_obtainer = color_obtainer   #paleta de colores
        self.withPallete = with_pallete        #permite usar o no la paleta de colores de la imagen
        self.population_size = population_size #tamaño de poblacion
        self.genes_sizeX = genes_sizeX         #tamaño horizontal de la imagen
        self.genes_sizeY = genes_sizeY         #tamaño vertical de la imagen  
        self.objective = objective             #imagen objetivo  Matriz pixeles
        self.population = []                   #Poblacion de la generacion [Matrizpixeles, Matrizpixeeles, ...]
        self.populationFitness = []            #Fitness de cada individuo de la poblacion, el numero %  [ 1, 2, 3, ..., 0.5 ]
        self.populationFitnessNoChange = []     #Fitnes de cada individuo que no sirve cambiar, la matriz tendrá true cuando el gen es el indicado y false si no [[true, false, false,..], [true,false,...],...]
        self.alpha_male = 0                    #Mejor Fitness de la población actual indice del macho alfa
        self.generation = 1                    #Numero de generación
        self.noChange = noChange               #será un boleano diciendo si es permitido o no el cambio de los genes iguales al objetivo en cada individuo
        self.parents = parents                 #cantidad de padres a seleccionar
        self.max_generation = max_generation   #generaciones máximas
        self.mutation_percent = mutation       #porcentaje de mutación de los individuos
        self.crossovernum = crossover_num      #indica la cantidad de individuos que se cruzan
        self.best = []                         #mejor individuo de cada generacion, imagen
        self.bestFitness = []                  #fitness del mejor de cada generacion, cada uno de acuerdo al indice de best
        self.queue = queue                     #Queue de tareas para poder ser utilizadas en el hilo de la interfaz
        self.average_fitness = []              #Lista del promedio de fitness de cada generacion
        self.completed = False

    #Funcion encargada de inicializar las poblaciones en imagenes random e imagenes blancas
    def population_init(self):
        # print("x, y:")
        # print(self.genes_sizeY)
        # print(self.genes_sizeX) #correctas dimensiones
       # for _ in range((self.population_size//2)):
           # self.population  += [self.first_gen.draw_blank_image(self.genes_sizeX, self.genes_sizeY)]
        for _ in range((self.population_size)):
            if(self.withPallete):
                self.population += [self.first_gen.draw_image_pallete(self.genes_sizeX, self.genes_sizeY, self.color_obtainer)]
            else:
                self.population += [self.first_gen.draw_image(self.genes_sizeX, self.genes_sizeY)]
        if(self.noChange):
            self.populationFitnessNoChange = self.create_false_matriz()

    #Agrega el fitnes de cada individuo evaluandolo con el objetivo, tiene en cuenta si se quiere cambiar o no el pixel
    def fitness_calculation_No_Change(self):  #esta se usará para el fitnes cuando la opcion no change esté en true
        for i in range(len(self.population)-1): #por cada individuo de la poblacion
            fitness = 0     #guardará la cantidad de pixeles similares al del objetivo
            for j in range(self.genes_sizeY): #por cada fila de la matriz individuo 
                for k in range(self.genes_sizeX): #por cada columna de la fila de la matriz del individuo
                    if(not self.populationFitnessNoChange[i][j][k]): #si el individuo i de la poblacion en su lista de no cambiar en la pocisión [j][k] es falso, se permite preguntar, sino ya se sabe que es bueno el pixel
                        if((self.population[i][j][k] == self.objective[j][k]).all()):   #si el individuo i en la posicion [j][k] tiene el mismo pixel que el objetivo en la posición [j][k] siga
                            fitness += 1   #se le suma un 1 al fitness
                            self.populationFitnessNoChange[i][j][k] = True   #se cambia el estado de false a true para que no se vueva a cambiar
                    else:
                        fitness += 1
            self.populationFitness += [(fitness/(self.genes_sizeX * self.genes_sizeY))*100] #se agrega el fitness del individuo
                        
    #Agrega el fitnes de cada individuo evaluandolo con el objetivo
    def fitness_calculation(self):  #esta se usará para el fitnes cuando la opcion no change esté en true
        for i in range(len(self.population)-1): #por cada individuo de la poblacion
            fitness = 0     #guardará la cantidad de pixeles similares al del objetivo
            for j in range(self.genes_sizeY): #por cada fila de la matriz individuo 
                for k in range(self.genes_sizeX): #por cada columna de la fila de la matriz del individuo
                    if((self.population[i][j][k] == self.objective[j][k]).all()):   #si el individuo i en la posicion [j][k] tiene el mismo pixel que el objetivo en la posición [j][k] siga
                        fitness += 1   #se le suma un 1 al fitness
            self.populationFitness += [(fitness/(self.genes_sizeX * self.genes_sizeY))*100] #se agrega el fitness del individuo a populationFitness en la posicion i


    def select_parents(self):
        best_individuals = self.obtain_best_individuals(self.populationFitness, self.parents)
        self.alpha_male = best_individuals[0] #me da la posición cero de los mejores individuos, osea el mayor de los fitness
        return best_individuals[1:]

    #Cruza de forma random los genes //aqui no aplica el nochange
    def crossoverRow(self, parent1, parent2):
        child = []
        for i in range(self.genes_sizeY):
            genoma = []
            numero_aleatorio = random.randint(0, 2 - 1)
            if(numero_aleatorio):
                genoma = parent1[i]
            else:
                genoma = parent2[i]
            child += [genoma]
        return child

    #Cruza de forma random los genes //aqui no aplica el nochange
    def crossover(self, parent1, parent2):
        child = []
        for i in range(self.genes_sizeY):
            genoma = []
            for j in range(self.genes_sizeX):
                gen = []
                numero_aleatorio = random.randint(0, 2 - 1)
                if(numero_aleatorio):
                    gen = parent1[i][j]
                else:
                    gen = parent2[i][j]
                genoma += [gen]
            child += [genoma]
        return child
    
    #Cruza de forma random los genes y da la posibilidad de mutar 33% pixel por pixel  //aqui no aplica el nochange
    def crossoverIfMute(self, parent1, parent2):
        child = []
        for i in range(self.genes_sizeY):
            genoma = []
            for j in range(self.genes_sizeX):
                gen = []
                numero_aleatorio = random.randint(0, 3 - 1)
                if(numero_aleatorio == 1):
                    gen = parent1[i][j]
                elif(numero_aleatorio == 0):
                    gen = parent2[i][j]
                else:
                    if(self.withPallete):
                        gen = np.array(random.choice(self.color_obtainer))
                    else:
                        gen = [random.randint(0, 255) for _ in range(3)]
                genoma += [gen]
            child += [genoma]
        return child
        
    #Cruza de forma random los genes y da la posibilidad de mutar 33% fila por fila
    def crossoverIfMuteRow(self, parent1, parent2):
        child = []
        for i in range(self.genes_sizeY):
            genoma = []
            numero_aleatorio = random.randint(0, 3 - 1)
            if(numero_aleatorio == 1):
                genoma = parent1[i]
            elif(numero_aleatorio == 0):
                genoma = parent2[i]
            else:
                for _ in range(self.genes_sizeX):
                    if(self.withPallete):
                        gen = np.array(random.choice(self.color_obtainer))
                    else:
                        gen = [random.randint(0, 255) for _ in range(3)]
                    genoma += [gen]
            child += [genoma]
        return child
    
    #cruce si aplica el no change pixel por pixel y con mutación
    def crossoverIfMuteNoChange(self, parent1, parent2, parent1NoChange, parent2NoChange):
        child = []
        for i in range(self.genes_sizeY):
            genoma = []
            for j in range(self.genes_sizeX):
                gen = []
                if(parent1NoChange[i][j]):
                    gen = parent1[i][j]
                elif(parent2NoChange[i][j]):
                    gen = parent2[i][j]
                else:
                    if(self.withPallete):
                        gen = np.array(random.choice(self.color_obtainer))
                    else:
                        gen = [random.randint(0, 255) for _ in range(3)]
                genoma += [gen]
            child += [genoma]
        return child
    
    #cruce si aplica el no change pixel por pixel y sin mutación
    def crossoverNoChange(self, parent1, parent2, parent1NoChange):
        child = []
        for i in range(self.genes_sizeY):
            genoma = []
            for j in range(self.genes_sizeX):
                gen = []
                if(parent1NoChange[i][j]):
                    gen = parent1[i][j]
                else:
                    gen = parent2[i][j]
                genoma += [gen]
            child += [genoma]
        return child
    
    #Existen 6 crossOver
        #4 para cuando hay posibilidad de cambiar valores que ya sirven
            #2 cambian filas y 2 cambian pixel por pixel, 2 admiten mutar y 2 solo admiten los genes de los padres
        #2 para cuando no se pueden cambiar valores que ya siven, es decir que el pixel hace match con el pixel del objetivo

    def evolve(self):
        new_generation = []
        parents = self.select_parents()
        best = self.population[self.alpha_male]
        bestFit = round(self.populationFitness[self.alpha_male], 5)
        
        average = sum(self.populationFitness)
        self.average_fitness += [average / len(self.populationFitness)]
        
        for _ in range(self.population_size):
            mutation = random.randint(0, 100 - 1) #indica un numero aleatorio del 0 al 100 para definir la mutacion
            parent2 = random.randint(0, len(parents) - 1) #numero aleatorio del padre 2
            child = []
            if(self.noChange):
                if(mutation >= (100 - self.mutation_percent)):
                    #aca lo que hace es que crea un hijo con el alfa y con el padre 2 que saca de la lista de los mejores padres segun el numero aleatorio,
                    #le envia la matriz de genes de ambos padres y la matris de genes que cambian o no del alfa y del padre 2
                    child = self.crossoverIfMuteNoChange(self.population[self.alpha_male], self.population[parents[parent2]], self.populationFitnessNoChange[self.alpha_male], self.populationFitnessNoChange[parents[parent2]])
                else:
                    child = self.crossoverNoChange(self.population[self.alpha_male], self.population[parents[parent2]], self.populationFitnessNoChange[self.alpha_male])
            else:
                if(mutation >= (100 - self.mutation_percent)): #si muta
                    mutation2 = random.randint(0, 100 - 1) #buscamos cual metodo de mutacion
                    if (mutation2 < 98):   #si es el 1
                        child = self.crossoverIfMute(self.population[self.alpha_male], self.population[parents[parent2]]) #posibilidad de mutar las filas
                    else: #solo un 2% para esta mutación brusca
                        child = self.crossoverIfMute(self.population[self.alpha_male], self.population[parents[parent2]]) #posibilidad de mutar pixel por pixel
                else:
                    crossoverNormal = random.randint(0, 2 - 1) #buscamos cual metodo de mutacion
                    if(crossoverNormal):
                        child = self.crossover(self.population[self.alpha_male], self.population[parents[parent2]]) #no muta ningun pixel
                    else:
                        child = self.crossoverRow(self.population[self.alpha_male], self.population[parents[parent2]])
            if(self.crossovernum != 2):  #aqui aparea nuevamente el child dependiendo de cuantos individuo desee aparear 
                for _ in range(self.crossovernum - 2):
                    parent3 = random.randint(0, len(parents) - 1) #numero aleatorio del padre 3
                    if(self.noChange):
                        if(mutation >= (100 - self.mutation_percent)):
                            #aca lo que hace es que crea un hijo con el alfa y con el padre 2 que saca de la lista de los mejores padres segun el numero aleatorio,
                            #le envia la matriz de genes de ambos padres y la matris de genes que cambian o no del alfa y del padre 2
                            child = self.crossoverIfMuteNoChange(self.population[self.alpha_male], self.population[parents[parent3]], self.populationFitnessNoChange[self.alpha_male], self.populationFitnessNoChange[parents[parent3]])
                        else:
                            child = self.crossoverNoChange(self.population[self.alpha_male], child, self.populationFitnessNoChange[self.alpha_male])
                    else:
                        if(mutation >= (100 - self.mutation_percent)): #si muta
                            mutation2 = random.randint(0, 2 - 1) #buscamos cual metodo de mutacion
                            if (mutation2):   #si es el 1
                                child = self.crossoverIfMuteRow(child, self.population[parents[parent3]]) #posibilidad de mutar las filas
                            else:
                                child = self.crossoverIfMute(child, self.population[parents[parent3]]) #posibilidad de mutar pixel por pixel
                        else:
                            crossoverNormal = random.randint(0, 2 - 1) #buscamos cual metodo de mutacion
                            if(crossoverNormal):
                                child = self.crossover(child, self.population[parents[parent3]]) #no muta ningun pixel
                            else:
                                child = self.crossoverRow(child, self.population[parents[parent3]])
            new_generation += [child]
        self.population = new_generation
        self.populationFitness = []
        if(self.noChange):
            self.populationFitnessNoChange = self.create_false_matriz()
        self.generation += 1
        self.bestFitness += [bestFit]
        self.best += [best]

    def execute_genetic_algorithm(self):
        self.population_init()
        for _ in range(self.max_generation):
             if(self.noChange):
                 self.fitness_calculation_No_Change()
             else:
                 self.fitness_calculation()
             self.evolve()
             
             print(self.generation)
             print(self.bestFitness[-1])

             graphic_image = self.generate_graphic()

             atributes = {'gen_actual': self.generation, 'fitness': self.bestFitness, "mejor_individuo": self.best, 'grafico': graphic_image}

             self.queue.put(atributes)
             if(self.bestFitness[-1] >= 100):
                 self.completed = True
                 return
             time.sleep(1)


    def generate_graphic(self):
        fig, ax = plt.subplots(figsize=(5, 3))
        ancho_barras = 0.10
        
        x = range(len(self.average_fitness))
        ax.bar(x, self.average_fitness, width=ancho_barras, label='Promedio', align='center')
        
        x_mejores = [i + ancho_barras for i in x]
        ax.bar(x_mejores, self.bestFitness, width=ancho_barras, label='Mejor Porcentaje', align='center')

        ax.set_xticks([i + ancho_barras / 2 for i in x])

        temporadas = list(range(1, self.generation))

        ax.set_xticklabels(temporadas)

        ax.set_xlabel('Generaciones')
        ax.set_ylabel('Porcentajes')
        ax.set_title('Promedios y Mejores Porcentajes por Generacion')
        ax.legend()
        plt.tight_layout()
        
        # Guardar la figura en un objeto BytesIO
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        
        # Limpiar la figura para liberar memoria
        plt.close(fig)
        
        # Devolver el objeto BytesIO
        return buffer

    def obtain_best_individuals(self, array_ind, ammount_best):
        # if not array_ind or ammount_best == 0:
        #     return []
        res = []
        for i, value in enumerate(array_ind):
            for j in range(len(res)):
                if value > array_ind[res[j]]:
                    res.insert(j, i)
                    break
            res.append(i)
            res = res[:ammount_best]
        return res
    
    def create_false_matriz(self):
        result = []
        for _ in range(self.population_size):
            matriz = [[False for _ in range(self.genes_sizeX)] for _ in range(self.genes_sizeY)]
            result += [matriz]
        return result
    

