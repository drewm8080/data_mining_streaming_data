from blackbox import BlackBox
import os
import sys
import time
import binascii
import math
import random
import statistics



def myhashs(data):
    encoded_data = int(binascii.hexlify(data.encode('utf8')), 16)
    # storing the number of hashes 
    num_hash= 75

    parameter_a = random.sample(range(1, int(1e8)), num_hash)
    parameter_b = random.sample(range(1, int(1e8)), num_hash)
    hash_funcs = [parameter_a, parameter_b]

    result = []

    def compute_hash(i):
        equation = hash_funcs[0][i] * encoded_data + hash_funcs[1][i]
        finalized_equation = equation % 69997
        return finalized_equation

    for i in range(num_hash):
        result.append(compute_hash(i))
    return result




def write_results_to_file(output_filepath, results):
    with open(output_filepath, 'w') as file:
        file.write("Time,Ground Truth,Estimation\n")

        for result in results:
            time, ground_truth, estimation = result
            file.write(f"{time},{ground_truth},{estimation}\n")





def calculate_estimation(users, num_groups):
    num_hash= 75
    unique_users_bitmap, hash_values = bitmap(users)
    
    # creating a group of estimations 
    group_estimations = []
    group_size = len(users) // num_groups

    # iterating each group
    for i in range(num_groups):
        group_estimation = 0
        # creating an index for each group
        start_index = i * group_size
        end_index = start_index + group_size

        for i in range(num_hash):
            # in each of the hash values, break them into groups, take average of leading zeros and then median
            max_trailing_zeros = 0
            for value in hash_values[start_index:end_index]:
                binary_string = bin(value[i])[2:]
                # finding all the trailing ones
                trailing_zeros = binary_string[::-1].find('1')
                # assuming not empty and trailing zeros 
                if trailing_zeros != -1 and trailing_zeros > max_trailing_zeros:
                    max_trailing_zeros = trailing_zeros
            group_estimation =group_estimation+( 2 ** max_trailing_zeros)

        # taking group average 
        group_average = group_estimation / group_size
        group_estimations.append(group_average)

    # taking the median estimation 
    median_estimation = statistics.median(group_estimations)
    final_median_estimation = round(median_estimation)
    # summing unique users in the 
    unique_users_count = sum(unique_users_bitmap)
    return unique_users_count, final_median_estimation



def bitmap(users):
    # creating a bit map
    unique_users_bitmap = [0] * len(users)
    hash_values = []

    for i, user in enumerate(users):
        # storing the results
        hash_result = myhashs(user)
        if unique_users_bitmap[i] == 0:
            # storing the unique users 
            unique_users_bitmap[i] = 1
        hash_values.append(hash_result)
    # returning the hash values 
    return unique_users_bitmap, hash_values







if __name__ == '__main__':
    input_path = '/Users/andrewmoore/Desktop/DSCI 553/DSCI 553 HW 5/users.txt'
    stream_size = 300
    num_of_asks = 1000
    output_filepath = '/Users/andrewmoore/Desktop/DSCI 553/DSCI 553 HW 5/finalized_output_3.csv'

    time_start = time.time()

    results = []
    blackbox = BlackBox()
    unique_users_sum = 0
    estimation_sum = 0

    # looping though
    for i in range(num_of_asks):
        users = blackbox.ask(input_path, stream_size)
        # getting the estimation
        unique_users, estimation = calculate_estimation(users, 5)

        unique_users_sum = unique_users_sum + unique_users
        estimation_sum =estimation_sum+ estimation

        results.append((i, unique_users, estimation))

    write_results_to_file(output_filepath, results)

    time_end = time.time()
    duration = time_end - time_start
    print('Duration:', duration)

    print("Ratio estimated/actual", estimation_sum / unique_users_sum)
