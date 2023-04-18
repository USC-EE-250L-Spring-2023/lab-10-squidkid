import time
import numpy as np
from typing import List, Optional
import matplotlib.pyplot as plt

import threading
import pandas as pd
import requests
import plotly.express as px

def generate_data() -> List[int]:
    """Generate some random data."""
    return np.random.randint(100, 10000, 1000).tolist()

def process1(data: List[int]) -> List[int]:
    """TODO: Document this function. What does it do? What are the inputs and outputs?"""
    """
    I/O: takes a list of inputs and retruns a list of intigers

    the foo function finds the next largest prime number greater than the input number
    it does this by taking the input number (x) then chcking if x+1 can be
    devided by any integer from 2 to x-1 if it cannot then x will be returned as the next
    prime number if it can then the input number will be incremented again and checked if
    it is prime

    A list of next prime numbers is returned based on the input list
    """
    def foo(x):
        """Find the next largest prime number."""
        while True:
            x += 1
            if all(x % i for i in range(2, x)):
                return x
    return [foo(x) for x in data]

def process2(data: List[int]) -> List[int]:
    """TODO: Document this function. What does it do? What are the inputs and outputs?"""
    """
        I/O: takes a list of inputs and retruns a list of intigers

        the foo function finds the next perfect square that is greater than the input number
        it does this by taking the input number (x) then taking the sqrt(x+1), casting it to
        an intiger then taking its sqare. Finally, it checks if this number is equal to the
        original number. This will only be true when x+1 is a perfect square.

        A list of next perfect squares is returned based on the input list

    """
    def foo(x):
        """Finds the next perfect square."""
        while True:
            x += 1
            if int(np.sqrt(x)) ** 2 == x:
                return x
    return [foo(x) for x in data]

def final_process(data1: List[int], data2: List[int]) -> List[int]:
    """TODO: Document this function. What does it do? What are the inputs and outputs?"""
    """
    this function calculates the mean of the element-wise differences between data1 and data2,
    and returns the mean value as a float.

    -> List[int] ???
    """
    return np.mean([x - y for x, y in zip(data1, data2)])

offload_url = 'http://172.20.10.2:5000/' # TODO: Change this to the IP address of your server
#offload_url = 'http://localhost:5000/'

def run(offload: Optional[str] = None) -> float:
    """Run the program, offloading the specified function(s) to the server.

    Args:
        offload: Which function(s) to offload to the server. Can be None, 'process1', 'process2', or 'both'.

    Returns:
        float: the final result of the program.
    """
    data = generate_data()
    if offload == 'none': # in this case, we run the program locally
        data1 = process1(data)
        data2 = process2(data)
    elif offload == 'process1':
        data1 = None
        def offload_process1(data):
            nonlocal data1
            # TODO: Send a POST request to the server with the input data
            url1 = f'{offload_url}/process1'
            response = requests.post(f'{offload_url}/process1', json=data)
            data1 = response.json()

        thread = threading.Thread(target=offload_process1, args=(data,))
        thread.start()
        data2 = process2(data)
        thread.join()
        # Question 2: Why do we need to join the thread here?
        # There are two threds hapening concurrently, The one that sends a post request to the
        # server
        # Question 3: Are the processing functions executing in parallel or just concurrently? What is the difference?
        #   See this article: https://oxylabs.io/blog/concurrency-vs-parallelism
        #   ChatGPT is also good at explaining the difference between parallel and concurrent execution!
        #   Make sure to cite any sources you use to answer this question.
    elif offload == 'process2':
        # TODO: Implement this case
        data2 = None
        def offload_process2(data):
            nonlocal data2

            url2 = f'{offload_url}/process2'
            response = requests.post(f'{offload_url}/process2', json=data)
            data2 = response.json()

        thread = threading.Thread(target=offload_process2, args=(data,))
        thread.start()
        data1 = process1(data)
        thread.join()
        pass

    elif offload == 'both':
        data2 = None
        data1 = None
        def offload_process2(data):
            nonlocal data2

            url2 = f'{offload_url}/process2'
            response = requests.post(f'{offload_url}/process2', json=data)
            data2 = response.json()

        def offload_process1(data):
            nonlocal data1
            # TODO: Send a POST request to the server with the input data
            url1 = f'{offload_url}/process1'
            response = requests.post(f'{offload_url}/process1', json=data)
            data1 = response.json()

        thread1 = threading.Thread(target=offload_process1, args=(data,))
        thread1.start()

        thread2 = threading.Thread(target=offload_process2, args=(data,))
        thread2.start()

        thread1.join()
        thread2.join()

        pass

    ans = final_process(data1, data2)
    return ans

def main():

    # TODO: Run the program 5 times for each offloading mode, and record the total execution time
    #   Compute the mean and standard deviation of the execution times
    #   Hint: store the results in a pandas DataFrame, use previous labs as a reference

    results_df = pd.DataFrame(columns=['Offloading Mode', 'Total Execution Time', 'Standard Deviation', 'Mean Execution Time'])
    offloading_modes = ['none', 'process1', 'process2', 'both']

    for mode in offloading_modes:
        print(str(mode) + ' working...')
        times = []
        start_total_time = time.time()
        for i in range(5):
            start_time = time.time()
            run(mode)
            execution_time = time.time() - start_time
            times.append(execution_time)

        total_execution_time = time.time() - start_total_time
        mean = np.mean(times)
        std = np.std(times)

        results_df.loc[len(results_df.index)] = [mode, total_execution_time, std, mean]

    print(results_df)

    # TODO: Plot makespans (total execution time) as a bar chart with error bars
    # Make sure to include a title and x and y labels

    results_df.set_index('Offloading Mode', inplace=True)
    ax = results_df['Total Execution Time'].plot(kind='bar', yerr=results_df['Standard Deviation'], alpha=0.7)
    ax.set_xlabel('Offloading Mode')
    ax.set_ylabel('Total Execution Time (s)')
    ax.set_title('Total Execution Time with Standard Deviation')

    plt.show()

    # TODO: save plot to "makespan.png"


    # Question 4: What is the best offloading mode? Why do you think that is?
    # Question 5: What is the worst offloading mode? Why do you think that is?
    # Question 6: The processing functions in the example aren't very likely to be used in a real-world application.
    #   What kind of processing functions would be more likely to be used in a real-world application?
    #   When would you want to offload these functions to a server?


if __name__ == '__main__':
    main()
