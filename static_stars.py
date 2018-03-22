import paramiko
import pymysql
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

total_mem_cmd = "top -b -n 1 |grep Mem|head -1|cut -d ',' -f 1|cut -d ':' -f 2|cut -d 't' -f 1"
used_mem_cmd = "top -b -n 1 |grep Mem|head -1|cut -d ',' -f 2|cut -d 'u' -f 1"

IPFile = "E:\Shaw\python_work\FTPClient\StarsIP.txt"
IP = []
present_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

with open(IPFile, 'r') as f:
	for line in f.readlines():
		IP.append(line.strip('\n'))

conn = pymysql.connect(host='localhost',user='root',password='chenxiao',database='stars',port=3306,charset='utf8')
cur = conn.cursor()

def cal_mem_cpu():
	for host in IP:
		ssh.connect(hostname=host, port=22, username="root", password="root")
		#内存占用
		stdin, total_mem, stderr = ssh.exec_command(total_mem_cmd)
		stdin, used_mem, stderr = ssh.exec_command(used_mem_cmd)
		total_mem = str(total_mem.read(), encoding="utf-8")
		used_mem = str(used_mem.read(), encoding="utf-8")
		mem = float(used_mem)/float(total_mem)
		mem_percent = int(mem*100)
#		print (host, mem_percent)
		

		#CPU占用
		need_data1, sum1 = cal_cpu(ssh)
		time.sleep(0.5)
		need_data2, sum2 = cal_cpu(ssh)
		total = sum2 - sum1
		idle = int(need_data2[3]) - int(need_data1[3])
		number = (total-idle)/total
		cpu_percent = int(number*100)
#		print (host, cpu_percent)

		sql = "insert into stars_infos (ip, cpu_used, mem_used, task_type) values (%s,%s,%s,%s)"
		print (host)
		task_type = judge_tasktype(ssh)
#		print (host, cpu_percent, mem_percent, task_type_pic)
		value = (host, cpu_percent, mem_percent, task_type)
		cur.execute(sql, value)
	conn.commit()
	cur.close()
	conn.close()

def cal_cpu(ssh):
	stdin, cpu_info, stderr = ssh.exec_command("head -n 1 /proc/stat")
	cpu_info = str(cpu_info.read())
	datas = cpu_info.split(' ')
	need_data = []
	sums = 0
	for data in datas:
		if data.isdigit():
			need_data.append(data)
			data = int(data)
			sums = sums + data
	return need_data, sums

def judge_tasktype(ssh):
	stdin, task_file, stderr = ssh.exec_command("ls /etc/vioncfg/Device/global_task.xml")
	if "global_task.xml" in str(task_file.read()):
		stdin, pic_video, stderr = ssh.exec_command("cat /etc/vioncfg/Device/global_task.xml")
		if "pic" in str(pic_video.read()):
			task_type = "pic"
		else:
			task_type = "video"
	else:
		task_type = "None"
	return task_type

if __name__ == '__main__':
	cal_mem_cpu()