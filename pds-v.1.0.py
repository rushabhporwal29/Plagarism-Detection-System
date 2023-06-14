import os

def preprocessText(text):
    text = text.lower()
    text = ''.join(c for c in text if c.isalnum())
    return text

def calculateLCSlength( text1, text2 ):
    m = len(text1)
    n = len(text2)

    lcsMatrix = [ [0]*(n+1) for _ in range(m+1) ]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                lcsMatrix[i][j] = lcsMatrix[i - 1][j - 1] + 1
            else:
                lcsMatrix[i][j] = max(lcsMatrix[i - 1][j], lcsMatrix[i][j - 1])

    return lcsMatrix[m][n]

def plagarismDetector(essays, threshold):
    numEssays = len(essays)
    plagarismCases = []

    for i in range(numEssays):
        for j in range(i + 1, numEssays):
            essay1 = preprocessText(essays[i])
            essay2 = preprocessText(essays[j])
            lcs_length = calculateLCSlength(essay1, essay2)
            thresholdLength = max(len(essay1), len(essay2))*(threshold/100)
            print("#LCS Length,Threshold Length, Essay lengths : ",lcs_length, thresholdLength, [len(essay1), len(essay2)])
            if lcs_length >= thresholdLength:
                plagarismPercent = lcs_length/max(len(essay1), len(essay2))*100
                # print("## Essays : ",[essay1,essay2])
                print("##Plagarism Case : ",i , j, plagarismPercent)
                plagarismCases.append((i, j, plagarismPercent))

    return plagarismCases

def getEssays(folderName):
    # print(folderName)
    essays = []
    text_files = [f for f in os.listdir(folderName) if f.endswith('.txt')]
    print("## Files : ",text_files)

    for file in text_files:
        essays.append(open(os.path.join(folderName, file),'r').read())

    return essays,text_files

def getReport(plagarismCases, essayNames):
    report = open('report.txt', 'w+')

    report.writelines("##### Plagarism Report #####")
    report.writelines(f"\nTotal Essays : {len(essayNames)}")
    report.writelines(f"\nTotal Plagarism Detected : {len(plagarismCases)}")
    report.writelines("\n---")

    print("##### PLAGIARISM REPORT #####")
    print("Total Essays : ",len(essayNames))
    print("Total Plagarism Detected : ",len(plagarismCases))
    print("---")
    for case in plagarismCases:
      essay1_index, essay2_index, plagarismPercent = case
      report.writelines(f"\nPotential plagiarism detected between '{essayNames[essay1_index]}' and '{essayNames[essay2_index]}'.")
      report.writelines(f"\nPlagarism Rate(%): {round(plagarismPercent,2)}%")
      report.writelines("\n---")
      print(f"Potential plagiarism detected between '{essayNames[essay1_index]}' and '{essayNames[essay2_index]}'.")
      print(f"Plagarism Rate(%): {round(plagarismPercent,2)}%")
      print("---")

folderName = input('Folder Location : ("./Submissions") ') or "./Submissions"
threshold = int(input('Threshold (%) : ("50")') or '50')
essays, essayNames = getEssays(folderName)
# print("TotalEssays : ",len(essays))
# print("Essays : ", essays)
plagarismCases = plagarismDetector(essays, threshold)
print("PlagarismCases : ", plagarismCases)
getReport(plagarismCases,essayNames)

