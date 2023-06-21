from SOJ import db, create_app
from SOJ.models import *

a = create_app()

with a.app_context():
    db.drop_all()
    db.create_all()
    p1 = Problem(title="Sum of 2 numbers.", statement="Given x and y. Print x+y.", input="The only input line has a string of length x and y.", output="Print one integer: x+y", constraint="1≤n≤106", solved=0, tried=0)
    t1 = TestCases(prob_id=1, input="2 3\n", output="5\n")
    t2 = TestCases(prob_id=1, input="4 5\n", output="9\n")
    p2 = Problem(title="Sum of 3 numbers.", statement="Given x, y and z. Print x+y+z.", input="The only input line has a string of length x, y and z.", output="Print one integer: x+y+z", constraint="1≤n≤106", solved=0, tried=0)
    t3 = TestCases(prob_id=2, input="2 3 4\n", output="9\n")
    t4 = TestCases(prob_id=2, input="4 5 6\n", output="15\n")
    p3 = Problem(title="Difference", statement="Given x and y. Print x-y.", input="The only input line has a string of length x and y.", output="Print one integer: x-y", constraint="1≤n≤106", solved=0, tried=0)
    t5 = TestCases(prob_id=3, input="2 3\n", output="-1\n")
    t6 = TestCases(prob_id=3, input="4 5\n", output="-1\n")
    db.session.add(p1)
    db.session.add(t1)
    db.session.add(t2)
    db.session.add(p2)
    db.session.add(t3)
    db.session.add(t4)
    db.session.add(p3)
    db.session.add(t5)
    db.session.add(t6)
    db.session.commit()
    