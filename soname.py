import json
import subprocess
import time
import yaml
from retrying import retry
from subprocess import PIPE

def main():
    try:
        if MODEL == 0:            
            for n in tuple(BANK[0]):                
                    soName(n)
        if MODEL == 1:
            for n in tuple(BANK[0]):
                for m in tuple(BANK[1]):                
                    soName(n + m)
    except subprocess.CalledProcessError as e:
        log(e)
        log(str(e.stderr, 'utf-8'))

def soName(thename):
    time.sleep(0.3)
    if getBidNameInfo(thename) == 0:
        log("已拍卖未使用名称:"+thename)
        return 0
    if getChainNameInfo(thename) == 0 :
        log("已使用名称:"+thename)
        return 0
    log("可用:"+thename)
    writeToFile(thename+"\n")
    return 1

@retry
def getBidNameInfo(thename):
    results = cleos('get table eosio eosio namebids --key-type name --limit 1 --lower-bound ' + thename)   
    results = json.loads(results.stdout.decode('utf-8'))
    rows = results['rows']
    for p in rows:
        if thename == p['newname'] and p['high_bid'] < 0:
           return 0
    return 1

def getChainNameInfo(thename):    
    try:
        results = cleos('get account ' + thename)
    except subprocess.CalledProcessError as e:
        return 1
    return 0

def log(message):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log = '{} - {}\n'.format(current_time, message)
    print(log)

def writeToFile(thename):
    f = open(SAVE_FILE,'a')
    f.write(thename)
    f.close()

def cleos(args):
    if isinstance(args, list):
        command = ['{} {} '.format(CLEOS_DIR, CLEOS_URL)]
        command.extend(args)
    else:
        command = CLEOS_DIR + CLEOS_URL + args
    results = subprocess.run(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True, check=True)

    return results

if __name__ == '__main__':
    f = open('config.yaml','r',encoding='utf-8')
    temp = yaml.load(f.read())
    CLEOS_DIR  = temp["eosc"]
    CLEOS_URL  = " -u " + temp["apiurl"] + " "
    MODEL = temp["model"]
    BANK = temp["bank"]
    SAVE_FILE = temp["savefile"]
    
    main()