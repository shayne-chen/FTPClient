from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from ftplib import FTP
import paramiko
from tkinter.scrolledtext import ScrolledText
import tkinter as tk
from tkinter import messagebox
import multiprocessing

class Window():

	def __init__(self):
		self.master = Tk()
		self.master.title("FTPClient")
		self.master.geometry("800x600")
		self.master.resizable(width=False, height=False)
		self.frame1 = Frame(width=800, height=230)
		self.frame2 = Frame(width=800, height=370)

		#起止IP设置
		self.start_ip = StringVar()
		self.end_ip = StringVar()
		self.label_startip = Label(self.frame1, text="起始IP:", fg="red")
		self.entry_startip = Entry(self.frame1, width=40, textvariable=self.start_ip)
		self.label_endip = Label(self.frame1, text="结束IP:", fg="red")
		self.entry_endip = Entry(self.frame1, width=40, textvariable=self.end_ip)
		self.start_ip.set('192.178.3.')
		self.end_ip.set('192.178.3.')

		#登录用户名及密码设置
		self.user = StringVar()
		self.password = StringVar()
		self.label_user = Label(self.frame1, text="用户名:", fg="red")
		self.entry_user = Entry(self.frame1, width=40, textvariable=self.user)
		self.label_password = Label(self.frame1, text="密码:", fg="red")
		self.entry_password = Entry(self.frame1, width=40, textvariable=self.password)
		self.user.set('root')
		self.password.set('root')

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
		self.button_uploadfile = Button(self.frame1, text="上传", width=10, fg="red", command=self.uploadfile)

		#测试指令
		self.test_content = StringVar()
		self.test_label = Label(self.frame1, text="输入指令", fg='red')
		self.test_entry = Entry(self.frame1, width=40, textvariable=self.test_content)

		#提交按钮
		self.submit = Button(self.frame1, text="提交", width=10, fg="red", command=self.run_shell)
		self.empty_button = Button(self.frame1, text="清空文本框", width=10, fg='red', command=self.delText)

		#结果显示框
		self.text = ScrolledText(self.frame2, width=111, height=25, wrap=tk.WORD)

		#元件布局
		self.frame1.grid(row=0, column=0)
		self.frame2.grid(row=1,column=0)
		self.frame1.grid_propagate(0)
		self.frame2.grid_propagate(0)

		#第一行
		self.label_startip.grid(row=0 ,column=0, padx=5, pady=10)
		self.entry_startip.grid(row=0, column=1, padx=5, pady=10)
		self.label_endip.grid(row=0, column=2, padx=5, pady=10)
		self.entry_endip.grid(row=0, column=3, padx=5, pady=10)

		#第二行
		self.label_user.grid(row=1, column=0, padx=5, pady=10)
		self.entry_user.grid(row=1, column=1, padx=5, pady=10)
		self.label_password.grid(row=1, column=2, padx=5, pady=10)
		self.entry_password.grid(row=1, column=3, padx=5, pady=10)

		#第三行
		self.label_file.grid(row=2, column=0, padx=5, pady=10)
		self.entry_file.grid(row=2, column=1, padx=5, pady=10)
		self.choose_file.grid(row=2, column=2, padx=5, pady=10)

		#第四行
		self.label_file_savepath.grid(row=3, column=0, padx=5, pady=10)
		self.entry_file_savepath.grid(row=3, column=1, padx=5, pady=10)
		self.label_file_savepath_tips.grid(row=3, column=2, padx=5, pady=10)
		self.button_uploadfile.grid(row=3, column=3, padx=5)

		#第五行
		self.test_label.grid(row=4, column=0, pady=5)
		self.test_entry.grid(row=4, column=1, pady=5)
		self.submit.grid(row=4, column=2)
		self.empty_button.grid(row=4, column=3)

		#文本框
		self.text.grid(row=0, column=0)

		mainloop()

	def getall_ip(self):
		all_ip = []
		start_ip = self.start_ip.get()
		end_ip = self.end_ip.get()
		if start_ip == "" or end_ip == "":
			messagebox.showinfo("Warning!", "ip地址为空！")
		else:
			try:
				ip_three_bytes = start_ip.split('.')[0] + '.' + start_ip.split('.')[1] + '.' + start_ip.split('.')[2] + '.'
				for i in range(int(start_ip.split('.')[3]), int(end_ip.split('.')[3])+1):
					all_ip.append(ip_three_bytes + str(i))
				return all_ip
			except:
				messagebox.showinfo("Warning!", "IP地址格式错误！")

	def choose_file(self):
		filename = askopenfilename(filetypes=[("All Files", "*.*")])
		self.filepath.set(filename)

	def uploadfile(self):
		ftp = FTP()
		fp = open(self.filepath.get(), 'rb')
#		ftp.set_debuglevel(2)
		allip = Window.getall_ip(self)
		upload_filename = self.filepath.get().split('/')[-1]
		file_des_path = self.entry_file_savepath.get() + upload_filename
#		need_command = "ls " + file_des_path
#		print (need_command)
#		print (file_des_path)
		if self.filepath.get() == "" or self.file_savepath.get() == "":
			messagebox.showinfo("Warning!", "未选择文件|上传路径")
		for ip in allip:
#			print (ip)
			ftp.connect(ip, 21)
			ftp.login(self.user.get(), self.password.get())		
			try:
				ftp.storbinary('STOR ' + file_des_path, fp, 1024)
				ftp.set_debuglevel(2)
				ftp.close()
			except:
				pass
				
		messagebox.showinfo("Warning!","上传完成!")

	def run_shell(self):
		input_command = self.test_content.get()
		allip = Window.getall_ip(self)
		if self.test_content.get() == '':
			messagebox.showinfo("Warning!", "输入指令！")
		for host in allip:
			result = Window.shell(self, host, input_command)
			self.text.insert(INSERT, host + '\n')
			self.text.insert(INSERT, result)
			self.text.insert(INSERT, '\n')
		messagebox.showinfo("Result","OK!")

	def shell(self, host, shell_command):
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			ssh.connect(hostname=host, port=22, username=self.user.get(), password=self.password.get())
			stdin, stdout, stderr = ssh.exec_command(shell_command)
			result = stdout.read()
			return result
		except:
			pass
		else:
			return result
		finally:
			ssh.close()

	def delText(self):
		self.text.delete(1.0, END)

if __name__ == '__main__':
	Window()