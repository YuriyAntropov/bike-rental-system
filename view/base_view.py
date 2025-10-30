import tkinter as tk
from tkinter import ttk, messagebox
import logging
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)
class BaseView:
    def __init__(self, root):
        self.root=root
        self.container=tk.Frame(self.root)
        self.container.pack(fill=tk.BOTH, expand=True)
    def create_treeview(self, parent, columns, headings, tree_id="tree"):
        logger.info(f"Creating treeview {tree_id} with columns: {columns}")
        tree=ttk.Treeview(parent, columns=columns, show="headings")
        for col, head in zip(columns, headings):
            tree.heading(col, text=head)
            tree.column(col, width=150, anchor=tk.W)
        tree.pack(fill=tk.BOTH, expand=True)
        return tree
    def handle_action(self, action, success_msg, error_msg=None):
        try:
            action()
            if success_msg:
                messagebox.showinfo("Успіх", success_msg)
            return True
        except Exception as e:
            logger.error(f"Action failed: {str(e)}")
            messagebox.showerror("Помилка", error_msg or str(e))
            return False
    def update_treeview(self, tree, items, columns):
        logger.info(f"Updating treeview with {len(items)} items for columns: {columns}")
        if not items:
            logger.warning("No items to insert into treeview")
        for item in tree.get_children():
            tree.delete(item)
        for item in items:
            values=[str(item.get(col, '')) for col in columns]
            logger.debug(f"Inserting values: {values}")
            tree.insert("", tk.END, values=values)