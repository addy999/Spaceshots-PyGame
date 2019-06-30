def totalNonClosestMomentum(self,planets,index_of_closest):#self is space craft
    total = 0
    for num in range(len(planets)):
        if(num != index_of_closest):
            total += (planets[num.mass])*(planets[num].velocity)

    
    