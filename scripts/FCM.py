# Fitness Center Management System

import json
import os
from datetime import datetime, timedelta


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
            print("Package name already exists. Please choose another name.")
            return

            # Kiểm tra tên gói đã tồn tại chưa
        
        package_id = len(self.packages_info) + 1
        package = Package(package_name, package_price, package_duration, package_id)
        self.packages_info[package_name] = package
        self.save_data()
        print(f"Package '{package_name}' added with ID {package_id}.")

    def delete_package(self, user_input): # Xóa gói theo tên hoặc ID
        if user_input.isdigit(): # Kiểm tra nếu nhập vào là số (ID)
            package_id = int(user_input)
            for name, pkg in list(self.packages_info.items()):
                if pkg.package_id == package_id:
                    del self.packages_info[name]
                    self.save_data()
                    print(f"Package with ID {package_id} deleted.")
                    return
            print("No package found with the entered ID.")
        else:
            if user_input in self.packages_info:
                del self.packages_info[user_input]
                self.save_data()
                print(f"Package '{user_input}' deleted.")
                return
            print("No package found with the entered name.")

    def view_packages(self): # Hiển thị tất cả các gói
        if not self.packages_info:
            print("No packages available. Please add packages first.")
            return
        for pkg in self.packages_info.values():
            print(
                f"Name: {pkg.package_name} || "
                f"ID: {pkg.package_id} || "
                f"Price: {pkg.package_price} || "
                f"Duration: {pkg.package_duration} days"
            )


    def add_trainer(self, name): # Thêm huấn luyện viên mới
        trainer_id = len(self.trainers_info) + 1
        trainer = Trainer(name, trainer_id)
        self.trainers_info[trainer_id] = trainer
        self.save_data()
        print(f"Trainer '{name}' added with ID {trainer_id}.")

    def delete_trainer(self, user_input): # Xóa huấn luyện viên theo tên hoặc ID
        if user_input.isdigit():
            trainer_id = int(user_input)
            if trainer_id in self.trainers_info:
                del self.trainers_info[trainer_id]
                self.save_data()
                print(f"Trainer with ID {trainer_id} deleted.")
                return
            print("No Trainer found with the entered ID.")
        else:
            for tid, t in list(self.trainers_info.items()):
                if t.name.lower() == user_input.lower():
                    del self.trainers_info[tid]
                    self.save_data()
                    print(f"Trainer '{t.name}' deleted.")
                    return
            print("No Trainer found with the entered name.")

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
        print(f"Member '{name}' added with Membership ID {membership_id}.")

    def view_members(self): # Hiển thị tất cả thành viên
        if not self.members_info:
            print("No members available. Please add members first.")
            return
        for m in self.members_info.values():
            print(f"Name: {m.name} || Membership ID: {m.membership_id}")

    def delete_member(self, user_input): # Xóa thành viên theo tên hoặc ID
        if user_input.isdigit():
            membership_id = int(user_input)
            if membership_id in self.members_info:
                del self.members_info[membership_id]
                self.save_data()
                print(f"Member with ID {membership_id} deleted.")
                return
            print("No Member found with the entered ID.")
        else:
            for mid, m in list(self.members_info.items()):
                if m.name.lower() == user_input.lower():
                    del self.members_info[mid]
                    self.save_data()
                    print(f"Member '{m.name}' deleted.")
                    return
            print("No Member found with the entered name.")


    def add_session(self, package: Package, member: Member, trainer: Trainer): # Thêm buổi tập mới
        session_id = len(self.sessions_info) + 1
        expiry_date = datetime.now() + timedelta(package.package_duration)
        session = Session(expiry_date)
        session.package = package
        session.member = member
        session.trainer = trainer
        self.sessions_info[session_id] = session
        self.save_data()
        print(f"Session created with ID {session_id}.")

    def delete_session(self, session_id): # Xóa buổi tập theo ID
        if session_id in self.sessions_info:
            del self.sessions_info[session_id]
            self.save_data()
            print(f"Session with ID {session_id} deleted.")
        else:
            print("No Session found with the entered ID.")

    def view_sessions(self): # Hiển thị tất cả buổi tập
        if not self.sessions_info:
            print("No sessions available. Please add sessions first.")
            return
        for s_id, s in self.sessions_info.items():
            print(
                f"Session ID: {s_id} || "
                f"Package: {s.package.package_name} || "
                f"Member: {s.member.name} || "
                f"Trainer: {s.trainer.name} || "
                f"Expiry Date: {s.expiry_date.strftime('%Y-%m-%d')}"
            )



def input_float(prompt): # Hàm nhập số thực với kiểm tra lỗi
    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Invalid number. Please enter a valid numeric value.")


