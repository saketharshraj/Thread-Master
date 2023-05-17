import os
import time
import pickle
import concurrent.futures
from scrape_emails import Scrape
import matplotlib.pyplot as plt


class ThreadMaster:
    def __init__(self):
        self.worker_count = 1
        # self.data_sizes = [10**i for i in range(1, 5)]
        self.data_sizes = [30000]
        self.results = []
        self.obs_filename = 'observation_data_30000'
        # self.worker_counts = [100, 200, 300, 400, 500, 600, 700, 800]
        self.worker_counts = [i*10 for i in range(1, 100)]
        try:

            with open(self.obs_filename, "rb") as fp:
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
            futures = [executor.submit(Scrape.dummy_function, company) for company in self.companies_data[:data_length]]
            concurrent.futures.wait(futures)

    # set data length limit and start thread visualization
    def start_thread_visualiser(self):
        self.results = []
        for data_size in self.data_sizes:
            # reset worker count
            self.worker_count = 1

            for worker_count in self.worker_counts:
                # set worker count
                self.worker_count = worker_count
                start_time = time.time()
                self.execute_thread_func(data_size)
                execution_time = time.time() - start_time

                self.results.append({
                    'data_size': data_size,
                    'execution_time': execution_time,
                    'worker_count': worker_count
                })
            print('Done till', data_size)
        # save the generated results
        filename = self.get_unique_filename(self.obs_filename)
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

    # generate graph and save images : data_size-worker_count
    def generate_and_save_graph(self):
        # generate graph for all data sizes
        for data_size in self.data_sizes:
            # get results of specific data size
            graph_data = [data for data in self.results if data['data_size'] == data_size]
            # split data in x-axis and y-axis
            if len(graph_data):
                worker_counts, exec_times = zip(*[(d['worker_count'], d['execution_time']) for d in graph_data])

                # create a new figure and axes for each data size
                fig, ax = plt.subplots()
                ax.plot(worker_counts, exec_times, marker='o')
                ax.set_xlabel('Thread Count')
                ax.set_ylabel('Execution Time (seconds)')
                ax.set_title(f'Program Performance for Data Size {data_size}')

                # for i, txt in enumerate(exec_times):
                #     ax.annotate(txt, (worker_counts[i], round(exec_times[i], 2)))

                # save the graph for each data size
                fig.savefig(f'performance_graph_{data_size}.png')
                plt.close(fig)  # close the figure to release memory


tm_obj = ThreadMaster()
tm_obj.start_thread_visualiser()
tm_obj.generate_and_save_graph()
