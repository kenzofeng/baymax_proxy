from concurrent.futures.thread import ThreadPoolExecutor

pool = ThreadPoolExecutor(max_workers=50)
emailPool = ThreadPoolExecutor(max_workers=50)
subPool = ThreadPoolExecutor(max_workers=50)
