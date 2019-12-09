from board_generator import genBoard
import os

ps = [3]
qs = [3]

base = "../boards_for_report/"

for p, q in zip(ps, qs):
    for m in range(0,45):
        dir_name = "boards_p_"+str(p)+"_q_"+str(q)+"/m_"+str(m)+"/"
        
        if not os.path.exists(base+dir_name):
            os.mkdir(base+dir_name)

        for i in range(20):
            genBoard(p, q, m, base+dir_name+"board_"+str(i)+".txt")
    

        