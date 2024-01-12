from blackbox import BlackBox
import os
import random
import sys
import time


def write_to_csv(output_filepath, data):
    with open(output_filepath, 'w') as file:
        for row in data:
            file.write(','.join(map(str, row)) + '\n')

def reservoir_sampling(users, reservoir, iteration, stream_size):
    for user in users:
        # counting the iterations
        iteration = iteration+ 1
        probability = 100 / iteration
        every_hundred = iteration % 100
        # creating the header 
        if iteration == 1:
            data.append(['seqnum', '0_id', '20_id', '40_id', '60_id', '80_id'])
        # we get our first 100
        if iteration <= 100:
            reservoir.append(user)
        else:
            # if over 100 use a probability 
            random_number = random.random()
            proability_of_staying = random_number < probability
            if proability_of_staying:
                # generating new number
                new_int = random.randint(0, stream_size - 1)
                reservoir[new_int] = user
        if every_hundred == 0:
            # recording every 100
            row = [iteration]
            # only getting the ones in these places 
            for i in [0, 20, 40, 60, 80]:
                row.append(reservoir[i])
            data.append(row)
    return reservoir, iteration

if __name__ == '__main__':
    time_start = time.time()
    input_path = '/Users/andrewmoore/Desktop/DSCI 553/DSCI 553 HW 5/users.txt'
    stream_size = 100
    num_of_asks = 30
    random.seed(553)
    output_filepath = '/Users/andrewmoore/Desktop/DSCI 553/DSCI 553 HW 5/output_8.txt'
    # generating the variables 
    results = []
    blackbox = BlackBox()
    reservoir = []
    iteration = 0
    data = []

    for i in range(num_of_asks):
        users = blackbox.ask(input_path, stream_size)
        # preform resivor samplaing
        reservoir, iteration = reservoir_sampling(users, reservoir, iteration, stream_size)
    # writing to CSV
    write_to_csv(output_filepath, data)

    time_end = time.time()
    duration = time_end - time_start
    print('Duration:', duration)
