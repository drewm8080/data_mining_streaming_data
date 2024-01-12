# Streaming Algorithms

## Task 1: Bloom Filtering 

I will implement the Bloom Filtering algorithm to estimate whether the user_id in the data stream has shown before. I will find proper hash functions and the number of hash functions in the Bloom Filtering algorithm.

### Execution Details
- Global filter bit array length: 69997
- Hash functions: Should be independent, uniformly distributed, and keep the same once created
- User_id conversion: Convert user_id to an integer and then apply hash functions
- Data stream size: 100
- Number of tests: More than 30
- False positive rate (FPR): Should not be larger than 0.5 more than once
- Run time: Within 100s for 30 data streams

### Output Results
- Save results in a CSV file with the header “Time,FPR”
- Encapsulate hash functions into a function called myhashs

## Task 2: Flajolet-Martin algorithm 

In this task, I will implement the Flajolet-Martin algorithm to estimate the number of unique users within a window in the data stream.

### Execution Details
- Stream size: 300
- Number of tests: More than 30
- Final result requirement: 0.2 <= (sum of all estimations / sum of all ground truths) <= 5
- Run time: Within 100s for 30 data streams

### Output Results
- Save results in a CSV file with the header “Time,Ground Truth,Estimation”
- Encapsulate hash functions into a function called myhashs

## Task 3: Fixed Size Sampling 

The goal of this task is to implement the fixed size sampling method (Reservoir Sampling Algorithm).

### Execution Details
- Stream size: 100
- Number of tests: More than 30
- Random seed: 553 in the main function
- Run time: Within 100s for 30 data streams

### Output Results
- Print the current stage of your reservoir into a CSV file every time you receive 100 users
