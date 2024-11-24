import tkinter as tk
from tkinter import ttk
import json
import keyboard
import os

class TextExpander:
    def __init__(self):
        self.triggers = {}
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
        if len(event.name) == 1:
            self.buffer += event.name
            self.check_for_trigger()

    def check_for_trigger(self):
        for trigger, data in self.triggers.items():
            if self.buffer.endswith(trigger) and data.get('enabled', True):
                for _ in range(len(trigger)):
                    keyboard.press_and_release('backspace')
                keyboard.write(data['response'])
                self.buffer = ""
                break

class SettingsUI:
    def __init__(self, expander):
        self.expander = expander
        self.root = tk.Tk()
        self.root.title("Smart Text Expander")
        self.setup_ui()

    def setup_ui(self):
        # Styling based on options.html lines 6-88
        self.root.configure(bg='#121212')
        
        # Add Trigger button
        add_button = tk.Button(self.root, 
                             text="Add Trigger",
                             command=self.add_trigger,
                             bg='#1e88e5',
                             fg='white')
        add_button.pack(pady=10)

        # Triggers list
        self.tree = ttk.Treeview(self.root, 
                                columns=('Enabled', 'Trigger', 'Response', 'Tags'),
                                show='headings')
        
        for col in ('Enabled', 'Trigger', 'Response', 'Tags'):
            self.tree.heading(col, text=col)
        
        self.tree.pack(pady=10, padx=10, fill='both', expand=True)
        self.refresh_triggers()

    def add_trigger(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Trigger")
        
        tk.Label(dialog, text="Trigger:").pack()
        trigger_entry = tk.Entry(dialog)
        trigger_entry.pack()
        
        tk.Label(dialog, text="Response:").pack()
        response_entry = tk.Entry(dialog)
        response_entry.pack()
        
        def save():
            trigger = trigger_entry.get().strip()
            if trigger:
                self.expander.triggers[trigger] = {
                    'enabled': True,
                    'response': response_entry.get(),
                    'tags': []
                }
                self.expander.save_triggers()
                self.refresh_triggers()
                dialog.destroy()
        
        tk.Button(dialog, text="Save", command=save).pack(pady=10)

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

    def run(self):
        self.root.mainloop()

def main():
    expander = TextExpander()
    ui = SettingsUI(expander)
    ui.run()

if __name__ == "__main__":
    main()