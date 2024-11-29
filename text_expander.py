import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import keyboard
import os
from typing import Dict, Any

class TextExpander:
    def __init__(self):
        self.triggers = {}
        self.buffer = ""
        self.config_file = "triggers.json"
        self.settings = {
            'require_space': False  # Default setting for space trigger
        }
        self.load_triggers()
        self.load_settings()
        keyboard.on_press(self.on_key_press)

    def load_triggers(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.triggers = json.load(f)
        except Exception as e:
            print(f"Error loading triggers: {e}")
            self.triggers = {}

    def save_triggers(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.triggers, f, indent=2)

    def load_settings(self):
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r') as f:
                    self.settings = json.load(f)
        except:
            self.save_settings()

    def save_settings(self):
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f, indent=2)

    def on_key_press(self, event):
        if self.settings['require_space']:
            # Space-triggered behavior
            if event.name == 'space':
                self.check_for_trigger()
                self.buffer = ""
            elif len(event.name) == 1:
                self.buffer += event.name
        else:
            # Immediate replacement behavior
            if len(event.name) == 1:
                self.buffer += event.name
                self.check_for_trigger()
            elif event.name == 'space':
                self.buffer = ""

    def check_for_trigger(self):
        for trigger, data in self.triggers.items():
            if not data.get('enabled', True):
                continue
            
            if self.buffer.endswith(trigger):
                # Check if this specific trigger requires space
                if data.get('require_space', False) and not self.last_key == 'space':
                    continue
                
                # Delete trigger characters
                for _ in range(len(trigger)):
                    keyboard.press_and_release('backspace')
                
                # Type the response
                keyboard.write(data['response'])
                self.buffer = ""
                break

