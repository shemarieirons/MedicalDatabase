import mysql.connector
import treatment
import visits
import time

mydb = mysql.connector.connect(
    host = "localhost",
    user="root",
    password="Shemarie",
    database="medicalDatabase"
)
mycursor = mydb.cursor()

#mycursor.execute("Create table visit_treatment (
#VARCHAR(255), treatidvisit VARCHAR(255), FOREIGN KEY (visitidtreat) REFERENCES visits(vid) ON UPDATE CASCADE , FOREIGN KEY (treatidvisit) REFERENCES treatment(treatid) ON UPDATE CASCADE, PRIMARY KEY(treatidvisit, visitidtreat))")
#You can have many treatments for 1 visit
def addVisitTreat():
    while True:
        try:
            visits.viewAllVisits()
            vid = input("Which visit would you like to add a treatment for? Visit ID: ")
            treatment.viewAllTreatment()
            tid = input("Enter the treatment you would like to add: ")
            sql = "Insert into visit_treatment (visitidtreat, treatidvisit) values (%s, %s)"
            val = (vid, tid)
            mycursor.execute(sql, val)
            mydb.commit()
            print("Treatment successfully added to visit.")
            break

        except mysql.connector.IntegrityError:
            print("\n\nTreatment id/Visit id does not exist \n\t\t\tOR \nTreatment for that visit was previously logged. Please try again.\n\n\n")
            time.sleep(2)
            mydb.rollback()

def viewAllVisitTreat():
    mycursor.execute("Select vt.visitidtreat, vt.treatidvisit, t.treatname from visit_treatment as vt LEFT JOIN treatment t on vt.treatidvisit = t.treatid")
    myresult = mycursor.fetchall()

    print("Visit Id \t\tTreatment ID \t\tTreatment Name")
    for x in myresult:
        print(x[0], "\t\t\t", x[1], "\t\t\t", x[2])

def viewOneVisitTreat():
    visits.viewAllVisits()
    findVisit=input("Enter visit id: ")
    sql = "Select vt.visitidtreat, vt.treatidvisit, t.treatname from visit_treatment as vt LEFT JOIN treatment t on vt.treatidvisit = t.treatid where visitidtreat = %s"
    mycursor.execute(sql, (findVisit,))
    myresult = mycursor.fetchall()
    if (myresult == []):
        print("No occurence exists. Please try again with a different visit id.")
    else:
        print("Treatment ID \t\tTreatment Name")
        for x in myresult:
            print(x[1], "\t\t\t", x[2])

def alterVisitTreat():
    viewAllVisitTreat()
    findVisit=input("Enter visit id for record you want to alter: ")
    findTreat = input("Enter treatment id for record you want to alter: : ")
    sql = "SELECT * FROM visit_treatment where visitidtreat = %s and treatidvisit= %s"
    mycursor.execute(sql, (findVisit,findTreat))
    myresult = mycursor.fetchall()
    if (myresult == []):
        print("No occurence exists. Please try again.")
    else:
        print("Select what you would like to modify: \n1. Visit id for record\t\t\t2. Treatment id for visit")
        mod = int(input("\nChange: "))

        if mod == 1:
            while True:
                try:
                    vid = input("Enter new visit id: ")
                    sql = "Update visit_treatment set visitidtreat = %s where visitidtreat = %s and treatidvisit= %s"
                    mycursor.execute(sql, (vid, findVisit, findTreat))
                    mydb.commit()
                    print("visit ID for record successfully updated.")
                    return
                except mysql.connector.IntegrityError:
                    print("Record already exists / Visit ID not in database. Please try again.")
                    mydb.rollback()

        elif mod == 2:
            while True:
                try:
                    tid = input("Enter new treatment id: ")
                    sql = "Update visit_treatment set treatidvisit = %s where visitidtreat = %s and treatidvisit= %s"
                    mycursor.execute(sql, (tid, findVisit, findTreat))
                    mydb.commit()
                    print("Treatment ID for record successfully updated.")
                    return
                except mysql.connector.IntegrityError:
                    print("Record already exists / Treatment ID not in database. Please try again.")
                    mydb.rollback()
        else:
            print("Invalid option. Please try again.")
            return
