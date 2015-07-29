import os
import sys
import random
import time
from scaling_timing_bloom_filter import ScalingTimingBloomFilter
import tornado.ioloop
import tornado.testing
import time
from utils import TimingBlock, TestFile

# from bloom import *

minimumTimeUnit = 1000 # milliseconds
sequenceNumber = 1

def sampleExp(rate):
    u = random.random() # [0.0, 1.0)
    x = (-1 * math.log(1 - u)) * float(rate)
    return int(math.ceil(x))

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def deleteFromFilter(bf):
    pass

def generateNewContent():
    global sequenceNumber
    name = "lci:/random/" + str(sequenceNumber)
    sequenceNumber += 1
    return name

def generateRandomContent(n):
    contents = []
    for i in range(n):
        contents.append(generateNewContent())
    return contents

# NOTE: this does not model the cache (i.e., it assumes the router does not
# have a cache, so everything goes into the filter)

def main(args):
    global minimumTimeUnit

    timeSteps = int(args[0]) # * minimumTimeUnit # epochs (input is seconds and then multiplied by the MTU)
    filterSize = int(args[1])
    filterHashes = int(args[2])
    decayRate = float(args[3]) # / minimumTimeUnit    # per second
    arrivalRate = float(args[4]) # / minimumTimeUnit  # per second
    deleteRate = float(args[5]) # / minimumTimeUnit # per second
    randomSampleSize = int(args[6])

    # bf = ScalingTimingBloomFilter(filterSize, filterHashes)
    stbf = ScalingTimingBloomFilter(500, decay_time=4, ioloop=self.io_loop).start()

    contents = []
    falsePositives = {}
    falseNegatives = {}
    counts = {}

    decayCount = sampleExp(decayRate)
    deleteCount = sampleExp(deleteRate)
    arrivalCount = sampleExp(arrivalRate)

    # print arrivalRate, deleteRate, decayRate
    # print arrivalCount, deleteCount, decayCount

    for t in range(timeSteps):
        start = time.time()
        
        for i in range(decayCount):
            print "decaying..."
            deleteFromFilter(bf)
        for i in range(arrivalCount):
            print "arriving... %d" % (arrivalCount - i)
            randomContent = generateNewContent()
            contents.append(randomContent)
            # bf.insert(randomContent)
            stbf += randomContent
        for i in range(deleteCount):
            print "deleting... %d" % (deleteCount - i)
            if len(contents) > 1:
                target = random.sample(contents, 1)[0]
                # bf.delete(target)
                # contents.remove(target)

        decayCount = sampleExp(decayRate)
        arrivalCount = sampleExp(arrivalRate)
        deleteCount = sampleExp(deleteRate)

        # print arrivalCount, deleteCount, decayCount

        falsePositives[t] = []
        falseNegatives[t] = []

        print >> sys.stderr, "Computing false negative probability..."

        # Check to see if decays deleted existing items from the filter
        for content in contents[:randomSampleSize]:
            if not bf.contains(content):
                falseNegatives[t].append(content)

        print >> sys.stderr, "Computing false positive probability..."

        # Check the false positive rate (by randomly generated samples)
        randomContents = generateRandomContent(randomSampleSize)
        for randomElement in randomContents:
            element = randomElement + "/" + str(os.urandom(10))
            if element not in contents and bf.contains(element):
                print >> sys.stderr, "Found false positive :( %s" % (element)
                falsePositives[t].append(element)
            else:
                print >> sys.stderr, "missed a false positive"

        end = time.time()

        fp = float(len(falsePositives[t])) / randomSampleSize
        fn = float(len(falseNegatives[t])) / randomSampleSize

        counts[t] = len(contents)

        print >> sys.stderr, "Time %d %f %f %f %d" % (t, end - start, fp, fn, counts[t])

    for t in range(timeSteps):
        fp = float(len(falsePositives[t])) / randomSampleSize
        fn = float(len(falseNegatives[t])) / randomSampleSize
        print "%d,%f,%f,%d" % (t, fp, fn, counts[t])

if __name__ == "__main__":
    main(sys.argv[1:])

