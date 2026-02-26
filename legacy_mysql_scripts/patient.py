import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user="root",
    password="Shemarie",
    database="medicalDatabase"
)

mycursor = mydb.cursor()

# mycursor.execute("Create table patient (pid VARCHAR(255) PRIMARY KEY, fname VARCHAR(255), lname VARCHAR(255), ptdob DATE, gender enum('F', 'M', 'O'), add1 VARCHAR(255), add2 VARCHAR(255), city VARCHAR(255), state VARCHAR(255), country VARCHAR(255))")
# mycursor.execute("Alter table patient alter gender set default 'O'")

def addPatient():
    while True:
        try:
            ptid = input("Enter patient id: ")
            sql = "Insert into patient (pid) values (%s)"
            val = (ptid,)
            mycursor.execute(sql, val)
            mydb.commit()
            print("ID successfully inserted. Please continue")
            break

        except mysql.connector.IntegrityError:
            print("Treatment with id entered already exists. Please try again.")
            mydb.rollback()

    fname = input("Enter first name of patient: ")
    sql = "UPDATE patient SET fname = %s where pid = %s"
    mycursor.execute(sql, (fname, ptid))
    mydb.commit()
    print("First name has been successfully added.")

    lname = input("Enter last name of patient: ")
    sql = "UPDATE patient SET lname = %s where pid = %s"
    mycursor.execute(sql, (lname, ptid))
    mydb.commit()
    print("Last name has been successfully added.")

    while True:
        try:
            dob = input("Enter patient date of birth(YYYY-MM-DD): ")
            sql = "UPDATE patient SET ptdob = %s where pid = %s"
            mycursor.execute(sql, (dob, ptid))
            mydb.commit()
            print("Date of birth has been successfully added.")
            break

        except mysql.connector.errors.DataError:
            print("Date of birth invalid. Please try again.")
            mydb.rollback()

    while True:
        try:
            print("F - Female \t\tM-Male \t\t O-Other")
            gender = input("Enter the gender of the patient (F/M/O): ")
            gender=gender.upper()
            sql = "UPDATE patient SET gender = %s where pid = %s"
            mycursor.execute(sql,(gender, ptid))
            mydb.commit()
            print("Gender has been successfully added.")
            break

        except mysql.connector.errors.DataError:
            print("Gender entered does not match list. Please revisit the list and try again.")
            mydb.rollback()

    add1 = input("Enter address line 1 of patient: ")
    sql = "UPDATE patient SET add1 = %s where pid = %s"
    mycursor.execute(sql, (add1, ptid))
    mydb.commit()
    print("Address line 1 successfully added.")

    add2 = input("Enter address line 2 of patient: ")
    sql = "UPDATE patient SET add2 = %s where pid = %s"
    mycursor.execute(sql, (add2, ptid))
    mydb.commit()
    print("Address line 2 successfully added.")

    city = input("Enter city of patient: ")
    sql = "UPDATE patient SET city = %s where pid = %s"
    mycursor.execute(sql, (city, ptid))
    mydb.commit()
    print("City successfully added.")

    state = input("Enter state/parish of patient: ")
    sql = "UPDATE patient SET state = %s where pid = %s"
    mycursor.execute(sql, (state, ptid))
    mydb.commit()
    print("State/Parish successfully added.")

    country = input("Enter country of patient: ")
    sql = "UPDATE patient SET country = %s where pid = %s"
    mycursor.execute(sql, (country, ptid))
    mydb.commit()

    print("Patient successfully added.")

def viewAllPatient():
    mycursor.execute("Select * from patient")
    myresult = mycursor.fetchall()

    print("Patient id \t First name \tLast name \t\tDate of Birth \tGender \t Address\n")

    for x in myresult:
        print(x[0].ljust(12), x[1].ljust(15), x[2].ljust(15), x[3], " \t", x[4], "\t\t", x[5], ", ", x[6], ", ", x[7], ", ", x[8], ", ", x[9])

def viewOnePatient():
    findPat = input("Enter the id for the patient you would like to view: ")
    sql = "SELECT * FROM patient where pid = %s"
    mycursor.execute(sql, (findPat,))
    myresult = mycursor.fetchall()
    if (myresult == []):
        print("No patient with that id number exists. Please try again with a different id.")
    else:
        print("Patient id \t First name \tLast name \t\tDate of Birth \tGender \t Address\n")

        for x in myresult:
            print(x[0].ljust(12), x[1].ljust(15), x[2].ljust(15), x[3], " \t", x[4], "\t\t", x[5], ", ", x[6], ", ", x[7], ", ", x[8], ", ", x[9])

