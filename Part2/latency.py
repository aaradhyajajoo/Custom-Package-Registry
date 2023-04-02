from selenium import webdriver      # selenium is the chosen library for automating load onto the system
import threading                    # since system needs to experience load simultaniously, threading needs to be utilized           
import time                         # used to measure latency data
import numpy as np                  # used to calculate latency data 

num_clients = 5                     # set to 5 for proof of concept, will be switch to 500 when ready
threads = []                        # stores thread objects

# Is this thread safe?
latency_list = []                   # stores latency time in seconds for each client. Size should be "num_clients" by the end 

#   performs a load to the system
def load_page():
    driver = webdriver.Chrome()

    start_time = time.time()                                # used to measure latency 
    driver.get("https://ece-461-ae1a9.uc.r.appspot.com")    # creates load
    # Add load here when we have the system fully ready     # interraction
    end_time = time.time()                                  # used to measure latency

    latency = end_time - start_time                         # latency time
    latency_list.append(latency)                            # puts load information in the list
    driver.quit()                                           # removes load from system

#   after all threads are ended, we analyze load experienced by the system
def get_data(latency_list):
  latency_list = np.array(latency_list)                     # converts to np array for friendly analytics
  mu = np.mean(latency_list)                                # mean
  median = np.median(latency_list)                          # median
  percentile99 = np.percentile(latency_list, 99)            # 99th percentile

  # show data results
  print(f'mean: {mu} seconds\nmedian: {median} seconds\n99th Percentile: {percentile99}seconds')

#   creates threads and adds load    
for i in range(num_clients):
    print(i)                                               # make sure the program is running.
    t = threading.Thread(target=load_page)
    threads.append(t)
    t.start()

#   end the threads
for t in threads:
    t.join()

#   calculate and prints data
get_data(latency_list)
