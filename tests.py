import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user="root",
    password="Shemarie",
    database="medicalDatabase"
)

mycursor = mydb.cursor()

#mycursor.execute("CREATE TABLE tests (testid VARCHAR(255), test_name VARCHAR(255), t_type INT)")

def addTest(): #function to insert test in database
    while True: #loop to ensure that the id entered is unique
        try:
            testid = input("Enter test id: ")
            sql = "Insert into tests (testid) values (%s)"
            val = (testid,)
            mycursor.execute(sql, val)
            mydb.commit()
            print("ID successfully inserted. Please continue")
            break

        except mysql.connector.IntegrityError:
            print("Test with id entered already exists. Please try again.")
            mydb.rollback()

    test_name = input("Enter test name: ")
    sql = "UPDATE tests SET test_name = %s where testid = %s"
    mycursor.execute(sql,(test_name, testid))
    mydb.commit()
    print("Name successfully inserted. Please continue")

    print("Select type of test from the menu below: \n1. Blood Tests \n2. Imaging Tests \n3. Urine Tests \n4. Allergy Tests \n5. Genetic Tests \n6. Cardiac Tests")
    print("7. Respiratory Tests \n8. Metabolic Tests \n9. Infection Tests \n10. Other")

    #loop to ensure that the number entered is one from the list
    while True:
        try:
            t_type = int(input("Enter the number corresponding to the test type: "))
            sql = "UPDATE tests SET t_type = %s where testid = %s"
            mycursor.execute(sql,(t_type, testid))
            mydb.commit()
            break

        except mysql.connector.errors.DatabaseError:
            print("Type entered does not match list. Please revisit the list and try again.")
            mydb.rollback()
    print("Test successfully added to database.")

def viewAllTests():
    mycursor.execute("Select * from tests")
    myresult = mycursor.fetchall()
    print("Test id \t Test name\t\t Test type\t")
    for x in myresult:
        print(x[0], "\t\t", x[1], "\t\t", x[2])

def viewOneTest():
    findTest = input("Enter the test id for the test you would like to view: ")
    sql = "SELECT * FROM tests where testid = %s"
    mycursor.execute(sql, (findTest,))
    myresult = mycursor.fetchall()
    if (myresult == []):
        print("No test with that id number exists. Please try again with a different number.")
    else:
        print("Test id \t Test name\t\t Test type\t")
        for x in myresult:
            print(x[0], "\t\t", x[1], "\t\t", x[2])

def deleteOneTest():
    viewAllTests()
    findTest = input("Enter the id for the test you would like to delete: ")
    sql = "SELECT * FROM tests where testid = %s"
    mycursor.execute(sql, (findTest,))
    myresult = mycursor.fetchall()
    if (myresult == []):
        print("No test with that id number exists. Please try again with a different number.")
    else:
        sql = "Delete from tests where testid = %s"
        mycursor.execute(sql, (findTest,))
        mydb.commit()
        print("Record has been deleted.")

def alterTests():
    viewAllTests()
    findTest = input("Enter the id for the test you would like to alter: ")
    sql = "SELECT * FROM tests where testid = %s"
    mycursor.execute(sql, (findTest,))
    myresult = mycursor.fetchall()
    if (myresult == []):
        print("No test with that id number exists. Please try again with a different number.")
        return
    else:
        testmod = int(input("Select what you would like to modify: \n1. Test id \n2. Test name \n3. Test Type \nChange: "))
        if testmod == 1:
            try:
                newtestmod = input("Enter new test id: ")
                sql = "Update tests set testid = %s where testid = %s"
                mycursor.execute(sql, (newtestmod, findTest))
                mydb.commit()
                print("ID successfully updated.")
                return

            except mysql.connector.IntegrityError:
                print("Test with id entered already exists. Please try again.")
                mydb.rollback()
                return

        elif testmod == 2:
            test_name = input("Enter new name for test: ")
            sql = "UPDATE tests SET test_name = %s where testid = %s"
            mycursor.execute(sql, (test_name, findTest))
            mydb.commit()
            print("Test name has been successfully updated.")

        elif testmod == 3:
            print("Select type of test from the menu below: \n1. Blood Tests \n2. Imaging Tests \n3. Urine Tests \n4. Allergy Tests \n5. Genetic Tests \n6. Cardiac Tests")
            print("7. Respiratory Tests \n8. Metabolic Tests \n9. Infection Tests \n10. Other")

            try:
                t_type = int(input("Enter the number corresponding to the test type: "))
                sql = "UPDATE tests SET t_type = %s where testid = %s"
                mycursor.execute(sql, (t_type, findTest))
                mydb.commit()
                print("Type successfully updated. Please continue")

            except mysql.connector.errors.DatabaseError:
                print("Type entered does not match list. Please revisit the list and try again.")
                mydb.rollback()

        else:
            print("Invalid input. Please try again.")
            return
