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
        #self.__packing()
        self.unpivotcsvs = {}
        self.selected_csv_name = None
        self.outputfolder = None
        self.cde_file = None

    def __init(self):
        self.hospital_frame()
        self.csv_file_frame()
        self.cdes_metadata_frame()
        self.output_frame()

    def hospital_frame(self):
        self.hosp_labelframe = tk.LabelFrame(self.master, text='Hospital')
        self.hospital_label = tk.Label(self.hosp_labelframe, text='Hospital Code:')
        self.hospital_entry = tk.Entry(self.hosp_labelframe)
        #packing...
        self.hosp_labelframe.grid(row=0, column=0)
        self.hospital_label.grid(row=0, column=0,sticky='w')
        self.hospital_entry.grid(row=0, column=1, columnspan=2, sticky='w')

    def cdes_metadata_frame(self):
        self.cde_labelframe = tk.LabelFrame(self.master, text='CDEs')
        self.cde_label_file = tk.Label(self.cde_labelframe, text='Metadata file:')
        self.cde_label = tk.Label(self.cde_labelframe, text='Not Selected', bg='white',  width=50)
        self.cde_load_btn = tk.Button(self.cde_labelframe, text='Select', command=self.load_cdes)
        #packing...
        self.cde_labelframe.grid(row=1, column=0)
        self.cde_label_file.grid(row=0, column=0)
        self.cde_label.grid(row=0, column=1, columnspan=3, padx=4, pady=4)
        self.cde_load_btn.grid(row=0, column=5)

    def csv_file_frame(self):
        self.harm_labelframe = tk.LabelFrame(self.master, text='CSV File Configuration')
        self.harm_label_csv = tk.Label(self.harm_labelframe, text='CSV File')
        self.harm_label_col = tk.Label(self.harm_labelframe, text='Columns')
        self.harm_label_fun = tk.Label(self.harm_labelframe, text='Functions')
        self.harm_label_exp = tk.Label(self.harm_labelframe, text='Expressions')
        self.harm_label_cde = tk.Label(self.harm_labelframe, text='CDEs')
        #
        self.harm_subframe_csv = tk.Frame(self.harm_labelframe)
        self.harm_subframe_col_fun = tk.Frame(self.harm_labelframe)
        #self.harm_subframe_fun = tk.Frame(self.harm_labelframe)
        #self.harm_subframe_exp = tk.Frame(self.harm_labelframe)
        self.harm_subframe_cde = tk.Frame(self.harm_labelframe)
        #
        self.csv_file_entry = tk.Entry(self.harm_subframe_csv)
        self.columns_cbox = ttk.Combobox(self.harm_subframe_col_fun, width=25)        
        self.functions_cbox = ttk.Combobox(self.harm_subframe_col_fun, width=25)
        self.expressions_text = tk.Text(self.harm_subframe_col_fun, width=35, height=3)        
        self.harm_plusCol_btn = tk.Button(self.harm_subframe_col_fun, text='+', command=self.add_column)
        self.harm_plusFun_btn = tk.Button(self.harm_subframe_col_fun, text='+', command=self.add_function)
        self.cdes_cbox = ttk.Combobox(self.harm_subframe_cde, width=25)
        #ok now start packing...
        self.harm_labelframe.grid(row=2, columnspan=8, 
                               padx=4, pady=4, ipadx=4, ipady=4,
                               sticky=['w','e'])
        self.harm_label_csv.grid(row=0, column=0)
        self.harm_subframe_col_fun.grid(row=3, column=0)
        self.harm_label_col.grid(row=2, column=0)
        self.columns_cbox.grid(row=3, column=0)
        self.harm_plusCol_btn.grid(row=3, column=4)
        self.harm_label_fun.grid(row=4, column=0)
        self.functions_cbox.grid(row=5, column=0)
        self.harm_plusFun_btn.grid(row=5, column=4)
        self.harm_label_exp.grid(row=2, column=6)
        self.expressions_text.grid(row=4, column=6)       

        self.harm_subframe_csv.grid(row=0, column=2, sticky='w')
      #  self.harm_label_cde.grid(row=2, column=10)
       # self.u_scrolbar1.pack(side='right', fill='y')      
        #self.u_scrolbar2.pack(side='right', fill='y')
        #self.harm_subframe_fun.grid(row=4, column=2, sticky='w') 
        #self.u_scrolbar3.pack(side='right', fill='y')
        #self.harm_subframe_exp.grid(row=2, column=6)
       # self.cdes_cbox.grid(row=3, column=8)
       # self.csv_file_entry.grid(row=3, column=8)

    def output_frame(self):
        self.out_labelframe = tk.LabelFrame(self.master, text='Output folder')
        self.out_label = tk.Label(self.out_labelframe, text='Not Selected', bg='white', width=50)       
        self.o_button1 = tk.Button(self.out_labelframe, text='Open', command=self.select_output)
        self.o_button2 = tk.Button(self.out_labelframe, text='Create files', command=self.createfiles)
        #packing...
        self.out_labelframe.grid(row=7, column=0)
        self.out_label.grid(row=7, column=1, pady=2)
        self.o_button1.grid(row=7, column=2)
        self.o_button2.grid(row=7, column=3, pady=2, padx=2)

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

    def load_cdes(self):
        return
    
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
        # get selected csv from previous listbox selection <--Update: needs to change
        csv_name = self.selected_csv_name
  
        csv_item = self.unpivotcsvs[csv_name]
        sel_index2 = self.u_listbox2.curselection()
        column = self.u_listbox2.get(sel_index2)
        if column not in csv_item.selected:
            csv_item.selected.add(column)
            csv_item = csv_item._replace(unpivoted = set(csv_item.headers) - csv_item.selected)
            self.u_listbox3.insert(tk.END, column)
            self.unpivotcsvs[csv_name]=csv_item

    def add_function(self):
        ok=True

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
 