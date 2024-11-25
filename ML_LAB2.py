import matplotlib.pyplot as plt
import numpy as np


def triangular_membership(x, a, b, c):
    #Функция для вычисления значения треугольной функции принадлежности
    if x <= a or x >= c:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x <= c:
        return (c - x) / (c - b)


def bmi_membership(bmi):
    #Функция для вычисления степени принадлежности индекса массы тела (BMI)
    categories = {
        "Недостаточный вес": (15, 35, 60),
        "Нормальный вес": (55, 65, 75),
        "Избыточный вес": (70, 80, 90),
        "Ожирение": (80, 90, 100),
    }
    memberships = {}
    for category, (a, b, c) in categories.items():
        memberships[category] = triangular_membership(bmi, a, b, c)
    return memberships


def activity_level_membership(activity_level):
    #Функция для вычисления степени принадлежности уровня физической активности
    categories = {
        "Малоподвижный": (0, 1, 2),
        "Умеренный": (1, 3, 4),
        "Активный": (3, 5, 6),
        "Очень активный": (5, 7, 10),
    }
    memberships = {}
    for category, (a, b, c) in categories.items():
        memberships[category] = triangular_membership(activity_level, a, b, c)
    return memberships


def plot_membership(x_vals, categories, membership_func, title):
    #Функция для построения графиков функции принадлежности
    # Вычисление значений функции принадлежности для всех категорий
    membership_values = {category: [membership_func(x, *params) for x in x_vals]
                         for category, params in categories.items()}

    # Создаем графики
    plt.figure(figsize=(10, 6))

    # Отображаем функции принадлежности
    for category, values in membership_values.items():
        plt.plot(x_vals, values, label=category)

    plt.title(f'{title} - Функции принадлежности')
    plt.xlabel('Значение')
    plt.ylabel('Степень принадлежности')
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    # Ввод данных от пользователя
    bmi = float(input("Введите индекс массы тела (BMI): "))
    activity_level = float(input("Введите уровень физической активности (0-10): "))

    # Диапазоны значений для построения графиков
    bmi_vals = np.linspace(10, 100, 400)
    activity_vals = np.linspace(0, 10, 400)

    # Определение категорий для BMI и уровня активности
    bmi_categories = {
        "Недостаточный вес": (15, 35, 60),
        "Нормальный вес": (55, 65, 75),
        "Избыточный вес": (70, 80, 90),
        "Ожирение": (80, 90, 100),
    }

    activity_categories = {
        "Малоподвижный": (0, 1, 2),
        "Умеренный": (1, 3, 4),
        "Активный": (3, 5, 6),
        "Очень активный": (5, 7, 10),
    }

    # Построение графиков для BMI и уровня физической активности
    plot_membership(bmi_vals, bmi_categories, triangular_membership, 'Индекс массы тела (BMI)')
    plot_membership(activity_vals, activity_categories, triangular_membership, 'Уровень физической активности')


if __name__ == "__main__":
    main()
