import os
import time
import pickle
import concurrent.futures
from scrape_emails import Scrape


class ThreadMaster:
    def __init__(self):
        self.worker_count = 1
        self.data_sizes = [10]
        self.results = []
        try:
            filename = self.get_unique_filename('observation_data')
            with open(filename, "rb") as fp:
                self.results = pickle.load(fp)
        except FileNotFoundError:
            print('No initial observation data found')

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
            self.worker_count = 1

            for _ in range(10):
                # set worker count
                self.worker_count *= 2

                start_time = time.time()
                self.execute_thread_func(data_size)
                execution_time = time.time() - start_time

                self.results.append({
                    'data_size': data_size,
                    'execution_time': execution_time,
                    'worker_count': self.worker_count
                })

        # save the generated results
        filename = self.get_unique_filename('observation_data')
        with open(filename, 'wb') as fp:
            pickle.dump(self.results, fp)

    @staticmethod
    def get_unique_filename(filename):
        if os.path.exists(filename):
            base_name, extension = os.path.splitext(filename)
            index = 1
            while os.path.exists(filename):
                filename = f"{base_name}_{index}"
                index += 1
        return filename

    # save generated graphs as image


tm_obj = ThreadMaster()
tm_obj.start_thread_visualiser()

