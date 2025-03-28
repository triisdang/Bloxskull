import random
gamelist = ["17625359962","10449761463","18687417158","7041939546","9391468976","17065532662","142823291","6516141723","16732694052"]
userlist = ["1","2","3","140258990","4061250786","4061250786","1241352401","22718068"]
badgelist = ["2127715318","2127965819","2127966064","445262853167408","2816915468916900","2125253106","2124935409"]
grouplist = ["3461453","35509406","32380007","10720185","3692974","3049798","15760185"]
def pickrandom(id):
    if id == "game" :
        return(random.choice(gamelist))
    elif id == "user" :
        return(random.choice(userlist))
    elif id == "badge" :
        return(random.choice(badgelist))
    elif id == "group" :
        return(random.choice(grouplist))
    else :
        return("Unkown option")