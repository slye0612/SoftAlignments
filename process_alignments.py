# coding: utf-8

import io, unicodedata, re, functions, sys, getopt, string, os, webbrowser, math, ntpath, numpy as np
from time import gmtime, strftime
from imp import reload
try:
    import configparser as cp
except ImportError:
    import ConfigParser as cp

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hi:o:s:t:f:n:a:b:c:d:g:")
    except getopt.GetoptError:
        functions.printHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            functions.printHelp()
            sys.exit()
        elif opt == '-i':
            inputfile = arg
        elif opt == '-o':
            outputType = arg
        elif opt == '-s':
            sourcefile = arg
        elif opt == '-t':
            targetfile = arg
        elif opt == '-f':
            from_system = arg
        elif opt == '-n':
            num = arg
        elif opt == '-v':
            from_system2 = arg
        elif opt == '-w':
            inputfile2 = arg
        elif opt == '-x':
            sourcefile2 = arg
        elif opt == '-y':
            targetfile2 = arg
        elif opt == '-c':
            config_file = arg
    
    try:
        config_file
    except NameError:
        config_file = False
    
    if(config_file):
        # There is a config file! Get info about inputs
        # with open(config_file) as cfg:
            # sample_config = cfg.read()
        config = cp.ConfigParser()
        config.read(config_file)
        try:
            inputfile = config.get('AlignmentsOne', 'InputFile')
        except NameError:
            print ('Provide an input file!\n')
            functions.printHelp()
            sys.exit()
        try:
            from_system = config.get('AlignmentsOne', 'From')
        except cp.NoOptionError:
            from_system = 'NeuralMonkey'
        try:
            num = config.getint('Options', 'Number')
        except cp.NoOptionError:
            num = -1
        try:
            outputType = config.get('Options', 'OutputType')
        except cp.NoOptionError:
            # Set output type to 'web' by default
            outputType = 'web'
        
        if from_system == 'NeuralMonkey' or from_system == 'Marian':
            try:
                sourcefile = config.get('AlignmentsOne', 'SourceFile')
            except cp.NoOptionError:
                print ('Provide a source sentence file!\n')
                functions.printHelp()
                sys.exit()
            if from_system == 'NeuralMonkey':
                try:
                    targetfile = config.get('AlignmentsOne', 'TargetFile')
                except cp.NoOptionError:
                    print ('Provide a target sentence file!\n')
                    functions.printHelp()
                    sys.exit()
        if outputType == 'compare':
            try:
                from_system2 = config.get('AlignmentsTwo', 'From')
            except cp.NoOptionError:
                from_system2 = 'NeuralMonkey'
            try:
                inputfile2 = config.get('AlignmentsTwo', 'InputFile')
            except cp.NoOptionError:
                print ('Provide a input file for the second system!\n')
                functions.printHelp()
                sys.exit()
            if from_system2 == 'NeuralMonkey' or from_system2 == 'Marian':
                try:
                    sourcefile2 = config.get('AlignmentsTwo', 'SourceFile')
                except cp.NoOptionError:
                    print ('Provide a source sentence file for the second system!\n')
                    functions.printHelp()
                    sys.exit()
                if from_system2 == 'NeuralMonkey':
                    try:
                        targetfile2 = config.get('AlignmentsTwo', 'TargetFile')
                    except cp.NoOptionError:
                        print ('Provide a target sentence file for the second system!\n')
                        functions.printHelp()
                        sys.exit()
        
    else:
        # There is no config file. Look for inputs in parameters
        try:
            inputfile
        except NameError:
            print ('Provide an input file!\n')
            functions.printHelp()
            sys.exit()
        try:
            from_system
        except NameError:
            from_system = 'NeuralMonkey'
        try:
            num
        except NameError:
            num = -1
        try:
            outputType
        except NameError:
            # Set output type to 'web' by default
            outputType = 'web'
        if from_system == 'NeuralMonkey' or from_system == 'Marian':
            try:
                sourcefile
            except NameError:
                print ('Provide a source sentence file!\n')
                functions.printHelp()
                sys.exit()
            if from_system == 'NeuralMonkey':
                try:
                    targetfile
                except NameError:
                    print ('Provide a target sentence file!\n')
                    functions.printHelp()
                    sys.exit()
        if outputType == 'compare':
            try:
                from_system2
            except NameError:
                from_system2 = 'NeuralMonkey'
            try:
                inputfile2
            except NameError:
                print ('Provide a input file for the second system!\n')
                functions.printHelp()
                sys.exit()
            if from_system2 == 'NeuralMonkey' or from_system2 == 'Marian':
                try:
                    sourcefile2
                except NameError:
                    print ('Provide a source sentence file for the second system!\n')
                    functions.printHelp()
                    sys.exit()
                if from_system2 == 'NeuralMonkey':
                    try:
                        targetfile2
                    except NameError:
                        print ('Provide a target sentence file for the second system!\n')
                        functions.printHelp()
                        sys.exit()
    if outputType != 'color' and outputType != 'block' and outputType != 'block2' and outputType != 'compare':
        # Set output type to 'web' by default
        outputType = 'web'

    if from_system == "NeuralMonkey":
        srcs = functions.readSnts(sourcefile)
        tgts = functions.readSnts(targetfile)
        alis = np.load(inputfile)
    if from_system == "Nematus" or from_system == "Sockeye":
        (srcs, tgts, alis) = functions.readNematus(inputfile)
    if from_system == "OpenNMT":
        (srcs, tgts, alis) = functions.readNematus(inputfile, 1)
    if from_system == "Marian":
        (srcs, tgts, alis) = functions.readAmu(inputfile, sourcefile)

    data = list(zip(srcs, tgts, alis))
    
    if outputType == 'compare':
        if from_system2 == "NeuralMonkey":
            srcs2 = functions.readSnts(sourcefile2)
            tgts2 = functions.readSnts(targetfile2)
            alis2 = np.load(inputfile2)
        if from_system2 == "Nematus" or from_system2 == "Sockeye":
            (srcs2, tgts2, alis2) = functions.readNematus(inputfile2)
        if from_system2 == "OpenNMT":
            (srcs2, tgts2, alis2) = functions.readNematus(inputfile2, 1)
        if from_system2 == "Marian":
            (srcs2, tgts2, alis2) = functions.readAmu(inputfile2, sourcefile2)
        data2 = list(zip(srcs2, tgts2, alis2))
        
        if functions.compare(srcs, srcs2) == False:
            print ('Source senctences from both systems need to be identical!\n')
            functions.printHelp()
            sys.exit()

    foldername = ntpath.basename(inputfile).replace(".","") + "_" + strftime("%d%m_%H%M", gmtime())
    if outputType == 'compare':
        foldername = 'cmp_' + foldername
    folder = './web/data/' + foldername
    try:
        os.stat(folder)
    except:
        os.mkdir(folder)
    
    if outputType == 'compare':
        try:
            os.stat(folder + '/NMT1')
        except:
            os.mkdir(folder + '/NMT1')
        try:
            os.stat(folder + '/NMT2')
        except:
            os.mkdir(folder + '/NMT2')
        functions.processAlignments(data, folder + '/NMT1', inputfile, outputType, num)
        functions.processAlignments(data2, folder + '/NMT2', inputfile2, outputType, num)
    else:
        functions.processAlignments(data, folder, inputfile, outputType, num)
            
    # Get rid of some junk
    if outputType == 'web' or outputType == 'compare':
        webbrowser.open("http://127.0.0.1:47155/?directory=" + foldername)
        os.system("php -S 127.0.0.1:47155 -t web")
    else:
        os.remove(folder + "/" + ntpath.basename(inputfile) + '.ali.js')
        os.remove(folder + "/" + ntpath.basename(inputfile) + '.src.js')
        os.remove(folder + "/" + ntpath.basename(inputfile) + '.trg.js')
        os.remove(folder + "/" + ntpath.basename(inputfile) + '.con.js')
        os.remove(folder + "/" + ntpath.basename(inputfile) + '.sc.js')
        os.rmdir(folder)

if __name__ == "__main__":
    if sys.version[0] == '2':
        reload(sys)
        sys.setdefaultencoding('utf-8')
    main(sys.argv[1:])
