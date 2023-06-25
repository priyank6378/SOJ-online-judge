from sqlite3 import Connection
from threading import Thread

from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from SOJ.models import Problem, TestCases, Submission, User
from SOJ.main.forms import FileForm, AddProblemForm, AddTestCasesForm
from SOJ.main.utils import run_code, get_dates
from SOJ import db

main = Blueprint('main', __name__)

@main.route("/home", methods=['GET', 'POST'])
@main.route("/", methods=['GET', 'POST'])
def home():
    problems = Problem.query.all()
    solved_status = ['-']*len(problems)
    if (current_user.is_authenticated):
        for prob_id in range(len(problems)):
            submission = Submission.query.filter_by(user_id=current_user.id, prob_id=prob_id+1, status='W').first()
            if submission:
                solved_status[submission.prob_id-1] = 'W'
            submission = Submission.query.filter_by(user_id=current_user.id, prob_id=prob_id+1, status='A').first()
            if submission:
                solved_status[submission.prob_id-1] = 'A'
    
    print(solved_status)
    return render_template("home.html", title='home', problems=problems, solved_status=solved_status, n=len(problems));

@main.route("/task/<int:id>")
def task(id):
    prob = Problem.query.filter_by(id=id).first()
    sample_inp_out = TestCases.query.filter_by(prob_id=id).first()

    if prob:
        return render_template('task.html' , prob=prob, sample=sample_inp_out)
    else :
        flash("Problem does not exist!",)
        return redirect(url_for("main.home"))
    
@main.route("/submit/<int:id>", methods=['POST', 'GET'])
@login_required
def submit(id):
    prob = Problem.query.filter_by(id=id).first();
    form = FileForm()
    if (request.method == 'GET'):
        return render_template("submit.html", prob=prob, form=form)  
    if form.validate_on_submit():
        # save the file and check for the result 
        code = request.files['code'].stream.read().decode('utf-8')
        lang = form.language.data
        pid = id # problem id
        tests = TestCases.query.filter_by(prob_id=pid)
        test_cases = []
        for test in tests:
            test_cases.append((test.input, test.output))

        t = Thread(target=run_code,
                   args=[code, lang, test_cases, current_user.id, pid])
        t.start()
        
        flash("Problem is in queue!", 'info')
        return redirect(url_for('main.result', prob_id=id))
    
    else :
        flash("wrong file format", 'danger')
        return redirect(url_for('main.submit', id=id))

@main.route("/result/<int:prob_id>", methods=['POST', 'GET'])
@login_required
def result(prob_id): 
    prob = Problem.query.filter_by(id=prob_id).first()
    submissions = Submission.query.filter_by(prob_id=prob_id, user_id=current_user.id )[::-1]
    n = 0
    if submissions:
        for _ in submissions:
            n+=1
    else :
        n = 0
    return render_template("result.html", submissions=submissions, prob=prob, n=n)

@main.route("/test", methods=['POST', 'GET'])
@login_required
def test():
    # incomplete function
    if request.method == 'POST':
        print(request.form)
        print(request.files)
    return redirect(url_for('main.home'))

@main.route("/dashboard")
def dashboard():
    total_problems = len(Problem.query.all())
    accepted_subs = Submission.query.filter_by(user_id=current_user.id, status='A').all()
    solved = 0
    dates = get_dates()
    subs = []
    tmp_db = Connection('instance/site.db')
    cursor = tmp_db.cursor()
    for d in dates:
        cursor.execute(r"SELECT COUNT(*) FROM submission WHERE user_id = ? AND strftime('%Y-%m-%d', date) = ?", (current_user.id, d))
        total_subs = cursor.fetchone()[0]
        subs.append(total_subs)
    unique = set()
    for sub in accepted_subs:
        unique.add(sub.prob_id)
    solved = len(unique)
    cursor.close()
    tmp_db.close()
    return render_template("statistics.html", solved=solved, total_problems=total_problems, subs=subs, dates=dates)

@main.route('/add_problem' , methods=['POST', 'GET'])
@login_required
def add_problem():
    if (request.method == 'POST'):
        prob = Problem(title=request.form['title'], 
                       statement=request.form['statement'], 
                       input=request.form['input_format'], 
                       output=request.form['output_format'], 
                       constraint=request.form['constraints'])
        db.session.add(prob)
        db.session.commit()
        return redirect(url_for('main.add_testcase', id=prob.id))
    if (current_user.username == 'zoid'):
        form = AddProblemForm()
        return render_template("add_problem.html", form=form)
    else :
        abort(404)

@main.route('/add_testcase/<int:id>' , methods=['POST', 'GET'])
@login_required
def add_testcase(id):
    if (request.method == 'POST'):
        prob = TestCases(prob_id=id,
                       input=request.form['input'], 
                       output=request.form['output'])
        db.session.add(prob)
        db.session.commit()
    if (current_user.username == 'zoid'):
        form = AddTestCasesForm()
        return render_template("add_testcase.html", form=form)
    else :
        abort(404)


@main.route('/prob_stats/<int:id>')
def prob_stats(id):
    prob = Problem.query.filter_by(id=id).first()
    subs = Submission.query.filter_by(prob_id=id, status='A').all()
    total_subs = len(subs)
    # sorting subs on runtime
    subs.sort(key=lambda x: x.runtime)
    
    user_visited = {}
    for s in subs[::-1]:
        if (s.user_id not in user_visited):
            user_visited[s.user_id] = s.runtime
        if (len(user_visited) == 10):
            break
    
    top_10 = []
    ind = 0
    for (uid, rtime) in sorted(user_visited.items(), key=lambda x: x[1]):
        top_10.append((ind,User.query.filter_by(id=uid).first().username, rtime))
        ind += 1

    return render_template("prob_stats.html", prob=prob, top_10 = top_10)


@main.app_errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404
