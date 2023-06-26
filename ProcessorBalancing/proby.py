import numpy as np

def generate_random_list(a, b, f, size):
    # Create the list of numbers from 'a' to 'b'
    numbers = np.arange(a, b+1)

    # Calculate the frequency of each number
    probabilities = np.repeat(f, len(numbers))

    # Generate the random list with specified frequency
    random_list = np.random.choice(numbers, size=size, p=probabilities/np.sum(probabilities))
    return random_list

random_numbers = generate_random_list(a, b, f, size)
print(random_numbers)
