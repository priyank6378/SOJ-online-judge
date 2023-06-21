import celery 
import os
from time import time
import multiprocessing as mp
from datetime import timedelta, date, datetime

# url for celery broker and backend
BORKER_URL = 'redis://localhost:6379'
BACKEND_URL = 'redis://localhost:6379'

app = celery.Celery("run_code", broker=BORKER_URL, backend=BACKEND_URL)

@app.task
def run_code(code : str, lang: str, test_case : list)->list:
    '''
    code : code to run in string
    test_case : list of test case in string [(input1, output1), (input2, output2)...]
    return : list of result of each test case on code
    '''
    results = []

    os.mkdir("tmp")

    if lang == "c++":
        tmp_file = open("tmp/tmp.cpp", "w")
        tmp_file.write(code)
        tmp_file.close()
        os.system("g++ tmp/tmp.cpp -o tmp/tmp")
    
    if lang == "c":
        tmp_file = open("tmp/tmp.c", "w")
        tmp_file.write(code)
        tmp_file.close()
        os.system("gcc tmp/tmp.c -o tmp/tmp")

    if lang == 'python':
        tmp_file = open("tmp/tmp.py", "w")
        tmp_file.write(code)
        tmp_file.close()
    
    for test in test_case:
        f = open("inp.txt", "w")
        f.write(test[0])
        f.close()
        f = open("out.txt", 'w')
        f.write(test[1])
        f.close()
        
        max_runtime = 0
        
        if lang == "c++":
            execution_time = time()
            os.system('./tmp/tmp < inp.txt > prog_out.txt')
            execution_time = time() - execution_time
            max_runtime = max(max_runtime, execution_time)
            if os.system('diff prog_out.txt out.txt') == 0:
                results.append("A")
            else:
                results.append("W")
        
        if lang == "c":
            execution_time = time()
            os.system('./tmp/tmp < inp.txt > prog_out.txt')
            execution_time = time() - execution_time
            max_runtime = max(max_runtime, execution_time)
            if os.system('diff prog_out.txt out.txt') == 0:
                results.append("A")
            else:
                results.append("W")
        
        if lang == "python":
            execution_time = time()
            os.system('python3 tmp/tmp.py < inp.txt > prog_out.txt')
            execution_time = time() - execution_time
            max_runtime = max(max_runtime, execution_time)
            if os.system('diff prog_out.txt out.txt') == 0:
                results.append("A")
            else:
                results.append("W")
    
    # clean up
    os.system("rm -rf tmp")

    return (results, max_runtime)


def get_dates():
    def daterange(date1, date2):
        dates = []
        for n in range(int ((date2 - date1).days)+1):
            dates.append((date1 + timedelta(n)).strftime("%Y-%m-%d"))
        return dates

    end_dt = datetime.utcnow().date()
    start_dt = end_dt - timedelta(days=364)
    dates = daterange(start_dt, end_dt)

    return dates