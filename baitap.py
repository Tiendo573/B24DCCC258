import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime
import os

CSV_FILE = "employees.csv"
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["Name", "Birthday"])
    df.to_csv(CSV_FILE, index=False)



def save_employee():
    name = entry_name.get()
    birthday = entry_birthday.get()
    if not name or not birthday:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
        return

    try:

        datetime.strptime(birthday, "%d/%m/%Y")
    except ValueError:
        messagebox.showwarning("Cảnh báo", "Ngày sinh không hợp lệ. Vui lòng nhập đúng định dạng (dd/mm/yyyy).")
        return


    df = pd.read_csv(CSV_FILE)
    new_employee = pd.DataFrame({"Name": [name], "Birthday": [birthday]})
    df = pd.concat([df, new_employee], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    messagebox.showinfo("Thông báo", "Thông tin nhân viên đã được lưu.")



def show_birthday_today():
    today = datetime.today().strftime("%d/%m")
    df = pd.read_csv(CSV_FILE)
    today_employees = df[df["Birthday"].str.contains(today, na=False)]

    if today_employees.empty:
        messagebox.showinfo("Thông báo", "Không có nhân viên nào có sinh nhật hôm nay.")
    else:
        result = "\n".join(today_employees["Name"].values)
        messagebox.showinfo("Sinh nhật hôm nay", result)



def export_to_excel():
    df = pd.read_csv(CSV_FILE)


    df["Birthday"] = pd.to_datetime(df["Birthday"], format="%d/%m/%Y")


    df = df.sort_values(by="Birthday", ascending=False)


    df.to_excel("employee_list.xlsx", index=False, engine='openpyxl')
    messagebox.showinfo("Thông báo", "Danh sách đã được xuất ra file Excel.")



root = tk.Tk()
root.title("Quản lý nhân viên")


label_name = tk.Label(root, text="Họ tên:")
label_name.grid(row=0, column=0, padx=10, pady=5)
entry_name = tk.Entry(root, width=30)
entry_name.grid(row=0, column=1, padx=10, pady=5)

label_birthday = tk.Label(root, text="Ngày sinh (dd/mm/yyyy):")
label_birthday.grid(row=1, column=0, padx=10, pady=5)
entry_birthday = tk.Entry(root, width=30)
entry_birthday.grid(row=1, column=1, padx=10, pady=5)


btn_save = tk.Button(root, text="Lưu thông tin", command=save_employee)
btn_save.grid(row=2, column=0, columnspan=2, pady=10)


btn_birthday_today = tk.Button(root, text="Sinh nhật ngày hôm nay", command=show_birthday_today)
btn_birthday_today.grid(row=3, column=0, columnspan=2, pady=5)


btn_export_excel = tk.Button(root, text="Xuất toàn bộ danh sách", command=export_to_excel)
btn_export_excel.grid(row=4, column=0, columnspan=2, pady=5)


root.mainloop()
