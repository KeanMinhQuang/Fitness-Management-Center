# Fitness Center Management System

import json
import os
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Vị trí thư mục hiện tại của tệp FCM.py
DATA_DIR = os.path.join(BASE_DIR, "..", "data") # Thư mục data là thư mục sẽ lưu trữ tệp dữ liệu
DATA_FILE = os.path.join(DATA_DIR, "data.json") # Tạo data.json trong thư mục data

# class Package, Trainer, Member và Session được dùng để tạo các đối tượng tương ứng trong hệ thống

class Package:
    def __init__(self, package_name, package_price, package_duration, package_id=None):
        self.package_name = package_name
        self.package_price = package_price
        self.package_duration = package_duration
        self.package_id = package_id


class Trainer:
    def __init__(self, name, trainer_id):
        self.name = name
        self.trainer_id = trainer_id


class Member:
    def __init__(self, name, membership_id):
        self.name = name
        self.membership_id = membership_id


class Session:
    def __init__(self, expiry_date):
        self.expiry_date = expiry_date
        self.package = None
        self.member = None
        self.trainer = None

# Class quản lý tất cả các chức năng của hệ thống và chạy các class khác

class Main:
    def __init__(self):
        self.packages_info = {}
        self.trainers_info = {}
        self.members_info = {}
        self.sessions_info = {}
        self.load_data() # Load dữ liệu từ file JSON nếu có

    def save_data(self):
        os.makedirs(DATA_DIR, exist_ok=True) # Tạo thư mục data nếu chưa tồn tại

        data = { # Viết dữ liệu vào file JSON
            "packages": {
                name: {
                    "package_name": pkg.package_name,
                    "package_price": pkg.package_price,
                    "package_duration": pkg.package_duration,
                    "package_id": pkg.package_id,
                }
                for name, pkg in self.packages_info.items()
            },
            "trainers": {
                str(tid): {
                    "name": t.name,
                    "trainer_id": t.trainer_id,
                }
                for tid, t in self.trainers_info.items()
                
                # tid là khóa, t là giá trị trong từ điển trainers_info
            },
            "members": {
                str(mid): {
                    "name": m.name,
                    "membership_id": m.membership_id,
                }
                for mid, m in self.members_info.items()
                
                # mid là khóa, m là giá trị trong từ điển members_info
            },
            "sessions": {
                str(sid): {
                    "expiry_date": s.expiry_date.isoformat(),
                    "package_name": s.package.package_name if s.package else None,
                    "member_id": s.member.membership_id if s.member else None,
                    "trainer_id": s.trainer.trainer_id if s.trainer else None,
                }
                for sid, s in self.sessions_info.items()
                
                # sid là khóa, s là giá trị trong từ điển sessions_info
            },
        }

        with open(DATA_FILE, "w", encoding="utf-8") as f: 
            json.dump(data, f, ensure_ascii=False, indent=4)
            
            # Ghi dữ liệu vào file data.json
            # "w" để ghi đè file nếu đã tồn tại
            # encoding="utf-8" để hỗ trợ ký tự Unicode
            # ensure_ascii=False để giữ nguyên ký tự Unicode
            # indent=4 để định dạng đẹp hơn

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            return
        
            # Nếu không có file data.json thì không làm gì cả

        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            # Đọc dữ liệu từ file data.json nếu có

        for name, pd in data.get("packages", {}).items():
            pkg = Package(
                pd["package_name"],
                pd["package_price"],
                pd["package_duration"],
                pd["package_id"],
            )
            self.packages_info[name] = pkg
            
            # Gắn dữ liệu vào từ điển packages_info

        for tid_str, td in data.get("trainers", {}).items():
            tid = int(tid_str)
            t = Trainer(td["name"], td["trainer_id"])
            self.trainers_info[tid] = t
            
            # Gắn dữ liệu vào từ điển trainers_info

        for mid_str, md in data.get("members", {}).items():
            mid = int(mid_str)
            m = Member(md["name"], md["membership_id"])
            self.members_info[mid] = m
            
            # Gắn dữ liệu vào từ điển members_info

        for sid_str, sd in data.get("sessions", {}).items():
            sid = int(sid_str)
            expiry = datetime.fromisoformat(sd["expiry_date"])
            s = Session(expiry)

            pkg_name = sd["package_name"]
            member_id = sd["member_id"]
            trainer_id = sd["trainer_id"]

            if pkg_name and pkg_name in self.packages_info:
                s.package = self.packages_info[pkg_name]
            if member_id and member_id in self.members_info:
                s.member = self.members_info[member_id]
            if trainer_id and trainer_id in self.trainers_info:
                s.trainer = self.trainers_info[trainer_id]

            self.sessions_info[sid] = s
            
            # Gắn dữ liệu vào từ điển sessions_info


    def add_package(self, package_name, package_price, package_duration): # Thêm gói mới
        if package_name in self.packages_info:
            return False, "Package name already exists. Please choose another name."

            # Kiểm tra tên gói đã tồn tại chưa
        
        package_id = len(self.packages_info) + 1
        package = Package(package_name, package_price, package_duration, package_id)
        self.packages_info[package_name] = package
        self.save_data()
        return True, f"Package '{package_name}' added with ID {package_id}."
    
    def delete_package(self, user_input): # Xóa gói theo tên hoặc ID
        if user_input.isdigit(): # Kiểm tra nếu nhập vào là số (ID)
            package_id = int(user_input)
            for name, pkg in list(self.packages_info.items()):
                if pkg.package_id == package_id:
                    del self.packages_info[name]
                    self.save_data()
                    return True, f"Package with ID {package_id} deleted."
            return False, "No package found with the entered ID."
        else:
            if user_input in self.packages_info:
                del self.packages_info[user_input]
                self.save_data()
                return True, f"Package '{user_input}' deleted."
            return False, "No package found with the entered name."

    def add_trainer(self, name): # Thêm huấn luyện viên mới
        trainer_id = len(self.trainers_info) + 1
        trainer = Trainer(name, trainer_id)
        self.trainers_info[trainer_id] = trainer
        self.save_data()
        return True, f"Trainer '{name}' added with ID {trainer_id}."
    
    def delete_trainer(self, user_input): # Xóa huấn luyện viên theo tên hoặc ID
        if user_input.isdigit():
            trainer_id = int(user_input)
            if trainer_id in self.trainers_info:
                del self.trainers_info[trainer_id]
                self.save_data()
                return True, f"Trainer with ID {trainer_id} deleted."
            return False, "No Trainer found with the entered ID."
        else:
            for tid, t in list(self.trainers_info.items()):
                if t.name.lower() == user_input.lower():
                    del self.trainers_info[tid]
                    self.save_data()
                    return True, f"Trainer '{t.name}' deleted."
            return False, "No Trainer found with the entered name."

    def view_trainers(self): # Hiển thị tất cả huấn luyện viên
        if not self.trainers_info:
            print("No trainers available. Please add trainers first.")
            return
        for t in self.trainers_info.values():
            print(f"Name: {t.name} || ID: {t.trainer_id}")


    def add_member(self, name): # Thêm thành viên mới
        membership_id = len(self.members_info) + 1
        member = Member(name, membership_id)
        self.members_info[membership_id] = member
        self.save_data()
        return True, f"Member '{name}' added with ID {membership_id}."

    def delete_member(self, user_input): # Xóa thành viên theo tên hoặc ID
        if user_input.isdigit():
            membership_id = int(user_input)
            if membership_id in self.members_info:
                del self.members_info[membership_id]
                self.save_data()
                return True, f"Member with ID {membership_id} deleted."
            return False, "No Member found with the entered ID."
        else:
            for mid, m in list(self.members_info.items()):
                if m.name.lower() == user_input.lower():
                    del self.members_info[mid]
                    self.save_data()
                    return True, f"Member '{m.name}' deleted."
            return False, "No Member found with the entered name."


    def add_session(self, package: Package, member: Member, trainer: Trainer): # Thêm buổi tập mới
        session_id = len(self.sessions_info) + 1
        expiry_date = datetime.now() + timedelta(package.package_duration)
        session = Session(expiry_date)
        session.package = package
        session.member = member
        session.trainer = trainer
        self.sessions_info[session_id] = session
        self.save_data()
        return True, f"Session added with ID {session_id}. Expiry date: {expiry_date.strftime('%Y-%m-%d')}."
    
    def delete_session(self, session_id): # Xóa buổi tập theo ID
        if session_id in self.sessions_info:
            del self.sessions_info[session_id]
            self.save_data()
            return True, f"Session with ID {session_id} deleted."
        return False, "No Session found with the entered ID."

    def print_invoice(self, session_id): # In hóa đơn
        if session_id not in self.sessions_info:
            return None
        
        session = self.sessions_info[session_id]
        return (
            "----- Invoice -----\n"
            f"Session ID: {session_id}\n"
            f"Package: {session.package.package_name}\n"
            f"Member: {session.member.name}\n"
            f"Trainer: {session.trainer.name}\n"
            f"Price: {session.package.package_price}\n"
            f"Expiry Date: {session.expiry_date.strftime('%Y-%m-%d')}\n"
            "-------------------"
        )      


