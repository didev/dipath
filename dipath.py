#coding:utf8
import re
import os
import glob

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

def Task(path):
	"""
	경로를 받아서 Task 문자열과 에러값을 리턴한다.
	만약 리턴할 Task 문자열이 없으면 ""를 리턴한다.
	"""
	# task
	task = re.findall('/show[/_]\S+?/seq/\S+?/\S+?_\S+/(\S+)/dev', path.replace("\\","/"))
	if len(task) == 1:
		return task[0], None
	task = re.findall('/show[/_]\S+?/seq/\S+?/\S+?_\S+/(\S+)/pub', path.replace("\\","/"))
	if len(task) == 1:
		return task[0], None
	# asset
	asset = re.findall('/show[/_]\S+?/assets/\S+?/\S+?/(\S+)/dev', path.replace("\\","/"))
	if len(asset) == 1:
		return asset[0], None
	asset = re.findall('/show[/_]\S+?/assets/\S+?/\S+?/(\S+)/pub', path.replace("\\","/"))
	if len(asset) == 1:
		return asset[0], None
	return "", "경로에서 Task를 가지고 올 수 없습니다."


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
	롤넘버가 없으면 빈문자열을 반환한다.
	"""
	hasRnum = re.findall("([ABCDEFGH][0-9]{4})_([a-zA-Z0-9]+)_([a-zA-Z]*[0-9]+)", path)
	if hasRnum: # 롤넘버가 존재할때(최대8권)
		return hasRnum[0][0], None
	return "", "파일 경로에서 롤넘버를 가지고 올 수 없습니다."

def PlateMov(project, seq, shot, type):
	"""
	plate경로에 mov 파일중 우선순위가 높은 mov를 검색해서 반환하는 함수이다.
	SS_0010_org11.mov
	SS_0010_org11_retime.mov
	SS_0010_org12.mov
	파일이 있다면 SS_0010_org12.mov 파일과 에러값을 반환한다.
	"""
	platepath = "/show/%s/seq/%s/%s_%s/plate" %  (project, seq, seq, shot)
	if not os.path.exists(platepath):
		return [], "플레이트 경로가 존재하지 않습니다."
	case1 = glob.glob(platepath + "/" + "%s_%s_%s*_retime.mov" %  (seq, shot, type))
	case2 = glob.glob(platepath + "/" + "%s_%s_%s[1-9][0-9].mov" %  (seq, shot, type))
	case3 = glob.glob(platepath + "/" + "%s_%s_%s[1-9].mov" %  (seq, shot, type))
	case4 = glob.glob(platepath + "/" + "%s_%s_%s.mov" %  (seq, shot, type))
	movs = case1 + case2 + case3 + case4
	if not movs:
		return "", "mov가 존재하지 않습니다."
	temp = 0
	last = ""
	for m in movs:
		# 파일경로에서 숫자만 뽑는다.
		current = int(filter(str.isdigit, m))
		if current < temp:
			continue
		elif current == temp:
			if "retime" not in m:
				continue
			last = m
		else: #current > temp
			last = m
			temp = current
	return last, None

def LastPlate(project, seq, shot, types):
	"""
	프로젝트, 시퀀스, 샷을 받아 가장 높은 버전의 plate를 반환합니다.
	"""
	platePath = "/show/%s/seq/%s/%s_%s/plate" % (project,seq,seq,shot)
	if not os.path.exists(platePath):
		return None, "%s 경로가 존재하지 않습니다." % platePath
	case1 = glob.glob(platePath + "/" + types)
	case2 = glob.glob(platePath + "/" + types + "[1-9]")
	case3 = glob.glob(platePath + "/" + types + "[1-9][0-9]")
	case4 = glob.glob(platePath + "/" + types + "_retime")
	case5 = glob.glob(platePath + "/" + types + "[1-9]_retime")
	case6 = glob.glob(platePath + "/" + types + "[1-9][0-9]_retime")
	files = case1 + case2 + case3 + case4 + case5 + case6
	if not files:
		return None, "%s plate가 존재하지 않습니다."%types
	temp = 0
	last = ""
	for f in files:
		current = int(filter(str.isdigit, f))
		if current < temp:
			continue
		elif current == temp:
			if "retime" not in f:
				continue
			last = f
		else:
			last = f
			temp = current
	return last, None

if __name__== "__main__":
	result, err = PlateMov("TEMP","SCX", "0010", "org")
	print result, err