class SettingsUI:
    def __init__(self, expander):
        self.expander = expander
        self.root = tk.Tk()
        self.root.title("Smart Text Expander")
        self.root.geometry("800x600")
        self.setup_ui()

    def setup_ui(self):
        # Style configuration (matching options.html lines 6-88)
        self.root.configure(bg='#121212')
        style = ttk.Style()
        style.configure("Treeview", background="#1e1e1e", foreground="white")
        style.configure("TButton", padding=6)

        # Header
        header = tk.Label(self.root, text="Smart Text Expander", 
                         font=('Arial', 24), bg='#121212', fg='white')
        header.pack(pady=20)

        # Buttons Frame
        buttons_frame = tk.Frame(self.root, bg='#121212')
        buttons_frame.pack(fill='x', padx=20)

        add_button = tk.Button(buttons_frame, text="Add Trigger",
                             command=self.add_trigger,
                             bg='#1e88e5', fg='white', bd=0)
        add_button.pack(side='left', padx=5)

        export_button = tk.Button(buttons_frame, text="Export CSV",
                                command=self.export_csv,
                                bg='#1e88e5', fg='white', bd=0)
        export_button.pack(side='left', padx=5)

        import_button = tk.Button(buttons_frame, text="Import CSV",
                                command=self.import_csv,
                                bg='#1e88e5', fg='white', bd=0)
        import_button.pack(side='left', padx=5)

        # Search Bar
        search_frame = tk.Frame(self.root, bg='#121212')
        search_frame.pack(fill='x', padx=20, pady=20)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.filter_triggers())
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                              bg='#2b2b2b', fg='white')
        search_entry.pack(fill='x')

        # Triggers Table
        self.tree = ttk.Treeview(self.root, columns=('Enabled', 'Trigger', 'Response', 'Tags'),
                                show='headings', selectmode='extended')
        
        for col in ('Enabled', 'Trigger', 'Response', 'Tags'):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        self.tree.pack(fill='both', expand=True, padx=20, pady=20)

        # Action Buttons
        actions_frame = tk.Frame(self.root, bg='#121212')
        actions_frame.pack(fill='x', padx=20, pady=(0, 20))

        tk.Button(actions_frame, text="Enable Selected",
                 command=lambda: self.toggle_selected(True),
                 bg='#1e88e5', fg='white', bd=0).pack(side='left', padx=5)
        
        tk.Button(actions_frame, text="Disable Selected",
                 command=lambda: self.toggle_selected(False),
                 bg='#1e88e5', fg='white', bd=0).pack(side='left', padx=5)
        
        tk.Button(actions_frame, text="Delete Selected",
                 command=self.delete_selected,
                 bg='#1e88e5', fg='white', bd=0).pack(side='left', padx=5)

        # Add Settings Frame
        settings_frame = tk.Frame(self.root, bg='#121212')
        settings_frame.pack(pady=10, padx=10, fill='x')

        # Space trigger checkbox
        self.space_trigger_var = tk.BooleanVar(value=self.expander.settings['require_space'])
        space_trigger_cb = tk.Checkbutton(
            settings_frame,
            text="Require space to trigger expansion",
            variable=self.space_trigger_var,
            command=self.update_space_trigger,
            bg='#121212',
            fg='white',
            selectcolor='#1e88e5'
        )
        space_trigger_cb.pack(side='left')

        self.refresh_triggers()

    def add_trigger(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add/Edit Trigger")
        dialog.geometry("800x700")  # Increased window size
        dialog.configure(bg='#121212')
        
        # Main container with padding
        main_frame = tk.Frame(dialog, bg='#121212', padx=20, pady=10)
        main_frame.pack(fill='both', expand=True)

        # Header
        header_label = tk.Label(main_frame, 
                               text="Create New Text Expansion", 
                               font=('Arial', 16, 'bold'),
                               bg='#121212', 
                               fg='#1e88e5')
        header_label.pack(pady=(0, 20))

        # Trigger section
        trigger_frame = tk.LabelFrame(main_frame, 
                                    text="Trigger Word/Phrase", 
                                    bg='#1e1e1e',
                                    fg='white',
                                    padx=10,
                                    pady=5)
        trigger_frame.pack(fill='x', pady=(0, 15))

        trigger_entry = tk.Entry(trigger_frame, 
                               bg='#2b2b2b',
                               fg='white',
                               font=('Arial', 11),
                               width=30,
                               insertbackground='white')  # Cursor color
        trigger_entry.pack(pady=10)

        # Response section
        response_frame = tk.LabelFrame(main_frame,
                                     text="Response Text",
                                     bg='#1e1e1e',
                                     fg='white',
                                     padx=10,
                                     pady=5)
        response_frame.pack(fill='both', expand=True, pady=(0, 15))

        # Response toolbar
        toolbar_frame = tk.Frame(response_frame, bg='#1e1e1e')
        toolbar_frame.pack(fill='x', pady=(0, 5))

        # Text formatting buttons
        def format_text(tag):
            try:
                selection = response_text.get(tk.SEL_FIRST, tk.SEL_END)
                response_text.delete(tk.SEL_FIRST, tk.SEL_END)
                response_text.insert(tk.INSERT, f"{tag}{selection}{tag}")
            except tk.TclError:
                response_text.insert(tk.INSERT, f"{tag}{tag}")
                response_text.mark_set(tk.INSERT, f"insert-{len(tag)}c")

        tk.Button(toolbar_frame,
                 text="B",
                 command=lambda: format_text("**"),
                 font=('Arial', 9, 'bold'),
                 bg='#2b2b2b',
                 fg='white',
                 width=3).pack(side='left', padx=2)

        tk.Button(toolbar_frame,
                 text="I",
                 command=lambda: format_text("*"),
                 font=('Arial', 9, 'italic'),
                 bg='#2b2b2b',
                 fg='white',
                 width=3).pack(side='left', padx=2)

        tk.Button(toolbar_frame,
                 text="Code",
                 command=lambda: format_text("`"),
                 font=('Arial', 9),
                 bg='#2b2b2b',
                 fg='white',
                 width=5).pack(side='left', padx=2)

        # Response text area
        response_text = tk.Text(response_frame,
                               bg='#2b2b2b',
                               fg='white',
                               font=('Arial', 11),
                               height=15,
                               width=60,
                               wrap=tk.WORD,
                               insertbackground='white',
                               padx=10,
                               pady=10)
        response_text.pack(fill='both', expand=True, pady=(0, 10))

        # Add scrollbar to response text
        response_scrollbar = tk.Scrollbar(response_text)
        response_scrollbar.pack(side='right', fill='y')
        response_text.config(yscrollcommand=response_scrollbar.set)
        response_scrollbar.config(command=response_text.yview)

        # Tags section
        tags_frame = tk.LabelFrame(main_frame,
                                 text="Tags (comma-separated)",
                                 bg='#1e1e1e',
                                 fg='white',
                                 padx=10,
                                 pady=5)
        tags_frame.pack(fill='x', pady=(0, 15))

        tags_entry = tk.Entry(tags_frame,
                             bg='#2b2b2b',
                             fg='white',
                             font=('Arial', 11),
                             width=30,
                             insertbackground='white')
        tags_entry.pack(pady=10)

        # Options frame
        options_frame = tk.LabelFrame(main_frame,
                                    text="Options",
                                    bg='#1e1e1e',
                                    fg='white',
                                    padx=10,
                                    pady=5)
        options_frame.pack(fill='x', pady=(0, 15))

        # Case sensitive option
        case_sensitive_var = tk.BooleanVar(value=False)
        case_sensitive_cb = tk.Checkbutton(options_frame,
                                         text="Case Sensitive",
                                         variable=case_sensitive_var,
                                         bg='#1e1e1e',
                                         fg='white',
                                         selectcolor='#2b2b2b',
                                         activebackground='#1e1e1e',
                                         activeforeground='white')
        case_sensitive_cb.pack(side='left', padx=5)

        # Spacebar trigger option
        spacebar_trigger_var = tk.BooleanVar(value=False)
        spacebar_trigger_cb = tk.Checkbutton(options_frame,
                                             text="Require Spacebar",
                                             variable=spacebar_trigger_var,
                                             bg='#1e1e1e',
                                             fg='white',
                                             selectcolor='#2b2b2b',
                                             activebackground='#1e1e1e',
                                             activeforeground='white')
        spacebar_trigger_cb.pack(side='left', padx=5)

        # Preview section
        preview_frame = tk.LabelFrame(main_frame,
                                    text="Preview",
                                    bg='#1e1e1e',
                                    fg='white',
                                    padx=10,
                                    pady=5)
        preview_frame.pack(fill='x', pady=(0, 15))

        preview_label = tk.Label(preview_frame,
                               text="No preview available",
                               bg='#1e1e1e',
                               fg='#888888',
                               wraplength=700)
        preview_label.pack(pady=10)

        def update_preview(*args):
            trigger = trigger_entry.get().strip()
            response = response_text.get("1.0", tk.END).strip()
            if trigger and response:
                preview_label.config(text=f'Typing "{trigger}" will expand to:\n{response[:100]}{"..." if len(response) > 100 else ""}',
                                   fg='white')
            else:
                preview_label.config(text="No preview available", fg='#888888')

        trigger_entry.bind('<KeyRelease>', update_preview)
        response_text.bind('<KeyRelease>', update_preview)

        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg='#121212')
        buttons_frame.pack(fill='x', pady=(0, 10))

        def save():
            trigger = trigger_entry.get().strip()
            if trigger:
                self.expander.triggers[trigger] = {
                    'enabled': True,
                    'response': response_text.get("1.0", tk.END).strip(),
                    'tags': [t.strip() for t in tags_entry.get().split(',') if t.strip()],
                    'case_sensitive': case_sensitive_var.get(),
                    'require_space': spacebar_trigger_var.get()
                }
                self.expander.save_triggers()
                self.refresh_triggers()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Trigger cannot be empty!")

        # Save button
        save_button = tk.Button(buttons_frame,
                              text="Save",
                              command=save,
                              bg='#1e88e5',
                              fg='white',
                              font=('Arial', 11),
                              width=20,
                              bd=0)
        save_button.pack(side='left', padx=5)

        # Cancel button
        cancel_button = tk.Button(buttons_frame,
                                text="Cancel",
                                command=dialog.destroy,
                                bg='#424242',
                                fg='white',
                                font=('Arial', 11),
                                width=20,
                                bd=0)
        cancel_button.pack(side='left', padx=5)

        # Center the dialog on screen
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

    def refresh_triggers(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for trigger, data in self.expander.triggers.items():
            self.tree.insert('', 'end', values=(
                'Yes' if data['enabled'] else 'No',
                trigger,
                data['response'],
                ', '.join(data.get('tags', []))
            ))

    def filter_triggers(self):
        search_text = self.search_var.get().lower()
        self.refresh_triggers()  # First refresh all triggers
        if search_text:  # Then remove non-matching ones
            for item in self.tree.get_children():
                values = self.tree.item(item)['values']
                if not any(search_text in str(v).lower() for v in values):
                    self.tree.delete(item)

    def toggle_selected(self, enabled):
        for item in self.tree.selection():
            values = self.tree.item(item)['values']
            trigger = values[1]
            if trigger in self.expander.triggers:
                self.expander.triggers[trigger]['enabled'] = enabled
        self.expander.save_triggers()
        self.refresh_triggers()

    def delete_selected(self):
        for item in self.tree.selection():
            values = self.tree.item(item)['values']
            trigger = values[1]
            if trigger in self.expander.triggers:
                del self.expander.triggers[trigger]
        self.expander.save_triggers()
        self.refresh_triggers()

    def export_csv(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if filename:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Trigger', 'Response', 'Tags', 'Enabled'])
                for trigger, data in self.expander.triggers.items():
                    writer.writerow([
                        trigger,
                        data['response'],
                        ';'.join(data.get('tags', [])),
                        data['enabled']
                    ])

    def import_csv(self):
        filename = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")]
        )
        if filename:
            with open(filename, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.expander.triggers[row['Trigger']] = {
                        'response': row['Response'],
                        'tags': row['Tags'].split(';') if row['Tags'] else [],
                        'enabled': row['Enabled'].lower() == 'true'
                    }
            self.expander.save_triggers()
            self.refresh_triggers()

    def update_space_trigger(self):
        self.expander.settings['require_space'] = self.space_trigger_var.get()
        self.expander.save_settings()

    def run(self):
        self.root.mainloop()

def main():
    if os.name == 'nt':  # Windows
        import ctypes
        import win32gui
        import win32con
        
        # Get the current console window
        console_window = win32gui.GetForegroundWindow()
        
        # Hide console window
        win32gui.ShowWindow(console_window, win32con.SW_MINIMIZE)
        
        # Optional: Hide from taskbar
        # win32gui.ShowWindow(console_window, win32con.SW_HIDE)
    
    expander = TextExpander()
    ui = SettingsUI(expander)
    ui.run()

if __name__ == "__main__":
    try:
        # Add required imports at the top of the file
        import os
        import win32gui
        import win32con
        main()
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        input("\nPress Enter to exit...")
