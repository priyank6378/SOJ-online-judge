import celery 
import os
import subprocess
from time import time, sleep
from threading import Thread
import multiprocessing as mp
from datetime import timedelta, date, datetime

from sqlite3 import Connection
from SOJ import db
from SOJ.models import Submission


# url for celery broker and backend
# BORKER_URL = 'redis://localhost:6379'
# BACKEND_URL = 'redis://localhost:6379'

# app = celery.Celery("run_code", broker=BORKER_URL, backend=BACKEND_URL)

# @app.task
def run_code(code : str, lang: str, test_case : list, user_id: int, prob_id: int)->list:
    '''
    code : code to run in string
    test_case : list of test case in string [(input1, output1), (input2, output2)...]
    return : list of result of each test case on code
    '''

    terminated = False
    max_runtime = 0
    results = []
    conn = Connection("instance/site.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO submission (user_id, prob_id, code, language, date, runtime, status) VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, prob_id, code, lang, datetime.utcnow(), -1, 'Q'))
    cursor.close()
    conn.commit()
    conn.close()
    file_name = str(user_id) + "_" + str(prob_id)
    def run_code_thread():
        nonlocal terminated
        nonlocal max_runtime
        nonlocal file_name
        os.mkdir(file_name)

        if lang == "c++":
            tmp_file = open(f"{file_name}/{file_name}.cpp", "w")
            tmp_file.write(code)
            tmp_file.close()
            os.system(f"g++ {file_name}/{file_name}.cpp -o {file_name}/{file_name}")
        
        if lang == "c":
            tmp_file = open(f"{file_name}/{file_name}.c", "w")
            tmp_file.write(code)
            tmp_file.close()
            os.system(f"gcc {file_name}/{file_name}.c -o {file_name}/{file_name}")

        if lang == 'python':
            tmp_file = open(f"{file_name}/{file_name}.py", "w")
            tmp_file.write(code)
            tmp_file.close()
        
        for test in test_case:
            f = open(f"{file_name}/{file_name}_inp.txt", "w")
            f.write(test[0])
            f.close()
            f = open(f"{file_name}/{file_name}_out.txt", 'w')
            f.write(test[1])
            f.close()
            
            if lang == "c++":
                execution_time = time()
                os.system(f'./{file_name}/{file_name} < {file_name}/{file_name}_inp.txt > {file_name}/prog_{file_name}_out.txt')
                execution_time = time() - execution_time
                max_runtime = max(max_runtime, execution_time)
                if os.system(f'diff {file_name}/prog_{file_name}_out.txt {file_name}/{file_name}_out.txt') == 0:
                    results.append("A")
                else:
                    results.append("W")
            
            if lang == "c":
                execution_time = time()
                os.system(f'./{file_name}/{file_name} < {file_name}/{file_name}_inp.txt > {file_name}/prog_{file_name}_out.txt')
                execution_time = time() - execution_time
                max_runtime = max(max_runtime, execution_time)
                if os.system(f'diff {file_name}/prog_{file_name}_out.txt {file_name}/{file_name}_out.txt') == 0:
                    results.append("A")
                else:
                    results.append("W")
            
            if lang == "python":
                execution_time = time()
                command = f'python3 {file_name}/{file_name}.py < {file_name}/{file_name}_inp.txt > {file_name}/prog_{file_name}_out.txt'
                os.system(command)
                execution_time = time() - execution_time
                max_runtime = max(max_runtime, execution_time)
                if os.system(f'diff {file_name}/prog_{file_name}_out.txt {file_name}/{file_name}_out.txt') == 0:
                    results.append("A")
                else:
                    results.append("W")
        
        # clean up
        terminated = True
        # print("Exiting code run thread!")
    
    os.system(f"rm -rf {file_name}")
    judge_thread = Thread(target=run_code_thread, args=[])
    judge_thread.start()
    sleep(2.2)
    r = "A"
    # print("Terminated status: ", terminated)
    if terminated :
        for x in results:
            if x == 'W':
                r = 'W'
                break
    else :
        # print('TLE ELSE BLOCK')
        r = 'T'
        max_runtime = 2.001
        # print("EXITING TLE BLOCK")

    conn = Connection("instance/site.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE submission SET runtime = ?, status = ? WHERE user_id = ? AND prob_id = ? AND code = ?", (max_runtime, r, user_id, prob_id, code))
    cursor.close()
    conn.commit()
    conn.close()
    os.system(f"rm -rf {file_name}")

def thread_killer(file_name):
    # print("RUNNIN THREAD_KILLER FUNCTION")
    sleep(10)
    os.system(f"kill $(ps aux | grep 'python3 {file_name}/{file_name}.py' | awk " + "'{print $2}')")
    os.system(f"kill $(ps aux | grep './{file_name}/{file_name}' | awk " + "'{print $2}')")
    # print("EXITING THREAD_KILLER FUNCTION")

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