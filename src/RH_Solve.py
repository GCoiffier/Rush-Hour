
##Variables globales

# Veh=plb.array([[2,True,1],[3,False,3],[4,False,4],[3,True,4],[2,False,2],[2,False,0],[2,True,2],[3,True,0],[2,True,5]])
# Pos=[1,0,0,3,3,1,1,0,3]
# Veh=plb.array([[2,1,2],[2,0,0],[3,1,0],[2,1,1],[3,0,4],[2,0,2],[2,0,3],[2,1,3],[2,1,5],[2,0,3],[2,1,4]])
# Pos=[0,0,1,2,0,2,2,0,0,4,4]
Veh=plb.array([[2,1,2],[3,0,0],[2,1,0],[2,0,2],[2,1,0],[3,1,3],[3,0,4],[2,0,5],[2,1,5],[2,0,3],[2,1,5]])
Pos=[1,1,0,0,3,1,1,2,0,4,4]

taille=6

nmax=taille-min(Veh[:,0])
nveh=len(Veh)
posfin=taille-Veh[0][0]

##Fonctions

def PostoCode(Pos):
    coeff=nmax+1
    s=0
    n=1
    for x in Pos:
        s+=n*x
        n*=coeff
    return s

def CodetoPos(code):
    coeff=nmax+1
    L=[]
    q=code//coeff
    while q!=0:
        L.append(code%coeff)
        code=q
        q=code//coeff
    L.append(code%coeff)
    return L

def CodetoPos2(code):
    sortie=[]
    coeff=nmax+1
    for _ in range(nveh):
        sortie.append(code%coeff)
        code//=coeff
    return sortie
    
def grille(pos):
    mat=[[True for _ in range(taille)] for _ in range(taille)]
    for v in range(nveh):
        for k in range(Veh[v][0]):
            if Veh[v][1]: #Si horriz
                mat[Veh[v][2]][pos[v]+k]=False
            else: #Si vertic
                mat[pos[v]+k][Veh[v][2]]=False
    return mat

def isFinal(pos):
    return pos[0]==posfin

def libre(mat,v,p):
    l1,l2=False,False
    if Veh[v][1]:
        if p>0 and mat[Veh[v][2]][p-1]: l1=True
        if p+Veh[v][0]<taille and mat[Veh[v][2]][p+Veh[v][0]]: l2=True
    else:
        if p>0 and mat[p-1][Veh[v][2]]: l1=True
        if p+Veh[v][0]<taille and mat[p+Veh[v][0]][Veh[v][2]]: l2=True
    return (l1,l2)

def accessibles(mat,pos,code):
    voisins=col.deque()
    coeff=nmax+1
    for v in range(nveh):
        p=pos[v]
        (l1,l2)=libre(mat,v,p)
        if l1: voisins.append(code-coeff**v)
        if l2: voisins.append(code+coeff**v)
    return voisins

def accessibles2(mat,pos,code):
    voisins=col.deque()
    coeff=nmax+1
    for v in range(nveh):
        p=pos[v]
        i=1
        if Veh[v,1]:
            while p-i>=0 and mat[Veh[v,2]][p-i]:
                voisins.append(code-i*(coeff**v))
                i+=1
            i=0
            while p+i+Veh[v,0]<taille and mat[Veh[v,2]][p+Veh[v,0]+i]:
                voisins.append(code+(i+1)*(coeff**v))
                i+=1
        else:
            while p-i>=0 and mat[p-i][Veh[v,2]]:
                voisins.append(code-i*(coeff**v))
                i+=1
            i=0
            while p+i+Veh[v,0]<taille and mat[p+Veh[v,0]+i][Veh[v,2]]:
                voisins.append(code+(i+1)*(coeff**v))
                i+=1
    return voisins

def chemin(code_fin,peres):
    c=code_fin
    c0=PostoCode(Pos)
    L=[c]
    while c != c0:
        c=peres[c]
        L.append(c)
    return L[::-1]

