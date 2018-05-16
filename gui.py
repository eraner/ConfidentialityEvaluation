from Tkinter import *
import datetime
import Controller
import subprocess as sp


def evaluate(log):
    results = Controller.check_auth_system(log)
    results_window = Tk()
    color = ""
    if results < 3:
        color = "green"
    elif results < 6:
        color = "yellow"
    else:
        color = "red"
    results_window.configure(bg=color)
    label_result = Label(results_window, text="Damage assessment: " + str(results), bg=color, font=("Helvetica", 32))
    label_result.pack(side="top")
    results_window.mainloop()


def open_NVD(log):
    log.print_to_log("NVD", "Opening the local copy of NVD file")
    programName = "notepad.exe"
    fileName = "Utils\\NVD\\NVD_File\\Modified\\nvdcve-1.0-modified.json"
    sp.Popen([programName, fileName])


def update_NVD(log):
    log.print_to_log("NVD", "Getting the latest NVD version..")
    programName = "python"
    fileName = "Utils\\NVD\\NVD_Handler.py"
    sp.Popen([programName, fileName])


class MainWindow:

    def __init__(self):
        self.log_window = Tk()
        self.root = Tk()
        self.fields_open = False

        # Main window
        self.root.title("Confidentiality assessment")
        self.root.geometry("600x450+200+200")

        mainFrame = Frame(self.root)
        mainFrame.pack(side="top")

        self.add_log()
        self.add_buttons(mainFrame)
        self.log_window.mainloop()
        self.root.mainloop()

    def add_buttons(self, mainFrame):
        editButton = Button(mainFrame, text="Edit Opt database", command=lambda: self.edit_auth_system())
        editButton.pack(side="left")

        evaluateButton = Button(mainFrame, text="Evaluate confidentiality", command=lambda: evaluate(self))
        evaluateButton.pack(side="left")

        openNVD = Button(mainFrame, text="Open NVD file", command=lambda: open_NVD(self))
        openNVD.pack(side="left")

        updateNVD = Button(mainFrame, text="Update NVD file", command=lambda: update_NVD(self))
        updateNVD.pack(side="left")

        print_auth = Button(mainFrame, text="Present Auth system", command=lambda: Controller.print_auth_system(self))
        print_auth.pack(side="left")

    def add_log(self):
        self.log_window.geometry("+810+0")
        self.log_window.title("Log")
        self.text = Text(self.log_window, height=45, width=80, bg="black", fg="green")

        vscroll = Scrollbar(self.log_window, orient=VERTICAL, command=self.text.yview)
        vscroll.pack(side="right", fill=Y)
        self.text.pack()
        self.text['yscroll'] = vscroll.set
        self.text.config(state=DISABLED)

    def print_to_log(self, module_name, log_message):
        time = datetime.datetime.now().time()
        self.text.configure(state=NORMAL)
        self.text.insert(END, "[<" + str(time) + "> " + module_name + "] " + log_message + "\n")
        self.text.config(state=DISABLED)
        self.text.see("end")

    def add_user(self, edit_frame):
        if self.fields_open:
            return
        self.fields_open = True
        add_user_frame = Frame(edit_frame)
        add_user_frame.grid(row=1)

        username_label = Label(add_user_frame, text="Username:")
        role_label = Label(add_user_frame, text="Role:")
        username_text = Entry(add_user_frame)
        role_text = Entry(add_user_frame)
        cancel_b = Button(add_user_frame, text="cancel", command=lambda: self.close_fields(add_user_frame))
        add_b = Button(add_user_frame, text="Add", command=lambda: Controller
                       .add_user(username_text.get(), role_text.get(), self) or self.close_fields(add_user_frame))

        add_b.grid(row=3, column=1)
        cancel_b.grid(row=3, column=0)
        username_label.grid(row=1, column=0)
        role_label.grid(row=2, column=0)
        username_text.grid(row=1, column=1)
        role_text.grid(row=2, column=1)

    def remove_user(self, edit_frame):
        if self.fields_open:
            return
        self.fields_open = True

        remove_user_frame = Frame(edit_frame)
        remove_user_frame.grid(row=1)

        username_label = Label(remove_user_frame, text="Username:")
        username_text = Entry(remove_user_frame)
        cancel_b = Button(remove_user_frame, text="cancel", command=lambda: self.close_fields(remove_user_frame))
        remove_b = Button(remove_user_frame, text="Remove", command=lambda: Controller
                          .delete_user(username_text.get(), self) or self.close_fields(remove_user_frame))

        remove_b.grid(row=3, column=1)
        cancel_b.grid(row=3, column=0)
        username_label.grid(row=1, column=0)
        username_text.grid(row=1, column=1)

    def add_role(self, edit_frame):
        if self.fields_open:
            return
        self.fields_open = True
        add_role_frame = Frame(edit_frame)
        add_role_frame.grid(row=1)

        role_label = Label(add_role_frame, text="Role:")
        rank_label = Label(add_role_frame, text="Rank:")
        role_text = Entry(add_role_frame)
        rank_text = Entry(add_role_frame)
        cancel_b = Button(add_role_frame, text="cancel", command=lambda: self.close_fields(add_role_frame))
        add_b = Button(add_role_frame, text="Add", command=lambda: Controller
                       .add_role(role_text.get(), rank_text.get(), self) or self.close_fields(add_role_frame))

        add_b.grid(row=3, column=1)
        cancel_b.grid(row=3, column=0)
        role_label.grid(row=1, column=0)
        rank_label.grid(row=2, column=0)
        role_text.grid(row=1, column=1)
        rank_text.grid(row=2, column=1)

    def remove_role(self, edit_frame):
        if self.fields_open:
            return
        self.fields_open = True

        remove_role_frame = Frame(edit_frame)
        remove_role_frame.grid(row=1)

        role_label = Label(remove_role_frame, text="Role name:")
        role_text = Entry(remove_role_frame)
        cancel_b = Button(remove_role_frame, text="cancel", command=lambda: self.close_fields(remove_role_frame))
        remove_b = Button(remove_role_frame, text="Remove", command=lambda: Controller
                          .delete_role(role_text.get(), self) or self.close_fields(remove_role_frame))

        remove_b.grid(row=3, column=1)
        cancel_b.grid(row=3, column=0)
        role_label.grid(row=1, column=0)
        role_text.grid(row=1, column=1)

    def add_resource(self, edit_frame):
        if self.fields_open:
            return
        self.fields_open = True
        add_resource_frame = Frame(edit_frame)
        add_resource_frame.grid(row=1)

        resource_name_label = Label(add_resource_frame, text="Resource name:")
        type_label = Label(add_resource_frame, text="Type:")
        resource_name_text = Entry(add_resource_frame)
        type_text = Entry(add_resource_frame)
        cancel_b = Button(add_resource_frame, text="cancel", command=lambda: self.close_fields(add_resource_frame))
        add_b = Button(add_resource_frame, text="Add", command=lambda: Controller
                       .add_resource(resource_name_text.get(), type_text.get(), self) or self.close_fields(add_resource_frame))

        add_b.grid(row=3, column=1)
        cancel_b.grid(row=3, column=0)
        resource_name_label.grid(row=1, column=0)
        type_label.grid(row=2, column=0)
        resource_name_text.grid(row=1, column=1)
        type_text.grid(row=2, column=1)

    def remove_resource(self, edit_frame):
        if self.fields_open:
            return
        self.fields_open = True

        remove_resource_frame = Frame(edit_frame)
        remove_resource_frame.grid(row=1)

        resource_label = Label(remove_resource_frame, text="Resource ID:")
        resource_text = Entry(remove_resource_frame)
        cancel_b = Button(remove_resource_frame, text="cancel", command=lambda: self.close_fields(remove_resource_frame))
        remove_b = Button(remove_resource_frame, text="Remove", command=lambda: Controller
                          .delete_role(resource_text.get(), self) or self.close_fields(remove_resource_frame))

        remove_b.grid(row=3, column=1)
        cancel_b.grid(row=3, column=0)
        resource_label.grid(row=1, column=0)
        resource_text.grid(row=1, column=1)

    def add_rule(self, edit_frame):
        if self.fields_open:
            return
        self.fields_open = True
        add_rule_frame = Frame(edit_frame)
        add_rule_frame.grid(row=1)

        role_label = Label(add_rule_frame, text="Role:")
        resourceID_label = Label(add_rule_frame, text="Resource ID:")
        role_text = Entry(add_rule_frame)
        resourceID_text = Entry(add_rule_frame)
        permission_label = Label(add_rule_frame, text="Permission:")
        permission_options = ["rw", "r", "x", "rwx"]

        permission_dropdown = Listbox(add_rule_frame, height=4)
        for permission in permission_options:
            permission_dropdown.insert(END, permission)

        permission_dropdown.grid(row=3, column=1)
        permission_label.grid(row=3, column=0)
        cancel_b = Button(add_rule_frame, text="cancel", command=lambda: self.close_fields(add_rule_frame))
        add_b = Button(add_rule_frame, text="Add", command=lambda: Controller
                       .add_rule(role_text.get(), resourceID_text.get(),
                                 permission_options[permission_dropdown.curselection()[0]], self) or self.close_fields(add_rule_frame))

        add_b.grid(row=4, column=1)
        cancel_b.grid(row=4, column=0)
        role_label.grid(row=1, column=0)
        resourceID_label.grid(row=2, column=0)
        role_text.grid(row=1, column=1)
        resourceID_text.grid(row=2, column=1)

    def remove_rule(self, edit_frame):
        if self.fields_open:
            return
        self.fields_open = True
        remove_rule_frame = Frame(edit_frame)
        remove_rule_frame.grid(row=1)

        role_name_label = Label(remove_rule_frame, text="Role name:")
        resource_ID_label = Label(remove_rule_frame, text="Resource ID:")
        role_name_text = Entry(remove_rule_frame)
        resource_ID_text = Entry(remove_rule_frame)
        cancel_b = Button(remove_rule_frame, text="cancel", command=lambda: self.close_fields(remove_rule_frame))
        add_b = Button(remove_rule_frame, text="Remove", command=lambda: Controller
                       .delete_rule(role_name_text.get(), resource_ID_text.get(), self) or self.close_fields(remove_rule_frame))

        add_b.grid(row=3, column=1)
        cancel_b.grid(row=3, column=0)
        role_name_label.grid(row=1, column=0)
        resource_ID_label.grid(row=2, column=0)
        role_name_text.grid(row=1, column=1)
        resource_ID_text.grid(row=2, column=1)

    def close_fields(self, frame):
        frame.destroy()
        self.fields_open = False

    def edit_auth_system(self):
        edit_frame = Frame(self.root, bg="gray", width=450, height=500, pady=10)
        edit_frame.pack()

        edit_options_frame = Frame(edit_frame, bg="gray")
        edit_options_frame.grid(row=0)

        add_user_b = Button(edit_options_frame, text="Add user", command=lambda: self.add_user(edit_frame))
        delete_user_b = Button(edit_options_frame, text="Delete user", command=lambda: self.remove_user(edit_frame))
        add_role_b = Button(edit_options_frame, text="Add role", command=lambda: self.add_role(edit_frame))
        delete_role_b = Button(edit_options_frame, text="Delete role", command=lambda: self.remove_role(edit_frame))
        add_resource_b = Button(edit_options_frame, text="Add resource", command=lambda: self.add_resource(edit_frame))
        delete_resource_b = Button(edit_options_frame, text="Delete resource", command=lambda: self.remove_resource(edit_frame))
        add_rule_b = Button(edit_options_frame, text="Add rule", command=lambda: self.add_rule(edit_frame))
        delete_rule_b = Button(edit_options_frame, text="Delete rule", command=lambda: self.remove_rule(edit_frame))

        add_user_b.grid(row=0, column=0)
        delete_user_b.grid(row=0, column=1)
        add_role_b.grid(row=0, column=2)
        delete_role_b.grid(row=0, column=3)
        add_resource_b.grid(row=0, column=4)
        delete_resource_b.grid(row=0, column=5)
        add_rule_b.grid(row=0, column=6)
        delete_rule_b.grid(row=0, column=7)


main_window = MainWindow()



