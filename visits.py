import mysql.connector
import patient

mydb = mysql.connector.connect(
    host = "localhost",
    user="root",
    password="Shemarie",
    database="medicalDatabase"
)

mycursor = mydb.cursor()
#mycursor.execute("Create table visits (vid VARCHAR(255) PRIMARY KEY, ptvisid VARCHAR(255), vdate Date, diag VARCHAR(255), doc VARCHAR(255), FOREIGN KEY (ptvisid) REFERENCES patient(pid) ON UPDATE CASCADE)")

def addVisit():
    while True:
        try:
            vid = input("Enter visit id: ")
            patient.viewAllPatient()
            pid = input("Enter patient id: ")
            sql = "Insert into visits (vid, ptvisid) values (%s, %s)"
            val = (vid, pid)
            mycursor.execute(sql, val)
            mydb.commit()
            print("Visit id and patient id successfully inserted. Please continue")
            break

        except mysql.connector.IntegrityError:
            print("Patient id does not exist OR visit with id entered already exists. Please try again.")
            mydb.rollback()

    while True:
        try:
            dob = input("Enter date of visit(YYYY-MM-DD): ")
            sql = "UPDATE visits SET vdate = %s where vid = %s"
            mycursor.execute(sql, (dob, vid))
            mydb.commit()
            print("Date of visit has been successfully added.")
            break

        except mysql.connector.errors.DataError:
            print("Date of visit invalid. Please try again.")
            mydb.rollback()

    diag = input("Enter the patient diagnosis (if pending, leave blank): ")
    sql = "UPDATE visits SET diag = %s where vid = %s"
    mycursor.execute(sql, (diag, vid))
    mydb.commit()
    print("Patient diagnosis has been successfully added. ")

    doc = input("Enter attending physician: ")
    sql = "UPDATE visits SET doc = %s where vid = %s"
    mycursor.execute(sql, (doc, vid))
    mydb.commit()
    print("Patient visit details has been successfully inserted.")

def viewAllVisits():
    mycursor.execute("Select * from visits")
    myresult = mycursor.fetchall()

    print("Visit Id \tPatient Id \t\tVisit Date \t\tDiagnosis \t\t\t\t\t\t\tDoctor")
    for x in myresult:
        print(x[0], "\t\t\t", x[1], "\t\t\t", x[2], "\t", x[3], "\t\t\t\t", x[4])

def viewSpecifVisit():
    viewAllVisits()
    findVisit = input("Enter the visit id for the visit details you would like to view: ")
    sql = "SELECT * FROM visits where vid = %s"
    mycursor.execute(sql, (findVisit,))
    myresult = mycursor.fetchall()
    if (myresult == []):
        print("No visit with that id number exists. Please try again with a different visit id.")
    else:
        print("Visit Id \tPatient Id \t\tVisit Date \t\tDiagnosis \t\t\t\t\t\t\tDoctor")

        for x in myresult:
            print(x[0], "\t\t\t", x[1], "\t\t\t", x[2], "\t", x[3], "\t\t\t\t", x[4])


def deleteOneVisit():
    viewAllVisits()
    findVisit = input("Enter the visit id for the visit you would like to delete: ")
    sql = "SELECT * FROM visits where vid = %s"
    mycursor.execute(sql, (findVisit,))
    myresult = mycursor.fetchall()
    if (myresult == []):
        print("No visit with that id exists. Please try again with a different id.")
    else:
        sql = "Delete from visits where vid = %s"
        mycursor.execute(sql, (findVisit,))
        mydb.commit()
        print("Record has been deleted.")

def alterVisit():
    viewAllVisits()
    findVisit = input("Enter the visit id for the patient you would like to alter: ")
    sql = "SELECT * FROM visits where vid = %s"
    mycursor.execute(sql, (findVisit,))
    myresult = mycursor.fetchall()
    if (myresult == []):
        print("No visit with that id exists. Please try again with a different id.")
        return
    else:
        print("Select what you would like to modify: \n1. Visit id \t\t\t2. Patient id for visit \n3. Date of Visit \t\t\t4. Diagnosis \n5. Doctor")
        visitmod = int(input("\nChange: "))

        if visitmod==1:
            while True:
                try:
                    vid = input("Enter new visit id: ")
                    sql = "Update visits set vid = %s where vid = %s"
                    mycursor.execute(sql, (vid, findVisit))
                    mydb.commit()
                    print("visit ID successfully updated.")
                    return
                except mysql.connector.IntegrityError:
                    print("Visit with id entered already exists. Please try again.")
                    mydb.rollback()

        elif visitmod==2:
            while True:
                try:
                    patient.viewAllPatient()
                    ptvid = input("Enter new patient id for visit: ")
                    sql = "Update visits set ptvisid = %s where vid = %s"
                    mycursor.execute(sql, (ptvid, findVisit))
                    mydb.commit()
                    print("Patient Id for visit successfully updated.")
                    return
                except mysql.connector.IntegrityError:
                    print("Patient id does not exist. Please try again.")
                    mydb.rollback()

        elif visitmod==3:
            while True:
                try:
                    dob = input("Enter date of visit(YYYY-MM-DD): ")
                    sql = "UPDATE visits SET vdate = %s where vid = %s"
                    mycursor.execute(sql, (dob, findVisit))
                    mydb.commit()
                    print("Date of visit has been successfully updated.")
                    break

                except mysql.connector.errors.DataError:
                    print("Date of visit invalid. Please try again.")
                    mydb.rollback()

        elif visitmod==4:
            diag = input("Enter new patient diagnosis in visit: ")
            sql = "UPDATE visits SET diag = %s where vid = %s"
            mycursor.execute(sql, (diag, findVisit))
            mydb.commit()
            print("Patient diagnosis has been successfully updated. ")
        elif visitmod==5:
            doc = input("Enter attending physician: ")
            sql = "UPDATE visits SET doc = %s where vid = %s"
            mycursor.execute(sql, (doc, findVisit))
            mydb.commit()
            print("Patient's attending physician has been successfully updated.")

        else:
            print("Invalid input. Please try again.")
            return
