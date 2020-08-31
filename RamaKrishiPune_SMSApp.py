import tkinter as tk
from tkinter import filedialog
import pandas as pd
import requests
import datetime
import math


file_location = ""
plant_name = "Rama Krishi Rasayan - Pune"
plant_name_short = "RamaKrishi-Pune"

master = tk.Tk()


def open():
    global file_location
    master.filename = filedialog.askopenfilename(initialdir = "/", title = "Select a file")
    file_location = master.filename

    e1.insert(10, file_location)

    file_path = e1.get()
       
    return file_path
       

def main_func():

    global file_path
    global file_location

    if e1.get() == "":
        #file_path = open()
        print('Please Enter a valid file path')
        T.insert(tk.END, "Please Enter a valid file path\n")
   
    else:
        file_path = e1.get()
        e1.delete(0, tk.END)
        print(file_path)
   
    try:
        if ".csv" in file_path:
            data = pd.read_csv(file_path)
        elif ".xlsx" or ".xls" in file_path:
            data = pd.read_excel(file_path)
        
        if data.columns[0] == "Unnamed: 0" or data.columns[0] != "INVOICE NO":
            data.drop([0,1,2], inplace=True)
            header_row = 0
            data.columns = data.iloc[header_row]
            data.reset_index(inplace=True, drop = True)
            data.drop(header_row, inplace=True)
            data.reset_index(inplace=True, drop = True)
        


    except Exception as e:
        T.insert(tk.END, str(e) + "\n")

    # data is Excel sheet that will be read. Do the further processing below in this function.

    
    print(data.shape)
    count = 0 
    for i in range(data.shape[0]):
        if math.isnan(data['DD No.'][i]) != True:
        
            mobile_number=data['MOBILE NO'][i]
            mobile_number = mobile_number[1:11]
            date = data['INVOICE DATE'][i]
            date = datetime.datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')
            message='{} has raised an invoice dated {}. Pl. Acknowledge using DD No-{}. Product Details: {}/{}/{} MT.'.format(plant_name, str(date), str(data['DD No.'][i]),plant_name_short, str(data['COMPANY PRODUCT'][i]), str(data['QUANTITY(MT)'][i]))
            url='http://sms.itbizcon.com/sms/sendsms.jsp?apikey=648D39BDDFA6CD89&sms='+message+'&mobiles='+str(mobile_number)
            response=requests.get(url)
            print(response.status_code)
            count+=1
            T.insert(tk.END, "Count = {}, Mobile number = {}, Status = {} \n".format(count, mobile_number, response.status_code))
            
    print(count)


    # End of main function
   

tk.Label(master, text="Enter File path or browse").grid(row=0, padx = 4, pady = 4)

tk.Label(master, text = "Output window:", justify ='left').grid(sticky = 'W', row = 4, column = 0, padx = 6)
tk.Label(master, text = "Software by PE Associates", font = ('Times italic', 7)).grid(sticky = 'E', row = 6, column = 2, pady = 4, padx = 10)

e1 = tk.Entry(master, width = 40)
e1.grid(row=0, column=1, padx = 4, pady = 4)

T = tk.Text(master, height=20, width = 70)
T.grid(row = 5, padx = 6, pady = 4, sticky=tk.W, columnspan = 4)

tk.Button(master,
          text='Quit',
          command=master.quit, width = 20).grid(row=2,
                                    column=1,
                                    sticky=tk.W,
                                    pady=6, padx = 40)


my_btn = tk.Button(master, text = 'Open File', command = open).grid(row = 0, column = 2, padx = 4, pady = 4)

my_btn2 = tk.Button(master, text = 'Run', command = main_func, width = 20).grid(row = 1, column = 1, sticky=tk.W, pady=6, padx = 40)

master.title(plant_name)
#p1 = tk.PhotoImage(file = 'icon/rama.jpg')
#master.iconphoto(False, p1)
master.resizable(False, False)

master.mainloop()