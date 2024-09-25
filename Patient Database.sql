create database Medical_Records1
use Medical_Records1

create table patient(
	pid int PRIMARY KEY,
	fname varchar(255) NOT NULL,
	lname varchar(255) NOT NULL,
	address1 varchar(255) NOT NULL,
	address2 varchar(255),
	city varchar(255) NOT NULL,
	parish varchar(255) NOT NULL,
	country varchar(255) NOT NULL,
	gender char NOT NULL
);

create table treat(
	treatid int PRIMARY KEY,
	tname varchar(255) NOT NULL
);

create table test (
	testid int PRIMARY KEY,
	testname varchar(255) NOT NULL
);

create table Diagnosis (
	diagid int PRIMARY KEY,
	dname varchar(255) NOT NULL,
	diagtreatid int NOT NULL,
	diagtestid int NOT NULL,
	constraint diag_test FOREIGN KEY (diagtestid) references test(testid),
	constraint diag_treat FOREIGN KEY (diagtreatid) references treat(treatid)
);


create table PtVisit (
	visitcode int identity(1,1) PRIMARY KEY,
	visitptid int NOT NULL,
	visitdiagid int,
	visitdate date NOT NULL,
	doctor varchar(255),
	visittestid int NOT NULL
	constraint visitptidlink FOREIGN KEY (visitptid) references patient(pid),
	constraint visitdiagidlink FOREIGN KEY (visitdiagid) references Diagnosis(diagid),
	constraint visittestidlink FOREIGN KEY (visittestid) references Test(testid)
);

-- Inserting test data into the patient table 
INSERT INTO patient (pid, fname, lname, address1, address2, city, parish, country, gender) 
VALUES (1, 'John', 'Doe', '123 Main St', 'Apt 4B', 'Kingston', 'Kingston', 'Jamaica', 'M'), 
(2, 'Jane', 'Smith', '456 Maple Ave', NULL, 'Montego Bay', 'St. James', 'Jamaica', 'F'), 
(3, 'Alice', 'Johnson', '789 Oak Dr', 'Suite 5', 'Negril', 'Westmoreland', 'Jamaica', 'F'), 
(4, 'Bob', 'Brown', '321 Pine Ln', NULL, 'Ocho Rios', 'St. Ann', 'Jamaica', 'M'); 

-- Inserting test data into the treat table 
INSERT INTO treat (treatid, tname)
VALUES (1, 'Physical Therapy'), (2, 'Medication'), (3, 'Surgery'), (4, 'Counseling');

-- Inserting test data into the test table 
INSERT INTO test (testid, testname) VALUES (1, 'Blood Test'), (2, 'X-Ray'), (3, 'MRI'), (4, 'Urine Test'); 

-- Inserting test data into the Diagnosis table 
INSERT INTO Diagnosis (diagid, dname, diagtreatid, diagtestid) 
VALUES (1, 'Flu', 1, 1), (2, 'Fracture', 3, 2), (3, 'Anxiety', 4, 3), (4, 'Diabetes', 2, 4); 

-- Inserting test data into the PtVisit table 
INSERT INTO PtVisit (visitptid, visitdiagid, visitdate, doctor, visittestid) 
VALUES (1, 1, '2024-09-01', 'Dr. Williams', 1), 
(2, 2, '2024-09-02', 'Dr. Smith', 2), 
(3, 3, '2024-09-03', 'Dr. Johnson', 3), 
(4, 4, '2024-09-04', 'Dr. Brown', 4); 

--just the pt visits
select pa
from PtVisit V
inner join PtVisit
on ptvisit.visitptid = p.pid