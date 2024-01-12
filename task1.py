from blackbox import BlackBox
import os
import sys
import time
import binascii
import math
import random
from pyspark import SparkContext, SparkConf

def setting_up_variables(num_of_asks,stream_size):    
    result_array = []
    seen_array = []
    bits_array = [0]*69997
    optimal_function = 69997/(num_of_asks*stream_size)
    optimal_k = math.ceil(optimal_function*math.log(2))
    return optimal_k,bits_array,result_array,seen_array,bits_array

def myhashs(data):
    encoded_data = int(binascii.hexlify(data.encode('utf8')), 16)

    parameter_a = random.sample(range(1, int(1e8)), optimal_k)
    parameter_b = random.sample(range(1, int(1e8)), optimal_k)
    hash_funcs = [parameter_a, parameter_b]

    result = []

    def compute_hash(i):
        equation = hash_funcs[0][i] * encoded_data + hash_funcs[1][i]
        finalized_equation = equation % 69997
        return finalized_equation

    for i in range(optimal_k):
        result.append(compute_hash(i))
    return result

def write_results_to_csv(result_array, filename):
    with open(filename, 'w') as f:
        f.write('Time,FPR\n')
        for i, fpr in result_array:
            f.write(f'{i},{fpr}\n')



if __name__ == '__main__':
    time_start = time.time()
    num_of_asks = 50
    input_path = '/Users/andrewmoore/Desktop/DSCI 553/DSCI 553 HW 5/users.txt'
    stream_size = 100
    blackbox = BlackBox()
    output_filepath = '/Users/andrewmoore/Desktop/DSCI 553/DSCI 553 HW 5/finalized_ouput_1.csv'
    # creating hash functions
    global optimal_k

    # creating the optimal number of hash functions
    optimal_k, bits_array, result_array, seen_array, bits_array = setting_up_variables(num_of_asks,stream_size)


   ## calculating FPR ####

    for i in range(num_of_asks):
        users = blackbox.ask(input_path,stream_size)
        negatives = 0
        false_positives = 0
        for user in users:
            # check if the user is present in the Bloom filter
            hashed_values = myhashs(user)
            is_present = all(bits_array[h] == 1 for h in hashed_values)
            # if user is not seen before its a negative
            if user not in seen_array:
                negatives = negatives + 1
                # the user is considered present in the Bloom filter, it's a false positive
                if is_present:
                    false_positives =false_positives+ 1
            # updating the bloom filter 
            for h in hashed_values:
                bits_array[h] = 1
            seen_array.append(user)
        fpr = false_positives / negatives if negatives > 0 else 0
        result_array.append((i, fpr))
    
    # writing results 
    write_results_to_csv(result_array,output_filepath)




    time_end = time.time()
    duration= time_end-time_start
    final_time = print('Duration:',duration)
