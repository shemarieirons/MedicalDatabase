import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user="root",
    password="Shemarie",
    database="medicalDatabase"
)

mycursor = mydb.cursor()

# mycursor.execute("Create table treatment (treatid VARCHAR(255) PRIMARY KEY, treatname VARCHAR(255))")

def addTreatment():#function to insert treatment in database
    while True: #loop to ensure that the id entered is unique
        try:
            treatid = input("Enter treatment id: ")
            sql = "Insert into treatment (treatid) values (%s)"
            val = (treatid,)
            mycursor.execute(sql, val)
            mydb.commit()
            print("ID successfully inserted. Please continue")
            break

        except mysql.connector.IntegrityError:
            print("Treatment with id entered already exists. Please try again.")
            mydb.rollback()
    treatname = input("Enter name for treatment: ")
    sql = "UPDATE treatment SET treatname = %s where treatid = %s"
    mycursor.execute(sql, (treatname, treatid))
    mydb.commit()
    print("Treatment has been successfully added.")

def viewAllTreatment():
    mycursor.execute("Select * from treatment")
    myresult = mycursor.fetchall()
    print("Treatment id \t\t\t Treatment name\n")
    for x in myresult:
        print(x[0].ljust(20), x[1])


def viewOneTreatment():
    findTreat = input("Enter the id for the treatment you would like to view: ")
    sql = "SELECT * FROM treatment where treatid = %s"
    mycursor.execute(sql, (findTreat,))
    myresult = mycursor.fetchall()
    if (myresult == []):
        print("No test with that id number exists. Please try again with a different number.")
    else:
        print("Treatment id \t Treatment name\n")
        for x in myresult:
            print(x[0], "\t\t", x[1])

def deleteOneTreatment():
    viewAllTreatment()
    findTreat = input("Enter the id for the treatment you would like to delete: ")
    sql = "SELECT * FROM treatment where treatid = %s"
    mycursor.execute(sql, (findTreat,))
    myresult = mycursor.fetchall()
    if (myresult == []):
        print("No test with that id exists. Please try again with a different id.")
    else:
        sql = "Delete from treatment where treatid = %s"
        mycursor.execute(sql, (findTreat,))
        mydb.commit()
        print("Record has been deleted.")


def alterTreatment():
    viewAllTreatment()
    findTreat = input("Enter the id for the treatment you would like to update: ")
    sql = "SELECT * FROM treatment where treatid = %s"
    mycursor.execute(sql, (findTreat,))
    myresult = mycursor.fetchall()
    if (myresult == []):
        print("No treatment with that id exists. Please try again with a different id.")
        return
    else:
        treatmod = int(input("Select what you would like to modify: \n1. Treatment id \n2. Treatment name \nChange: "))
        if treatmod == 1:
            try:
                newtreatid = input("Enter new treatment id: ")
                sql = "Update treatment set treatid = %s where treatid = %s"
                mycursor.execute(sql, (newtreatid, findTreat))
                mydb.commit()
                print("ID successfully updated.")
                return

            except mysql.connector.IntegrityError:
                print("Treatment with id entered already exists. Please try again.")
                mydb.rollback()
                return

        elif treatmod == 2:
            treatname = input("Enter new name for treatment: ")
            sql = "UPDATE treatment SET treatname = %s where treatid = %s"
            mycursor.execute(sql, (treatname, findTreat))
            mydb.commit()
            print("Treatment name has been successfully updated.")

        else:
            print("Invalid input. Please try again.")
            return
