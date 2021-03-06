import datetime
import sys
import codecs
import multiprocessing
from multiprocessing import Pool, Manager

        
def processQuestion(qCount, lock, index, entityList, qList):        
    for qStr in qList:
        for eStr in entityList:
            if qStr.find(eStr) != -1:
                lock.acquire()
                qCount.value += 1
                print(str(qCount.value) + ' ' + qStr)
                fo = open(sys.argv[3], 'a', encoding='utf8')
                fo.write(qStr.strip() + ' | ' + eStr +'\n')
                fo.close()
                lock.release()
                break
        

if __name__ == '__main__':

    qCount = Manager().Value('i', 0)
    lock = Manager().Lock()

    fe = open(sys.argv[1], 'r', encoding='utf8')
    fq = open(sys.argv[2], 'r', encoding='utf8')
    
    thread = 20
    
    if len(sys.argv) >= 5:
        thread = int(sys.argv[4])


    qCache = set()
    qMaxLen = 0
    for line in fq:
        qStr = line
        qCache.add(qStr.lower())
        qMaxLen = max(len(qStr), qMaxLen) 

    questionList = list(qCache)

    setEntity = set()

    for nS in list(fe):
        setEntity.add(nS.strip().lower())
       
    lEntity = list(setEntity)

    lEntity.sort(key = lambda x : len(x), reverse = True)

    print('Entity list is sorted!')

    lenQuestionList = len(questionList)
    lenSubQuestion = int(lenQuestionList / thread)

    p = Pool(thread + 1)
    for i in range(thread):
        p.apply_async(processQuestion, (qCount, lock, i, lEntity, questionList[i * lenSubQuestion : (i + 1) * lenSubQuestion]))  #增加新的进程
    
    p.apply_async(processQuestion, (qCount, lock, thread, lEntity, questionList[thread * lenSubQuestion :]))
    p.close() # 禁止增加新的进程
    p.join()
    print('pool process done')

    fe.close()
    fq.close()

