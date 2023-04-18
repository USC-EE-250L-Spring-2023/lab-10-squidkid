# Lab 10
[Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) this repo and clone it to your machine to get started!

## Team Members
Elliott Meeks

## Lab Question Answers

#Question 1: Under what circumstances do you think it will be worthwhile to offload one or both of the processing tasks to your PC? And conversely, under what circumstances will it not be worthwhile?

It would be worth offloading if the task is computationally expensive and you can offload the task to a server with more specialized hardware (GPU's or CPU'S). For instance, if a raspberry pi is collecting data it may be better to offload that data to a server for processing because the raspberry pi is just a little guy with not the best processor and my get overwelled with a lot of data. On the other hand if your dealing with a small amount of data that is not computationally expensive you might as well process it locally.

# Question 2: Why do we need to join the thread here?
There are two threads happening concurrently, The first sends a post request to the
server to offload process1, while the second thread, process2, is done locally. join is needed to ensure synchronization between the two threads. So if one finishes faster than the other the program does not proceed

# Question 3: Are the processing functions executing in parallel or just concurrently? What is the difference?

The processing functions are executing concurrently. the offload_process1 function is executed in a separate thread using the threading module, while the process2 function is executed in the main thread.

Concurrency refers to the ability of multiple tasks to start, run, and complete in overlapping time intervals, without necessarily executing simultaneously on multiple processor cores.

parallelism refers to the ability of tasks to execute simultaneously on multiple processor cores, where each task has its own dedicated processor core.

source: Chat GPT

# Question 4: What is the best offloading mode? Why do you think that is?
When we just offload porcess2 because we can complete two processes in parallel.

# Question 5: What is the worst offloading mode? Why do you think that is?
offloading neither process because the raspberry pies processor is very poor

# Question 6: The processing functions in the example aren't very likely to be used in a real-world application.

#   What kind of processing functions would be more likely to be used in a real-world application?
Processes used to train an IA or ML module. Training an AI requires enormous amounts of data and computation. This could be offloaded to a server with specialized hardware such as GPU's and TPU's
#   When would you want to offload these functions to a server?
If you have a large amount of data to process or preforming computationally expensive tasks. It could be best to offload the data to a server with more computational resources
