# Практична робота 1 -
# Написати генератор, що видає всі можливі комбінації елементів заданого списку.
from itertools import combinations


def generate_combinations(elements):
    result = []
    n = len(elements)
    for r in range(1, n + 1):
        indices = list(range(r))
        while True:
            result.append(tuple(elements[i] for i in indices))
            for i in reversed(range(r)):
                if indices[i] != i + n - r:
                    break
            else:
                break
            indices[i] += 1
            for j in range(i + 1, r):
                indices[j] = indices[j - 1] + 1
    return result

def test_gen_combinations(data: list):
    print(f'\ninput list: {data}')

    print(f'\nself made func:')
    for combination in generate_combinations(data):
        print(combination)

    print(f'\nstandard lib usage:')
    for i in range(0, len(data)):
        print(f'{i + 1} elements: {list(combinations(data, i + 1))}')



# Example usage
data1 = [1, 2, 3, 4]
data2 = ['a', 'b', 'c', 'd']
test_gen_combinations(data1)
test_gen_combinations(data2)