def input_int(prompt): # Hàm nhập số nguyên với kiểm tra lỗi
    while True:
        value = input(prompt)
        try:
            return int(value)
        except ValueError:
            print("Invalid integer. Please enter a whole number.")



main = Main() # Chạy Main class

while True: # Lặp vô hạn cho đến khi người dùng chọn thoát
    # Menu chính
    print("\nWelcome to Fitness Center Management System")
    print("1. Manage Packages")
    print("2. Manage Trainers")
    print("3. Manage Members")
    print("4. Manage Sessions")
    print("5. Exit")

    choice = input("Enter your choice: ").strip()
    # Xử lý lựa chọn của người dùng
    # Khi người dùng chọn một mục, hiển thị menu con tương ứng
    if choice == '1':
        print("\n1. Add Package\n2. Delete Package\n3. View Packages\n4. Back")
        pkg_choice = input("Enter your choice: ").strip()

        if pkg_choice == '1':
            name = input("Enter package name: ").strip()
            price = input_float("Enter package price: ")
            duration = input_int("Enter package duration (in days): ")
            main.add_package(name, price, duration)

        elif pkg_choice == '2':
            if not main.packages_info:
                print("No packages available. Please add packages first.")
                # Kiểm tra nếu không có gói nào thì không thể xóa
            else:
                user_input = input("Enter package name or ID to delete: ").strip()
                main.delete_package(user_input)

        elif pkg_choice == '3':
            main.view_packages()

        elif pkg_choice == '4':
            continue
        else:
            print("Invalid choice. Please try again.")

    elif choice == '2':
        print("\n1. Add Trainer\n2. Delete Trainer\n3. View Trainers\n4. Back")
        tr_choice = input("Enter your choice: ").strip()

        if tr_choice == '1':
            name = input("Enter trainer name: ").strip()
            main.add_trainer(name)

        elif tr_choice == '2':
            if not main.trainers_info:
                print("No trainers available. Please add trainers first.")
                # Kiểm tra nếu không có huấn luyện viên nào thì không thể xóa
            else:
                user_input = input("Enter trainer name or ID to delete: ").strip()
                main.delete_trainer(user_input)

        elif tr_choice == '3':
            main.view_trainers()

        elif tr_choice == '4':
            continue
        else:
            print("Invalid choice. Please try again.")

    elif choice == '3':
        print("\n1. Add Member\n2. Delete Member\n3. View Members\n4. Back")
        mem_choice = input("Enter your choice: ").strip()

        if mem_choice == '1':
            name = input("Enter member name: ").strip()
            main.add_member(name)

        elif mem_choice == '2':
            if not main.members_info:
                print("No members available. Please add members first.")
                # Kiểm tra nếu không có thành viên nào thì không thể xóa
            else:
                user_input = input("Enter member name or ID to delete: ").strip()
                main.delete_member(user_input)

        elif mem_choice == '3':
            main.view_members()

        elif mem_choice == '4':
            continue
        else:
            print("Invalid choice. Please try again.")

    elif choice == '4':
        print("\n1. Add Session\n2. Delete Session\n3. View Sessions\n4. Back")
        ses_choice = input("Enter your choice: ").strip()

        if ses_choice == '1':
            if not main.packages_info:
                print("No packages available. Please add packages first.")
                continue
            if not main.members_info:
                print("No members available. Please add members first.")
                continue
            if not main.trainers_info:
                print("No trainers available. Please add trainers first.")
                continue
            
            # Check xem có gói, thành viên, huấn luyện viên không trước khi thêm buổi tập
            
            print("Info to input for creating a session:")
            print("----------Packages----------")
            main.view_packages()
            print("----------Members----------")
            main.view_members()
            print("----------Trainers----------")            
            main.view_trainers()
            print("----------------------------")

            pkg_name = input("Enter package name: ").strip()
            mem_id = input_int("Enter member ID: ")
            tr_id = input_int("Enter trainer ID: ")

            if pkg_name in main.packages_info and mem_id in main.members_info and tr_id in main.trainers_info: # Kiểm tra tính hợp lệ của đầu vào
                package = main.packages_info[pkg_name]
                member = main.members_info[mem_id]
                trainer = main.trainers_info[tr_id]
                main.add_session(package, member, trainer)
            else:
                print("Invalid package name, member ID, or trainer ID.")

        elif ses_choice == '2':
            if not main.sessions_info:
                print("No sessions available. Please add sessions first.")
            else:
                ses_id = input_int("Enter session ID to delete: ")
                main.delete_session(ses_id)

        elif ses_choice == '3':
            main.view_sessions()

        elif ses_choice == '4':
            continue
        else:
            print("Invalid choice. Please try again.")

    elif choice == '5':
        print("Exiting the system")
        break
    else:
        print("Invalid choice. Please try again.")
        
# Data sẽ không được lưu nếu người dùng chưa điền gì cả và thoát ngay lập tức