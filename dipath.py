#coding:utf8
import re
import os

def Project(path):
	"""
	경로를 받아서 프로젝트 문자열과 에러값을 리턴한다.
	만약 리턴할 프로젝트 문자열이 없으면 ""를 리턴한다.
	"""
	# show
	show = re.findall('/show[/_](\S[^/]+)', path.replace("\\","/"))
	if len(show) == 1:
		return show[0], None
	# backup
	backup = re.findall('/backup/\d+?/(\S[^/]+)', path.replace("\\","/"))
	if len(backup) == 1:
		return backup[0], None
	return "", "경로에서 프로젝트를 가지고 올 수 없습니다."

def Seq(path):
	"""
	경로를 받아서 시퀀스 문자열과 에러값을 리턴한다.
	만약 리턴할 시퀀스 문자열이 없으면 ""를 리턴한다.
	"""
	# show
	show = re.findall('/show[/_]\S+?/seq/(\S[^/]+)', path.replace("\\","/"))
	if len(show) == 1:
		return show[0], None
	# backup
	backup = re.findall('/backup/\d+?/\S+?/\S+?/seq/(\S[^/]+)', path.replace("\\","/"))
	if len(backup) == 1:
		return backup[0], None
	return "", "경로에서 시퀀스를 가지고 올 수 없습니다."

def Shot(path):
	"""
	경로를 받아서 샷 문자열과 에러값을 리턴한다.
	만약 리턴할 샷 문자열이 없으면 ""를 리턴한다.
	"""
	# show
	show = re.findall('/show[/_]\S+?/seq/\S+?/\S+?_(\S[^/]+)', path.replace("\\","/"))
	if len(show) == 1:
		return show[0], None
	# backup
	backup = re.findall('/backup/\d+?/\S+?/\S+?/seq/\S+?/\S+?_(\S[^/]+)', path.replace("\\","/"))
	if len(backup) == 1:
		return backup[0], None
	return "", "경로에서 샷을 가지고 올 수 없습니다."



def ShotFromBaseName(path):
	"""
	파일경로를 받아서 베이스샷 문자열과 에러값을 리턴한다.
	만약 리턴할 베이스샷 문자열이 없으면 ""를 리턴한다.
	"""
	hasRnum = re.findall("([ABCDEFGH][0-9]{4})_([a-zA-Z0-9]+)_([a-zA-Z]*[0-9]+)", path)
	if hasRnum: # 롤넘버가 존재할때(최대8권)
		return hasRnum[0][1] + "_" + hasRnum[0][2], None
	hasShot = re.findall("([a-zA-Z0-9]+)_([a-zA-Z]*[0-9]+)", path)
	if hasShot:
		return hasShot[0][0] + "_" + hasShot[0][1], None
	return "", "파일 경로에서 샷을 가지고 올 수 없습니다."

def Seqnum(path):
	"""
	경로를 받아서 시퀀스넘버를 반환한다.                                                                                                                                                                                          
	만약 리턴할 시컨스넘버가 없으면 -1과 에러를 반환한다.
	"""
	p = re.compile("([0-9]+)\\.[a-zA-Z]+$")
	result = p.findall(path)

	if len(result) == 0:
		return -1, "시퀀스 파일이 아닙니다."
	seqnum = int(result[0])	
	return seqnum,None


def Vernum(path):
	"""
	파일을 받아서 파일 버전과 서브 버전을 반환한다.
	만약 리턴할 버전과 서브버전이 없으면 -1과 에러를 반환한다.
	"""
	p = re.compile("_[vV]([0-9]+)(_[wW]([0-9]+))*")
	results = p.findall(path)

	if len(results) == 0:
		return -1, -1, "버전 정보를 가지고 올 수 없습니다."
	
	vernum = int(results[0][0])
	if results[0][2] != "":
		subnum = int(results[0][2])
	else:
		subnum = -1
	
	return vernum,subnum, None

def Lin2win(path):
	"""
	리눅스 경로를 윈도우즈 경로로 바꾸어줍니다.
	이 함수는 UNC패스(\\\\10.0.200.100형태)로 변경되지 않습니다.
	변경되지 않으면 입력된 경로를 그대로 반환합니다.
	"""
	if path.startswith("/show/"):
		return "//10.0.200.100/show_" + path[6:]
	if path.startswith("/lustre/INHouse/"):
		return "//10.0.200.100/_lustre_INHouse/" + path[16:]
	if path.startswith("/lustre/show/"):
		return "//10.0.200.100/show_" + path[13:]
	if path.startswith("/lustre2/show/"):
		return "//10.0.200.100/show_" + path[14:]
	if path.startswith("/lustre3/show/"):
		return "//10.0.200.100/show_" + path[14:]
	if path.startswith("/clib/"):
		return "//10.0.200.100/clib/" + path[6:]
	if path.startswith("/backup/"):
		return "//10.0.200.100/_IDEA_BackUP/" + path[8:]
	return path

def Rmlustre(path):
	"""
	경로의 시작이 /lustre/show, /lustre2/show, /lustre3/show 로 시작한다면 /show로 바꾸어줍니다.
	위 사항이 아니라면 입력된 경로를 그대로 반환합니다.
	"""
	if path.startswith("/lustre/show"):
		return path[7:]
	if path.startswith("/lustre2/show"):
		return path[8:]
	if path.startswith("/lustre3/show"):
		return path[8:]
	return path

def Rnum(path):
	"""
	파일경로를 받아서 롤넘버와 None을  반환한다.
	잘못된 롤넘버의 경우 해당 롤넙버와 err를 반환한다.
	롤넘버가 없으면 빈문자열을 반환한다.
	"""
	hasRnum = re.findall("([ABCDEFGH][0-9]{4})_([a-zA-Z0-9]+)_([a-zA-Z]*[0-9]+)", path)
	if hasRnum: # 롤넘버가 존재할때(최대8권)
		return hasRnum[0][0], None
	return "", "파일 경로에서 롤넘버를 가지고 올 수 없습니다."
