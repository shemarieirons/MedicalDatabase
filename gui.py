"""
gui.py
Provides the graphical user interface for the Medical Records System using Tkinter.
Contains the main application class that connects user actions to the backend database.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import backend

class MedicalRecordsApp:
    """
    Main application class for the Medical Records System.
    Handles the creation of the notebook tabs, UI layouts, and event bindings.
    """
    def __init__(self, root):
        """Initialize the main application window and its tabs."""
        self.root = root
        self.root.title("Medical Records System")
        self.root.geometry("900x600")
        
        # Configure grid resizing so the notebook expands with the window
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Initialize Frame for each tab
        self.tab_patients = ttk.Frame(self.notebook)
        self.tab_diagnosis = ttk.Frame(self.notebook)
        self.tab_visits = ttk.Frame(self.notebook)
        self.tab_analytics = ttk.Frame(self.notebook)
        
        # Add tabs to the notebook
        self.notebook.add(self.tab_patients, text="Patient Management")
        self.notebook.add(self.tab_diagnosis, text="Diagnosis & Treatments")
        self.notebook.add(self.tab_visits, text="Visits")
        self.notebook.add(self.tab_analytics, text="Analytics")
        
        # Setup the UI layouts for each specific tab
        self.setup_patients_tab()
        self.setup_diagnosis_tab()
        self.setup_visits_tab()
        self.setup_analytics_tab()

        # Bind tab change event to refresh data automatically
        self.root.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.on_tab_changed(None)

    def on_tab_changed(self, event):
        """Refresh treeviews and analytics when navigating between tabs."""
        self.refresh_patients_list()
        self.refresh_diagnosis_data()
        self.refresh_visits_list()
        self.refresh_analytics()

    # --- PATIENT MANAGEMENT TAB ---
    def setup_patients_tab(self):
        """Build the input form and data table for the Patient Management tab."""
        self.tab_patients.columnconfigure(1, weight=1)
        self.tab_patients.rowconfigure(10, weight=1)
        
        # Form
        fields = ["First Name", "Last Name", "Address 1", "Address 2", "City", "Parish", "Country", "Gender"]
        self.patient_vars = {}
        
        for i, field in enumerate(fields):
            ttk.Label(self.tab_patients, text=field + ":").grid(row=i, column=0, padx=5, pady=5, sticky="e")
            if field == "Gender":
                var = tk.StringVar()
                cb = ttk.Combobox(self.tab_patients, textvariable=var, values=["Male", "Female", "Other"], state="readonly")
                cb.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                self.patient_vars[field] = var
            else:
                var = tk.StringVar()
                ttk.Entry(self.tab_patients, textvariable=var).grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                self.patient_vars[field] = var
                
        ttk.Button(self.tab_patients, text="Add Patient", command=self.add_patient_action).grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        # Treeview
        columns = ("ID", "First Name", "Last Name", "Gender", "City", "Country")
        self.patient_tree = ttk.Treeview(self.tab_patients, columns=columns, show="headings")
        for col in columns:
            self.patient_tree.heading(col, text=col)
            self.patient_tree.column(col, width=100)
        self.patient_tree.grid(row=len(fields)+1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    def add_patient_action(self):
        """Retrieve form data, validate it, and save the new patient to the database."""
        fname = self.patient_vars["First Name"].get().strip()
        lname = self.patient_vars["Last Name"].get().strip()
        gender = self.patient_vars["Gender"].get().strip()
        
        if not fname or not lname:
            messagebox.showerror("Validation Error", "First Name and Last Name are required.")
            return

        try:
            backend.add_patient(
                fname, lname, 
                self.patient_vars["Address 1"].get(),
                self.patient_vars["Address 2"].get(),
                self.patient_vars["City"].get(),
                self.patient_vars["Parish"].get(),
                self.patient_vars["Country"].get(),
                gender
            )
            messagebox.showinfo("Success", "Patient added successfully.")
            for var in self.patient_vars.values():
                var.set("")
            self.refresh_patients_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_patients_list(self):
        for item in self.patient_tree.get_children():
            self.patient_tree.delete(item)
        for p in backend.get_all_patients():
            self.patient_tree.insert("", "end", values=(p[0], p[1], p[2], p[8], p[5], p[7]))

    # --- DIAGNOSIS & TREATMENTS TAB ---
    def setup_diagnosis_tab(self):
        """Build the input forms and data table for the Diagnosis & Treatments tab."""
        self.tab_diagnosis.columnconfigure(1, weight=1)
        self.tab_diagnosis.columnconfigure(3, weight=1)
        self.tab_diagnosis.rowconfigure(10, weight=1)
        
        # Treat & Test entry frame
        tt_frame = ttk.LabelFrame(self.tab_diagnosis, text="Add Treatment or Test")
        tt_frame.grid(row=0, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        tt_frame.columnconfigure(1, weight=1)
        tt_frame.columnconfigure(4, weight=1)

        ttk.Label(tt_frame, text="Treatment Name:").grid(row=0, column=0, padx=5, pady=5)
        self.treat_var = tk.StringVar()
        ttk.Entry(tt_frame, textvariable=self.treat_var).grid(row=0, column=1, sticky="ew", padx=5)
        ttk.Button(tt_frame, text="Add Treatment", command=self.add_treatment_action).grid(row=0, column=2, padx=5)

        ttk.Label(tt_frame, text="Test Name:").grid(row=0, column=3, padx=5, pady=5)
        self.test_var = tk.StringVar()
        ttk.Entry(tt_frame, textvariable=self.test_var).grid(row=0, column=4, sticky="ew", padx=5)
        ttk.Button(tt_frame, text="Add Test", command=self.add_test_action).grid(row=0, column=5, padx=5)

        # Diagnosis block
        diag_frame = ttk.LabelFrame(self.tab_diagnosis, text="Add Diagnosis")
        diag_frame.grid(row=1, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        diag_frame.columnconfigure(1, weight=1)

        ttk.Label(diag_frame, text="Diagnosis Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.diag_name_var = tk.StringVar()
        ttk.Entry(diag_frame, textvariable=self.diag_name_var).grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(diag_frame, text="Treatment ID:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.diag_treat_var = tk.StringVar()
        self.cb_treat = ttk.Combobox(diag_frame, textvariable=self.diag_treat_var, state="readonly")
        self.cb_treat.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(diag_frame, text="Test ID:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.diag_test_var = tk.StringVar()
        self.cb_test = ttk.Combobox(diag_frame, textvariable=self.diag_test_var, state="readonly")
        self.cb_test.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        ttk.Button(diag_frame, text="Add Diagnosis", command=self.add_diagnosis_action).grid(row=3, column=0, columnspan=2, pady=10)

        # Treeview
        self.diag_tree = ttk.Treeview(self.tab_diagnosis, columns=("ID", "Diagnosis", "Treat ID", "Test ID"), show="headings")
        for col in ("ID", "Diagnosis", "Treat ID", "Test ID"):
            self.diag_tree.heading(col, text=col)
        self.diag_tree.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

    def add_treatment_action(self):
        tname = self.treat_var.get().strip()
        if not tname:
            messagebox.showerror("Error", "Treatment name required.")
            return
        backend.add_treatment(tname)
        messagebox.showinfo("Success", "Treatment added.")
        self.treat_var.set("")
        self.refresh_diagnosis_data()

    def add_test_action(self):
        testname = self.test_var.get().strip()
        if not testname:
            messagebox.showerror("Error", "Test name required.")
            return
        backend.add_test(testname)
        messagebox.showinfo("Success", "Test added.")
        self.test_var.set("")
        self.refresh_diagnosis_data()

    def add_diagnosis_action(self):
        dname = self.diag_name_var.get().strip()
        treat_val = self.diag_treat_var.get()
        test_val = self.diag_test_var.get()

        if not dname:
            messagebox.showerror("Error", "Diagnosis name required.")
            return
            
        treat_id = treat_val.split(":")[0] if treat_val else None
        test_id = test_val.split(":")[0] if test_val else None

        try:
            backend.add_diagnosis(dname, treat_id, test_id)
            messagebox.showinfo("Success", "Diagnosis added.")
            self.diag_name_var.set("")
            self.diag_treat_var.set("")
            self.diag_test_var.set("")
            self.refresh_diagnosis_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_diagnosis_data(self):
        treats = backend.get_all_treatments()
        self.cb_treat['values'] = [f"{t[0]}: {t[1]}" for t in treats]
        
        tests = backend.get_all_tests()
        self.cb_test['values'] = [f"{t[0]}: {t[1]}" for t in tests]
        
        for item in self.diag_tree.get_children():
            self.diag_tree.delete(item)
            
        for d in backend.get_all_diagnoses():
            self.diag_tree.insert("", "end", values=(d[0], d[1], d[2], d[3]))

    # --- VISITS TAB ---
    def setup_visits_tab(self):
        """Build the input form and data table for the Patient Visits tab."""
        self.tab_visits.columnconfigure(1, weight=1)
        self.tab_visits.rowconfigure(10, weight=1)

        ttk.Label(self.tab_visits, text="Patient:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.visit_patient_var = tk.StringVar()
        self.cb_visit_patient = ttk.Combobox(self.tab_visits, textvariable=self.visit_patient_var, state="readonly")
        self.cb_visit_patient.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(self.tab_visits, text="Diagnosis:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.visit_diag_var = tk.StringVar()
        self.cb_visit_diag = ttk.Combobox(self.tab_visits, textvariable=self.visit_diag_var, state="readonly")
        self.cb_visit_diag.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(self.tab_visits, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.visit_date_var = tk.StringVar()
        ttk.Entry(self.tab_visits, textvariable=self.visit_date_var).grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(self.tab_visits, text="Doctor:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.visit_doc_var = tk.StringVar()
        ttk.Entry(self.tab_visits, textvariable=self.visit_doc_var).grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(self.tab_visits, text="Test ID:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.visit_test_var = tk.StringVar()
        self.cb_visit_test = ttk.Combobox(self.tab_visits, textvariable=self.visit_test_var, state="readonly")
        self.cb_visit_test.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

        ttk.Button(self.tab_visits, text="Record Visit", command=self.record_visit_action).grid(row=5, column=0, columnspan=2, pady=10)

        # Treeview
        cols = ("Visit Code", "Patient", "Diagnosis", "Date", "Doctor", "Test")
        self.visit_tree = ttk.Treeview(self.tab_visits, columns=cols, show="headings")
        for col in cols:
            self.visit_tree.heading(col, text=col)
        self.visit_tree.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    def record_visit_action(self):
        pat_val = self.visit_patient_var.get()
        diag_val = self.visit_diag_var.get()
        date = self.visit_date_var.get().strip()
        doc = self.visit_doc_var.get().strip()
        test_val = self.visit_test_var.get()

        if not pat_val or not date or not doc:
            messagebox.showerror("Error", "Patient, Date and Doctor are required.")
            return

        pid = pat_val.split(":")[0]
        did = diag_val.split(":")[0] if diag_val else None
        tid = test_val.split(":")[0] if test_val else None

        try:
            backend.record_visit(pid, did, date, doc, tid)
            messagebox.showinfo("Success", "Visit recorded.")
            self.refresh_visits_list()
            self.visit_date_var.set("")
            self.visit_doc_var.set("")
            self.visit_patient_var.set("")
            self.visit_diag_var.set("")
            self.visit_test_var.set("")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_visits_list(self):
        patients = backend.get_all_patients()
        self.cb_visit_patient['values'] = [f"{p[0]}: {p[1]} {p[2]}" for p in patients]

        diags = backend.get_all_diagnoses()
        self.cb_visit_diag['values'] = [f"{d[0]}: {d[1]}" for d in diags]

        tests = backend.get_all_tests()
        self.cb_visit_test['values'] = [f"{t[0]}: {t[1]}" for t in tests]
        
        for item in self.visit_tree.get_children():
            self.visit_tree.delete(item)
        
        for v in backend.get_all_visits():
            self.visit_tree.insert("", "end", values=v)

    # --- ANALYTICS TAB ---
    def setup_analytics_tab(self):
        """Build the summary statistics layout and patient history search."""
        self.tab_analytics.columnconfigure(0, weight=1)
        self.tab_analytics.columnconfigure(1, weight=1)
        
        self.lbl_total_patients = ttk.Label(self.tab_analytics, text="Total Patients: 0", font=("Arial", 14))
        self.lbl_total_patients.grid(row=0, column=0, columnspan=2, pady=10)

        self.lbl_total_visits = ttk.Label(self.tab_analytics, text="Total Visits: 0", font=("Arial", 14))
        self.lbl_total_visits.grid(row=1, column=0, columnspan=2, pady=10)

        self.lbl_top_diagnosis = ttk.Label(self.tab_analytics, text="Most Common Diagnosis: N/A", font=("Arial", 14))
        self.lbl_top_diagnosis.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(self.tab_analytics, text="Refresh Analytics", command=self.refresh_analytics).grid(row=3, column=0, columnspan=2, pady=20)
        
        # Add basic patient history search
        ttk.Separator(self.tab_analytics, orient='horizontal').grid(row=4, column=0, columnspan=2, sticky='ew', pady=10)
        
        ttk.Label(self.tab_analytics, text="Patient History Search (PID):").grid(row=5, column=0, sticky='e', padx=5)
        self.hist_pid_var = tk.StringVar()
        ttk.Entry(self.tab_analytics, textvariable=self.hist_pid_var).grid(row=5, column=1, sticky='w', padx=5)
        ttk.Button(self.tab_analytics, text="Search", command=self.search_history).grid(row=6, column=0, columnspan=2, pady=10)
        
        self.hist_tree = ttk.Treeview(self.tab_analytics, columns=("Date", "Doctor", "Diagnosis", "Treatment", "Test"), show="headings")
        for col in ("Date", "Doctor", "Diagnosis", "Treatment", "Test"):
            self.hist_tree.heading(col, text=col)
        self.hist_tree.grid(row=7, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.tab_analytics.rowconfigure(7, weight=1)

    def refresh_analytics(self):
        stats = backend.basic_analytics()
        self.lbl_total_patients.config(text=f"Total Patients: {stats.get('total_patients', 0)}")
        self.lbl_total_visits.config(text=f"Total Visits: {stats.get('total_visits', 0)}")
        
        top_diag = stats.get('most_common_diagnosis', ("None", 0))
        if top_diag:
            self.lbl_top_diagnosis.config(text=f"Most Common Diagnosis: {top_diag[0]} ({top_diag[1]} times)")
        else:
            self.lbl_top_diagnosis.config(text="Most Common Diagnosis: N/A")

    def search_history(self):
        pid = self.hist_pid_var.get().strip()
        if not pid:
            return
            
        try:
            results = backend.get_patient_history(pid)
            for item in self.hist_tree.get_children():
                self.hist_tree.delete(item)
            for r in results:
                self.hist_tree.insert("", "end", values=r)
        except Exception as e:
            messagebox.showerror("Error", str(e))
