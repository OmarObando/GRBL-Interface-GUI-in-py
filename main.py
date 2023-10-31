import customtkinter
import tkinter as tk
import serial
import serial.tools.list_ports as port_list
from grbl_interface import connect_to_grbl, send_gcode, disconnect_from_grbl


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


BAUD_RATE = '115200'
COM_PORT = ''
SERIAL = None


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1100x500")
        self.title("AniSelf")
        
        self.SERIAL = None
        
        self.left_aside = customtkinter.CTkFrame(self)
        self.left_aside.grid(column=0, row=0)

        # Create a frame to hold the OptionMenu and buttons with padding   
        self.option_frame = customtkinter.CTkFrame(self.left_aside)
        self.option_frame.grid(column=0, row=0, padx=10, pady=10, sticky="nswe")

        # Create an OptionMenu with available serial ports
        self.com_text = customtkinter.CTkLabel(self.option_frame, text = "COM PORT")
        self.com_text.grid(column = 0, row = 0, padx = 10, pady = 10)
        self.com_ports =  customtkinter.CTkComboBox(self.option_frame, values=self.load_com_ports())
        self.com_ports.grid(column = 0, row = 1, padx = 10, pady = 10)
        self.button_connect = customtkinter.CTkButton(self.option_frame, text = "Conectar", command = self.connect_plotter)
        self.button_connect.grid(column = 0, row = 2, padx = 10, pady = 10)
        self.button_disconnect =  customtkinter.CTkButton(self.option_frame, text = "Desconectar", command = self.disconnect_plotter)
        self.button_disconnect.configure(state="disabled")
        self.button_disconnect.grid(column = 0, row = 3, padx = 10, pady = 10)

        # Create a frame to hold the buttons with padding
        self.button_frame = customtkinter.CTkFrame(self.left_aside)
        self.button_frame.grid(column=0, row=1, padx=10, pady=10, sticky="nswe")

        # Create the first button
        self.button1 = customtkinter.CTkButton(self.button_frame, text="Ejecutar Job 1", command=self.execute_job1)
        self.button1.grid(column=0, row=0, padx = 10, pady = 10)
        # Create the second button
        self.button2 = customtkinter.CTkButton(self.button_frame, text="Ejecutar Job 2", command=self.execute_job2)
        self.button2.grid(column=0, row=1, padx = 10, pady = 10)
        
        ##Create a frame to Cross 
        self.cross_frame = customtkinter.CTkFrame(self.left_aside)
        self.cross_frame.grid(column=0, row = 2, padx = 10, pady = 10, sticky="nswe")
        
        
        ##Create the cross
        self.button_left = customtkinter.CTkButton(self.cross_frame, text="Left", command=self.move_left)
        self.button_left.grid(column=0, row=1, padx=2, pady=2)

        self.button_right = customtkinter.CTkButton(self.cross_frame, text="Right", command=self.move_right)
        self.button_right.grid(column=2, row=1, padx=1, pady=1)

        self.button_up = customtkinter.CTkButton(self.cross_frame, text="Up", command=self.move_up)
        self.button_up.grid(column=1, row=0, padx=1, pady=1)

        self.button_down = customtkinter.CTkButton(self.cross_frame, text="Down", command=self.move_down)
        self.button_down.grid(column=1, row=2, padx=1, pady=1)


        
        
        ##Right Aside
        
        self.right_aside = customtkinter.CTkFrame(self)
        self.right_aside.grid(column=1, row=0)

        # Create a Text widget for output
        self.output_text = tk.Text(self.right_aside)
        self.output_text.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")
        self.output_text.config(state="disabled")  # Disable text widget for output
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        if self.SERIAL is not None:
            disconnect_from_grbl(self.SERIAL)
        self.destroy()
       
    def move_left(self):
        # Add your code for moving left here -x
        _gcode = "G0 X-10 F100"
        send_gcode(self.SERIAL, _gcode)

    def move_right(self):
        _gcode = "G0 X10 F100"
        send_gcode(self.SERIAL, _gcode)

    def move_up(self):
        _gcode = "G0 Y10 F100"
        send_gcode(self.SERIAL, _gcode)

    def move_down(self):
        _gcode = "G0 Y-10 F100"
        send_gcode(self.SERIAL, _gcode)

        
    def connect_plotter(self):
        _com_port = self.com_ports.get()
        self.SERIAL = connect_to_grbl(_com_port, BAUD_RATE)
        self.output_text.config(state="normal")  # Enable text widget for editing
        self.output_text.insert("end", "\n Conexión Exitosa con el puerto")  # Append the message to the end
        self.output_text.config(state="disabled") 
        self.button_connect.configure(state = "disabled")
        self.button_disconnect.configure(state = "normal")
        
    def disconnect_plotter(self):
        disconnect_from_grbl(self.SERIAL)
        self.SERIAL = None
        self.output_text.config(state="normal")  # Enable text widget for editing
        self.output_text.insert("end", "\n Desconexión Exitosa con el puerto")  # Append the message to the end
        self.output_text.config(state="disabled") 
        self.button_connect.configure(state = "normal")
        self.button_disconnect.configure(state = "disabled")
        
        
    def execute_job1(self):
        gcode_file_path = "jobs/job_1.txt"
        try:
            with open(gcode_file_path, 'r') as file:
                gcode_instructions = file.readlines()
                self.output_text.config(state="normal")
                self.output_text.insert("end", "\n")# Enable text widget for editing
                for line in gcode_instructions:
                    _serial_msg = send_gcode(self.SERIAL, line)
                    self.output_text.insert("end", _serial_msg)  # Append the message to the end
                self.output_text.config(state="disabled")
        except FileNotFoundError:
            print(f"File not found: {gcode_file_path}")
    
    def execute_job2(self):
        gcode_file_path = "jobs/job_2.txt"
        try:
            with open(gcode_file_path, 'r') as file:
                gcode_instructions = file.readlines()
                self.output_text.config(state="normal")
                self.output_text.insert("end", "\n")# Enable text widget for editing
                for line in gcode_instructions:
                    _serial_msg = send_gcode(self.SERIAL, line)
                    self.output_text.insert("end", _serial_msg)  # Append the message to the end
                self.output_text.config(state="disabled")
        except FileNotFoundError:
            print(f"File not found: {gcode_file_path}")


    def load_com_ports(self):
        list = [p.device for p in port_list.comports()]
        if not list:
            list.append("Not COM PORTS Available")
        return list

if __name__ == "__main__":
    app = App()
    app.mainloop()
