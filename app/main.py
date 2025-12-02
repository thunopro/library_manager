import tkinter as tk
from tkinter import ttk, messagebox,filedialog
import sys
import os
import csv 
# --- PHẦN QUAN TRỌNG: SỬ DỤNG 2 LẦN DIRNAME ĐỂ TRỎ VỀ ĐÚNG GỐC DỰ ÁN ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# -----------------------------------------------------------------------

# Import Models
from app.models.book_model import BookModel
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app.models.report_model import ReportModel
from app.models.borrower_model import BorrowerModel 
from app.models.loan_model import LoanModel 
from app.models.author_model import AuthorModel 


class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1100x650") # Chỉnh to lên một chút cho thoáng
        
        # ========================================================
        # [MỚI] CẤU HÌNH FONT CHỮ TOÀN BỘ ỨNG DỤNG
        # ========================================================
        # 1. Set font cho các widget cơ bản (Label, Button, Entry...)
        self.option_add("*Font", "Helvetica 10") 
        
        # 2. Set font cho các widget nâng cao (Treeview, Notebook...)
        style = ttk.Style()
        style.theme_use('clam') # Dùng theme 'clam' hoặc 'alt' để trông hiện đại hơn trên Linux
        
        # Cấu hình font chung
        style.configure(".", font=("Helvetica", 10))
        
        # Cấu hình riêng cho Tiêu đề bảng (Heading)
        style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))
        
        # Cấu hình riêng cho Dòng dữ liệu (Row) - Tăng chiều cao dòng cho dễ đọc
        style.configure("Treeview", rowheight=25, font=("Helvetica", 10))
        # ========================================================
        # Khởi tạo Model
        self.book_model = BookModel()
        self.borrower_model = BorrowerModel() 
        self.loan_model = LoanModel() 
        self.author_model = AuthorModel()
        # Tạo giao diện chính
        self.create_widgets()

    def create_widgets(self):
        # 1. Tiêu đề chung
        lbl_main_title = tk.Label(self, text="QUẢN LÝ THƯ VIỆN", font=("Arial", 24, "bold"), fg="#333", pady=10)
        lbl_main_title.pack(side=tk.TOP, fill=tk.X)

        # 2. Tạo hệ thống Tabs
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # --- TAB : QUẢN LÝ SÁCH ---
        self.tab_books = tk.Frame(self.tabs)
        self.tabs.add(self.tab_books, text=" Quản Lý Sách ")
        self.setup_book_tab()

        # --- TAB : TÁC GIẢ
        self.tab_authors = tk.Frame(self.tabs)
        self.tabs.add(self.tab_authors, text=" Quản Lý Tác Giả ") # Tab mới
        self.setup_author_tab() 
        
        # --- TAB : NGƯỜI MƯỢN ---
        self.tab_borrowers = tk.Frame(self.tabs)
        self.tabs.add(self.tab_borrowers, text=" Người Mượn ")
        self.setup_borrower_tab()

        # --- TAB : MƯỢN / TRẢ ---
        self.tab_loans = tk.Frame(self.tabs)
        self.tabs.add(self.tab_loans, text=" Mượn Trả Sách ")
        self.setup_loan_tab()
        
        # --- TAB : THỐNG KÊ & BÁO CÁO ---
        self.tab_reports = tk.Frame(self.tabs)
        self.tabs.add(self.tab_reports, text=" Báo Cáo & Dashboard ")
        self.setup_report_tab()
        
        # ========================================================
        # [MỚI] BẮT SỰ KIỆN KHI NGƯỜI DÙNG CHUYỂN TAB
        # ========================================================
        self.tabs.bind("<<NotebookTabChanged>>", self.on_tab_change)
        
    # ==========================================
    # LOGIC TAB BÁO CÁO & DASHBOARD (NÂNG CẤP)
    # ==========================================

    def setup_report_tab(self):
        # Đảm bảo Model đã được khởi tạo
        if not hasattr(self, 'report_model'):
            self.report_model = ReportModel()
        
        # --- PHẦN 1: KPI & BIỂU ĐỒ (GIỮ NGUYÊN) ---
        frame_top = tk.Frame(self.tab_reports)
        frame_top.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Hiển thị KPI
        kpis = self.report_model.get_kpis()
        lbl_text = f"Tổng Sách: {kpis['total_books']} | Khách Hàng: {kpis['total_borrowers']} | Đang Mượn: {kpis['active_loans']} | Quá Hạn: {kpis['overdue_count']}"
        lbl_info = tk.Label(frame_top, text=lbl_text, font=("Arial", 11, "bold"), fg="#D32F2F")
        lbl_info.pack(pady=5)
        
        # Vẽ biểu đồ tròn
        try:
            fig = Figure(figsize=(5, 2.5), dpi=100) # Chỉnh nhỏ lại chút cho gọn
            ax = fig.add_subplot(111)
            # Dữ liệu giả lập cho đẹp (hoặc lấy từ kpis)
            data = [kpis['active_loans'], kpis['overdue_count'], 10] 
            labels = ['Đang Mượn', 'Quá Hạn', 'Đã Trả']
            colors = ['#2196F3', '#F44336', '#4CAF50']
            ax.pie(data, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
            ax.set_title("Tỉ lệ Mượn/Trả", fontsize=10)
            
            canvas = FigureCanvasTkAgg(fig, master=frame_top)
            canvas.draw()
            canvas.get_tk_widget().pack()
        except Exception as e:
            tk.Label(frame_top, text="Không thể vẽ biểu đồ").pack()

        # --- PHẦN 2: THANH CÔNG CỤ CHỌN BÁO CÁO (MỚI) ---
        frame_bot = tk.Frame(self.tab_reports)
        frame_bot.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        toolbar = tk.Frame(frame_bot)
        toolbar.pack(fill=tk.X, pady=5)

        tk.Label(toolbar, text="Loại Báo Cáo:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Combobox để chọn 1 trong 4 loại báo cáo
        self.cbb_report_type = ttk.Combobox(toolbar, state="readonly", width=35)
        self.cbb_report_type['values'] = (
            "1. Sách Quá Hạn (Overdue)", 
            "2. Hoạt Động Mượn (Inner Join)", 
            "3. Tất Cả Khách Hàng (Left Join)", 
            "4. Chi Tiết Đầy Đủ (Multi-table Join)"
        )
        self.cbb_report_type.current(0) # Mặc định chọn cái đầu tiên
        self.cbb_report_type.pack(side=tk.LEFT, padx=5)
        
        # Nút Xem
        btn_view = tk.Button(toolbar, text="👁 Xem Báo Cáo", bg="#2196F3", fg="white", 
                             command=self.load_selected_report)
        btn_view.pack(side=tk.LEFT, padx=5)

        # Nút Xuất CSV
        btn_export = tk.Button(toolbar, text="⬇ Xuất CSV", bg="green", fg="white", font=("Arial", 9, "bold"),
                               command=self.export_csv)
        btn_export.pack(side=tk.RIGHT, padx=5)

        # --- PHẦN 3: BẢNG DỮ LIỆU (DYNAMIC) ---
        # Chúng ta khởi tạo Treeview rỗng, cột sẽ được tạo lại khi bấm nút Xem
        self.tree_report = ttk.Treeview(frame_bot, show="headings", height=8)
        self.tree_report.pack(fill=tk.BOTH, expand=True)

        # Load mặc định cái đầu tiên
        self.load_selected_report()

    def setup_author_tab(self):
        # 1. Toolbar
        frame_controls = tk.Frame(self.tab_authors, pady=10)
        frame_controls.pack(fill=tk.X, padx=10)

        # Nút Thêm
        btn_add = tk.Button(frame_controls, text="+ Thêm Tác Giả", bg="#2196F3", fg="white", 
                            command=self.open_add_author_dialog)
        btn_add.pack(side=tk.LEFT, padx=5)

        # Nút Xóa
        btn_del = tk.Button(frame_controls, text="✕ Xóa", bg="#F44336", fg="white",
                            command=self.delete_author_action)
        btn_del.pack(side=tk.LEFT, padx=5)

        # Nút Tải lại
        btn_reload = tk.Button(frame_controls, text="⟳ Tải lại", command=self.load_authors)
        btn_reload.pack(side=tk.RIGHT, padx=5)

        # 2. Bảng dữ liệu (Treeview)
        self.tree_authors = ttk.Treeview(self.tab_authors, columns=("id", "name"), show="headings", height=15)
        
        self.tree_authors.heading("id", text="ID")
        self.tree_authors.heading("name", text="Tên Tác Giả")
        
        self.tree_authors.column("id", width=50, anchor=tk.CENTER)
        self.tree_authors.column("name", width=400)
        
        self.tree_authors.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Load dữ liệu lần đầu
        self.load_authors()

    def load_authors(self):
        """Lấy danh sách tác giả từ DB đổ vào bảng"""
        # Xóa cũ
        for item in self.tree_authors.get_children():
            self.tree_authors.delete(item)
        
        # Lấy mới
        authors = self.author_model.get_all_authors()
        if authors:
            for a in authors:
                self.tree_authors.insert("", tk.END, values=(a['AuthorID'], a['AuthorName']))

    def open_add_author_dialog(self):
        """Mở cửa sổ thêm tác giả"""
        dialog = tk.Toplevel(self)
        dialog.title("Thêm Tác Giả Mới")
        dialog.geometry("350x150")
        
        tk.Label(dialog, text="Nhập Tên Tác Giả:").pack(pady=10)
        entry_name = tk.Entry(dialog, width=35)
        entry_name.pack(pady=5)
        entry_name.focus()
        
        def save():
            name = entry_name.get().strip()
            if not name:
                messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập tên tác giả!")
                return
            
            if self.author_model.add_author(name):
                messagebox.showinfo("Thành công", "Đã thêm tác giả mới!")
                self.load_authors() # Refresh lại bảng
                dialog.destroy()
            else:
                messagebox.showerror("Lỗi", "Có lỗi khi lưu vào Database")
                
        tk.Button(dialog, text="Lưu", bg="#4CAF50", fg="white", command=save).pack(pady=10)

    def delete_author_action(self):
        """Xóa tác giả"""
        sel = self.tree_authors.selection()
        if not sel:
            messagebox.showwarning("Chọn dòng", "Vui lòng chọn tác giả cần xóa!")
            return
            
        item = self.tree_authors.item(sel[0])
        a_id = item['values'][0]
        a_name = item['values'][1]
        
        msg = f"Bạn có chắc muốn xóa tác giả: {a_name}?\n(Các cuốn sách của tác giả này sẽ bị mất thông tin tác giả)"
        if messagebox.askyesno("Xác nhận xóa", msg):
            if self.author_model.delete_author(a_id):
                messagebox.showinfo("Đã xóa", "Xóa thành công!")
                self.load_authors()
                self.load_books() # Refresh cả tab sách vì sách có thể bị đổi thông tin
            else:
                messagebox.showerror("Lỗi", "Không thể xóa tác giả này.")
                
    def load_selected_report(self):
        """Hàm xử lý logic khi chọn loại báo cáo"""
        report_type = self.cbb_report_type.get()
        
        # 1. Xóa dữ liệu cũ
        self.tree_report.delete(*self.tree_report.get_children())
        
        # 2. Xác định Columns và Data dựa trên lựa chọn
        columns = []
        data = []
        
        if "1. Sách Quá Hạn" in report_type:
            columns = ["Người Mượn", "Tên Sách", "Hạn Trả", "Trạng Thái"]
            data = self.report_model.get_overdue_report()
            
        elif "2. Hoạt Động Mượn" in report_type:
            columns = ["Người Mượn", "Tên Sách", "Trạng Thái"]
            data = self.report_model.get_borrowing_activity()
            
        elif "3. Tất Cả Khách Hàng" in report_type:
            columns = ["Người Mượn", "Tên Sách (Nếu có)", "Trạng Thái"]
            data = self.report_model.get_all_borrowers_status()
            
        elif "4. Chi Tiết Đầy Đủ" in report_type:
            columns = ["Người Mượn", "Tên Sách", "Tác Giả", "Ngày Mượn", "Hạn Trả"]
            data = self.report_model.get_full_loan_details()
        
        # 3. Cấu hình lại cột cho Treeview (Vì mỗi báo cáo số cột khác nhau)
        self.tree_report["columns"] = columns
        
        for col in columns:
            self.tree_report.heading(col, text=col)
            # Chỉnh độ rộng tương đối
            self.tree_report.column(col, width=150, anchor=tk.W)

        # 4. Đổ dữ liệu mới vào
        if data:
            for row in data:
                # Xử lý dữ liệu None thành chuỗi rỗng để tránh lỗi hiển thị
                safe_row = [str(item) if item is not None else "" for item in row]
                self.tree_report.insert("", tk.END, values=safe_row)

    def export_csv(self):
        """Xuất dữ liệu HIỆN TẠI đang có trên bảng ra CSV"""
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                 filetypes=[("CSV files", "*.csv")],
                                                 title="Lưu file báo cáo")
        if not file_path:
            return
            
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                
                # 1. Lấy tiêu đề cột hiện tại
                # (Vì cột thay đổi theo loại báo cáo, nên phải lấy động)
                current_columns = self.tree_report["columns"]
                writer.writerow(current_columns)
                
                # 2. Lấy dữ liệu dòng
                for item in self.tree_report.get_children():
                    row = self.tree_report.item(item)['values']
                    writer.writerow(row)
                    
            messagebox.showinfo("Thành công", f"Đã xuất báo cáo:\n{self.cbb_report_type.get()}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất file: {e}")
    # ==========================================
    # LOGIC CHO TAB SÁCH
    # ==========================================
    def setup_book_tab(self):
        # --- Toolbar ---
        frame_controls = tk.Frame(self.tab_books, pady=10)
        frame_controls.pack(fill=tk.X, padx=10)

        # [PHẦN MỚI] Giao diện Tìm kiếm
        tk.Label(frame_controls, text="Tìm kiếm:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.entry_search_book = tk.Entry(frame_controls, width=25)
        self.entry_search_book.pack(side=tk.LEFT, padx=5)
        
        # Nút icon kính lúp hoặc chữ Tìm
        btn_search = tk.Button(frame_controls, text="Tìm", command=self.search_book)
        btn_search.pack(side=tk.LEFT, padx=5)

        # [PHẦN CŨ] Các nút chức năng (Thêm khoảng cách padx để tách nhóm tìm kiếm ra)
        # Tăng padx ở nút Thêm Sách lên 20 để tạo khoảng trống ngăn cách
        btn_add = tk.Button(frame_controls, text="+ Thêm Sách", bg="#2196F3", fg="white", width=12, 
                            command=self.open_add_book_dialog)
        btn_add.pack(side=tk.LEFT, padx=(20, 5)) 

        btn_edit = tk.Button(frame_controls, text="✎ Sửa", bg="#FFC107", width=10,
                             command=self.open_edit_book_dialog)
        btn_edit.pack(side=tk.LEFT, padx=5)

        btn_delete = tk.Button(frame_controls, text="✕ Xóa", bg="#F44336", fg="white", width=10,
                               command=self.delete_book_action)
        btn_delete.pack(side=tk.LEFT, padx=5)

        btn_reload = tk.Button(frame_controls, text="⟳ Tải lại", command=self.load_books, width=10)
        btn_reload.pack(side=tk.RIGHT, padx=5)

        # --- TẠO BẢNG DANH SÁCH (TREEVIEW) ---
        columns = ("id", "title", "author", "status")
        self.tree_books = ttk.Treeview(self.tab_books, columns=columns, show="headings", height=15)
        
        # Định nghĩa tiêu đề cột
        self.tree_books.heading("id", text="ID")
        self.tree_books.heading("title", text="Tên Sách")
        self.tree_books.heading("author", text="Tác Giả")
        self.tree_books.heading("status", text="Trạng Thái")
        
        # Chỉnh kích thước cột
        self.tree_books.column("id", width=50, anchor=tk.CENTER)
        self.tree_books.column("title", width=400)
        self.tree_books.column("author", width=200)
        self.tree_books.column("status", width=150, anchor=tk.CENTER)
        
        # Thêm thanh cuộn (Scrollbar)
        scrollbar = ttk.Scrollbar(self.tab_books, orient=tk.VERTICAL, command=self.tree_books.yview)
        self.tree_books.configure(yscroll=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_books.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Gọi hàm tải dữ liệu lần đầu
        self.load_books()
    def search_book(self):
        """Logic tìm kiếm sách theo Tên hoặc Tác giả"""
        # 1. Lấy từ khóa người dùng nhập (chuyển về chữ thường để so sánh không phân biệt hoa thường)
        keyword = self.entry_search_book.get().strip().lower()
        
        # 2. Xóa dữ liệu cũ trên bảng
        for item in self.tree_books.get_children():
            self.tree_books.delete(item)
            
        # 3. Lấy tất cả sách từ Database
        all_books = self.book_model.get_all_books()
        
        # 4. Lọc và hiển thị lại
        found_count = 0
        if all_books:
            for book in all_books:
                # Lấy tên sách và tác giả, xử lý trường hợp None
                title = book['BookTitle'].lower() if book['BookTitle'] else ""
                author = book['AuthorName'].lower() if book['AuthorName'] else ""
                
                # Kiểm tra: Nếu từ khóa xuất hiện trong Tên Sách HOẶC Tên Tác Giả
                if keyword in title or keyword in author:
                    status_text = "Đã mượn" if book['CurrentStatus'] else "Sẵn sàng"
                    
                    self.tree_books.insert("", tk.END, values=(
                        book['BookID'],
                        book['BookTitle'],
                        book['AuthorName'] if book['AuthorName'] else "N/A",
                        status_text
                    ))
                    found_count += 1
        
        # (Tuỳ chọn) Thông báo nếu không tìm thấy
        if found_count == 0 and keyword:
             messagebox.showinfo("Thông báo", "Không tìm thấy kết quả nào!")
    def load_books(self):
        """Đọc dữ liệu từ Database và hiển thị lên Treeview"""
        # 1. Xóa dữ liệu cũ trên bảng
        for item in self.tree_books.get_children():
            self.tree_books.delete(item)
        
        # 2. Lấy dữ liệu mới từ Model
        books = self.book_model.get_all_books()
        
        # 3. Đổ dữ liệu vào bảng
        if books:
            for book in books:
                # Xử lý trạng thái hiển thị
                # book['CurrentStatus'] lấy từ câu query trong Model
                status_text = "Đã mượn" if book['CurrentStatus'] else "Sẵn sàng"
                
                # Lưu ý: Thứ tự values phải khớp với columns đã khai báo ở trên
                self.tree_books.insert("", tk.END, values=(
                    book['BookID'],
                    book['BookTitle'],
                    book['AuthorName'] if book['AuthorName'] else "N/A",
                    status_text
                ))
    # ==========================================
    # CÁC CHỨC NĂNG MỚI (THÊM, SỬA, XÓA)
    # ==========================================

    def open_add_book_dialog(self):
        """Mở cửa sổ thêm sách"""
        self.show_book_dialog("Thêm Sách Mới")

    def open_edit_book_dialog(self):
        """Mở cửa sổ sửa sách"""
        selected_item = self.tree_books.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một cuốn sách để sửa!")
            return
        
        # Lấy dữ liệu dòng đang chọn
        item_data = self.tree_books.item(selected_item[0])
        vals = item_data['values'] # (ID, Title, Author, Status)
        
        self.show_book_dialog("Sửa Sách", book_id=vals[0], current_title=vals[1], current_author_name=vals[2])

    def show_book_dialog(self, title_window, book_id=None, current_title="", current_author_name=""):
        """Hàm dựng cửa sổ chung cho Thêm và Sửa Sách (Đã cập nhật logic Tác giả)"""
        dialog = tk.Toplevel(self)
        dialog.title(title_window)
        dialog.geometry("400x250")
        
        # 1. Nhập tên sách
        tk.Label(dialog, text="Tên Sách:").pack(pady=5)
        entry_title = tk.Entry(dialog, width=40)
        entry_title.insert(0, current_title)
        entry_title.pack(pady=5)
        
        # 2. Chọn tác giả (Dropdown)
        tk.Label(dialog, text="Tác Giả:").pack(pady=5)
        
        # --- [QUAN TRỌNG] Lấy danh sách từ AuthorModel ---
        authors = self.author_model.get_all_authors() 
        # authors là list các dict: [{'AuthorID': 1, 'AuthorName': 'ABC'}, ...]
        
        author_names = [a['AuthorName'] for a in authors]
        
        cbb_author = ttk.Combobox(dialog, values=author_names, width=37, state="readonly")
        cbb_author.pack(pady=5)
        
        # Logic chọn giá trị mặc định cho Combobox
        if current_author_name and current_author_name != "N/A":
            if current_author_name in author_names:
                cbb_author.set(current_author_name)
        elif author_names:
            cbb_author.current(0) # Mặc định chọn người đầu tiên
        # ------------------------------------------------
        
        # Hàm Lưu
        def save_action():
            title_input = entry_title.get().strip()
            author_input = cbb_author.get()
            
            if not title_input:
                messagebox.showerror("Lỗi", "Vui lòng nhập tên sách!")
                return
            
            if not author_input:
                messagebox.showerror("Lỗi", "Vui lòng chọn tác giả (Nếu chưa có, hãy qua tab Tác Giả để thêm)!")
                return
            
            # Tìm ID của tác giả dựa trên tên
            author_id = next((a['AuthorID'] for a in authors if a['AuthorName'] == author_input), None)
            
            if book_id is None:
                # Thêm mới
                if self.book_model.add_book(title_input, author_id):
                    messagebox.showinfo("Thành công", "Đã thêm sách mới!")
                    self.load_books()
                    dialog.destroy()
                else:
                    messagebox.showerror("Lỗi", "Không thể thêm sách vào DB.")
            else:
                # Cập nhật
                if self.book_model.update_book(book_id, title_input, author_id):
                    messagebox.showinfo("Thành công", "Đã cập nhật sách!")
                    self.load_books()
                    dialog.destroy()
                else:
                    messagebox.showerror("Lỗi", "Lỗi khi cập nhật.")

        tk.Button(dialog, text="Lưu Dữ Liệu", bg="#4CAF50", fg="white", command=save_action).pack(pady=20)

    def delete_book_action(self):
        """Xử lý xóa sách"""
        selected_item = self.tree_books.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một cuốn sách để xóa!")
            return
        
        # Lấy ID sách
        item_data = self.tree_books.item(selected_item[0])
        book_id = item_data['values'][0]
        book_title = item_data['values'][1]
        
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa sách: {book_title}?\nLưu ý: Không thể xóa sách đang có lịch sử mượn!")
        
        if confirm:
            if self.book_model.delete_book(book_id):
                messagebox.showinfo("Thành công", "Đã xóa sách.")
                self.load_books()
            else:
                messagebox.showerror("Lỗi", "Không thể xóa sách này (Có thể do ràng buộc khóa ngoại với bảng Loans).")

    # ==========================================
    # LOGIC CHO TAB NGƯỜI MƯỢN (BORROWERS)
    # ==========================================
    
    def setup_borrower_tab(self):
        # --- Toolbar ---
        frame_controls = tk.Frame(self.tab_borrowers, pady=10)
        frame_controls.pack(fill=tk.X, padx=10)

        btn_add = tk.Button(frame_controls, text="+ Thêm Mới", bg="#2196F3", fg="white", width=12, 
                            command=self.open_add_borrower_dialog)
        btn_add.pack(side=tk.LEFT, padx=5)

        btn_edit = tk.Button(frame_controls, text="✎ Sửa", bg="#FFC107", width=10,
                             command=self.open_edit_borrower_dialog)
        btn_edit.pack(side=tk.LEFT, padx=5)

        btn_delete = tk.Button(frame_controls, text="✕ Xóa", bg="#F44336", fg="white", width=10,
                               command=self.delete_borrower_action)
        btn_delete.pack(side=tk.LEFT, padx=5)

        btn_reload = tk.Button(frame_controls, text="⟳ Tải lại", command=self.load_borrowers, width=10)
        btn_reload.pack(side=tk.RIGHT, padx=5)

        # --- Treeview ---
        columns = ("id", "name", "email", "phone")
        self.tree_borrowers = ttk.Treeview(self.tab_borrowers, columns=columns, show="headings", height=15)
        
        self.tree_borrowers.heading("id", text="ID")
        self.tree_borrowers.heading("name", text="Họ và Tên")
        self.tree_borrowers.heading("email", text="Email")
        self.tree_borrowers.heading("phone", text="Số Điện Thoại")
        
        self.tree_borrowers.column("id", width=50, anchor=tk.CENTER)
        self.tree_borrowers.column("name", width=250)
        self.tree_borrowers.column("email", width=250)
        self.tree_borrowers.column("phone", width=150)
        
        scrollbar = ttk.Scrollbar(self.tab_borrowers, orient=tk.VERTICAL, command=self.tree_borrowers.yview)
        self.tree_borrowers.configure(yscroll=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_borrowers.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Tải dữ liệu lần đầu
        self.load_borrowers()

    def load_borrowers(self):
        """Đọc dữ liệu từ DB và đổ vào bảng"""
        # Xóa dữ liệu cũ
        for item in self.tree_borrowers.get_children():
            self.tree_borrowers.delete(item)
        
        # Lấy dữ liệu mới
        borrowers = self.borrower_model.get_all_borrowers()
        
        if borrowers:
            for b in borrowers:
                self.tree_borrowers.insert("", tk.END, values=(
                    b['BorrowerID'],
                    b['BorrowerName'],
                    b['Email'],
                    b['Phone']
                ))

    # --- CÁC CHỨC NĂNG CRUD ---

    def open_add_borrower_dialog(self):
        self.show_borrower_dialog("Thêm Người Mượn")

    def open_edit_borrower_dialog(self):
        selected_item = self.tree_borrowers.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một người để sửa!")
            return
        
        # Lấy dữ liệu dòng đang chọn
        item_data = self.tree_borrowers.item(selected_item[0])
        vals = item_data['values'] # (ID, Name, Email, Phone)
        
        # Lưu ý: vals[0] là ID, vals[1] là Name...
        self.show_borrower_dialog("Sửa Thông Tin", 
                                  b_id=vals[0], 
                                  name=vals[1], 
                                  email=vals[2], 
                                  phone=str(vals[3])) # convert phone về string để tránh lỗi hiển thị

    def show_borrower_dialog(self, title_window, b_id=None, name="", email="", phone=""):
        """Dialog dùng chung cho Thêm và Sửa"""
        dialog = tk.Toplevel(self)
        dialog.title(title_window)
        dialog.geometry("400x300")
        
        # 1. Tên
        tk.Label(dialog, text="Họ và Tên (*):").pack(pady=5)
        entry_name = tk.Entry(dialog, width=40)
        entry_name.insert(0, name)
        entry_name.pack(pady=5)
        
        # 2. Email
        tk.Label(dialog, text="Email (*):").pack(pady=5)
        entry_email = tk.Entry(dialog, width=40)
        entry_email.insert(0, email)
        entry_email.pack(pady=5)
        
        # 3. Phone
        tk.Label(dialog, text="Số Điện Thoại:").pack(pady=5)
        entry_phone = tk.Entry(dialog, width=40)
        entry_phone.insert(0, phone)
        entry_phone.pack(pady=5)
        
        def save_action():
            val_name = entry_name.get().strip()
            val_email = entry_email.get().strip()
            val_phone = entry_phone.get().strip()
            
            # Validate cơ bản
            if not val_name or not val_email:
                messagebox.showerror("Lỗi", "Tên và Email không được để trống!")
                return
            
            if b_id is None:
                # Thêm Mới
                if self.borrower_model.add_borrower(val_name, val_email, val_phone):
                    messagebox.showinfo("Thành công", "Đã thêm người mượn!")
                    self.load_borrowers()
                    dialog.destroy()
                else:
                    messagebox.showerror("Lỗi", "Thêm thất bại (Có thể trùng Email).")
            else:
                # Cập nhật
                if self.borrower_model.update_borrower(b_id, val_name, val_email, val_phone):
                    messagebox.showinfo("Thành công", "Đã cập nhật thông tin!")
                    self.load_borrowers()
                    dialog.destroy()
                else:
                    messagebox.showerror("Lỗi", "Cập nhật thất bại.")

        tk.Button(dialog, text="Lưu Dữ Liệu", bg="#4CAF50", fg="white", command=save_action).pack(pady=20)

    def delete_borrower_action(self):
        selected_item = self.tree_borrowers.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn người cần xóa!")
            return
        
        item_data = self.tree_borrowers.item(selected_item[0])
        b_id = item_data['values'][0]
        b_name = item_data['values'][1]
        
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa: {b_name}?\nLưu ý: Nếu người này đang mượn sách, lịch sử mượn cũng sẽ bị xóa (theo Cascade)!")
        
        if confirm:
            if self.borrower_model.delete_borrower(b_id):
                messagebox.showinfo("Thành công", "Đã xóa người mượn.")
                self.load_borrowers()
            else:
                messagebox.showerror("Lỗi", "Không thể xóa.")
                
    # ==========================================
    # LOGIC CHO TAB MƯỢN TRẢ (LOANS)
    # ==========================================

    def setup_loan_tab(self):
        # --- Toolbar ---
        frame_controls = tk.Frame(self.tab_loans, pady=10)
        frame_controls.pack(fill=tk.X, padx=10)

        # Nút Mượn Sách
        btn_borrow = tk.Button(frame_controls, text="➕ Mượn Sách Mới", bg="#2196F3", fg="white", 
                               command=self.open_borrow_dialog)
        btn_borrow.pack(side=tk.LEFT, padx=5)

        # Nút Trả Sách
        btn_return = tk.Button(frame_controls, text="✅ Trả Sách", bg="#4CAF50", fg="white", 
                               command=self.return_book_action)
        btn_return.pack(side=tk.LEFT, padx=5)

        # Nút Tải lại
        btn_reload = tk.Button(frame_controls, text="⟳ Tải lại", command=self.load_loans)
        btn_reload.pack(side=tk.RIGHT, padx=5)

        # --- Treeview (Bảng danh sách) ---
        columns = ("id", "borrower", "book", "date_out", "date_due", "status")
        self.tree_loans = ttk.Treeview(self.tab_loans, columns=columns, show="headings", height=15)
        
        self.tree_loans.heading("id", text="ID")
        self.tree_loans.heading("borrower", text="Người Mượn")
        self.tree_loans.heading("book", text="Tên Sách")
        self.tree_loans.heading("date_out", text="Ngày Mượn")
        self.tree_loans.heading("date_due", text="Hạn Trả")
        self.tree_loans.heading("status", text="Trạng Thái")
        
        # Chỉnh độ rộng cột
        self.tree_loans.column("id", width=50, anchor=tk.CENTER)
        self.tree_loans.column("borrower", width=200)
        self.tree_loans.column("book", width=250)
        self.tree_loans.column("date_out", width=100, anchor=tk.CENTER)
        self.tree_loans.column("date_due", width=100, anchor=tk.CENTER)
        self.tree_loans.column("status", width=100, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(self.tab_loans, orient=tk.VERTICAL, command=self.tree_loans.yview)
        self.tree_loans.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_loans.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.load_loans()

    def load_loans(self):
        """Tải dữ liệu mượn trả"""
        for item in self.tree_loans.get_children():
            self.tree_loans.delete(item)
            
        loans = self.loan_model.get_all_loans()
        for loan in loans:
            # Tô màu trạng thái (Optional)
            status = loan['Status']
            
            # Insert vào bảng
            self.tree_loans.insert("", 0, values=(
                loan['LoanID'],
                loan['BorrowerName'],
                loan['BookTitle'],
                loan['BorrowedDate'],
                loan['DueDate'],
                status
            ))

    # --- CHỨC NĂNG MƯỢN SÁCH ---
    def open_borrow_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Mượn Sách")
        dialog.geometry("400x250")
        
        # 1. Chọn Người Mượn
        tk.Label(dialog, text="Người Mượn:").pack(pady=5)
        
        # Lấy list borrower từ Model
        borrowers = self.borrower_model.get_all_borrowers()
        borrower_names = [f"{b['BorrowerID']} - {b['BorrowerName']}" for b in borrowers]
        
        cbb_borrower = ttk.Combobox(dialog, values=borrower_names, width=40, state="readonly")
        cbb_borrower.pack(pady=5)
        
        # 2. Chọn Sách (Chỉ hiện sách CÓ SẴN)
        tk.Label(dialog, text="Chọn Sách (Chỉ hiện sách chưa được mượn):").pack(pady=5)
        
        available_books = self.loan_model.get_available_books()
        book_names = [f"{b['BookID']} - {b['BookTitle']}" for b in available_books]
        
        cbb_book = ttk.Combobox(dialog, values=book_names, width=40, state="readonly")
        cbb_book.pack(pady=5)
        
        def save_loan():
            b_str = cbb_borrower.get()
            bk_str = cbb_book.get()
            
            if not b_str or not bk_str:
                messagebox.showerror("Lỗi", "Vui lòng chọn người mượn và sách!")
                return
            
            # Cắt chuỗi để lấy ID (Vì định dạng là "ID - Name")
            borrower_id = int(b_str.split(" - ")[0])
            book_id = int(bk_str.split(" - ")[0])
            
            if self.loan_model.borrow_book(borrower_id, book_id):
                messagebox.showinfo("Thành công", f"Đã mượn sách thành công!\nHạn trả: 14 ngày tới.")
                self.load_loans()
                # Cập nhật lại tab sách để thấy trạng thái thay đổi
                self.load_books() 
                dialog.destroy()
            else:
                messagebox.showerror("Lỗi", "Có lỗi xảy ra khi lưu vào CSDL.")

        tk.Button(dialog, text="Xác Nhận Mượn", bg="#2196F3", fg="white", command=save_loan).pack(pady=20)

    # --- CHỨC NĂNG TRẢ SÁCH ---
    def return_book_action(self):
        selected_item = self.tree_loans.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng để trả sách!")
            return
        
        item_data = self.tree_loans.item(selected_item[0])
        loan_id = item_data['values'][0]
        status = item_data['values'][5]
        
        if status == 'Returned':
            messagebox.showinfo("Thông báo", "Sách này đã được trả rồi!")
            return
            
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn trả cuốn sách này?")
        if confirm:
            if self.loan_model.return_book(loan_id):
                messagebox.showinfo("Thành công", "Đã trả sách.")
                self.load_loans()
                self.load_books() # Refresh cả tab sách
            else:
                messagebox.showerror("Lỗi", "Không thể cập nhật trạng thái.")
    # LOGIC TAB BÁO CÁO (ĐÃ NÂNG CẤP AUTO-REFRESH)
    # ==========================================

    def setup_report_tab(self):
        if not hasattr(self, 'report_model'):
            self.report_model = ReportModel()
        
        # 1. Khung chứa KPI và Biểu đồ (Dashboard)
        # Chúng ta gán self.frame_dashboard để lát nữa có thể truy cập vào xóa đi vẽ lại
        self.frame_dashboard = tk.Frame(self.tab_reports)
        self.frame_dashboard.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Vẽ nội dung Dashboard lần đầu
        self.refresh_dashboard_ui()

        # 2. Khung chứa Toolbar và Bảng dữ liệu
        frame_bot = tk.Frame(self.tab_reports)
        frame_bot.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        toolbar = tk.Frame(frame_bot)
        toolbar.pack(fill=tk.X, pady=5)

        tk.Label(toolbar, text="Loại Báo Cáo:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.cbb_report_type = ttk.Combobox(toolbar, state="readonly", width=35)
        self.cbb_report_type['values'] = (
            "1. Sách Quá Hạn (Overdue)", 
            "2. Hoạt Động Mượn (Inner Join)", 
            "3. Tất Cả Khách Hàng (Left Join)", 
            "4. Chi Tiết Đầy Đủ (Multi-table Join)"
        )
        self.cbb_report_type.current(0)
        self.cbb_report_type.pack(side=tk.LEFT, padx=5)
        
        btn_view = tk.Button(toolbar, text="👁 Xem", bg="#2196F3", fg="white", 
                             command=self.load_selected_report)
        btn_view.pack(side=tk.LEFT, padx=5)

        btn_export = tk.Button(toolbar, text="⬇ Xuất CSV", bg="green", fg="white", font=("Arial", 9, "bold"),
                               command=self.export_csv)
        btn_export.pack(side=tk.RIGHT, padx=5)

        # Treeview
        self.tree_report = ttk.Treeview(frame_bot, show="headings", height=8)
        self.tree_report.pack(fill=tk.BOTH, expand=True)
        self.load_selected_report()

    def refresh_dashboard_ui(self):
        """Hàm này sẽ xóa Dashboard cũ và vẽ lại cái mới (KPI + Biểu đồ)"""
        # 1. Xóa sạch các widget cũ trong frame_dashboard
        for widget in self.frame_dashboard.winfo_children():
            widget.destroy()

        # 2. Lấy số liệu mới nhất từ DB
        kpis = self.report_model.get_kpis()
        
        # 3. Vẽ lại KPI text
        lbl_text = f"Tổng Sách: {kpis['total_books']} | Khách Hàng: {kpis['total_borrowers']} | Đang Mượn: {kpis['active_loans']} | Quá Hạn: {kpis['overdue_count']}"
        lbl_info = tk.Label(self.frame_dashboard, text=lbl_text, font=("Arial", 11, "bold"), fg="#D32F2F")
        lbl_info.pack(pady=5)
        
        # 4. Vẽ lại Biểu đồ tròn
        try:
            fig = Figure(figsize=(5, 2.5), dpi=100)
            ax = fig.add_subplot(111)
            
            # Xử lý trường hợp không có dữ liệu để tránh lỗi vẽ
            if kpis['active_loans'] == 0 and kpis['overdue_count'] == 0:
                ax.text(0.5, 0.5, "Chưa có dữ liệu mượn", ha='center')
            else:
                # Tính toán số đã trả (Giả định hoặc lấy query riêng)
                # Ở đây mình lấy ví dụ là số sách còn lại
                returned_estimated = 5 # Hoặc query đếm số dòng status='Returned'
                
                data = [kpis['active_loans'], kpis['overdue_count'], returned_estimated] 
                labels = ['Đang Mượn', 'Quá Hạn', 'Đã Trả/Khác']
                colors = ['#2196F3', '#F44336', '#4CAF50']
                
                ax.pie(data, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
                ax.set_title("Tỉ lệ Mượn/Trả", fontsize=10)
            
            canvas = FigureCanvasTkAgg(fig, master=self.frame_dashboard)
            canvas.draw()
            canvas.get_tk_widget().pack()
        except Exception as e:
            tk.Label(self.frame_dashboard, text=f"Lỗi vẽ biểu đồ: {e}").pack()

    # [HÀM QUAN TRỌNG NHẤT] - Tự động chạy khi bấm chuyển tab
    def on_tab_change(self, event):
        """Sự kiện này kích hoạt mỗi khi người dùng bấm vào một Tab bất kỳ"""
        # Lấy tab đang được chọn
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")
        
        # Nếu tab được chọn có chữ "Báo Cáo"
        if "Báo Cáo" in tab_text:
            # Gọi hàm làm mới Dashboard
            self.refresh_dashboard_ui()
            # Gọi hàm làm mới bảng dữ liệu bên dưới
            self.load_selected_report()
            # (Optional) Nếu muốn tab Sách/Mượn cũng tự refresh thì thêm elif ở đây
        elif "Quản Lý Sách" in tab_text:
            self.load_books()
        elif "Mượn Trả" in tab_text:
            self.load_loans()
if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()