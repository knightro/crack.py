#! /usr/bin/env python
import getopt, os.path, sys
import crypt

def testPass(cryptPass, dictionaryFile):
    salt = None
    # TODO: get rsplit() to work with multiple delimiters ($ and !)
    if '$' in cryptPass:
        tokens = cryptPass.rsplit('$', 1)
        if len(tokens) > 1:
            salt = tokens[0]
    elif '!' in cryptPass:
        tokens = cryptPass.rsplit('!', 1)
        if len(tokens) > 1:
            salt = tokens[0]
    else:
        salt = cryptPass[0:2]
    if salt:
        try:
            dictFile = open(dictionaryFile, 'r')
        except IOError as err:
            print "\n" + str(err)
            print "Error: unable to open \'" + dictionaryFile + "\' for read access\n"
            sys.exit(2)
        for word in dictFile.readlines():
            word = word.strip('\n')
            cryptWord = crypt.crypt(word, salt)
            if (cryptWord == cryptPass):
                print "[+] Found Password: " +word +"\n"
                dictFile.close()
                return
        dictFile.close()
    print "[-] Password Not Found.\n"
    return


def parsePasswordFile(passwordFile, dictionaryFile):
    try:
        passFile = open(passwordFile)
    except IOError as err:
        print "\n" + str(err)
        print "Error: unable to open \'" + passwordFile + "\' for read access\n"
        sys.exit(2)

    for line in passFile.readlines():
        if ':' in line:
            user, cryptPass, junk = line.split(':', 2)
            if not cryptPass:
                print "[!] No Password For: " +user + "\n"
            elif "*" == cryptPass:
                continue # User cannot login, move on to the next user
            else:
                cryptPass = line.split(':')[1].strip(' ')
                if '!' in cryptPass:
                    print "[!] Password Locked For: " +user
                print "[*] Cracking Password For: " +user
                testPass(cryptPass, dictionaryFile)
    passFile.close()

def fileExists(filePath):
    exists = True
    if not os.path.isfile(filePath):
        print "\n\'" +filePath + "\' does not exist.\n"
        exists = False
    return exists

def fileReadable(filePath):
    readable = True
    if not os.access(filePath, os.R_OK):
        print "\n\'" +filePath + "\' no read access.\n"
        readable = False
    return readable

def usage():
    print "\nUsage: crack [-h] -p <password_file> -d <dictionary_file>"
    print "\t-h\tshow this help message and exit"
    print "\t-p\tpath to file containing hashed passwords"
    print "\t-d\tpath to dictionary file\n"

def main(argv):

    passwordFile = None
    dictionaryFile = None

    try:
        opts, args = getopt.getopt(argv, "hp:d:")
    except getopt.GetoptError as err:
        print "\n" + str(err)
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            usage()
            sys.exit()
        elif opt == "-p":
            passwordFile = arg
        elif opt == "-d":
            dictionaryFile = arg

    if passwordFile and dictionaryFile:
        if fileExists(passwordFile) and \
           fileReadable(passwordFile) and \
           fileExists(dictionaryFile) and \
           fileReadable(dictionaryFile):
            parsePasswordFile(passwordFile, dictionaryFile)
        else:
            sys.exit()
    else:
        usage()
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])