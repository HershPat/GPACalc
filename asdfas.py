import requests, stdiomask, os
from bs4 import BeautifulSoup

j_username = input("Enter Genesis Email: ")
j_password = stdiomask.getpass(prompt='Enter Genesis Password: ')


studentId = input("Enter Student ID: ")
markingPeriodNumber = input("Enter Marking Period number (Example: 4): ")
markingPeriod = f"MP{markingPeriodNumber}"

loginInfo = {
    'j_username': j_username,
    'j_password': j_password
}

url="https://parents.edison.k12.nj.us/genesis/sis/j_security_check"
gradebook=f"https://parents.edison.k12.nj.us/genesis/parents?tab1=studentdata&tab2=gradebook&tab3=weeklysummary&studentid={studentId}&action=form&mpToView={markingPeriod}"

with requests.session() as s:
    r = s.post(url, loginInfo)
    r = s.get(gradebook)
    soup = BeautifulSoup(r.text, 'html.parser')

    #Finding Grades in HTML
    rawGrades = soup.find_all('div', attrs={'style':'text-decoration: underline'})
    outputString = ' '.join([item.get_text() for item in rawGrades])
    outputString = outputString.replace('%','')
    classGrades = outputString.split()

    for i in range(0, len(classGrades)):
        classGrades[i] = float(classGrades[i])

    #Finding Classnames in html
    rawClassnames = soup.find_all('u')
    outputString1 = ' '.join([item.get_text() for item in rawClassnames])
    classNames = ' '.join(outputString1.split())

    xxx = outputString1.replace('\r', '')
    yyy = xxx.replace('\n', '')
    zzz = yyy.replace('  ', '|')

    res = []
    res[:] = zzz

    aaa = zzz.split('|')
    realClassnames = list(dict.fromkeys(aaa))

    print("\n=================================")
    print("Parent Portal GPA Calculator v0.1")
    print("=================================\n\n")

    print("=================================")
    print("Weekly Summary")
    print("=================================\n")

    for x in range(7):
        tempClassname1 = realClassnames[x+1]
        tempClassGrade = classGrades[x]
        print(f"{tempClassname1.strip()}: {tempClassGrade}0%")

    #Unweighted
    uwPoints = []

    for x in range(7):
        if classGrades[x] >= 96.5:
            uwPoints.append(4.33)
        elif classGrades[x] < 96.5 and classGrades[x] >= 92.5:
            uwPoints.append(4.0)
        elif classGrades[x] < 92.5 and classGrades[x] >= 89.5:
            uwPoints.append(3.67)
        elif classGrades[x] < 89.5 and classGrades[x] >= 86.5:
            uwPoints.append(3.34)
        elif classGrades[x] < 86.5 and classGrades[x] >= 82.5:
            uwPoints.append(3)
        elif classGrades[x] < 82.5 and classGrades[x] >= 79.5:
            uwPoints.append(2.67)
        elif classGrades[x] < 79.5 and classGrades[x] >= 76.5:
            uwPoints.append(2.34)
        elif classGrades[x] < 76.5 and classGrades[x] >= 72.5:
            uwPoints.append(2.0)
        elif classGrades[x] < 72.5 and classGrades[x] >= 69.5:
            uwPoints.append(1.67)
        elif classGrades[x] < 69.5 and classGrades[x] >= 64.5:
            uwPoints.append(1.0)
        elif classGrades[x] < 64.5:
            uwPoints.append(0)

    credits = []

    for x in range(7):
        if (realClassnames[x+1].find('BIO') >= 0 or realClassnames[x+1].find('CHEM') >= 0 or realClassnames[x+1].find('PHYSICS') >= 0) and realClassnames[x+1].find('AP') == -1:
            credits.append(6)
        if (realClassnames[x+1].find('BIO') >= 0 or realClassnames[x+1].find('CHEM') >= 0 or realClassnames[x+1].find('PHYSICS') >= 0) and realClassnames[x+1].find('AP') >= 0:
            credits.append(7)
        if realClassnames[x+1].find('PHYS ED') >= 0:
            credits.append(3.75)
        if realClassnames[x+1].find('HEALTH') >= 0:
            credits.append(1.25)
        if realClassnames[x+1].find('BIO') == -1 and realClassnames[x+1].find('CHEM') == -1 and realClassnames[x+1].find('PHYSICS') == -1 and realClassnames[x+1].find('PHYS ED') == -1 and realClassnames[x+1].find('HEALTH') == -1:
            credits.append(5)


    qualityPoints = []

    for x in range(7):
        qualityPoints.append(credits[x] * uwPoints[x])

    for x in range(7):
        unweightedGPA = (sum(qualityPoints)/sum(credits))

    #Weighted

    wPoints = []

    #wPoints calculator for loop
    for x in range(7):
        tempClassname2 = realClassnames[x+1]
        if tempClassname2.find("AP") >= 0 or tempClassname2.find("-H") >= 0 or tempClassname2.find(" H") >= 0:
            if classGrades[x] >= 96.5:
                wPoints.append(6.33)
            elif classGrades[x] < 96.5 and classGrades[x] >= 92.5:
                wPoints.append(6.0)
            elif classGrades[x] < 92.5 and classGrades[x] >= 89.5:
                wPoints.append(5.67)
            elif classGrades[x] < 89.5 and classGrades[x] >= 86.5:
                wPoints.append(5.34)
            elif classGrades[x] < 86.5 and classGrades[x] >= 82.5:
                wPoints.append(5)
            elif classGrades[x] < 82.5 and classGrades[x] >= 79.5:
                wPoints.append(4.67)
            elif classGrades[x] < 79.5 and classGrades[x] >= 76.5:
                wPoints.append(4.34)
            elif classGrades[x] < 76.5 and classGrades[x] >= 72.5:
                wPoints.append(4.0)
            elif classGrades[x] < 72.5 and classGrades[x] >= 69.5:
                wPoints.append(3.67)
            elif classGrades[x] < 69.5 and classGrades[x] >= 64.5:
                wPoints.append(1.0)
            elif classGrades[x] < 64.5:
                wPoints.append(0)
        elif tempClassname2.find("-1") >= 0 or tempClassname2.find("Programming") >= 0:
            if classGrades[x] >= 96.5:
                wPoints.append(5.33)
            elif classGrades[x] < 96.5 and classGrades[x] >= 92.5:
                wPoints.append(5.0)
            elif classGrades[x] < 92.5 and classGrades[x] >= 89.5:
                wPoints.append(4.67)
            elif classGrades[x] < 89.5 and classGrades[x] >= 86.5:
                wPoints.append(4.34)
            elif classGrades[x] < 86.5 and classGrades[x] >= 82.5:
                wPoints.append(4)
            elif classGrades[x] < 82.5 and classGrades[x] >= 79.5:
                wPoints.append(3.67)
            elif classGrades[x] < 79.5 and classGrades[x] >= 76.5:
                wPoints.append(3.34)
            elif classGrades[x] < 76.5 and classGrades[x] >= 72.5:
                wPoints.append(3.0)
            elif classGrades[x] < 72.5 and classGrades[x] >= 69.5:
                wPoints.append(2.67)
            elif classGrades[x] < 69.5 and classGrades[x] >= 64.5:
                wPoints.append(1.0)
            elif classGrades[x] < 64.5:
                wPoints.append(0)
        elif tempClassname2.find("PHYS ED") >= 0 or tempClassname2.find("HEALTH") >= 0 or tempClassname2.find("-2") >= 0:
            wPoints.append(uwPoints[x])
        else:
            weightOfClass = input(f"""\nWhat level is {realClassnames[x+1].strip()}?
H - Honors/AP
A - Accelerated
R - Regular/Gym/HEALTH
> """)
            if weightOfClass == "H":
                if classGrades[x] >= 96.5:
                    wPoints.append(6.33)
                elif classGrades[x] < 96.5 and classGrades[x] >= 92.5:
                    wPoints.append(6.0)
                elif classGrades[x] < 92.5 and classGrades[x] >= 89.5:
                    wPoints.append(5.67)
                elif classGrades[x] < 89.5 and classGrades[x] >= 86.5:
                    wPoints.append(5.34)
                elif classGrades[x] < 86.5 and classGrades[x] >= 82.5:
                    wPoints.append(5)
                elif classGrades[x] < 82.5 and classGrades[x] >= 79.5:
                    wPoints.append(4.67)
                elif classGrades[x] < 79.5 and classGrades[x] >= 76.5:
                    wPoints.append(4.34)
                elif classGrades[x] < 76.5 and classGrades[x] >= 72.5:
                    wPoints.append(4.0)
                elif classGrades[x] < 72.5 and classGrades[x] >= 69.5:
                    wPoints.append(3.67)
                elif classGrades[x] < 69.5 and classGrades[x] >= 64.5:
                    wPoints.append(1.0)
                elif classGrades[x] < 64.5:
                    wPoints.append(0)
            elif weightOfClass == "A":
                if classGrades[x] >= 96.5:
                    wPoints.append(5.33)
                elif classGrades[x] < 96.5 and classGrades[x] >= 92.5:
                    wPoints.append(5.0)
                elif classGrades[x] < 92.5 and classGrades[x] >= 89.5:
                    wPoints.append(4.67)
                elif classGrades[x] < 89.5 and classGrades[x] >= 86.5:
                    wPoints.append(4.34)
                elif classGrades[x] < 86.5 and classGrades[x] >= 82.5:
                    wPoints.append(4)
                elif classGrades[x] < 82.5 and classGrades[x] >= 79.5:
                    wPoints.append(3.67)
                elif classGrades[x] < 79.5 and classGrades[x] >= 76.5:
                    wPoints.append(3.34)
                elif classGrades[x] < 76.5 and classGrades[x] >= 72.5:
                    wPoints.append(3.0)
                elif classGrades[x] < 72.5 and classGrades[x] >= 69.5:
                    wPoints.append(2.67)
                elif classGrades[x] < 69.5 and classGrades[x] >= 64.5:
                    wPoints.append(1.0)
                elif classGrades[x] < 64.5:
                    wPoints.append(0)
            elif weightOfClass == "R":
                wPoints.append(uwPoints[x])
    #End of wPoints for loop
    qualityPointsWeighted = []

    for x in range(7):
        qualityPointsWeighted.append(credits[x] * wPoints[x])

    for x in range(7):
        weightedGPA = (sum(qualityPointsWeighted)/sum(credits))

    print("\n=================================")
    print("GPA")
    print("=================================\n\n")

    print(f"Unweighted GPA for MP{markingPeriodNumber}: {unweightedGPA}")
    print(f"Weighted GPA for MP{markingPeriodNumber}  : {weightedGPA}")

    os.system('pause')