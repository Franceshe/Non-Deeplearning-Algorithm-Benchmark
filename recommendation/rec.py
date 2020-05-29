# A dictionary of movie critics and their ratings of a small set of movies

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
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}


# Euclidean distance score

from math import sqrt

# Return a distance-based similarity score for person 1 and person 2

def sim_distance(prefs, person1, person2):
    si = dict()
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1

    if len(si)==0: return 0

    # Add up the squares of all the differences
    sum_of_squares = sum([pow(prefs[person1][item]-prefs[person2][item],2) for item in prefs[person1] if item in prefs[person2]])
    return (1/(1+sum_of_squares))

sim_distance(critics, 'Lisa Rose', 'Gene Seymour')

"""Pearson correlation score - works better where the data isn't well normalized 
e.g. if critics are routinely more harsh than average. Pearson correlation score corrects for grade inflation (can still be
perfect correlation if the difference between scores is consistent) whereas Euclidean score will say two critics are dissimilar
because one is consistently harsher than the other, even if their tastes are very similar. 
Pearson correlation coefficient - how much variables change together divided by the product of how much they vary individually"""

# Returns the Pearson correlation coefficient for person 1 and person 2

def sim_pearson(prefs, p1, p2):
    si = dict()
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item]=1
            
    if len(si) == 0: return 0
    
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
    
    sum1Sq = sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it],2) for it in si])
    
    pSum = sum([prefs[p1][it]*prefs[p2][it] for it in si])
    
    num = pSum - ((sum1*sum2)/len(si))
    den = sqrt((sum1Sq - pow(sum1,2)/len(si))*(sum2Sq-pow(sum2,2)/len(si)))
    if den == 0: return 0
    
    I = num/den
    
    return I

sim_pearson(critics, 'Lisa Rose', 'Gene Seymour')

# To get an ordered list of people with similar tastes to the specified person

def topmatches(prefs, person, n=5, similarity = sim_pearson):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other!=person]
    
    scores.sort()
    scores.reverse()
    return scores[0:n]

topmatches(critics, 'Toby', n=3)

# Get recommendations for a person by using a weighted average of every other user's rankings

def getrecommendations(prefs, person, similarity = sim_pearson):
    totals = dict()
    simSums = dict()
    
    for other in prefs:
        if other==person: continue
        sim = similarity(prefs, person, other)
        
        if sim<=0: continue
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item]==0:
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
                
                simSums.setdefault(item,0)
                simSums[item]+=sim
                
    rankings = [(total/simSums[item],item) for item,total in totals.items()]
    
    rankings.sort()
    rankings.reverse()
    
    return rankings

getrecommendations(critics, 'Toby')

def transformprefs(prefs):
    result=dict()
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            result[item][person] = prefs[person][item]
        
    return result

movies = transformprefs(critics)
topmatches(movies, 'Superman Returns')
getrecommendations(movies, 'Just My Luck')

#Use transformprefs to give a list of items with their user rating, then loop over every item through topmatches to get most 
# similar items along with their similarity scores
# Item-based filtering outperforms user-based filtering in sparse datasets, perform equally in dense datasets. Item-based filtering
# is significantly faster on a large dataset
def calculateSimilarItems(prefs, n=10):
    result = dict()
    itemPrefs = transformprefs(prefs)
    c=0
    for item in itemPrefs:
        c+=1
        if c%100==0: print(c, len(itemPrefs))
        scores = topmatches(itemPrefs, item, n=n, similarity = sim_distance)
        result[item] = scores
    return result

itemsim = calculateSimilarItems(critics)
print(itemsim)

# Give recommendations using the item similarity dictionary without going through the whole database

def getRecommendedItems(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = dict()
    totalSim = dict()
    
    # Loop over items rated by this user
    for item, rating in userRatings.items():
        # Loop over items similar to this one
        for similarity, item2 in itemMatch[item]:
            # Ignore if this user has already rated this item
            if item2 in userRatings: continue
            
            # Weighted sum of rating times similarity
            scores.setdefault(item2,0)
            scores[item2]+=similarity*rating
            
            # Sum of all the similarities
            totalSim.setdefault(item2,0)
            totalSim[item2]+=similarity
            
    # Divide each total score by total weighting to get an average
    rankings = [(score/totalSim[item],item) for item,score in scores.items()]
        
    # Return the rankings from highest to lowest
    rankings.sort()
    rankings.reverse()
    return rankings    

getRecommendedItems(critics, itemsim, 'Toby')    


def loadMovieLens(path = '\\data\\movielens'):
    movies = dict()
    for line in open(path+'/u.item'):
        id, title = line.split('|')[0:2]
        movies[id] = title
        
    prefs = dict()
    for line in open(path+'/u.data'):
        user, movieid, rating, ts = line.split('\t')
        prefs.setdefault(user,{})
        prefs[user][movies[movieid]] = float(rating)
    return prefs

prefs=loadMovieLens()
#prefs['87']
#getrecommendations(prefs, '87')[0:30]
itemsim = calculateSimilarItems(prefs, n=50)
getRecommendedItems(prefs, itemsim, '87')[0:30]