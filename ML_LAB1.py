import numpy as np
import random
import matplotlib.pyplot as plt
from itertools import permutations

# Параметры
n = 7  # Количество пунктов производства
k = 3  # Количество городов
p_crossover = 0.8  # вероятность скрещивания (не используется)
p_mutation = 0.2  # вероятность мутации индивидуума
max_products_per_city = 100  # Максимум продуктов на город
max_products_per_factory = 150  # Максимум продуктов на фабрику

# Генерация случайных данных
np.random.seed(42)  # Для воспроизводимости
factories = np.random.randint(50, max_products_per_factory, n)
cities = np.random.randint(50, max_products_per_city, k)

# Расстояния между фабриками и городами (в километрах)
distances = np.random.rand(n, k) * 10  # случайные расстояния от 0 до 10 км

print("Фабрики:", factories)
print("Города:", cities)
print("Расстояния:\n", distances)


# Полный перебор
def total_cost(route):
    cost = 0
    for i, city in enumerate(route):
        cost += distances[i][city] * factories[i]
    return cost


def exhaustive_search():
    best_cost = float('inf')
    best_route = None
    for perm in permutations(range(k)):
        current_cost = total_cost(perm)
        if current_cost < best_cost:
            best_cost = current_cost
            best_route = perm
    return best_route, best_cost


best_route, best_cost = exhaustive_search()
print("Лучший маршрут (полный перебор):", best_route)
print("Стоимость:", best_cost)


# Генетический алгоритм с методами мутации.
class Individual:
    def __init__(self, factories, cities):
        self.route = self.create_route(len(cities))
        self.fitness = self.calculate_fitness(factories, cities)

    def create_route(self, length):
        return random.sample(range(length), length)

    def calculate_fitness(self, factories, cities):
        total_cost = sum(distances[f][c] * factories[f] for f, c in enumerate(self.route))
        return total_cost


# Функции мутации
def mutate_swap(individual):
    idx1, idx2 = random.sample(range(len(individual.route)), 2)
    individual.route[idx1], individual.route[idx2] = individual.route[idx2], individual.route[idx1]
    individual.fitness = individual.calculate_fitness(factories, cities)


def mutate_random(individual):
    index = random.randint(0, len(individual.route) - 1)
    individual.route[index] = random.randint(0, len(cities) - 1)
    individual.fitness = individual.calculate_fitness(factories, cities)


def mutate_shift(individual):
    start = random.randint(0, len(individual.route) - 1)
    end = random.randint(start + 1, len(individual.route))
    segment = individual.route[start:end]
    position = random.randint(0, len(individual.route) - len(segment))
    individual.route = individual.route[:position] + segment + individual.route[position:]
    individual.fitness = individual.calculate_fitness(factories, cities)


def genetic_algorithm(population_size=100, generations=500):
    mutation_methods = ['swap', 'random', 'shift']

    fitness_results_avg = {m: [] for m in mutation_methods}
    fitness_results_max = {m: [] for m in mutation_methods}

    for mutation_method in mutation_methods:
        population = [Individual(factories, cities) for _ in range(population_size)]
        for generation in range(generations):
            population.sort(key=lambda x: x.fitness)
            new_population = population[:population_size // 2]

            while len(new_population) < population_size:
                parent1, parent2 = random.sample(new_population[:20], 2)

                # Поскольку мы не используем методы скрещивания,
                # просто создаем новые индивиды.
                child1 = Individual(factories, cities)
                child2 = Individual(factories, cities)

                if random.random() < p_mutation:
                    if mutation_method == 'swap':
                        mutate_swap(child1)
                        mutate_swap(child2)
                    elif mutation_method == 'random':
                        mutate_random(child1)
                        mutate_random(child2)
                    elif mutation_method == 'shift':
                        mutate_shift(child1)
                        mutate_shift(child2)

                new_population.extend([child1, child2])

            population = new_population

            avg_fitness = np.mean([ind.fitness for ind in population])
            max_fitness = min(ind.fitness for ind in population)  # Минимальная стоимость (лучший фитнес)

            fitness_results_avg[mutation_method].append(avg_fitness)
            fitness_results_max[mutation_method].append(max_fitness)

        best_individual_genetic = min(population, key=lambda x: x.fitness)

        print(f"Лучший маршрут (генетический алгоритм) с методом {mutation_method}: {best_individual_genetic.route}")
        print(f"Стоимость: {best_individual_genetic.fitness}")

    return fitness_results_avg, fitness_results_max


fitness_results_avg_genetic_algorithm, fitness_results_max_genetic_algorithm = genetic_algorithm()

# Визуализация результатов только для методов мутации
plt.figure(figsize=(15, 8))

# Отображение только для методов мутации
for mutation_method in ['swap', 'random', 'shift']:
    plt.plot(range(len(fitness_results_avg_genetic_algorithm[mutation_method])),
             fitness_results_avg_genetic_algorithm[mutation_method],
             label=f'Avg {mutation_method}')

    plt.plot(range(len(fitness_results_max_genetic_algorithm[mutation_method])),
             fitness_results_max_genetic_algorithm[mutation_method],
             label=f'Max {mutation_method}', linestyle='--')

plt.xlabel('Поколения')
plt.ylabel('Фитнес')
plt.title('Динамика фитнеса для методов мутации')

# Установка пределов осей
plt.xlim(0, 30)  # Ограничение по оси X
plt.ylim(1100, )  # Ограничение по оси Y (от нуля до максимума фитнеса)

plt.legend(title='Методы мутации')  # Заголовок для легенды
plt.show()
