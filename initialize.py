from SOJ import db, create_app
from SOJ.models import *

a = create_app()

with a.app_context():
    db.drop_all()
    db.create_all()
    p1 = Problem(title="Sum of 2 numbers.", statement="Given x and y. Print x+y.", input="The only input line has a string of length x and y.", output="Print one integer: x+y", constraint="1≤n≤106", solved=0, tried=0, categories="Math")
    t1 = TestCases(prob_id=1, input="2 3\n", output="5\n")
    t2 = TestCases(prob_id=1, input="4 5\n", output="9\n")
    p2 = Problem(title="Sum of 3 numbers.", statement="Given x, y and z. Print x+y+z.", input="The only input line has a string of length x, y and z.", output="Print one integer: x+y+z", constraint="1≤n≤106", solved=0, tried=0, categories="Math")
    t3 = TestCases(prob_id=2, input="2 3 4\n", output="9\n")
    t4 = TestCases(prob_id=2, input="4 5 6\n", output="15\n")
    p3 = Problem(title="Difference", statement="Given x and y. Print x-y.", input="The only input line has a string of length x and y.", output="Print one integer: x-y", constraint="1≤n≤106", solved=0, tried=0, categories="Math")
    t5 = TestCases(prob_id=3, input="2 3\n", output="-1\n")
    t6 = TestCases(prob_id=3, input="4 5\n", output="-1\n")
    p4 = Problem(title="Connected Components", statement="Given a graph with n nodes and m edges. Print the number of connected components.", input="The first line contains two integers n and m. Each of the next m lines contains two integers u and v, meaning that there is an edge between nodes u and v.", output="Print one integer: the number of connected components.", constraint="1≤n≤106", solved=0, tried=0, categories="Graph")
    t7 = TestCases(prob_id=4, input="4 2\n1 2\n3 2\n", output="2\n")
    t8 = TestCases(prob_id=4, input="4 3\n1 2\n3 2\n4 3\n", output="1\n")
    p5 = Problem(title="Shortest Path", statement="Given a graph with n nodes and m edges. Print the shortest path from node 1 to node n.", input="The first line contains two integers n and m. Each of the next m lines contains three integers u, v and w, meaning that there is an edge between nodes u and v with weight w.", output="Print one integer: the shortest path from node 1 to node n.", constraint="1≤n≤106", solved=0, tried=0, categories="Graph")
    t9 = TestCases(prob_id=5, input="4 2\n1 2 1\n3 2 1\n", output="2\n")
    t10 = TestCases(prob_id=5, input="4 3\n1 2 1\n3 2 1\n4 3 1\n", output="1\n")
    db.session.add(p1)
    db.session.add(t1)
    db.session.add(t2)
    db.session.add(p2)
    db.session.add(t3)
    db.session.add(t4)
    db.session.add(p3)
    db.session.add(t5)
    db.session.add(t6)
    db.session.add(p4)
    db.session.add(t7)
    db.session.add(t8)
    db.session.add(p5)
    db.session.add(t9)
    db.session.add(t10)

    p6 = Problem(title="Longest common subsequence", statement="Given two strings s and t. Print the length of the longest common subsequence of s and t.", input="The first line contains two integers n and m. The second line contains a string of length n. The third line contains a string of length m.", output="Print one integer: the length of the longest common subsequence of s and t.", constraint="1≤n,m≤106", solved=0, tried=0, categories="DP")
    t11 = TestCases(prob_id=6, input="4 2\nabba\nab\n", output="2\n")
    t12 = TestCases(prob_id=6, input="4 3\nabba\naba\n", output="3\n")
    p7 = Problem(title="Longest increasing subsequence", statement="Given a sequence of n integers a1,a2,…,an. Print the length of the longest increasing subsequence of this sequence.", input="The first line contains one integer n. The second line contains n integers a1,a2,…,an.", output="Print one integer: the length of the longest increasing subsequence of this sequence.", constraint="1≤n≤106", solved=0, tried=0, categories="DP")
    t13 = TestCases(prob_id=7, input="4\n1 2 3 4\n", output="4\n")
    t14 = TestCases(prob_id=7, input="4\n1 2 3 1\n", output="3\n")
    p8 = Problem(title="Knapsack", statement="Given n items with weights w1,w2,…,wn and values v1,v2,…,vn, and a knapsack of capacity W. Print the maximum total value of items that can be put into the knapsack.", input="The first line contains two integers n and W. The second line contains n integers w1,w2,…,wn. The third line contains n integers v1,v2,…,vn.", output="Print one integer: the maximum total value of items that can be put into the knapsack.", constraint="1≤n≤106", solved=0, tried=0, categories="DP")
    t15 = TestCases(prob_id=8, input="4 10\n1 2 3 4\n1 2 3 4\n", output="10\n")
    t16 = TestCases(prob_id=8, input="4 10\n1 2 3 4\n4 3 2 1\n", output="10\n")
    p9 = Problem(title="Longest path in a tree", statement="Given a tree with n nodes and n−1 edges. Print the length of the longest path in this tree.", input="The first line contains one integer n. Each of the next n−1 lines contains two integers u and v, meaning that there is an edge between nodes u and v.", output="Print one integer: the length of the longest path in this tree.", constraint="1≤n≤106", solved=0, tried=0, categories="Graph")
    t17 = TestCases(prob_id=9, input="4\n1 2\n2 3\n3 4\n", output="3\n")
    t18 = TestCases(prob_id=9, input="4\n1 2\n2 3\n3 4\n", output="3\n")
    p10 = Problem(title="Preorder traversal", statement="Given a tree with n nodes and n−1 edges. Print the preorder traversal of this tree.", input="The first line contains one integer n. Each of the next n−1 lines contains two integers u and v, meaning that there is an edge between nodes u and v.", output="Print one integer: the preorder traversal of this tree.", constraint="1≤n≤106", solved=0, tried=0, categories="Graph")
    t19 = TestCases(prob_id=10, input="4\n1 2\n2 3\n3 4\n", output="1 2 3 4\n")
    t20 = TestCases(prob_id=10, input="4\n1 2\n2 3\n3 4\n", output="1 2 3 4\n")

    db.session.add(p6)
    db.session.add(t11)
    db.session.add(t12)
    db.session.add(p7)
    db.session.add(t13)
    db.session.add(t14)
    db.session.add(p8)
    db.session.add(t15)
    db.session.add(t16)
    db.session.add(p9)
    db.session.add(t17)
    db.session.add(t18)
    db.session.add(p10)
    db.session.add(t19)
    db.session.add(t20)

    db.session.commit()