def deleteOnePatient():
    viewAllPatient()
    findPat = input("Enter the id for the patient you would like to delete: ")
    sql = "SELECT * FROM patient where pid = %s"
    mycursor.execute(sql, (findPat,))
    myresult = mycursor.fetchall()
    if (myresult == []):
        print("No patient with that id exists. Please try again with a different id.")
    else:
        try:
            sql = "Delete from patient where pid = %s"
            mycursor.execute(sql, (findPat,))
            mydb.commit()
            print("Record has been deleted.")
        except mysql.connector.errors.IntegrityError:
            print("Cannot delete patient row because it is being used in other tables.")
        except:
            print("Something went wrong. Please try again.")

def alterPatient():
    viewAllPatient()
    findPat = input("Enter the id for the patient you would like to alter: ")
    sql = "SELECT * FROM patient where pid = %s"
    mycursor.execute(sql, (findPat, ))
    myresult = mycursor.fetchall()
    if (myresult == []):
        print("No Patient with that id exists. Please try again with a different id.")
        return
    else:
        print("Select what you would like to modify: \n1. Patient id \t\t\t2. Patient first name \n3. Patient last name \t\t\t4. Patient date of birth")
        print("5. Patient gender \t\t\t6. Patient Address Line 1 \n7. Patient Address Line 2 \t\t\t8. Patient City")
        print("9. Patient State/Parish \t\t\t10. Patient Country ")


        ptmod = int(input("\nChange: "))

        if ptmod == 1:
            try:
                newpid = input("Enter new patient id: ")
                sql = "Update patient set pid = %s where pid = %s"
                mycursor.execute(sql, (newpid, findPat))
                mydb.commit()
                print("ID successfully updated.")
                return

            except mysql.connector.IntegrityError:
                print("Patient with id entered already exists. Please try again.")
                mydb.rollback()
                return

        elif ptmod == 2:
            ptname = input("Enter new first name for patient: ")
            sql = "UPDATE treatment SET fname = %s where pid = %s"
            mycursor.execute(sql, (ptname, findPat))
            mydb.commit()
            print("Patient first name has successfully been updated.")

        elif ptmod == 3:
            ptname = input("Enter new last name for patient: ")
            sql = "UPDATE treatment SET lname = %s where pid = %s"
            mycursor.execute(sql, (ptname, findPat))
            mydb.commit()
            print("Patient last name has successfully been updated.")

        elif ptmod == 4:
            while True:
                try:
                    dob = input("Enter new patient date of birth(YYYY-MM-DD): ")
                    sql = "UPDATE patient SET ptdob = %s where pid = %s"
                    mycursor.execute(sql, (dob, findPat))
                    mydb.commit()
                    print("Date of birth has been successfully updated.")
                    break

                except mysql.connector.errors.DataError:
                    print("Date of birth invalid. Please try again.")
                    mydb.rollback()

        elif ptmod == 5:
            while True:
                try:
                    print("F - Female \t\tM-Male \t\t O-Other")
                    gender = input("Enter the new gender of the patient (F/M/O): ")
                    gender = gender.upper()
                    sql = "UPDATE patient SET gender = %s where pid = %s"
                    mycursor.execute(sql, (gender, findPat))
                    mydb.commit()
                    print("Gender has been successfully updated.")
                    break

                except mysql.connector.errors.DataError:
                    print("Gender entered does not match list. Please revisit the list and try again.")
                    mydb.rollback()

        elif ptmod == 6:
            add1 = input("Enter new address line 1 of patient: ")
            sql = "UPDATE patient SET add1 = %s where pid = %s"
            mycursor.execute(sql, (add1, findPat))
            mydb.commit()
            print("Address line 1 successfully updated.")

        elif ptmod == 7:
            add2 = input("Enter new address line 2 of patient: ")
            sql = "UPDATE patient SET add2 = %s where pid = %s"
            mycursor.execute(sql, (add2, findPat))
            mydb.commit()
            print("Address line 2 successfully updated.")

        elif ptmod == 8 :
            city = input("Enter new city of patient: ")
            sql = "UPDATE patient SET city = %s where pid = %s"
            mycursor.execute(sql, (city, findPat))
            mydb.commit()
            print("City successfully updated.")

        elif ptmod == 9:
            state = input("Enter new state/parish of patient: ")
            sql = "UPDATE patient SET state = %s where pid = %s"
            mycursor.execute(sql, (state, findPat))
            mydb.commit()
            print("State/Parish successfully updated.")

        elif ptmod == 10:
            country = input("Enter new country of patient: ")
            sql = "UPDATE patient SET country = %s where pid = %s"
            mycursor.execute(sql, (country, findPat))
            mydb.commit()
            print("Country successfully updated.")

        else:
            print("Invalid input. Please try again.")
            return
