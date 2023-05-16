for i in range(5) :    #à modifier pour nbre sommet en x
    for j in range(5) : #à modifier pour nbre sommet en y
        for k in range (-1,2):
            for l in range (-1,2) :
                if k==0 and l==0 :
                    continue
                print(i+k," ",j+l," pour ",i," ",j)