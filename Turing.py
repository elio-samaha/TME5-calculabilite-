#=====================================================================#
# UE Calculabilite L3                                                 #
# TME Machines de Turing : Machines de Turing deterministes           #
# Mathieu.Jaume@lip6.fr                                               #
#=====================================================================#


#=====================================================================#
# Machines de Turing deterministes a 1 bande                          #
#=====================================================================#


# Fonction associee a une liste representant une fonction sur un domaine fini
#----------------------------------------------------------------------------

def assoc_f(lf,x):
    """ list[alpha*beta] * alpha -> beta """
    for (xf,yf) in lf:
        if xf == x:
            return yf
    return None

# Machine de Turing deterministe a 1 bande
#-----------------------------------------
#
# M = (d,q0,qok,qko)
# d = ((q,a),(q',a',m))
#

# exemple

l_M_ex1 = [((0,"A"),(1,"A","R")), ((0,"a"),(3,"a","R")), ((0,"b"),(3,"b","R")),
           ((0,"B"),(3,"B","R")), ((1,"A"),(3,"A","R")), ((1,"B"),(2,"B","R")),
           ((1,"a"),(1,"b","R")), ((1,"b"),(1,"a","R"))]

M_ex1 =(l_M_ex1,0,2,3)


# Affichage d'une configuration pour une machine de Turing a 1 bande
#-------------------------------------------------------------------

def print_config_1(L,t,q,qok,qko):
    for s in L[:t]:
        print(s,end='')
    print("|",end='')
    if q == qok:
        print("ok",end='')
    elif q == qko:
        print("ko",end='')
    else:
        print(q,end='')
    print("|",end='')
    for s in L[t:]:
        print(s,end='')
    print(" ")


# Execution d'une machine de Turing deterministe a 1 bande
#---------------------------------------------------------

def exec_MT_1(M,L,i):
    # M : machine de Turing deterministe a 1 bande
    # L : liste representant la bande initiale
    # i0 : position initiale de la tete de lecture
    (delta , q0, qok, qko) = M
    curr = q0
    i0 = i
    Mv = "R"
    print_config_1(L,i0,curr,qok,qko)
    while curr != qko and curr != qok :
        if assoc_f(delta,(curr,L[i0])) == None :
            curr = qko
            break
        (curr, L[i0], Mv) = assoc_f(delta,(curr,L[i0]))
        if Mv == "R" :
            i0 += 1

        if Mv == "L" :
            i0 -= 1

        if i0 >= len(L) :
            L.append("Z")
        if i0 < 0 :
            i0 = 0
        print_config_1(L,i0,curr,qok,qko)

    return ((curr == qok),i0,L)

# Exo 2 (Fait deja en Amphi mais avec 2 bandes. Pour une bande on va faire des allers retours : 
#A chaque fois qu on lit un "a" on le marque en X et on va aller chercher un "b" si on ne trouve pas de b on va vers qko 
#et si on a plus de "a" mais qu il reste des "b" on va vers qko et sinon si on a coche tout les "a" avec des X 
#et tous les "b" avec des Y c est que c est bon, on part vers qok)


l_ex2 = [((0,"Z"),(1,"Z","R")), # cas ou c est bon tout a ete coche ou si c est le mot vide (qok = 1)
         ((0,"a"),(2,"X","R")), ((0,"b"),(3,"Y","R")), # si on lit un a donc on doit chercher un b et si on lit un b on doit chercher un a 
         ((0,"X"),(0,"X","R")),((0,"Y"),(0,"Y","R")),  #Pour bien se placer dans la bande on passe par ce qu on a deja lu
         ((2,"a"),(2,"a","R")), ((3,"b"),(3,"b","R")),((3,"X"),(3,"X","R")), ((3,"Y"),(3,"Y","R")), ((2,"Y"),(2,"Y","R")),
             ((2,"X"),(2,"X","R")),  #quand on a deja lu la 1ere lettre et on cherche l'autre on ne doit pas changer la bande tant qu on pas trouver l autre lettre
         ((2,"b"),(4,"Y","L")), ((3,"a"),(5,"X","L")), # On a trouve l autre caractere (si on est en q2 on doit trouver un "b" , en q3 un "a")
         ((4,"a"),(4,"a","L")),((4,"Y"),(4,"Y","L")), ((5,"b"),(5,"b","L")), ((5,"X"),(5,"X","L")), # On se replace (en cherchant la 1ere case non lu selon si on est sur q4 ou q5, cf ligne suivante), 
         ((4,"X"),(0,"X","R")), ((5,"Y"),(0,"Y","R"))] # si on est a q4 on se replace en trouvant le 1er "a" non lu, celui ci se trouve apres (mais peut etre pas directement apres : ex abba) le dernier X qu on a mit (de meme pour q5, b et Y)

M_ex2 = (l_ex2 , 0 , 1 , 6) #qko = 6

# Exo 3


#============================================================#
# Composition de machines de Turing                          #
#============================================================#

# Machines de Turing utiles pour le TME
#---------------------------------------

# complement binaire et repositionnement de la tete de lecture au debut
# bande = mot binaire  se terminant par Z

d_compl_bin = [((0,"0"),(0,"1","R")), ((0,"1"),(0,"0","R")),\
               ((0,"Z"),(1,"Z","L")), ((1,"0"),(1,"0","L")),\
               ((1,"1"),(1,"1","L")), ((1,"Z"),(2,"Z","R"))]

M_compl_bin = (d_compl_bin,0,2,3)

# successeur d'un entier en representation binaire (bit de poids faibles a gauche)
# et repositionnement de la tete de lecture sur le bit de poids faible
# bande = mot binaire avec bits de poids faibles a gauche et se terminant par Z

