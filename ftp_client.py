from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from ftplib import FTP

class Window():

	def __init__(self):
		self.master = Tk()
		self.master.title("FTPClient")
		self.master.geometry("800x600")
		self.master.resizable(width=False, height=False)
		self.frame1 = Frame(width=800, height=250)
		self.frame2 = Frame(width=800, height=350, bg="green")

		#起止IP设置
		self.start_ip = StringVar()
		self.end_ip = StringVar()
		self.label_startip = Label(self.frame1, text="起始IP:", fg="red")
		self.entry_startip = Entry(self.frame1, width=40, textvariable=self.start_ip)
		self.label_endip = Label(self.frame1, text="结束IP:", fg="red")
		self.entry_endip = Entry(self.frame1, width=40, textvariable=self.end_ip)

		#登录用户名及密码设置
		self.user = StringVar()
		self.password = StringVar()
		self.label_user = Label(self.frame1, text="用户名:", fg="red")
		self.entry_user = Entry(self.frame1, width=40, textvariable=self.user)
		self.label_password = Label(self.frame1, text="密码:", fg="red")
		self.entry_password = Entry(self.frame1, width=40, textvariable=self.password)

		#文件路径设置
		self.filepath = StringVar()
		self.label_file = Label(self.frame1, text="文件路径:", fg="red")
		self.entry_file = Entry(self.frame1, width=40, textvariable=self.filepath)
		self.choose_file = Button(self.frame1, text="选择文件", fg="red", width=10, command=self.choose_file)

		#文件的保存路径
		self.file_savepath = StringVar()
		self.label_file_savepath = Label(self.frame1, text="保存路径", fg="red")
		self.entry_file_savepath = Entry(self.frame1, width=40, textvariable=self.file_savepath)
		self.label_file_savepath_tips = Label(self.frame1, text="例如：/home/ubuntu/", fg='green')

		#提交按钮
		self.submit = Button(self.frame1, text="提交", width=10, fg="green", command=self.uploadfile)

		#元件布局
		self.frame1.grid(row=0, column=0)
		self.frame2.grid(row=1,column=0)
		self.frame1.grid_propagate(0)
		self.frame2.grid_propagate(0)
		self.label_startip.grid(row=0 ,column=0, padx=5, pady=10)
		self.entry_startip.grid(row=0, column=1, padx=5, pady=10)
		self.label_endip.grid(row=0, column=2, padx=5, pady=10)
		self.entry_endip.grid(row=0, column=3, padx=5, pady=10)
		self.label_user.grid(row=1, column=0, padx=5, pady=10)
		self.entry_user.grid(row=1, column=1, padx=5, pady=10)
		self.label_password.grid(row=1, column=2, padx=5, pady=10)
		self.entry_password.grid(row=1, column=3, padx=5, pady=10)
		self.label_file.grid(row=2, column=0, padx=5, pady=10)
		self.entry_file.grid(row=2, column=1, padx=5, pady=10)
		self.choose_file.grid(row=2, column=2, padx=5, pady=10)
		self.label_file_savepath.grid(row=3, column=0, padx=5, pady=10)
		self.entry_file_savepath.grid(row=3, column=1, padx=5, pady=10)
		self.label_file_savepath_tips.grid(row=3, column=2, padx=5, pady=10)
		self.submit.grid(row=4, column=0, columnspan=5, pady=10)

		mainloop()


	def choose_file(self):
		filename = askopenfilename(filetypes=[("All Files", "*.*")])
		self.filepath.set(filename)

	def uploadfile(self):
		ftp = FTP()
		ftp.set_debuglevel(2)
		allip = []
		start_ip = self.start_ip.get()
		end_ip = self.end_ip.get()
		ip_three_bytes = start_ip.split('.')[0] + '.' + start_ip.split('.')[1] + '.' + start_ip.split('.')[2] + '.'
		for i in range(int(start_ip.split('.')[3]), int(end_ip.split('.')[3])+1):
			allip.append(ip_three_bytes + str(i))
		for ip in allip:
			print (ip)
			ftp.connect(ip, 21)
			ftp.login(self.user.get(), self.password.get())
			fp = open(self.filepath.get(), 'rb')
			ftp.storbinary('STOR ' + self.entry_file_savepath.get() + self.filepath.get().split('/')[-1], fp, 1024)
			ftp.set_debuglevel(2)
			ftp.close()

		messagebox.showinfo("Result", "Upload Finished!")


if __name__ == '__main__':
	Window()