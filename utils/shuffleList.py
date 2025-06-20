import random

'''In Dokumentation auch benannt als SuS Durchmischen
'''
def shuffleList(listToShuffle:list):
    random.shuffle(listToShuffle)
    return listToShuffle

if __name__ == "__main__":
    testList = [1,2,3,4,5,6,7,8,9]
    shuffleList(testList)
    print(testList)