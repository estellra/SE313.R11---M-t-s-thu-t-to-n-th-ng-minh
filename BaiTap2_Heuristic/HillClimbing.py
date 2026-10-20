import math
import random

# Cài đặt thuật toán luyện kim mô phỏng thay vì tìm kiếm leo đồi bthuog để tránh bị kẹt tại các đỉnh cục bộ. 

def evaluate(state, heights):
    return heights[state]


def get_neighbors(state, n):
    neighbors = []

    if state > 0:
        neighbors.append(state - 1)

    if state < n - 1:
        neighbors.append(state + 1)

    return neighbors


def main(heights, start_state, init_temperature=2.5, cooling_rate=0.99, min_temperature=0.01, max_steps=2000):
    current_state = start_state
    current_score = evaluate(current_state, heights)

    best_state = current_state
    best_score = current_score

    temperature = init_temperature

    for step in range(max_steps):
        if temperature <= min_temperature:
            break

        neighbors = get_neighbors(current_state, len(heights))

        if not neighbors:
            break

        next_state = random.choice(neighbors)
        next_score = evaluate(next_state, heights)

        delta = next_score - current_score

        if delta >= 0:
            accept = True
        else:
            probability = math.exp(delta / temperature)
            accept = random.random() < probability

        if accept:
            current_state = next_state
            current_score = next_score

        if current_score > best_score:
            best_state = current_state
            best_score = current_score

        temperature *= cooling_rate

    return best_state, best_score


def input_data():
    while True:
            n = int(input("Nhap vao so luong dinh nui : "))
            if n > 0:
                break
            print("So luong dinh nui phai > 0")



    heights = []
    for i in range(n):
                height = float(
                    input(f"Nhap vao do cao cua dinh nui thu {i+1}: ")
                )
                heights.append(height)
                



    while True:
            start = int(
                input(f"Nhap dinh bat dau (1-{n}):")
            )
            if 1 <= start <=n:
                break
            print(f"Dinh bat dau phai tu 1 den {n}")


    return heights, start - 1


random.seed(1)
heights, start_state = input_data()
best_state, best_score = main(heights, start_state)

print(f"Dinh tot nhat tim thay: Dinh{best_state+1} ")
print(f"Do cao lon nhat tim thay: {best_score}")