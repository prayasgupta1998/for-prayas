import tkinter as tk
from tkinter import filedialog
import pandas as pd
import requests


file_location = ""

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
        
        if data.columns[0] == "Unnamed: 0":
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
    for i in range(data.shape[0] - 1):
        mobile_number=data['MOBILE NO'][i]
        mobile_number = mobile_number[1:11]
        message='Your Quantity is:'+str(data['QUANTITY(MT)'][i])
    
        url="http://sms.itbizcon.com/sms/sendsms.jsp?apikey=648D39BDDFA6CD89&sms="+message+"&mobiles="+str(mobile_number)
        response=requests.get(url)
        print(response.status_code)
        count+=1
        T.insert(tk.END, "Count = {}, Mobile number = {}, Status = {} \n".format(count, mobile_number, response.status_code))
    print(count)


    # End of main function
   

tk.Label(master, text="Enter File path or browse").grid(row=0)

tk.Label(master, text = "Output window:").grid(row = 4, column = 0)

e1 = tk.Entry(master)
e1.grid(row=0, column=1, padx = 2)

T = tk.Text(master, height=10, width = 40)
T.grid(row = 5, padx = 8, pady = 4, sticky=tk.W, columnspan = 3)

tk.Button(master,
          text='Quit',
          command=master.quit).grid(row=2,
                                    column=1,
                                    sticky=tk.W,
                                    pady=6)


my_btn = tk.Button(master, text = 'Open File', command = open).grid(row = 0, column = 2, padx = 2)

my_btn2 = tk.Button(master, text = 'Run', command = main_func).grid(row = 1, column = 1, sticky=tk.W, pady=6)


master.mainloop()