def parcours():
    peres=plb.zeros((nmax+1)**nveh,int)-1
    vus=plb.zeros((nmax+1)**nveh,bool)
    c=PostoCode(Pos)
    p=Pos
    L=col.deque()
    L.append(c)
    final=False
    non_vide=True
    while non_vide and not(final):
        try:
            c=L.popleft()
            if not(vus[c]):
                vus[c]=True
                p=CodetoPos2(c)
                if isFinal(p):
                    final = True
                else:
                    mat=grille(p)
                    voisins=accessibles(mat,p,c)
                    for x in voisins:
                        if peres[x]==(-1):peres[x]=c
                    L.extend(voisins)
        except IndexError:
            non_vide=False
    if final:
        return chemin(c,peres)
    return []

def parcours2():
    peres=plb.zeros((nmax+1)**nveh,int)-1
    vus=plb.zeros((nmax+1)**nveh,bool)
    c=PostoCode(Pos)
    p=Pos
    L=col.deque()
    L.append(c)
    final=False
    non_vide=True
    while non_vide and not(final):
        try:
            c=L.popleft()
            if not(vus[c]):
                vus[c]=True
                p=CodetoPos2(c)
                if isFinal(p):
                    final = True
                else:
                    mat=grille(p)
                    voisins=accessibles2(mat,p,c)
                    for x in voisins:
                        if peres[x]==(-1):peres[x]=c
                    L.extend(voisins)
        except IndexError:
            non_vide=False
    if final:
        return chemin(c,peres)
    return []

def deplacement(p1,p2):
    for i in range(nveh):
        d=p2[i]-p1[i]
        if d!=0: return i,d

def mouvements(L):
    n=len(L)
    mvts=plb.zeros((n-1,2),int)
    p2=CodetoPos2(L[0])
    for k in range(n-1):
        p1,p2=p2,CodetoPos2(L[k+1])
        cp=deplacement(p1,p2)
        mvts[k]=plb.array(cp)
    return mvts

## Execution
# chem=parcours()
chem=parcours2()
mvts=mouvements(chem)
nb_mvts=len(mvts)

## Animation
cote=50
intervalle=16777215-1000000
pas=intervalle/max(nveh-1,29)
couleur=["#"+("%06x"%int(k*pas)) for k in range(nveh)]
step=0

fen=Tk()
fen.title('Déplacements')
canevas=Canvas(fen,height=cote*taille, width=cote*taille)
canevas.pack() 
incr=cote/10
stop=True

for k in range(nveh):
    if Veh[k,1]:
        _=canevas.create_rectangle(cote*Pos[k],cote*Veh[k,2],cote*(Pos[k]+Veh[k,0]),cote*(1+Veh[k,2]),fill=couleur[k])
    else:
        _=canevas.create_rectangle(cote*Veh[k,2],cote*Pos[k],cote*(1+Veh[k,2]),cote*(Pos[k]+Veh[k,0]),fill=couleur[k])


def anime():
    global step
    i=step//10
    if step<nb_mvts*10:
        k=mvts[i,0]
        dep=mvts[i,1]
        if Veh[k,1]:
            canevas.move(k+1,dep*incr,0)
        else:
            canevas.move(k+1,0,dep*incr)
        canevas.update()
        step+=1
        fen.after(80, anime)

def anime2():
    global step,stop
    i=step//10
    if step<nb_mvts*10:
        k=mvts[i,0]
        dep=mvts[i,1]
        if Veh[k,1]:
            canevas.move(k+1,dep*incr,0)
        else:
            canevas.move(k+1,0,dep*incr)
        canevas.update()
        step+=1
        if step%10 != 0:        
            fen.after(80, anime2)
        else:
            stop=True

def declenche(event):
    global stop
    if stop:
        stop=False
        anime()

def declenche2(event):
    global stop
    if stop:
        stop=False
        anime2()

canevas.bind("<1>",declenche) 
canevas.bind("<3>",declenche2)

## Lancement
print("Nombre de mouvements :",nb_mvts)
fen.mainloop()