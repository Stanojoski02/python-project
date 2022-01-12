import tkinter as tk
calculation = ""
def add_to_calculation(symbol):
    global calculation
    calculation += str(symbol)
    text_result.delete(1.0,"end")
    text_result.insert(1.0,calculation)
def evaluate_calculation():
    try:
        global calculation
        result = str(eval(calculation))
        calculation = ""
        text_result.delete(1.0, "end")
        text_result.insert(1.0, result)
    except:
        clear_filed()
        text_result.insert(1.0,"Error")
def clear_filed():
    global calculation
    calculation = ""
    text_result.delete(1.0,"end")
root = tk.Tk()
root.config(bg="grey")
root.geometry("280x210")
text_result = tk.Text(root, height=2, width=16, font=("Ariel",24))
text_result.grid(columnspan=5)
btn_1 = tk.Button(root,text="1", command=lambda:add_to_calculation(1),width=8,bg="black",fg="white")
btn_1.grid(column=0,row=2)
btn_2 = tk.Button(root,text="2", command=lambda:add_to_calculation(2),width=8,bg="black",fg="white")
btn_2.grid(column=1,row=2)
btn_3 = tk.Button(root,text="3", command=lambda:add_to_calculation(3),width=8,bg="black",fg="white")
btn_3.grid(column=2,row=2)
btn_4 = tk.Button(root,text="4", command=lambda:add_to_calculation(4),width=8,bg="black",fg="white")
btn_4.grid(column=0,row=3)
btn_5 = tk.Button(root,text="5", command=lambda:add_to_calculation(5),width=8,bg="black",fg="white")
btn_5.grid(column=1,row=3)
btn_6 = tk.Button(root,text="6", command=lambda:add_to_calculation(6),width=8,bg="black",fg="white")
btn_6.grid(column=2,row=3)
btn_7 = tk.Button(root,text="7", command=lambda:add_to_calculation(7),width=8,bg="black",fg="white")
btn_7.grid(column=0,row=4)
btn_8 = tk.Button(root,text="8", command=lambda:add_to_calculation(8),width=8,bg="black",fg="white")
btn_8.grid(column=1,row=4)
btn_9 = tk.Button(root,text="9", command=lambda:add_to_calculation(9),width=8,bg="black",fg="white")
btn_9.grid(column=2,row=4)
btn_0 = tk.Button(root,text="0", command=lambda:add_to_calculation(1),width=8,bg="black",fg="white")
btn_0.grid(column=4,row=2)
btn_plus = tk.Button(root,text="+", command=lambda:add_to_calculation("+"),width=8,bg="black",fg="white")
btn_plus.grid(column=4,row=3)
btn_minus = tk.Button(root,text="-", command=lambda:add_to_calculation(1),width=8,bg="black",fg="white")
btn_minus.grid(column=4,row=4)
btn_ednak = tk.Button(root,text="=", command=evaluate_calculation,width=18,bg="black",fg="white")
btn_ednak.grid(columnspan=2,column=0,row=5)
btn_mn = tk.Button(root,text="*", command=lambda:add_to_calculation("*"),width=8,bg="black",fg="white")
btn_mn.grid(column=2,row=5)
btn_del = tk.Button(root,text="/", command=lambda:add_to_calculation("/"),width=8,bg="black",fg="white")
btn_del.grid(column=4,row=5)
btn_clear = tk.Button(root,text="c", command=clear_filed,width=8,bg="black",fg="white")
btn_clear.grid(column=4,row=6)




root.mainloop()