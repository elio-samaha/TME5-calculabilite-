from Turing import *

def position_tete_lecture(i, L):
    for l in L[0:i]:
        if l!="Z":
            return False
    return L[i]!="Z"
    
def contenu_bande(i,L,L_init):
    return L[i::]==L_init 
	
print("\n\n----------------------------------------------\n\n")
print("Test 1 : Machine Misneg")
print("---------------------------")
(b1,i1,L1)=exec_MT_1(M_isneg,["0","0","1","0","Z"],0)
assert b1==False, "Erreur dans l'etat final de la machine"
assert position_tete_lecture(i1,L1), "Erreur: la tete de lecture n'est pas repositionnee au debut de w"
assert contenu_bande(i1,L1,["0","0","1","0","Z"]), "Erreur: le contenu de la bande a ete change"

print("\n\n----------------------------------------------\n\n")
print("Test 2 : Machine Misneg")
print("---------------------------")
(b1,i1,L1)=exec_MT_1(M_isneg,["1","0","1","0","1","Z"],0)
assert b1==True, "Erreur dans l'etat final de la machine"
assert position_tete_lecture(i1,L1), "Erreur: la tete de lecture n'est pas repositionnee au debut de w"
assert contenu_bande(i1,L1,["1","0","1","0","1","Z"]), "Erreur: le contenu de la bande a ete change"

print("\n\n----------------------------------------------\n\n")
print("Test 3 : Machine Misneg")
print("---------------------------")
(b1,i1,L1) = exec_MT_1(M_isneg,["1","0","1","0","0","Z"],0)
assert b1 == False, "Erreur dans l'etat final de la machine"
assert position_tete_lecture(i1,L1),"Erreur: la tete de lecture n'est pas repositionnee au debut de w"
assert contenu_bande(i1,L1,["1","0","1","0","0","Z"]), "Erreur: le contenu de la bande a ete change"
print("\n\n----------------------------------------------\n\n")
print("Test 4 : Machine Misneg")
print("---------------------------")
(b1,i1,L1) = exec_MT_1(M_isneg,["0","0","1","0","1","Z"],0)
assert b1 == True, "Erreur dans l'etat final de la machine"
assert position_tete_lecture(i1,L1), "Erreur: la tete de lecture n'est pas repositionnee au debut de w"
assert contenu_bande(i1,L1,["0","0","1","0","1","Z"]), "Erreur: le contenu de la bande a ete change"

