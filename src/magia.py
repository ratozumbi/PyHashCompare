
import hashlib
import os
import shutil
from pathlib import Path

def log(strLog):
    print(strLog)
    with open("./result.txt", "a+") as searchResult:
        searchResult.write(strLog + "\n")


def getHashes(path, fileHashes):
    log("executing in "+ path)
    for filename in os.listdir(path):
        fullpath = os.path.join(path,filename)


        if os.path.isfile(fullpath):

            with open("./ignore.txt", "r") as ignoreFile:
                for line in ignoreFile:
                    comp = os.path.commonpath([fullpath, line])
                    if line == comp:
                        log("ignoring " + fullpath)
                        return
                                
            hasher = hashlib.md5()

            with open(fullpath, 'rb') as afile:
                #swap lines to work with big files
                buf = afile.read()
                hasher.update(buf)
                # BLOCKSIZE = 65536
                # buf = afile.read(BLOCKSIZE)
                # while len(buf) > 0:
                #     hasher.update(buf)
                #     buf = afile.read(BLOCKSIZE)

            fileHashes.write(hasher.hexdigest() + "##" + fullpath + "\n")
            
        else:
            getHashes(fullpath, fileHashes)

def moveFileWithBranch (pathMove, filePath):
    filePath = filePath[:-1]
    if not os.path.exists(filePath):
        log(filePath + " already deleted. Skipping")
        return

    fileDirName = os.path.dirname(filePath)

    fullNewPath =os.path.normpath(os.path.join(pathMove,filePath)) 
    # fullNewPath = fullNewPath[:-1]
    fullNewDir = os.path.normpath(os.path.join(pathMove,fileDirName))
    os.makedirs(fullNewDir, exist_ok=True)

    # my_file = Path(fullNewPath)
    if os.path.exists(fullNewPath):
        log(fullNewPath + " already exist. Not going to move.")
    else:
        shutil.move(filePath,fullNewDir)

    if len([name for name in os.listdir(fileDirName)]) == 0:
        log("will delete " + fileDirName)
        shutil.rmtree(fileDirName)


with open("./hashes.txt", "w+") as fileHashes:
    getHashes('.', fileHashes)

dicHashPath = {}
with open("./hashes.txt", "r") as fileHashes:
    # with open("./result.txt", "w+") as searchResult:
    with open("./keepers.txt", "r") as keepers:
        hashLines = fileHashes.readlines()
        keeperLines = keepers.readlines()
        for line in hashLines:
            lineHashPath = line.split("##")

            if lineHashPath[0] in dicHashPath:
                strPrint = "===================\nCopia encontrada em " + lineHashPath[1] + "Original: " + dicHashPath[lineHashPath[0]] + "MD5: " +lineHashPath[0]
                log(strPrint)
                # searchResult.write(strPrint+ "\n")

                eqOriginal = False
                eqLineHash = False
                for kline in keeperLines:
                    kline = kline[:-1]
                    try:
                        comp = os.path.commonpath([lineHashPath[1], kline])
                    except:
                        log("paths compare line hash error")

                    if comp == kline:
                        eqLineHash = True
                    
                    try:
                        comp = os.path.commonpath([dicHashPath[lineHashPath[0]], kline])
                    except:
                        log("paths compare original error")

                    if comp == kline:
                        eqOriginal = True
                
                if eqOriginal and not eqLineHash:
                    log("==KEEPER FOUND on original == " + kline + " Moving curr line "+ lineHashPath[1]+ " to copia_deletar")
                    moveFileWithBranch("./copia_deletar", lineHashPath[1] )
                elif eqLineHash and not eqOriginal:
                    log("==KEEPER FOUND on curr line== " + kline + " Moving original "+ dicHashPath[lineHashPath[0]] + " to original_deletar")

                    moveFileWithBranch("./original_deletar", dicHashPath[lineHashPath[0]] )
                elif eqOriginal and eqLineHash:
                    log("duplicated files found in keepers, nothing will be done")
                else:
                    log("Same image found. No keeper path for any. First entry "+dicHashPath[lineHashPath[0]]+" will be kept")
                    moveFileWithBranch("./original_deletar", lineHashPath[0] )

            
            
            else: 
                dicHashPath[lineHashPath[0]] =lineHashPath[1]