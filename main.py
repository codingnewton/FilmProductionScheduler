import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import threading
import sys
import traceback
from pathlib import Path

# Add the current directory to the path to ensure modules can be found
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Set up logging to help debug any issues
import logging
logging.basicConfig(
    filename='scheduler_app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logger.info("Application starting...")

class FilmSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Film Production Scheduler")
        self.root.geometry("600x450")
        self.root.resizable(True, True)
        
        # Variables
        self.excel_file_path = tk.StringVar()
        self.output_folder_path = tk.StringVar()
        self.timeout = tk.IntVar(value=60)
        self.num_workers = tk.IntVar(value=8)
        self.break_duration = tk.IntVar(value=60)
        self.max_time_before_break = tk.IntVar(value=240)
        
        # Create UI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        file_frame.pack(fill=tk.X, pady=10)
        
        # Excel file selection
        ttk.Label(file_frame, text="Excel File:").grid(column=0, row=0, sticky=tk.W, pady=5)
        ttk.Entry(file_frame, textvariable=self.excel_file_path, width=50).grid(column=1, row=0, padx=5)
        ttk.Button(file_frame, text="Browse...", command=self.browse_excel_file).grid(column=2, row=0, padx=5)
        
        # Output folder selection
        ttk.Label(file_frame, text="Output Folder:").grid(column=0, row=1, sticky=tk.W, pady=5)
        ttk.Entry(file_frame, textvariable=self.output_folder_path, width=50).grid(column=1, row=1, padx=5)
        ttk.Button(file_frame, text="Browse...", command=self.browse_output_folder).grid(column=2, row=1, padx=5)
        
        # Parameters section
        params_frame = ttk.LabelFrame(main_frame, text="Scheduler Parameters", padding="10")
        params_frame.pack(fill=tk.X, pady=10)
        
        # Timeout
        ttk.Label(params_frame, text="Timeout (seconds):").grid(column=0, row=0, sticky=tk.W, pady=5)
        ttk.Spinbox(params_frame, from_=10, to=600, textvariable=self.timeout, width=10).grid(column=1, row=0, padx=5, sticky=tk.W)
        
        # Number of workers
        ttk.Label(params_frame, text="Number of Workers:").grid(column=0, row=1, sticky=tk.W, pady=5)
        ttk.Spinbox(params_frame, from_=1, to=32, textvariable=self.num_workers, width=10).grid(column=1, row=1, padx=5, sticky=tk.W)
        
        # Break duration
        ttk.Label(params_frame, text="Break Duration (minutes):").grid(column=0, row=2, sticky=tk.W, pady=5)
        ttk.Spinbox(params_frame, from_=0, to=120, textvariable=self.break_duration, width=10).grid(column=1, row=2, padx=5, sticky=tk.W)
        
        # Max time before break
        ttk.Label(params_frame, text="Max Time Before Break (minutes):").grid(column=0, row=3, sticky=tk.W, pady=5)
        ttk.Spinbox(params_frame, from_=60, to=480, textvariable=self.max_time_before_break, width=10).grid(column=1, row=3, padx=5, sticky=tk.W)
        
        # Status section
        status_frame = ttk.Frame(main_frame, padding="10")
        status_frame.pack(fill=tk.X, pady=10)
        
        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT)
        
        self.progress = ttk.Progressbar(status_frame, orient=tk.HORIZONTAL, length=200, mode='indeterminate')
        self.progress.pack(side=tk.RIGHT, padx=10)
        
        # Run button
        run_frame = ttk.Frame(main_frame)
        run_frame.pack(fill=tk.X, pady=20)
        
        # Configure style for the button
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Segoe UI", 11, "bold"))
        
        ttk.Button(
            run_frame, 
            text="Generate Schedule", 
            command=self.run_scheduler,
            style="Accent.TButton",
            padding=10
        ).pack(side=tk.RIGHT)
        
    def browse_excel_file(self):
        filename = filedialog.askopenfilename(
            title="Select Excel file",
            filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*"))
        )
        if filename:
            self.excel_file_path.set(filename)
            
            # If output folder is not set, default to a subfolder in the same location
            if not self.output_folder_path.get():
                default_output = os.path.join(os.path.dirname(filename), "output")
                self.output_folder_path.set(default_output)
    
    def browse_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder_path.set(folder)
    
    def run_scheduler(self):
        # Validate inputs
        if not self.excel_file_path.get():
            messagebox.showerror("Error", "Please select an Excel file")
            return
            
        if not self.output_folder_path.get():
            messagebox.showerror("Error", "Please select an output folder")
            return
            
        if not os.path.exists(self.excel_file_path.get()):
            messagebox.showerror("Error", f"Excel file not found: {self.excel_file_path.get()}")
            return
            
        # Create output directory if it doesn't exist
        os.makedirs(self.output_folder_path.get(), exist_ok=True)
        
        # Start progress bar
        self.progress.start()
        self.status_label.config(text="Generating schedule...")
        
        # Disable the run button while processing
        for child in self.root.winfo_children():
            if isinstance(child, ttk.Frame):
                for widget in child.winfo_children():
                    if isinstance(widget, ttk.Button) and widget["text"] == "Generate Schedule":
                        widget.configure(state="disabled")
        
        # Run scheduler in a separate thread to prevent UI freezing
        threading.Thread(target=self.run_scheduler_thread, daemon=True).start()
    
    def run_scheduler_thread(self):
        try:
            logger.info("Starting scheduler thread with direct implementation")
            
            # DIRECT IMPLEMENTATION - properly calling export_schedules
            
            # Direct import of all the components we need
            from scheduler.scheduler import Optimizer
            from scheduler.scheduler_classes import Member, Task, ROLE_NAME
            from scheduler.data_loader import get_members_and_tasks
            from scheduler.export_schedules import export_schedules  # Import the export function directly
            
            # Get tasks and members directly
            tasks, members = get_members_and_tasks(excel_file=self.excel_file_path.get())
            
            # Create optimizer directly
            model = Optimizer(tasks, members)
            
            # Schedule tasks directly
            result = model.schedule_tasks(
                timeout=self.timeout.get(),
                num_workers=self.num_workers.get(),
                break_duration=self.break_duration.get(),
                max_time_before_break=self.max_time_before_break.get()
            )
            
            # Export schedule directly using the standalone function with CORRECT parameters
            # export_schedules expects (res, model, export_location)
            export_schedules(result, model, self.output_folder_path.get())
            
            # Create result directly
            cost_result = {"cost": model.optimized_cost}
            
            logger.info(f"Direct implementation completed with result: {cost_result}")
            
            # Update UI on completion
            self.root.after(0, self.on_scheduler_complete, cost_result)
        
        except Exception as e:
            logger.error(f"Error in scheduler thread: {e}")
            logger.exception("Detailed traceback:")
            
            # Handle any other errors with a detailed traceback
            error_details = traceback.format_exc()
            self.root.after(0, self.on_scheduler_error, f"{str(e)}\n\nDetails:\n{error_details}")
    
    def on_scheduler_complete(self, result):
        logger.info("Scheduler completed successfully")
        self.progress.stop()
        
        # Display cost if available in result
        cost_info = f"Optimized cost: {result['cost']}" if isinstance(result, dict) and 'cost' in result else ""
        
        self.status_label.config(text=f"Done! {cost_info}")
        
        # Re-enable the run button
        for child in self.root.winfo_children():
            if isinstance(child, ttk.Frame):
                for widget in child.winfo_children():
                    if isinstance(widget, ttk.Button) and widget["text"] == "Generate Schedule":
                        widget.configure(state="normal")
        
        # Show success message with output file paths
        output_files = []
        if os.path.exists(self.output_folder_path.get()):
            for file in os.listdir(self.output_folder_path.get()):
                if file.startswith("schedule_solution"):
                    output_files.append(file)
        
        file_list = "\n".join(output_files) if output_files else "No output files found."
        
        messagebox.showinfo(
            "Schedule Generated", 
            f"Schedule has been successfully generated!\n\n{cost_info}\n\nOutput saved to: {self.output_folder_path.get()}\n\nFiles generated:\n{file_list}"
        )
    
    def on_scheduler_error(self, error_message):
        logger.error(f"Error occurred: {error_message}")
        self.progress.stop()
        self.status_label.config(text="Error occurred")
        
        # Re-enable the run button
        for child in self.root.winfo_children():
            if isinstance(child, ttk.Frame):
                for widget in child.winfo_children():
                    if isinstance(widget, ttk.Button) and widget["text"] == "Generate Schedule":
                        widget.configure(state="normal")
        
        messagebox.showerror("Error", f"An error occurred while generating the schedule:\n\n{error_message}")


if __name__ == "__main__":
    try:
        # Set app icon and theme if available
        root = tk.Tk()
        
        # Try to load an icon if one exists
        try:
            icon_path = os.path.join(current_dir, "scheduler/assets/app_icon.ico")
            if os.path.exists(icon_path):
                root.iconbitmap(icon_path)
        except Exception as e:
            logger.error(f"Failed to load icon: {e}")
        
        app = FilmSchedulerApp(root)
        root.mainloop()
    except Exception as e:
        logger.error(f"Critical error during startup: {e}")
        logger.exception("Detailed traceback:")
        
        # Show error in a message box
        try:
            messagebox.showerror("Critical Error", f"A critical error occurred:\n\n{str(e)}")
        except:
            # If even the messagebox fails, print to console
            print(f"CRITICAL ERROR: {e}")
            traceback.print_exc()