class FCMApp: # Class quản lý giao diện người dùng bằng Tkinter
    def __init__(self, root):
        self.root = root
        self.root.title("FCM")
        self.root.geometry("800x600")
        self.root.configure(bg="white")
        
        self.main = Main()

        title = tk.Label(
            root,
            text="Fitness Center Management System",
            font=("Arial", 24, "bold"),
            bg="white",
        )
        title.pack(pady=10)
        
        self.view_frame = ttk.Notebook(root)
        self.view_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.package_tab = ttk.Frame(self.view_frame)
        self.trainer_tab = ttk.Frame(self.view_frame)
        self.member_tab = ttk.Frame(self.view_frame)
        self.session_tab = ttk.Frame(self.view_frame)
        
        self.view_frame.add(self.package_tab, text="Packages")
        self.view_frame.add(self.trainer_tab, text="Trainers")
        self.view_frame.add(self.member_tab, text="Members")
        self.view_frame.add(self.session_tab, text="Sessions")
        
        more_buttons_frame = tk.Frame(root)
        more_buttons_frame.pack(fill="x", pady=10)
        
        tk.Button(more_buttons_frame, width=20, text="Refresh All", command=self.refresh_all).grid(row=0, column=0, padx=5)
        tk.Button(more_buttons_frame, width=20, text="Print Invoice", command=self.print_invoice_gui).grid(row=0, column=1, padx=5)
        
        self.setup_package_tab()
        self.setup_trainer_tab()
        self.setup_member_tab()
        self.setup_session_tab()

        self.refresh_all()
        
    def build_treeview(self, parent, columns, headings): # Xây dựng Treeview cho hiển thị dữ liệu
        tree = ttk.Treeview(parent, columns=columns, show="headings")
        for col, hd in zip(columns, headings): # Zip được dùng để kết hợp hai danh sách columns và headings lại với nhau
            tree.heading(col, text=hd)
            tree.column(col, width=150, anchor="center")
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        return tree
    
    def setup_package_tab(self): # Thiết lập tab Packages
        top = tk.Frame(self.package_tab)
        top.pack(fill="x", pady=5)
        
        tk.Button(top, text="Add Package", command=lambda: self.add_gui("package")).pack(side="left", padx=5)
        tk.Button(top, text="Delete Package", command=lambda: self.delete_gui("package")).pack(side="left", padx=5)
        
        self.package_tree = self.build_treeview(
            self.package_tab, 
            ["id", "name", "price", "duration"], 
            ["ID", "Name", "Price", "Duration (Days)"]
        )
        
    def setup_trainer_tab(self): # Thiết lập tab Trainers
        top = tk.Frame(self.trainer_tab)
        top.pack(fill="x", pady=5)
        
        tk.Button(top, text="Add Trainer", command=lambda: self.add_gui("trainer")).pack(side="left", padx=5)
        tk.Button(top, text="Delete Trainer", command=lambda: self.delete_gui("trainer")).pack(side="left", padx=5)
        
        self.trainer_tree = self.build_treeview(
            self.trainer_tab, 
            ["id", "name"], 
            ["ID", "Name"]
        )
        
    def setup_member_tab(self): # Thiết lập tab Members
        top = tk.Frame(self.member_tab)
        top.pack(fill="x", pady=5)
        
        tk.Button(top, text="Add Member", command=lambda: self.add_gui("member")).pack(side="left", padx=5)
        tk.Button(top, text="Delete Member", command=lambda: self.delete_gui("member")).pack(side="left", padx=5)
        
        self.member_tree = self.build_treeview(
            self.member_tab, 
            ["id", "name"], 
            ["ID", "Name"]
        )
        
    def setup_session_tab(self): # Thiết lập tab Sessions
        top = tk.Frame(self.session_tab, bg="white")
        top.pack(fill="x", pady=5)
        
        tk.Button(top, text="Add Session", command=lambda: self.add_gui("session")).pack(side="left", padx=5)
        tk.Button(top, text="Delete Session", command=lambda: self.delete_gui("session")).pack(side="left", padx=5)
        
        self.session_tree = self.build_treeview(
            self.session_tab, 
            ["id", "package", "member", "trainer", "expiry"], 
            ["ID", "Package", "Member", "Trainer", "Expiry Date"]
        )
        
    def clear_treeview(self, tree): # Xóa tất cả dữ liệu trong Treeview
        for item in tree.get_children():
            tree.delete(item)
            
    def refresh_packages(self): # Làm mới dữ liệu trong tab Packages
        self.clear_treeview(self.package_tree)
        for pkg in self.main.packages_info.values():
            self.package_tree.insert("", "end", values=(pkg.package_id, pkg.package_name, pkg.package_price, pkg.package_duration))
            
    def refresh_trainers(self): # Làm mới dữ liệu trong tab Trainers
        self.clear_treeview(self.trainer_tree)
        for trainer in self.main.trainers_info.values():
            self.trainer_tree.insert("", "end", values=(trainer.trainer_id, trainer.name))
            
    def refresh_members(self): # Làm mới dữ liệu trong tab Members
        self.clear_treeview(self.member_tree)
        for member in self.main.members_info.values():
            self.member_tree.insert("", "end", values=(member.membership_id, member.name))
            
    def refresh_sessions(self): # Làm mới dữ liệu trong tab Sessions
        self.clear_treeview(self.session_tree)
        for session_id, session in self.main.sessions_info.items():
            self.session_tree.insert("", "end", values=(
                session_id, 
                session.package.package_name if session.package else "N/A", 
                session.member.name if session.member else "N/A", 
                session.trainer.name if session.trainer else "N/A", 
                session.expiry_date.strftime("%Y-%m-%d")
            ))
            
    def refresh_all(self): # Làm mới tất cả dữ liệu trong tất cả các tab
        self.refresh_packages()
        self.refresh_trainers()
        self.refresh_members()
        self.refresh_sessions()
        
    def open_packages(self):
        self.view_frame.select(self.package_tab)
        
    def open_trainers(self):
        self.view_frame.select(self.trainer_tab)
        
    def open_members(self):
        self.view_frame.select(self.member_tab)
        
    def open_sessions(self):
        self.view_frame.select(self.session_tab)
        
    def add_gui(self, type):
        if type == "package":
            name = simpledialog.askstring("Add Package", "Enter package name:")
            if not name:
                return
            
            try:
                price = float(simpledialog.askfloat("Add Package", "Enter package price:"))
                if price is None:
                    return
                
                duration = int(simpledialog.askinteger("Add Package", "Enter package duration (days):"))
                if duration is None:
                    return
            except (ValueError, TypeError):
                messagebox.showerror("Error", "Invalid input for price or duration.")
                return
            
            success, msg = self.main.add_package(name, price, duration)
            if success:
                messagebox.showinfo("Success", msg)
                self.refresh_all()
            else:
                messagebox.showerror("Error", msg)
        elif type == "trainer":
            name = simpledialog.askstring("Add Trainer", "Enter trainer name:")
            if not name:
                return
            
            success, msg = self.main.add_trainer(name)
            if success:
                messagebox.showinfo("Success", msg)
                self.refresh_all()
            else:
                messagebox.showerror("Error", msg)     
        elif type == "member":
            name = simpledialog.askstring("Add Member", "Enter member name:")
            if not name:
                return
            
            success, msg = self.main.add_member(name)
            if success:
                messagebox.showinfo("Success", msg)
                self.refresh_all()
            else:
                messagebox.showerror("Error", msg)
        elif type == "session":
            if not self.main.packages_info:
                messagebox.showerror("Error", "No packages available. Please add packages first.")
                return
            if not self.main.members_info:
                messagebox.showerror("Error", "No members available. Please add members first.")
                return
            if not self.main.trainers_info:
                messagebox.showerror("Error", "No trainers available. Please add trainers first.")
                return
            
            package_name = simpledialog.askstring("Add Session", "Enter package name:")
            member_id = simpledialog.askinteger("Add Session", "Enter member ID:")
            trainer_id = simpledialog.askinteger("Add Session", "Enter trainer ID:")
            
            if not package_name or member_id is None or trainer_id is None:
                return
            
            package = self.main.packages_info.get(package_name)
            member = self.main.members_info.get(member_id)
            trainer = self.main.trainers_info.get(trainer_id)
            
            if not package:
                messagebox.showerror("Error", "Package not found.")
                return
            if not member:
                messagebox.showerror("Error", "Member not found.")
                return
            if not trainer:
                messagebox.showerror("Error", "Trainer not found.")
                return
            
            success, msg = self.main.add_session(package, member, trainer)
            if success:
                messagebox.showinfo("Success", msg)
                self.refresh_all()
            else:
                messagebox.showerror("Error", msg)

    def delete_gui(self, type):
        if type == "package":
            if not self.main.packages_info:
                messagebox.showerror("Error", "No packages available to delete.")
                return
            user_input = simpledialog.askstring("Delete Package", "Enter package name or ID to delete:")
            if not user_input:
                return
            
            success, msg = self.main.delete_package(user_input)
            if success:
                messagebox.showinfo("Success", msg)
                self.refresh_all()
            else:
                messagebox.showerror("Error", msg)
        elif type == "trainer":
            if not self.main.trainers_info:
                messagebox.showerror("Error", "No trainers available to delete.")
                return
            user_input = simpledialog.askstring("Delete Trainer", "Enter trainer name or ID to delete:")
            if not user_input:
                return
            
            success, msg = self.main.delete_trainer(user_input)
            if success:
                messagebox.showinfo("Success", msg)
                self.refresh_all()
            else:
                messagebox.showerror("Error", msg)     
        elif type == "member":
            if not self.main.members_info:
                messagebox.showerror("Error", "No members available to delete.")
                return
            user_input = simpledialog.askstring("Delete Member", "Enter member name or ID to delete:")
            if not user_input:
                return
            
            success, msg = self.main.delete_member(user_input)
            if success:
                messagebox.showinfo("Success", msg)
                self.refresh_all()
            else:
                messagebox.showerror("Error", msg)
        elif type == "session":
            if not self.main.sessions_info:
                messagebox.showerror("Error", "No sessions available to delete.")
                return
            session_id = simpledialog.askinteger("Delete Session", "Enter session ID to delete:")
            if session_id is None:
                return
            
            success, msg = self.main.delete_session(session_id)
            if success:
                messagebox.showinfo("Success", msg)
                self.refresh_all()
            else:
                messagebox.showerror("Error", msg)

    def print_invoice_gui(self):
        if not self.main.sessions_info:
            messagebox.showerror("Error", "No sessions available to print invoice.")
            return
        session_id = simpledialog.askinteger("Print Invoice", "Enter session ID to print invoice:")
        if session_id is None:
            return
        
        invoice = self.main.print_invoice(session_id)
        if invoice is None:
            messagebox.showerror("Error", "No session found with the entered ID.")
            return
        
        invoice_window = tk.Toplevel(self.root)
        invoice_window.title(f"Invoice - Session {session_id}")
        invoice_window.geometry("400x300")
        
        text = tk.Text(invoice_window, wrap="word", font=("Courier new", 11))
        text.insert("1.0", invoice)
        text.config(state="disabled")
        text.pack(fill="both", expand=True, padx=10, pady=10)


root = tk.Tk()
app = FCMApp(root)
root.mainloop()
  
# Data sẽ không được lưu nếu người dùng chưa điền gì cả và thoát ngay lập tức