d_succ_bin = [((0,"0"),(1,"1","L")), ((0,"1"),(0,"0","R")),\
              ((0,"Z"),(2,"1","R")), ((1,"0"),(1,"0","L")),\
              ((1,"1"),(1,"1","L")), ((1,"Z"),(3,"Z","R")),\
              ((2,"Z"),(1,"Z","L"))]

M_succ_bin = (d_succ_bin,0,3,4)

# fonction identite

M_id =([],0,0,1)

# Fonction qui construit une machine de Turing permettant de determiner
# si le symbole sous la tete de lecture est le caractere x et ne modifie
# pas la position de la tete de lecture
# C'est la MT qui accepte le langage { x }

def make_test_eq(c,alphabet):
    d = []
    for x in alphabet:
        if c==x:
            d = d + [((0,c),(1,c,"R"))]
        else:
            d = d + [((0,x),(2,x,"R"))]
        d = d + [((1,x),(3,x,"L")), ((2,x),(4,x,"L"))]
    M = (d,0,3,4)
    return M

# exemple

M_eq_0 = make_test_eq("0",["0","1","Z"])

def make_test_neq(c,alphabet):
    (d,q0,qok,qko) = make_test_eq(c,alphabet)
    return (d,q0,qko,qok)

M_neq_1 = make_test_neq("1",["0","1","Z"])

# deplacement de la tete de lecture a droite :

def make_MTright(alphabet):
    d = []
    for a in alphabet:
        d = d + [((0,a),(1,a,"R"))]
    M = (d,0,1,2)
    return M

M_Right_bin = make_MTright(["0","1","Z"])

# (propagation du bit de signe) : duplication du dernier bit d'un mot binaire


d_prop1 = [((0,"0"),(1,"0","R")), ((0,"1"),(2,"1","R")), \
           ((1,"0"),(1,"0","R")), ((1,"1"),(2,"1","R")), ((1,"Z"),(3,"0","L")),\
           ((2,"0"),(1,"0","R")), ((2,"1"),(2,"1","R")), ((2,"Z"),(3,"1","L")),\
           ((3,"0"),(3,"0","L")), ((3,"1"),(3,"1","L")), ((3,"Z"),(4,"Z","R"))]


M_prop1 =(d_prop1,0,4,5)

# Composition de machines de Turing : sequence
#---------------------------------------------

def exec_seq_MT_1(M1,M2,L,i1):
    (b,i2,L2)=exec_MT_1(M1,L,i1)
    if b:
        return exec_MT_1(M2,L2,i2)
    else:
        return (b,i2,L2)

def make_seq_MT(M1,M2):
    # M1,M2 : machines de Turing deterministes a 1 bande
    return

# Composition de machines de Turing : conditionnelle
#---------------------------------------------------

def exec_cond_MT_1(MC,M1,M2,L,i0):
    (bc,ic,Lc)=exec_MT_1(MC,L,i0)
    if bc:
        return exec_MT_1(M1,Lc,ic)
    else:
        return exec_MT_1(M2,Lc,ic)


def make_cond_MT(MC,M1,M2):
    # MC, M1, M2 : machines de Turing deterministes a 1 bande
    return

# Composition de machines de Turing : boucle
#-------------------------------------------

def exec_loop_MT_1(MC,M,L,i0):
    (bc,ic,Lc)=exec_MT_1(MC,L,i0)
    if bc:
        (bM,iM,LM) = exec_MT_1(M,Lc,ic)
        if bM:
            return exec_loop_MT_1(MC,M,LM,iM)
        else:
            return (False,iM,LM)
    else:
        return (True,ic,Lc)

def make_loop_MT(MC,M):
    # MC,M : machines de Turing deterministes a 1 bande
    return

#======================================================================#
# Machines de Turing deterministes a k bandes                          #
#======================================================================#

# Machine de Turing deterministe a k bandes
#
# M = (d,q0,qok,qko)
#
# d = [((q,(a1,...,an)),(q',(a'1,...,a'n),(m1,...,mn))),...]
#
# bandes : L = [L1,...,Ln]
#

# Affichage d'une configuration pour une machine de Turing a k bandes
#--------------------------------------------------------------------

def print_config_k(L,T,q,qok,qko,k):
    for i in range(k):
        print_config_1(L[i],T[i],q,qok,qko)


def exec_MT_k(M,k,L,T):
    # M : machine de Turing deterministe a k bandes
    # k : nombre de bandes
    # L : liste des representations des bandes initiales
    # T : positions initiales des k tetes de lecture
    return

# mots sur {a,b} contenant autant de a que de b
#

d2_ex1 = [((0,("a","Z")),(1,("a","X"),("R","R"))),\
          ((0,("b","Z")),(2,("b","X"),("R","R"))),\
          ((0,("Z","Z")),(3,("Z","Z"),("S","S"))),\
          ((1,("a","X")),(1,("a","X"),("R","R"))),\
          ((1,("a","Z")),(1,("a","Z"),("R","R"))),\
          ((1,("b","Z")),(1,("b","Z"),("R","L"))),\
          ((1,("b","X")),(2,("b","X"),("R","R"))),\
          ((1,("Z","X")),(3,("Z","X"),("S","S"))),\
          ((2,("a","X")),(1,("a","X"),("R","R"))),\
          ((2,("a","Z")),(2,("a","Z"),("R","L"))),\
          ((2,("b","Z")),(2,("b","Z"),("R","R"))),\
          ((2,("b","X")),(2,("b","X"),("R","R"))),\
          ((2,("Z","X")),(3,("Z","X"),("S","S")))]


M2_ex1 = (d2_ex1,0,3,4)
