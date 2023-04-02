from selenium import webdriver
import threading
import time

num_clients = 5 # will change to 500, later. Dont want to put to much load
threads = []
latency_list = []

def load_page():
    driver = webdriver.Chrome()  
    start_time = time.time()
    driver.get("https://ece-461-ae1a9.uc.r.appspot.com")  
    end_time = time.time()
    latency = end_time - start_time
    latency_list.append(latency)
    driver.quit()

for i in range(num_clients):
    print(i) # make sure the program is running.
    t = threading.Thread(target=load_page)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(latency_list)