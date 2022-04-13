import tkinter as tk

def W_Input (label='Input dialog box', timeout=5000):
    w = tk.Tk()
    w.title(label)
    W_Input.data=''
    wFrame = tk.Frame(w, background="light yellow", padx=20, pady=20)
    wFrame.pack()
    wEntryBox = tk.Entry(wFrame, background="white", width=100)
    wEntryBox.focus_force()
    wEntryBox.pack()

    def fin():
        W_Input.data = str(wEntryBox.get())
        w.destroy()
    wSubmitButton = tk.Button(w, text='OK', command=fin, default='active')
    wSubmitButton.pack()

# --- optionnal extra code in order to have a stroke on "Return" equivalent to a mouse click on the OK button
    def fin_R(event):  fin()
    w.bind("<Return>", fin_R)
# --- END extra code ---

    w.after(timeout, w.destroy) # This is the KEY INSTRUCTION that destroys the dialog box after the given timeout in millisecondsd
    w.mainloop()

# W_Input() # can be called with 2 parameter, the window title (string), and the timeout duration in miliseconds
#
# if W_Input.data: print('\nYou entered this : ', W_Input.data, end=2*'\n')
#
# else: print('\nNothing was entered \n')