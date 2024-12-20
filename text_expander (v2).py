import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import keyboard
import os
from typing import Dict, Any

class TextExpander:
    def __init__(self):
        self.triggers: Dict[str, Any] = {}
        self.buffer = ""
        self.config_file = "triggers.json"
        self.load_triggers()
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

    def on_key_press(self, event):
        if event.name == 'space':
            self.check_for_trigger()
            self.buffer = ""
        elif len(event.name) == 1:
            self.buffer += event.name

    def check_for_trigger(self):
        for trigger, data in self.triggers.items():
            if self.buffer.endswith(trigger) and data.get('enabled', True):
                keyboard.write('\b' * len(trigger))
                keyboard.write(data['response'])
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

        self.refresh_triggers()

    def add_trigger(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Trigger")
        dialog.geometry("400x300")
        dialog.configure(bg='#121212')

        tk.Label(dialog, text="Trigger:", bg='#121212', fg='white').pack(pady=5)
        trigger_entry = tk.Entry(dialog, bg='#2b2b2b', fg='white')
        trigger_entry.pack(pady=5)

        tk.Label(dialog, text="Response:", bg='#121212', fg='white').pack(pady=5)
        response_entry = tk.Entry(dialog, bg='#2b2b2b', fg='white')
        response_entry.pack(pady=5)

        tk.Label(dialog, text="Tags:", bg='#121212', fg='white').pack(pady=5)
        tags_entry = tk.Entry(dialog, bg='#2b2b2b', fg='white')
        tags_entry.pack(pady=5)

        def save():
            trigger = trigger_entry.get().strip()
            if trigger:
                self.expander.triggers[trigger] = {
                    'enabled': True,
                    'response': response_entry.get(),
                    'tags': [t.strip() for t in tags_entry.get().split(',') if t.strip()]
                }
                self.expander.save_triggers()
                self.refresh_triggers()
                dialog.destroy()

        tk.Button(dialog, text="Save", command=save,
                 bg='#1e88e5', fg='white', bd=0).pack(pady=20)

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

    def run(self):
        self.root.mainloop()

def main():
    expander = TextExpander()
    ui = SettingsUI(expander)
    ui.run()

if __name__ == "__main__":
    main()
