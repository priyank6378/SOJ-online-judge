import celery 
import os
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

    def run_code_thread():
        nonlocal terminated
        nonlocal max_runtime

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
            f = open("tmp/inp.txt", "w")
            f.write(test[0])
            f.close()
            f = open("tmp/out.txt", 'w')
            f.write(test[1])
            f.close()
            
            if lang == "c++":
                execution_time = time()
                os.system('./tmp/tmp < tmp/inp.txt > tmp/prog_out.txt')
                execution_time = time() - execution_time
                max_runtime = max(max_runtime, execution_time)
                if os.system('diff tmp/prog_out.txt tmp/out.txt') == 0:
                    results.append("A")
                else:
                    results.append("W")
            
            if lang == "c":
                execution_time = time()
                os.system('./tmp/tmp < tmp/inp.txt > tmp/prog_out.txt')
                execution_time = time() - execution_time
                max_runtime = max(max_runtime, execution_time)
                if os.system('diff tmp/prog_out.txt tmp/out.txt') == 0:
                    results.append("A")
                else:
                    results.append("W")
            
            if lang == "python":
                execution_time = time()
                os.system('python3 tmp/tmp.py < tmp/inp.txt > tmp/prog_out.txt')
                execution_time = time() - execution_time
                max_runtime = max(max_runtime, execution_time)
                if os.system('diff tmp/prog_out.txt tmp/out.txt') == 0:
                    results.append("A")
                else:
                    results.append("W")
        
        # clean up
        os.system("rm -rf tmp")
        nonlocal terminated
        terminated = True
    
    os.system("rm -rf tmp")
    judge_thread = Thread(target=run_code_thread, args=[])
    judge_thread.start()
    sleep(2.2)
    r = "A"
    if terminated :
        for x in results:
            if x == 'W':
                r = 'W'
                break
    else :
        os.system("kill $(ps aux | grep 'python3 tmp/tmp.py < tmp/inp.txt > tmp/prog_out.txt' | awk '{print $2}')")
        os.system("kill $(ps aux | grep './tmp/tmp < tmp/inp.txt > tmp/prog_out.txt' | awk '{print $2}')")
        r = 'T'
        max_runtime = 2.001
    # print( "cur dir : ",os.path.abspath(os.curdir))
    conn = Connection("instance/site.db")
    cursor = conn.cursor()
    # cursor.execute("INSERT INTO submission (user_id, prob_id, code, language, date, runtime, status) VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, prob_id, code, lang, datetime.utcnow(), max_runtime, r))
    cursor.execute("UPDATE submission SET runtime = ?, status = ? WHERE user_id = ? AND prob_id = ? AND code = ?", (max_runtime, r, user_id, prob_id, code))
    cursor.close()
    conn.commit()
    conn.close()

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