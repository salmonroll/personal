import copy, collections, logging, random, sys, time

class Veterinarian(object):
    def __init__(self, *args):
        super(Veterinarian, self).__init__(*args)

    def __init__(self, startingSet):
        # initialize veterinarian container with defined starting Set
        self.container = startingSet
        self.received  = []
        self.draws     = 0

class Stat(object):
    def __init__(self, *args):
        super(Stat, self).__init__(*args)
    
    def __init__(self, sheep, boar, cattle):
        # initialize from a result set
        self.sheep  = sheep
        self.boar   = boar
        self.cattle = cattle
        
    def __repr__(self):
        return '<s:{0}, b:{1}, c:{2}>'.format(self.sheep, self.boar, self.cattle)

    def __add__(self, other):
        return Stat(self.sheep + other.sheep, self.boar + other.boar, self.cattle + other.cattle)
    
    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)
    
    def __div__(self, other):
        return Stat(self.sheep / other, self.boar / other, self.cattle / other)
           
def drawAnimals(vet):
    logging.debug('--- STARTING ROUND %s ---', vet.draws + 1)
    # Shuffle animals, then pick the first 2
    random.shuffle(vet.container)
    logging.info('Shuffled %s animals', len(vet.container))
    logging.debug('Current animal list: %s', vet.container)
    a1 = vet.container.pop()
    a2 = vet.container.pop()
    logging.info('Picked 2 animals: %s & %s', a1, a2)
    if (a1 == a2):
        # Collect one animal, put other back
        logging.info('Animals match! Receiving %s', a1)
        vet.received.append(a1)
        vet.container.append(a2)
    else:
        # Put both back
        logging.info('Animals different! Replacing both')
        vet.container.append(a1)
        vet.container.append(a2)
    # Cleanup and increment counter
    vet.draws += 1
    logging.debug('--- ENDING ROUND %s ---', vet.draws)


def runOnce(animalSet, numRounds):
    # Run one set of animal drawing simulations
    vet = Veterinarian(copy.copy(animalSet))
    results = []
    for i in range(numRounds):
        drawAnimals(vet)
        count = collections.Counter(vet.received)
        results.append(Stat(count['s'], count['b'], count['c']))
    logging.info('SUMMARY: Received %s animals', vet.received)
    logging.debug('RESULTS: %s', results)
    return results

def main():
    # CONFIG
    logging.basicConfig(stream=sys.stdout, level=logging.WARN)
    originalAnimalSet = ['s', 's', 's', 's', 'b', 'b', 'b', 'c', 'c']
    animalSet = originalAnimalSet
    numGames = 1000000
    numRounds = 14
    resultSet = [Stat(0, 0, 0)] * numRounds
    # SIMULATE
    timeStart = time.time()
    print 'Simulating {} games of {} rounds with animal set:'.format(numGames, numRounds)
    print originalAnimalSet
    for i in range(numGames):
        resultSet = map(sum, zip(resultSet, runOnce(animalSet, numRounds)))
    timeSimulate = time.time()
    # CALCULATE STATS
    averageStats = [x / float(numGames) for x in resultSet]
    timeCalculate = time.time()
    print '--- SUMMARY ---'
    for i in range(numRounds-1, -1, -1):
        print '{} rounds in play - S:{} B:{} C:{}'.format(i+1, averageStats[i].sheep, averageStats[i].boar, averageStats[i].cattle)
    logging.debug('Time for simulation: %ss', timeSimulate-timeStart)
    logging.debug('Time for calcuation: %ss', timeCalculate-timeSimulate)
    print 'Took {}s'.format(timeCalculate-timeStart)

if __name__ == "__main__":
    main()