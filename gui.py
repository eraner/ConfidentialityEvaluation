from Tkinter import *
import datetime
import Controller
import subprocess as sp





def evaluate(log):
    msg = Controller.check_auth_system()
    try:
        log.print_to_log("Controller", msg)
    except:
        return


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
    log_window = Tk()
    root = Tk()

    def __init__(self):
        # Main window
        self.root.title("Confidentiality assessment")
        self.root.geometry("450x450+200+200")

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

    def add_log(self):
        self.log_window.geometry("+800+0")
        self.log_window.title("Log")
        self.text = Text(self.log_window, height=45, width=65)

        vscroll = Scrollbar(self.log_window, orient=VERTICAL, command=self.text.yview)
        vscroll.pack(side="right", fill=Y)
        self.text.pack()
        self.text['yscroll'] = vscroll.set

    def print_to_log(self, module_name, log_message):
        time = datetime.datetime.now().time()
        self.text.configure(state=NORMAL)
        self.text.insert(END, "[<" + str(time) + "> " + module_name + "] " + log_message + "\n")
        self.text.config(state=DISABLED)
        self.text.see("end")

    def edit_auth_system(self):
        edit_frame = Frame(self.root, bg="gray", width=450, height=350, pady=3)
        edit_frame.pack(side="bottom")

        edit_options_frame = Frame(edit_frame, bg="black")
        edit_options_frame.pack(side="left")

        add_user_b = Button(edit_options_frame, text="Add user", command="")
        delete_user_b = Button(edit_options_frame, text="Delete user", command="")
        add_role_b = Button(edit_options_frame, text="Add role", command="")
        delete_role_b = Button(edit_options_frame, text="Delete role", command="")
        add_resource_b = Button(edit_options_frame, text="Add resource", command="")
        delete_resource_b = Button(edit_options_frame, text="Delete resource", command="")
        add_rule_b = Button(edit_options_frame, text="Add rule", command="")
        delete_rule_b = Button(edit_options_frame, text="Delete rule", command="")

        add_user_b.pack()
        delete_user_b.pack()
        add_role_b.pack()
        delete_role_b.pack()
        add_resource_b.pack()
        delete_resource_b.pack()
        add_rule_b.pack()
        delete_rule_b.pack()

        #edit_frame.destroy()

main_window = MainWindow()



