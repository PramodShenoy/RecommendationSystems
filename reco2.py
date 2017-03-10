from math import sqrt,pow
# mock dataset for movie reviews

critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
'The Night Listener': 4.5, 'Superman Returns': 4.0,
'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0},
'Pramod':{'Snakes on a Plane':2.5,'You, Me and Dupree':2.0,'Superman Returns':4.5,'The Night Listener':3.0}}

def invertcritics():
	res={}
	for person in critics:
		for item in critics[person]:
			res.setdefault(item,{})
			res[item][person]=critics[person][item]

	return res


def euclidean_dist(prefs,p1,p2):
	si={}
	#finding common ratings
	for item in prefs[p1]:
		if item in prefs[p2]:
			si[item]=1

	#no ratings in common
	if(len(si)==0):
		return 0
	
	func=sum([pow(prefs[p1][item]-prefs[p2][item],2) for item in prefs[p1] if item in prefs[p2]])
	return 1/(1+func)
	
#print euclidean_dist(critics,'Lisa Rose','Jack Matthews')

def pearson_score(prefs,p1,p2):
	si={}
	#list of mutually rated items
	for item in prefs[p1]:
		if item in prefs[p2]:
			si[item]=1
	n=len(si)

	if n==0:
		return 0

	sum1=sum([prefs[p1][it] for it in si])
	sum2=sum([prefs[p2][it] for it in si])

	#finding sum of squares
	sum1sq=sum([pow(prefs[p1][it],2) for it in si])		
	sum2sq=sum([pow(prefs[p2][it],2) for it in si])

	#sum of products
	prod_sum=sum([prefs[p1][it]*prefs[p2][it] for it in si])

	#Pearson score
	num=prod_sum-((sum1*sum2)/n)
	den=sqrt((sum1sq-pow(sum1,2)/n)*(sum2sq-pow(sum2,2)/n))
	if den != 0:
		r=num/den
		return r
	else:
		return 0
#print pearson_score(critics,'Lisa Rose','Gene Seymour')

def matches(prefs,p,n=3,similarity=pearson_score):
	scores=[(similarity(prefs,p,other),other) for other in prefs if other!=p]

	scores.sort()
	scores.reverse()
	return scores[0:]

movies=invertcritics()

print matches(movies,'Superman Returns')

#inverting the dictionary critics


def getreco(prefs,p,similarity=pearson_score):
	totals={}
	simsum={}
	for other in prefs:
		if other==p:
			continue
		sim=similarity(prefs,p,other)
		if sim<=0:
			continue
		# show me movies i haven't watched yet
		for item in prefs[other]:

			if item not in prefs[p] or prefs[p][item]==0:
				#Similarity * score
				totals.setdefault(item,0)
				totals[item]+=prefs[other][item]*sim
				#find sum of similarities
				simsum.setdefault(item,0)
				simsum[item]+=sim

	#getting normalized list
	rankings=[(total/simsum[item],item) for item,total in totals.items()]

	rankings.sort()
	rankings.reverse()
	return rankings

#print getreco(critics,'Pramod')
