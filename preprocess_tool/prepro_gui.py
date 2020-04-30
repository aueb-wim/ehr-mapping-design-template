#!/usr/bin/env python3
import os
import csv
from collections import namedtuple
from tkinter import ttk
import tkinter as tk
import tkinter.filedialog as tkfiledialog
import tkinter.messagebox as tkmessagebox
from prepare import produce_encounter_properties, produce_patient_properties
from prepare import produce_unpivot_files, produce_run_sh_script

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

UnpivotCsv = namedtuple('UnpivotCsv', ['name', 'headers', 'selected', 'unpivoted'])

class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.__init()
        self.__packing()
        self.patientcsv = None
        self.visitscsv = None
        self.unpivotcsvs = {}
        self.selected_csv_name = None
        self.outputfolder = None
        #self.add_headers(['one','two','three', 'four'], self.p_csv_headers_lbox)

    def __init(self):

        #hospital code section
        self.hospital_label = tk.Label(self.master, text = 'Hospital Code:')
        self.hospital_entry = tk.Entry(self.master)


        # patient mapping section
        self.p_labelframe = tk.LabelFrame(self.master, text='Patient Mapping Configuration')
        self.p_csv_label1 = tk.Label(self.p_labelframe, text='Patient csv file:')
        self.p_csv_label2 = tk.Label(self.p_labelframe, text='Not Selected',
                                     bg='white',  width=50)
        self.p_csv_load_btn = tk.Button(self.p_labelframe, text='Select', command=self.load_patient_csv)
        self.p_csv_label3 = tk.Label(self.p_labelframe, text='Select column for PatientID:')
        #self.p_headers_frame = tk.Frame(self.p_labelframe)
        #self.p_csv_headers_lbox = tk.Listbox(self.p_headers_frame, selectmode='SINGLE',  height=3)
        self.p_csv_headers_cbox = ttk.Combobox(self.p_labelframe, width=50)
        #self.p_csv_scrollbar = tk.Scrollbar(self.p_headers_frame, command=self.p_csv_headers_lbox.yview)
        #self.p_csv_headers_lbox.config(yscrollcommand = self.p_csv_scrollbar.set)

        # encounter mapping section 
        self.c_labelframe = tk.LabelFrame(self.master, text='Encounter Mapping Configuration')
        self.c_csv_label1 = tk.Label(self.c_labelframe, text='Visits csv file:')
        self.c_csv_label2 = tk.Label(self.c_labelframe, text='Not Selected',
                                     bg='white', width=50)
        self.c_csv_load_btn = tk.Button(self.c_labelframe, text='Select', command=self.load_visit_csv)
        self.c_csv_label3 = tk.Label(self.c_labelframe, text='Select column for VisitID:')
        self.c_csv_label4 = tk.Label(self.c_labelframe, text='Select column for PatientID:')
        self.c_csv_headers_cbox1 = ttk.Combobox(self.c_labelframe, width=50)
        self.c_csv_headers_cbox2 = ttk.Combobox(self.c_labelframe, width=50)

        # unpivoting section
        self.u_labelframe = tk.LabelFrame(self.master, text='Unpivoting Configuration')
        self.u_label1 = tk.Label(self.u_labelframe, text='csv files to be unpivoted')
        self.u_label2 = tk.Label(self.u_labelframe, text='csv Headers')
        self.u_label3 = tk.Label(self.u_labelframe, text='Selected Columns')

        self.u_subframe1 = tk.Frame(self.u_labelframe)
        self.u_subframe2 = tk.Frame(self.u_labelframe)
        self.u_subframe3 = tk.Frame(self.u_labelframe)

        self.u_listbox1 = tk.Listbox(self.u_subframe1, exportselection=0)
        self.u_listbox1.bind('<<ListboxSelect>>', self.on_select_csv)
        
        self.u_listbox2 = tk.Listbox(self.u_subframe2, exportselection=0)
        self.u_listbox3 = tk.Listbox(self.u_subframe3, exportselection=0)

        self.u_scrolbar1 = tk.Scrollbar(self.u_subframe1, command=self.u_listbox1.yview)
        self.u_scrolbar2 = tk.Scrollbar(self.u_subframe2, command=self.u_listbox2.yview)
        self.u_scrolbar3 = tk.Scrollbar(self.u_subframe3, command=self.u_listbox3.yview)

        self.u_listbox1.config(yscrollcommand=self.u_scrolbar1.set)
        self.u_listbox2.config(yscrollcommand=self.u_scrolbar2.set)
        self.u_listbox3.config(yscrollcommand=self.u_scrolbar3.set)

        self.u_subframe4 = tk.Frame(self.u_labelframe)
        self.u_load_btn = tk.Button(self.u_subframe4, text='Add file', command=self.load_unpivot_csv)
        self.u_unload_btn = tk.Button(self.u_subframe4, text='Remove file', command=self.unload_unpivot_csv)
        self.u_add_btn = tk.Button(self.u_labelframe, text='Add', command=self.add_column)
        self.u_remove_btn = tk.Button(self.u_labelframe, text='Remove', command=self.remove_column)

        # output path folder section
        self.o_label1 = tk.Label(self.master, text='output folder:')
        self.o_label2 = tk.Label(self.master, text='Not Selected', bg='white', width=50)
        
        self.o_button1 = tk.Button(self.master, text='Open', command=self.select_output)
        self.o_button2 = tk.Button(self.master, text='Create files', command=self.createfiles)


    def __packing(self):
        self.hospital_label.grid(row=0, sticky='e')
        self.hospital_entry.grid(row=0, column=1, sticky='w', pady=4)


        #self.p_labelframe.pack(fill='both', expand='yes', ipadx=4, ipady=4,
        #                      padx=4, pady=4)
        self.p_labelframe.grid(row=1, columnspan=4, padx=4, pady=4, ipadx=4, ipady=4)
        self.p_csv_label1.grid(row=0, column=0, sticky='e')
        self.p_csv_label2.grid(row=0, column=1, sticky='e', padx=2)
        self.p_csv_load_btn.grid(row=0, column=2)
        self.p_csv_label3.grid(row=1, column=0, sticky='e')

        self.p_csv_headers_cbox.grid(row=1, column=1)

        #self.p_headers_frame.grid(row=2, column=0)
        #self.p_csv_headers_lbox.pack(side='left')
        #self.p_csv_scrollbar.pack(side='right', fill='y')

        self.c_labelframe.grid(row=2, columnspan=4, padx=4, pady=4, ipadx=4, ipady=4)
        self.c_csv_label1.grid(row=0, column=0, sticky='e')
        self.c_csv_label2.grid(row=0, column=1)
        self.c_csv_load_btn.grid(row=0, column=2)
        self.c_csv_label3.grid(row=1, column=0, sticky='e')
        self.c_csv_headers_cbox1.grid(row=1, column=1, pady=4)
        self.c_csv_label4.grid(row=2, column=0, sticky='e')
        self.c_csv_headers_cbox2.grid(row=2, column=1)

        self.u_labelframe.grid(row=3, columnspan=4, 
                               padx=4, pady=4, ipadx=4, ipady=4,
                               sticky=['w','e'])
        self.u_label1.grid(row=0, column=0),
        self.u_label2.grid(row=0, column=2)
        self.u_label3.grid(row=0, column=4)

        self.u_subframe1.grid(row=1, column=0, sticky='w', padx=2, pady=2)
        self.u_listbox1.pack(side='left', fill='x')
        self.u_scrolbar1.pack(side='right', fill='y')

        self.u_subframe2.grid(row=1, column=2, sticky='w')
        self.u_listbox2.pack(side='left')
        self.u_scrolbar2.pack(side='right', fill='y')

        self.u_subframe3.grid(row=1, column=4, sticky='e')
        self.u_listbox3.pack(side='left')
        self.u_scrolbar3.pack(side='right', fill='y')

        self.u_subframe4.grid(row=2, column=0)
        self.u_load_btn.pack(side='left')
        self.u_unload_btn.pack(side='left')
        self.u_add_btn.grid(row=1, column=3)
        self.u_remove_btn.grid(row=2, column=4)

        self.o_label1.grid(row=4, column=0)
        self.o_label2.grid(row=4, column=1, pady=2)
        self.o_button1.grid(row=4, column=2)
        self.o_button2.grid(row=4, column=3, pady=2, padx=2)


    def add_items(self, headers, listbox):
        index = 1
        for header in headers:
            listbox.insert(index, header)
            index += 1

    def load_patient_csv(self):
        filepath = tkfiledialog.askopenfilename(title='select patient csv file',
                                                filetypes=(('csv files', '*.csv'),
                                                           ('all files', '*.*')))
        if filepath:
            csv_name = os.path.basename(filepath)
            self.patientcsv = csv_name
            with open(filepath, 'r') as csvfile:
                data = csv.DictReader(csvfile)
                self.p_csv_label2.config(text=csv_name)
                self.p_csv_headers_cbox.config(values=data.fieldnames)

    def load_visit_csv(self):
        filepath = tkfiledialog.askopenfilename(title='select visits csv file',
                                                filetypes=(('csv files', '*.csv'),
                                                           ('all files', '*.*')))
        if filepath:
            csv_name = os.path.basename(filepath)
            self.visitscsv = csv_name
            with open(filepath, 'r') as csvfile:
                data = csv.DictReader(csvfile)
                self.c_csv_label2.config(text=csv_name)
                self.c_csv_headers_cbox1.config(values=data.fieldnames)
                self.c_csv_headers_cbox2.config(values=data.fieldnames)

    def load_unpivot_csv(self):
        filepath = tkfiledialog.askopenfilename(title='select visits csv file',
                                                filetypes=(('csv files', '*.csv'),
                                                           ('all files', '*.*')))
        if filepath:
            csv_name = os.path.basename(filepath)
            with open(filepath, 'r') as csvfile:
                data = csv.DictReader(csvfile)
                unpivot_csv = UnpivotCsv(name=csv_name, headers=data.fieldnames,
                                         selected=set(), unpivoted=set())
                if csv_name not in self.unpivotcsvs:
                    self.u_listbox1.insert(tk.END, csv_name)
                self.unpivotcsvs[csv_name] = unpivot_csv
            self.u_listbox2.delete(0, tk.END)
            self.u_listbox3.delete(0, tk.END)
                
    
    def unload_unpivot_csv(self):
        sel_index = self.u_listbox1.curselection()
        csv_name = self.u_listbox1.get(sel_index)
        del self.unpivotcsvs[csv_name]
        self.u_listbox1.delete(sel_index)
        self.u_listbox2.delete(0, tk.END)
        self.u_listbox3.delete(0, tk.END)
        self.selected_csv_name = None


                    
    def on_select_csv(self, event):
        sel_index = self.u_listbox1.curselection()
        csv_name = self.u_listbox1.get(sel_index)
        csv_item = self.unpivotcsvs[csv_name]
        self.u_listbox2.delete(0, tk.END)
        self.u_listbox3.delete(0, tk.END)
        self.add_items(csv_item.headers, self.u_listbox2)
        self.add_items(csv_item.selected, self.u_listbox3)
        self.selected_csv_name = csv_name
        #self.u_listbox2.insert(tk.END, csv_name)
    
    
    def add_column(self):
        # get selected csv from previous listbox selection
        csv_name = self.selected_csv_name
  
        csv_item = self.unpivotcsvs[csv_name]
        sel_index2 = self.u_listbox2.curselection()
        column = self.u_listbox2.get(sel_index2)
        if column not in csv_item.selected:
            csv_item.selected.add(column)
            csv_item = csv_item._replace(unpivoted = set(csv_item.headers) - csv_item.selected)
            self.u_listbox3.insert(tk.END, column)
            self.unpivotcsvs[csv_name]=csv_item

    def remove_column(self):
        # get selected csv from previous listbox selection
        csv_name = self.selected_csv_name
        csv_item = self.unpivotcsvs[csv_name]
        
        sel_index = self.u_listbox3.curselection()
        column = self.u_listbox3.get(sel_index)
        csv_item.selected.remove(column)
        self.u_listbox3.delete(sel_index)
        csv_item = csv_item._replace(unpivoted = set(csv_item.headers) - csv_item.selected)
        self.unpivotcsvs[csv_name]=csv_item

    def select_output(self):
        outputfolder = tkfiledialog.askdirectory(title='Select Output Folder')
        if outputfolder:
            if not os.path.isdir(outputfolder):
                os.mkdir(outputfolder)
            self.outputfolder = outputfolder
            self.o_label2.config(text=outputfolder)

    def createfiles(self):
        hospital_code = self.hospital_entry.get()
        warningtitle='Could not create config files'

        p_patientid = self.p_csv_headers_cbox.get()

        visitid = self.c_csv_headers_cbox1.get()
        c_patienid = self.c_csv_headers_cbox2.get()

        if hospital_code == '':
            tkmessagebox.showwarning(warningtitle,
                                     'Please, enter hospital code')
        
        elif not self.patientcsv:
            tkmessagebox.showwarning(warningtitle,
                                     'Please, select patient csv file')

        elif not p_patientid:
            tkmessagebox.showwarning(warningtitle,
                                     'Please, select patientID column in patient csv')

        elif not self.visitscsv:
            tkmessagebox.showwarning(warningtitle,
                                     'Please, select visits csv file')

        elif not visitid:
            tkmessagebox.showwarning(warningtitle,
                                     'Please, select visitID column in visits csv')

        elif not c_patienid:
            tkmessagebox.showwarning(warningtitle,
                                     'Please, select patientID column in visits csv')

        elif not self.outputfolder:
            tkmessagebox.showwarning(warningtitle,
                                     'Please, select configuration files output folder')

        produce_patient_properties(self.outputfolder, self.patientcsv, p_patientid, hospital_code)
        produce_encounter_properties(self.outputfolder, self.visitscsv, visitid, c_patienid, hospital_code)
        produce_run_sh_script(self.outputfolder, self.unpivotcsvs)
        if len(self.unpivotcsvs) != 0:
            for key, item in self.unpivotcsvs.items():
                produce_unpivot_files(self.outputfolder, item.name, item.selected, item.unpivoted)

        tkmessagebox.showinfo(title='Status info',
                message='Config files have been created successully')

        
        




def main():
    """Main Application Window"""
    root = tk.Tk()
    app = Application(master=root)
    app.master.title('Preprocess Step - Designing Tool')
    app.master.resizable(False, False)
    app.mainloop()


if __name__ == '__main__':
    main()
 