import glob, sv_ttk, customtkinter
from CTkListbox import *
from tkinter import filedialog
# from tkinter import StringVar, ttk, filedialog, Listbox

customtkinter.set_appearance_mode("dark")

class App(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()
        
        self.title("Mr. Renamer")
        # self.width = int(self.winfo_screenwidth()/2)
        # self.height = int(self.winfo_screenheight()/2)
        self.width = 820
        self.height = 530
        self.geometry(f"{self.width}x{self.height}")
        self.minsize(700, 404)
        
        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.sm_padx = 10
        self.sm_pady = 7
        self.files = []
        self.is_specific_file_type = customtkinter.StringVar(value='disabled')
        self.file_type = customtkinter.StringVar(value='.mkv')
        self.selected_directory = customtkinter.StringVar(value='No Folder Selected')
        self.short_directory = customtkinter.StringVar(value='No Folder Selected')
        self.selected_option = customtkinter.StringVar(value='')
        
        # self.buildGUI()
        
    # def buildGUI(self):
        self.main_frame = customtkinter.CTkFrame(self.frame)

        self.left_frame = customtkinter.CTkFrame(self.main_frame)
        self.left_frame.grid(row = 0, column = 0, rowspan = 8, columnspan = 2)

        self.right_frame = customtkinter.CTkFrame(self.main_frame)
        self.right_frame.grid(row = 0, column = 2, rowspan = 6, columnspan = 10)

        self.first_label = customtkinter.CTkLabel(self.left_frame, text = "1. SELECT FOLDER")
        self.first_label.grid(row = 0, column = 0, columnspan = 2, pady=self.sm_pady)

        self.open_button = customtkinter.CTkButton(self.left_frame, text = "Open Folder...", command = self.browse)
        self.open_button.grid(row = 1, column = 0)

        self.selected_dir = customtkinter.CTkLabel(self.left_frame, textvariable = self.short_directory)
        self.selected_dir.grid(row = 1, column = 1)

        self.file_type_check = customtkinter.CTkCheckBox(self.left_frame, text = " Specific File Type", offvalue='disabled', onvalue='normal', variable=self.is_specific_file_type, command=self.setCheckbox)
        self.file_type_check.grid(row = 2, column = 0, padx=self.sm_padx, pady=(15, 60), sticky="w")

        self.file_type_entry = customtkinter.CTkEntry(self.left_frame, state="disabled", textvariable=self.file_type)
        self.file_type_entry.grid(row = 2, column = 1, padx=self.sm_padx, pady=(15, 60))
        self.file_type_entry.bind("<KeyRelease>", lambda *args: self.setFiles())

        self.second_label = customtkinter.CTkLabel(self.left_frame, text = "2. SELECT AN OPTION")
        self.second_label.grid(row = 3, column = 0, columnspan = 2, pady=self.sm_pady)

        self.add_before_radio = customtkinter.CTkRadioButton(self.left_frame, text = " Add Text Before", value = "before", variable=self.selected_option, command=self.enableOptionEntry)
        self.add_before_radio.grid(row = 4, column = 0, padx=self.sm_padx, pady=self.sm_pady, sticky="w")

        self.add_before_entry = customtkinter.CTkEntry(self.left_frame, state="disabled")
        self.add_before_entry.grid(row = 4, column = 1, padx=self.sm_padx, pady=self.sm_pady)

        self.add_after_radio = customtkinter.CTkRadioButton(self.left_frame, text = " Add Text After", value = "after", variable=self.selected_option, command=self.enableOptionEntry)
        self.add_after_radio.grid(row = 5, column = 0, padx=self.sm_padx, pady=self.sm_pady, sticky="w")

        self.add_after_entry = customtkinter.CTkEntry(self.left_frame, state="disabled")
        self.add_after_entry.grid(row = 5, column = 1, padx=self.sm_padx, pady=self.sm_pady)

        self.replace_radio = customtkinter.CTkRadioButton(self.left_frame, text = " Replace Text", value = "replace", variable=self.selected_option, command=self.enableOptionEntry)
        self.replace_radio.grid(row = 6, column = 0, padx=self.sm_padx, pady=self.sm_pady, sticky="w")

        self.replace_entry = customtkinter.CTkEntry(self.left_frame, state="disabled")
        self.replace_entry.grid(row = 6, column = 1, padx=self.sm_padx, pady=self.sm_pady)

        self.format_radio = customtkinter.CTkRadioButton(self.left_frame, text = " Format Text", value = "format", variable=self.selected_option, command=self.enableOptionEntry)
        self.format_radio.grid(row = 7, column = 0, padx=self.sm_padx, pady=self.sm_pady, sticky="w")

        self.format_entry = customtkinter.CTkEntry(self.left_frame, state="disabled")
        self.format_entry.grid(row = 7, column = 1, padx=self.sm_padx, pady=self.sm_pady)

        self.listbox = CTkListbox(self.right_frame, width=450, height=450, orientation="vertical")
        self.listbox.bind("<Button-2>", lambda *args: self.changeScrollingDir())
        self.listbox.grid(row = 1, column = 1, rowspan = 4, columnspan = 10)
        for v in range(10):
            self.listbox.insert("end", f"From Name {v} → To Name {v}")

        self.third_label = customtkinter.CTkLabel(self.right_frame, text = "3. NO GOING BACK!")
        self.third_label.grid(row = 5, column = 0, columnspan = 5, pady=self.sm_pady, sticky="e")

        self.doit_button = customtkinter.CTkButton(self.right_frame, text = "Do it!")
        self.doit_button.grid(row = 5, column = 7, columnspan = 5, sticky="e")

        self.main_frame.pack(expand=True, fill="both")
        
    def changeScrollingDir(self):
        print('hi')
        self.listbox = CTkListbox(self.right_frame, width=450, height=450, orientation="horizontal")
        
    def setCheckbox(self):
        self.file_type_entry.configure(state = self.is_specific_file_type.get())
        print(f'{self.files} @{len(self.files)} Files')
        if len(self.files) > 0:
            self.setFiles()
            
    def browse(self):
        self.selected_directory.set(filedialog.askdirectory())
        self.short_directory.set(self.selected_directory.get().split("/")[-1])
        self.setFiles()
    
    def setFiles(self):
        if self.is_specific_file_type.get() == "normal":
            self.files = glob.glob(glob.escape(self.selected_directory.get()) + "/*" + self.file_type.get())
        else:
            self.files = glob.glob(glob.escape(self.selected_directory.get()) + "/*.*")
        self.listbox.delete(0,'end')
        for index, file in enumerate(self.files):
            self.listbox.insert("end", f"{file.split('/')[-1]} → Test {index}.{file.split('.')[-1]}")
        
    def enableOptionEntry(self):
        # First, disable all entries
        self.add_before_entry.configure(state="disabled")
        self.add_after_entry.configure(state="disabled")
        self.replace_entry.configure(state="disabled")
        self.format_entry.configure(state="disabled")

        # Then, enable the entry for the selected radio button
        selected = self.selected_option.get()
        if selected == "before":
            self.add_before_entry.configure(state="normal")
        elif selected == "after":
            self.add_after_entry.configure(state="normal")
        elif selected == "replace":
            self.replace_entry.configure(state="normal")
        elif selected == "format":
            self.format_entry.configure(state="normal")

if __name__ == "__main__":
    app = App()
    app.mainloop()