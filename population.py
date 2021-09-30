from dna import dna


import random







class population:
    def __init__(self , blurry_image , real_image , pop_size , m) :
        self.blurry_image = blurry_image
        self.real_image = real_image
        self.mating_pool = []
        self.generations = 0
        self.finished = False
        self.mutation_rate = m
        self.perfect_score = 1
        self.best = []
        
        self.population = []
        for i in range(pop_size):
            self.population.append(dna(self.blurry_image , self.real_image))

        self.calc_fitness()


        
    def calc_fitness(self):
        for i in range(len(self.population)):
            self.population[i].calc_fitness() 



    def natural_selection(self):
        self.mating_pool = []
        max_fitness = 0
        min_fitness = 10000000000
        for i in range(len(self.population)):
            if(self.population[i].fitness > max_fitness):
                max_fitness = self.population[i].fitness
            if(self.population[i].fitness < min_fitness):
                min_fitness = self.population[i].fitness


        for j in range(len(self.population)):
            n = int((self.population[j].get_fitness() - min_fitness)*10000000000000)
            #print(n)
            for k in range(n):
                self.mating_pool.append(self.population[j])


    def generate(self):
        for i in range(len(self.population)):
            a =  random.randint(0,len(self.mating_pool)-1)
            b =  random.randint(0,len(self.mating_pool)-1)
            partner_a = self.mating_pool[a]
            partner_b = self.mating_pool[b]
            child = partner_a.crossover(partner_b)
            child.mutate(self.mutation_rate)
            self.population[i] = child
        self.generations += 1

    def evaluate(self):
        world_record = 0
        index = 0
        for i in range(len(self.population)):
            if(self.population[i].fitness > world_record):
                world_record = self.population[i].fitness
                index = i

        self.best = self.population[index]
        if(self.best == self.perfect_score):
            self.finished == True

    def is_finished(self):
        return self.finished

    def get_generations(self):
        return self.generations

    def get_best(self):
        return self.best

    






#blurred_image = all_blurry_train[0][400 : 800 , 400:800] 
#realed_image = all_real_train[0][400 : 800 , 400:800] 

#pop = population(blurred_image , realed_image , 10 , 0.5)


#pop.calc_fitness()
#for i in range(len(pop.population)):
    #print(pop.population[i].fitness)

