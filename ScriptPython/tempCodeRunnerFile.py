 differences(L1,L2):
    regex = re.compile("Groupe (.)")
    groupe = regex.search(L2)
    regex2 = re.compile("[^\[\]]")

    
    list1 = regex2.search(L1)
    list2 = regex2.search(L2)

    #1er parametre est une liste de personnage
    if list1!=None :
        print("yep")
        L1 = list1.group(1)
        print(L1)
        L1 = str(L1).split(str=",")
    else: 
        print("no match")

    # 2e parametre est un cluster
    if groupe!=None:
        L2=[int(groupe.group(1))]
    # 2e parametre est une liste de personnage
    else : 
        if list2 != None:
            L2 = list2.group(1)
            L2 = [L2.split(str=',')]        
    print(L1)
    print(L2)
    """
    if(isinstance(L1[0], str) and isinstance(L2[0], str)):
        differences2Selection(L,L3)
    elif(isinstance(L1[0], str) and isinstance(L2[0], int)):
        differencesSelectionCluster(L,L2)
    else:
        raise ValueError("Erreur dans les paramètres")
    """