import mysql.connector
import tests
import visits
import time

mydb = mysql.connector.connect(
    host = "localhost",
    user="root",
    password="Shemarie",
    database="medicalDatabase"
)
mycursor = mydb.cursor()

#mycursor.execute("Create table visit_test (visitidtest VARCHAR(255), testidvisit VARCHAR(255), testresult VARCHAR(255), FOREIGN KEY (visitidtest) REFERENCES visits(vid) ON UPDATE CASCADE , FOREIGN KEY (testidvisit) REFERENCES tests(testid) ON UPDATE CASCADE, PRIMARY KEY(testidvisit, visitidtest))")
# #You can have many tests for 1 visit

def addVisitTest():
    while True:
        try:
            visits.viewAllVisits()
            vid = input("Which visit would you like to add a test for? Visit ID: ")
            tests.viewAllTests()
            tid = input("Enter the test you would like to add: ")
            sql = "Insert into visit_test (visitidtest, testidvisit) values (%s, %s)"
            val = (vid, tid)
            mycursor.execute(sql, val)
            mydb.commit()
            print("Test successfully added to visit.")
            break

        except mysql.connector.IntegrityError:
            print("\n\nTest id/Visit id does not exist \n\t\t\tOR \nTest for that visit was previously logged. Please try again.\n\n\n")
            time.sleep(2)
            mydb.rollback()

    result = input("Enter the test result: ")
    sql = "UPDATE visit_test SET testresult = %s where visitidtest = %s and testidvisit= %s"
    mycursor.execute(sql, (result, vid,tid))
    mydb.commit()
    print("Test record for visit has been successfully added.")

def viewAllVisitTest():
    mycursor.execute("Select vt.visitidtest, vt.testidvisit, t.test_name, vt.testresult from visit_test as vt LEFT JOIN tests t on vt.testidvisit = t.testid")
    myresult = mycursor.fetchall()

    print("Visit Id \t\tTest ID \t\t\tTest Name \t\t\tTest Result")
    for x in myresult:
        print(x[0], "\t\t\t", x[1], "\t\t\t", x[2], "\t\t\t", x[3])

def viewOneVisitTest():
    visits.viewAllVisits()
    findVisit=input("Enter visit id: ")
    sql = ("SELECT vt.visitidtest, vt.testidvisit, t.test_name, vt.testresult from visit_test as vt LEFT JOIN tests t on vt.testidvisit = t.testid where vt.visitidtest=%s")
    mycursor.execute(sql, (findVisit, ))
    myresult = mycursor.fetchall()
    if (myresult == []):
        print("No occurence exists. Please try again.")
    else:
        print("Visit Id \t\tTest ID \t\t\tTest Name \t\t\tTest Result")
        for x in myresult:
            print(x[0], "\t\t\t", x[1], "\t\t\t", x[2], "\t\t\t", x[3])

def alterVisitTest():
    viewAllVisitTest()
    findVisit=input("Enter visit id for record you want to alter: ")
    findTest = input("Enter test id for record you want to alter: : ")
    sql = "SELECT * FROM visit_test where visitidtest = %s and testidvisit= %s"
    mycursor.execute(sql, (findVisit,findTest))
    myresult = mycursor.fetchall()
    if (myresult == []):
        print("No occurence exists. Please try again with a different visit id.")
    else:
        print("Select what you would like to modify: \n1. Visit id for record\t\t\t2. Test id for visit \n3. Test result")
        mod = int(input("\nChange: "))

        if mod == 1:
            while True:
                try:
                    vid = input("Enter new visit id: ")
                    sql = "Update visit_test set visitidtest = %s where visitidtest = %s and testidvisit= %s"
                    mycursor.execute(sql, (vid, findVisit, findTest))
                    mydb.commit()
                    print("visit ID for record successfully updated.")
                    return
                except mysql.connector.IntegrityError:
                    print("Record already exists / Visit ID not in database. Please try again.")
                    mydb.rollback()

        elif mod == 2:
            while True:
                try:
                    tests.viewAllTests()
                    tid = input("Enter updated test id for that visit: ")
                    sql = "Update visit_test set testidvisit = %s where visitidtest = %s and testidvisit= %s"
                    mycursor.execute(sql, (tid, findVisit, findTest))
                    mydb.commit()
                    print("Test ID for record successfully updated.")
                    return
                except mysql.connector.IntegrityError:
                    print("Record already exists / Test ID not in database. Please try again.")
                    mydb.rollback()
        elif mod==3:
            tres = input("Enter new test result: ")
            sql = "Update visit_test set testresult = %s where visitidtest = %s and testidvisit= %s"
            mycursor.execute(sql, (tres, findVisit, findTest))
            mydb.commit()
            print("Test result successfully updated.")
            return
        else:
            print("Invalid option. Please try again.")
            return
