import mysql.connector
import patient
import visit_treatment
import tests
import visits
import visit_test
import treatment

mydb = mysql.connector.connect(
    host = "localhost",
    user="root",
    password="Shemarie",
    database="medicalDatabase"
)

mycursor = mydb.cursor()

print("Hello! Welcome to the medical database!")
while True:
    print("MAIN MENU")
    cat = int(input("Select category: 1. Patient \t2. Treatments \t3. Tests \t4. Visits \nWhat would you like to do today? "))
    match cat:
        case 1:
            while True:
                print("PATIENT MENU")
                print("1. Add patient \t2. Modify existing patient \t3. View All Patients \t4. Search Patient by ID \t5. Delete Specific Patient")

                while True:
                    try:
                        task = int(input("Please select task from the menu above: "))
                        break
                    except:
                        print("Something went wrong. Try again")

                match task:
                    case 1:
                        patient.addPatient()
                    case 2:
                        patient.alterPatient()
                    case 3:
                        patient.viewAllPatient()
                    case 4:
                        patient.viewOnePatient()
                    case 5:
                        patient.deleteOnePatient()
                    case _:
                        print("Invalid Selection")
                end = input("Are you finished with Patient Menu? (Y/N)")
                end = end.upper()
                if end == 'Y':
                    break
                elif end == 'N':
                    continue
                else:
                    print("Invalid input.")
                    continue
        case 2:
            while True:
                print("TREATMENT MENU")
                print("1. Add treatment \t2. Modify existing treatments \n3. View All Treatments \t4. View Specific Treatment")
                while True:
                    try:
                        task = int(input("Please select task from the menu above: "))
                        break
                    except:
                        print("Something went wrong. Try again")
                match task:
                    case 1:
                        treatment.addTreatment()
                    case 2:
                        treatment.alterTreatment()
                    case 3:
                        treatment.viewAllTreatment()
                    case 4:
                        treatment.viewOneTreatment()
                    case _:
                        print("Invalid input.")
                        continue
                end = input("Are you finished with Treatment Menu? (Y/N)")
                end = end.upper()
                if end == 'Y':
                    break
                elif end == 'N':
                    continue
                else:
                    print("Invalid input.")
                    continue
        case 3:
            while True:
                print("TEST MENU")
                print("1. Add test \t2. Modify existing test \n3. View all tests \t4. View specific test")
                while True:
                    try:
                        task = int(input("Please select task from the menu above: "))
                        break
                    except:
                        print("Something went wrong. Try again")
                match task:
                    case 1:
                        tests.addTest()
                    case 2:
                        tests.alterTests()
                    case 3:
                        tests.viewAllTests()
                    case 4:
                        tests.viewOneTest()
                    case _:
                        print("Invalid input.")
                        continue
                end = input("Are you finished with Test Menu? (Y/N)")
                end = end.upper()
                if end == 'Y':
                    break
                elif end == 'N':
                    continue
                else:
                    print("Invalid input.")
                    continue
        case 4:
            while True:
                print("PATIENT HISTORY MENU")
                print("1. Add visit \t2. Modify existing visit \n3. View all visits (detailed)"
                                 "\t4. View visit history for patient \n5. Add test done at visit \t6. View test(s) done at visit \n7. Alter test done at visit"
                                 " 8. Add treatment done at visit \t9. View treatment(s) done at visit \n10. Alter treatment done at visit")
                while True:
                    try:
                        task = int(input("Please select task from the menu above: "))
                        break
                    except:
                        print("Something went wrong. Try again")
                match task:
                    case 1:
                        visits.addVisit()
                    case 2:
                        visits.alterVisit()
                    case 3:
                        mycursor.execute('''
                            SELECT v.vid, v.ptvisid, p.fname, p.lname, v.vdate, v.diag, v.doc, vt.treatidvisit, t.treatname, te.testid, te.test_name from visits as v
                            LEFT JOIN visit_treatment as vt ON v.vid = vt.visitidtreat
                            LEFT JOIN visit_test as vtest on v.vid = vtest.visitidtest
                            Right Join patient as p on p.pid = v.ptvisid
                            Right Join treatment as t on t.treatid = vt.treatidvisit
                            Right Join tests as te on te.testid = vtest.testidvisit
                        ''')
                        myresult = mycursor.fetchall()
                        print("Visit id \t Patient id Patient Name \tDate of Visit \t\tDiagnosis \t\tPhysician \t\tTreatment ID \t\tTreatment Name \t\tTest id \t\tTest Name")
                        for x in myresult:
                            print(x[0], "\t\t", x[1], "\t\t", x[2], x[3], "\t\t", x[4], "\t\t", x[5], "\t\t", x[6], "\t\t", x[7], "\t\t", x[8], "\t\t", x[9], "\t\t", x[10])
                    case 4:
                        patient.viewAllPatient()
                        findPat = input("Enter the id for the patient you would like to view: ")
                        sql = '''SELECT v.vid, v.ptvisid, p.fname, p.lname, v.vdate, v.diag, v.doc, vt.treatidvisit, t.treatname, te.testid, te.test_name from visits as v
                                LEFT JOIN visit_treatment as vt ON v.vid = vt.visitidtreat
                                LEFT JOIN visit_test as vtest on v.vid = vtest.visitidtest
                                Right Join patient as p on p.pid = v.ptvisid
                                Right Join treatment as t on t.treatid = vt.treatidvisit
                                Right Join tests as te on te.testid = vtest.testidvisit
                                where p.pid = %s
                                '''
                        mycursor.execute(sql, (findPat, ))
                        myresult = mycursor.fetchall()
                        if (myresult == []):
                            print("No record for patient with that id number exists. Please add record.")
                        else:
                            print(
                                "Visit id \t Patient id Patient Name \tDate of Visit \t\tDiagnosis \t\tPhysician \t\tTreatment ID \t\tTreatment Name \t\tTest id \t\tTest Name")
                            for x in myresult:
                                print(x[0], "\t\t", x[1], "\t\t", x[2], x[3], "\t\t", x[4], "\t\t", x[5], "\t\t", x[6],
                                      "\t\t", x[7], "\t\t", x[8], "\t\t", x[9], "\t\t", x[10])
                    case 5:
                        visit_test.addVisitTest()
                    case 6:
                        visit_test.viewOneVisitTest()
                    case 7:
                        visit_test.alterVisitTest()
                    case 8:
                        visit_treatment.addVisitTreat()
                    case 9:
                        visit_treatment.viewOneVisitTreat()
                    case 10:
                        visit_treatment.alterVisitTreat()
                    case _:
                        print("Invalid input.")
                        continue
                end = input("Are you finished with Patient History? (Y/N)")
                end = end.upper()
                if end == 'Y':
                    break
                elif end == 'N':
                    continue
                else:
                    print("Invalid input.")
                    continue
        case _:
            print("Invalid input")

    end = input("Are you finished with program? (Y/N)")
    end = end.upper()
    if end == 'Y':
        print("Thank you for using! Have a good day :)")
        quit()
    elif end == 'N':
        continue
    else:
        print("Invalid input.")
        continue