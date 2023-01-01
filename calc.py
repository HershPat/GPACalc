import selenium, stdiomask
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

class Account():
    auth_link = "https://parents.edison.k12.nj.us/"

    def authInfo(self, username, password, studentId, markingPeriod):
        self.gradebook = f"https://parents.edison.k12.nj.us/genesis/parents?tab1=studentdata&tab2=gradebook&tab3=weeklysummary&studentid={studentId}&action=form&mpToView=MP{markingPeriod}"
        self.creditPage = f"https://parents.edison.k12.nj.us/genesis/parents?tab1=studentdata&tab2=grading&tab3=current&action=form&studentid={studentId}"
        self.username = username
        self.password = password
    
    def get_grades_and_credits(self):
        options = Options()
        #options.add_argument('--headless')
        options.add_argument('window-size=1920x1080')
        #options.add_argument(r'user-agent=Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54')
        driver = webdriver.Chrome(options=options)
        driver.get(self.auth_link)

        usernameField = driver.find_element(By.NAME, 'j_username')
        usernameField.send_keys(self.username)
        passwordField = driver.find_element(By.NAME, 'j_password')
        passwordField.send_keys(self.password)
        driver.find_element(By.CLASS_NAME, 'saveButton').click()

        driver.get(self.gradebook)
        elem = driver.find_element(By.CLASS_NAME, 'list')
        html = elem.get_attribute("outerHTML")
        self.grades = html

        driver.get(self.creditPage)
        elem = driver.find_element(By.CLASS_NAME, 'list')
        html = elem.get_attribute("outerHTML")
        self.creditTable = html

        driver.save_screenshot('screen.png')

        
    
    def parse_data(self):
        soup_grades = bs(self.grades, 'html.parser')
        soup_credits = bs(self.creditTable, 'html.parser')

        gradebookData = []
        table = soup_grades.find('table')
        table_body = table.find('tbody')

        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            gradebookData.append([' '.join(ele.split()) for ele in cols if ele]) # Get rid of empty values
        
        creditPageData = []
        table = soup_credits.find('table')
        table_body = table.find('tbody')

        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            creditPageData.append([' '.join(ele.split()) for ele in cols if ele]) # Get rid of empty values

        return gradebookData[1:], creditPageData[1:]

def organizeGradeTable(gradeTable, creditTable):
    classes = []
    teachers = []
    letterGrades = []
    percentGrades = []
    credits = []
    for list in creditTable: credits.append(float(list[-1]))
    organizedGradeTable = [[],[],[],[], []]
    for i in range(len(gradeTable)):
        if (len(gradeTable[i]) > 2):
            classes.append(gradeTable[i][0])
            teachers.append(gradeTable[i][1].replace(" Email:", ""))
            letterGrades.append(gradeTable[i][4])
        else:
            percentGrades.append(gradeTable[i][0])
    for i in range(len(letterGrades)):
        if letterGrades[i].find('0') != 0 or percentGrades[i].find('Not Graded') != 0:
            organizedGradeTable[0].append(classes[i])
            organizedGradeTable[1].append(teachers[i])
            organizedGradeTable[2].append(letterGrades[i])
            organizedGradeTable[3].append(percentGrades[i])
            organizedGradeTable[4].append(credits[i])

    return organizedGradeTable

print("\n=================================")
print("Parent Portal GPA Calculator v0.1")
print("=================================\n\n")

j_username = input("Enter Genesis Email: ")
j_password = stdiomask.getpass(prompt='Enter Genesis Password: ')


studentId = input("Enter Student ID: ")
markingPeriodNumber = input("Enter Marking Period number (Example: 4): ")
markingPeriod = f"{markingPeriodNumber}"
account = Account()
account.authInfo(j_username, j_password, studentId, markingPeriod)
account.get_grades_and_credits()
gradeTable, creditTable = account.parse_data()
organizedGrades = organizeGradeTable(gradeTable=gradeTable, creditTable=creditTable)

listGradeNums = {
    'A+': 10,
    'A': 9,
    'A-': 8,
    'B+': 7,
    'B': 6,
    'B-': 5,
    'C+': 4,
    'C': 3,
    'C-': 2,
    'D': 1,
    'F': 0
}

listQualityPoints = {
    'A+': 4.33,
    'A': 4,
    'A-': 3.67,
    'B+': 3.33,
    'B':  3,
    'B-': 2.67,
    'C+': 2.33,
    'C': 2,
    'C-': 1.67,
    'D': 1, 
    'F': 0
}

credits = organizedGrades[4]
qualityPoints = []
weightedQualityPoints = []

# Unweighted
for list in organizedGrades[2]:
    qualityPoints.append(listQualityPoints[list])

# Weighted
for list, class_name in zip(organizedGrades[2], organizedGrades[0]):
    if ((list != 'D' or list != 'F') and (class_name.find('AP') == 0 or class_name.find('-H') != -1 or class_name.find(' H') != -1)):
        weightedQualityPoints.append(listQualityPoints[list]+2)
    elif ((list != 'D' or list != 'F') and class_name.find('-1') != -1):
        weightedQualityPoints.append(listQualityPoints[list]+1)
    else:
        weightedQualityPoints.append(listQualityPoints[list])

uwGPA = 0
wGPA = 0
creds = 0
for i in range(len(credits)):
    uwGPA += credits[i] * qualityPoints[i]
    wGPA  += credits[i] * weightedQualityPoints[i]
    creds += credits[i]
uwGPA = uwGPA/creds
wGPA = wGPA/creds

print("\n=================================")
print("GPA")
print("=================================")
print(f"Unweighted GPA for MP{markingPeriodNumber}: {uwGPA}")
print(f"Weighted GPA for MP{markingPeriodNumber}  : {wGPA}")

