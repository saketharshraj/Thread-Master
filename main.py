import time
import pickle
import concurrent.futures
from scrape_emails import Scrape


class ThreadMaster:
    def __init__(self):
        self.worker_count = 2
        self.data_sizes = [10, 100, 1000, 10000, 100000]
        try:
            with open("companies-data", "rb") as fp:
                self.companies_data = pickle.load(fp)
        except FileNotFoundError:
            print('No cached data found')

    def execute_thread_func(self, data_length):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.worker_count) as executor:
            futures = [executor.submit(Scrape.extract_email, company) for company in self.companies_data[:data_length]]
            concurrent.futures.wait(futures)

    # set data length limit and start thread visualization
    def start_thread_visualiser(self):
        for data_size in self.data_sizes:
            # reset worker count
            self.worker_count = 2

            # set worker count
            self.worker_count *= 2

            self.execute_thread_func(data_size)

    # save generated graphs as image


tm_obj = ThreadMaster()
start_time = time.time()
tm_obj.start_thread_visualiser()
execution_time = time.time() - start_time

