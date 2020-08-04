
import hashlib
import os
import shutil

def getHashes(path, fileHashes):
    print("executing in "+ path)
    for filename in os.listdir(path):
        fullpath = os.path.join(path,filename)

        if os.path.isfile(fullpath):
            
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

with open("./hashes.txt", "w+") as fileHashes:
    getHashes('.', fileHashes)

dicHashPath = {}
with open("./hashes.txt", "r") as fileHashes:
    with open("./result.txt", "w+") as searchResult:
        with open("./keepers.txt", "r") as keepers:
            hashLines = fileHashes.readlines()
            keeperLines = keepers.readlines()
            for line in hashLines:
                lineHashPath = line.split("##")

                if lineHashPath[0] in dicHashPath:
                    strPrint = "===================\nCopia encontrada em " + lineHashPath[1] + "Original: " + dicHashPath[lineHashPath[0]] + "MD5: " +lineHashPath[0]
                    print(strPrint)
                    searchResult.write(strPrint+ "\n")


                    for kline in keeperLines:
                        eqOriginal = False
                        eqLineHash = False
                        print("kline " + kline)
                        try:
                            comp = os.path.commonpath([lineHashPath[1], kline])
                            print(">"+comp +"|result of comparing " + lineHashPath[1] + " and " + kline)
                        except:
                            print("paths compare line hash error")

                        if comp == kline:
                            eqLineHash = True
                        
                        try:
                            comp = os.path.commonpath([dicHashPath[lineHashPath[0]], kline])
                            print(">"+comp +"|result of comparing " + dicHashPath[lineHashPath[0]] + " and " + kline)
                        except:
                            print("paths compare original error")

                        if comp == kline:
                            eqOriginal = True
                    
                        if eqOriginal and not eqLineHash:
                            print("==KEEPER FOUND on original == " + kline + " moving curr line"+ lineHashPath[1]+ " to copia_deletar")
                            shutil.move(lineHashPath[1], "./copia_deletar", copy_function = shutil.copytree)
                            searchResult.write("==KEEPER FOUND on original == " + kline + " moving curr line"+ lineHashPath[1]+ " to copia_deletar"+ "\n")
                        elif eqLineHash and not eqOriginal:
                            print("==KEEPER FOUND on curr line== " + kline + " moving original"+ dicHashPath[lineHashPath[0]] + " to original_deletar")
                            shutil.move(dicHashPath[lineHashPath[0]], "./original_deletar", copy_function = shutil.copytree) 
                            searchResult.write("==KEEPER FOUND on curr line== " + kline + " moving original"+ dicHashPath[lineHashPath[0]] + " to original_deletar" +"\n")
                        elif eqOriginal and eqLineHash:
                            print("duplicated files found in keepers, nothing will be done")
                            searchResult.write("duplicated files found in keepers, nothing will be done \n")
                
                

                else: 
                    dicHashPath[lineHashPath[0]] =lineHashPath[1]