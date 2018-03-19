from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from ftplib import FTP
import paramiko
from tkinter.scrolledtext import ScrolledText
import tkinter as tk
from tkinter import messagebox
import multiprocessing
import time

class Window():

	def __init__(self):
		self.master = Tk()
		self.master.title("FTPClient")
		self.master.geometry("1000x800")
		self.master.resizable(width=False, height=False)
		self.frame1 = Frame(width=1000, height=300)
		self.frame2 = Frame(width=1000, height=500)

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

		#按钮
		self.submit = Button(self.frame1, text="提交", width=10, fg="red", command=self.run_shell)
		self.empty_button = Button(self.frame1, text="清空文本框", width=10, fg='red', command=self.delText)

		#监控资源的按钮
		self.operateserver_button = Button(self.frame1, text="运维重启状况", width=10, fg='red', command=self.watch_operate)
		self.vaserver_button = Button(self.frame1, text="分析重启状况", width=10, fg='red', command=self.watch_vaserver)
		self.cpu_button = Button(self.frame1, text="CPU占用", width=10, fg='red', command=self.cpu_used)
		self.memory_button = Button(self.frame1, text="内存占用", width=10, fg='red', command=self.memory_used)

		#结果显示框
		self.text = ScrolledText(self.frame2, width=140, height=38, wrap=tk.WORD, bg='white')

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

		#第六行
		self.operateserver_button.grid(row=5, column=0, padx=5, pady=5)
		self.vaserver_button.grid(row=5, column=1, padx=5, pady=5)
		self.cpu_button.grid(row=5, column=2, padx=5, pady=5)
		self.memory_button.grid(row=5, column=3, padx=5, pady=5)			

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

	def watch_operate(self):
		input_shell = "tail -n 1 /home/cx/scripts/operateserver.log"
		print (type(input_shell))
		allip = Window.getall_ip(self)
		for host in allip:
			result = Window.shell(self, host, input_shell)
			result = str(result, encoding="utf-8")		
			self.text.insert(INSERT, host + '\n')
			self.text.insert(INSERT, "OperateServer重启次数: " + result.split(',')[0] + '\n')
		messagebox.showinfo("Result", "OK!")

	def watch_vaserver(self):
		pass

#	def cpu_used(self):
#		cpu_cmd = "top -b -n 1|grep Cpu|cut -d ',' -f 2|cut -d 's' -f 1"
#		print (type(cpu_cmd))
#		allip = Window.getall_ip(self)
#		for host in allip:
#			cpu_result = Window.shell(self, host, cpu_cmd)
#			print (cpu_result)
#			print (type(cpu_result))
#			cpu_result = str(cpu_result, encoding="utf-8")
#			self.text.insert(INSERT, host + '\n')
#			self.text.insert(INSERT, "CPU使用率：" + cpu_result.strip('\n') + "%" + '\n')
#		messagebox.showinfo("Result", "OK!")

	def cpu_used(self):
		cpu_cmd = "head -n 1 /proc/stat"
		allip = Window.getall_ip(self)
		for host in allip:
			cpu_result1 = Window.shell(self, host, cpu_cmd)
			cpu_result1 = str(cpu_result1)
			datas1 = cpu_result1.split(' ')
			need_data1 = []
			sum1 = 0
			for data in datas1:
				if data.isdigit():
					need_data1.append(data)
			for a in need_data1:
				a = int(a)
				sum1 = sum1 + a
			time.sleep(1)
			cpu_result2 = Window.shell(self, host, cpu_cmd)
			cpu_result2 = str(cpu_result2)
			datas2 = cpu_result2.split(' ')
			need_data2 = []
			sum2 = 0
			for data in datas2:
				if data.isdigit():
					need_data2.append(data)
			for b in need_data2:
				b = int(b)
				sum2 = sum2 + b

			total = sum2 - sum1
#			print(sum1)
#			print(sum2)
			idle = int(need_data2[3]) - int(need_data1[3])
#			print (idle)
			number = (total-idle)/total
			percent = "%.2f%%"%(number*100)

			self.text.insert(INSERT, '\n' + host + '\n')
			self.text.insert(INSERT, "CPU使用率：" + percent + '\n')
		messagebox.showinfo("Result", "OK!")

	def memory_used(self):
		total_mem_cmd = "top -b -n 1 |grep Mem|head -1|cut -d ',' -f 1|cut -d ':' -f 2|cut -d 't' -f 1"
		used_mem_cmd = "top -b -n 1 |grep Mem|head -1|cut -d ',' -f 2|cut -d 'u' -f 1"
		allip = Window.getall_ip(self)
		for host in allip:
			total_mem = Window.shell(self, host, total_mem_cmd)
			used_mem = Window.shell(self, host, used_mem_cmd)
#			print (total_mem)
#			print (type(total_mem))
#			print (used_mem)
#			print (type(used_mem))
			total_mem = str(total_mem, encoding="utf-8")
			used_mem = str(used_mem, encoding="utf-8")
			percent = float(used_mem)/float(total_mem)
			percent = "%.2f%%"%(percent*100)
#			print (type(percent))
			self.text.insert(INSERT, '\n' + host + '\n')
			self.text.insert(INSERT, "内存占用：" + percent + '\n')
		messagebox.showinfo("Result", "OK!")

if __name__ == '__main__':
	Window()