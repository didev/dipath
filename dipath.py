#coding:utf8
import re
import os

def Project(path):
	"""
	경로를 받아서 프로젝트 문자열과 에러값을 리턴한다.
	만약 리턴할 프로젝트 문자열이 없으면 ""를 리턴한다.
	"""
	# show
	show = re.findall('/show[/_](\S+?)/', path.replace("\\","/"))
	if len(show) == 1:
		return show[0], None
	# backup
	backup = re.findall('/backup/\d+?/(\S+?)/', path.replace("\\","/"))
	if len(backup) == 1:
		return backup[0], None
	return "", "경로에서 프로젝트를 가지고 올 수 없습니다."

def Shot(path):
	"""
	경로를 받아서 샷문자열과 에러값을 리턴한다.
	만약 리턴할 샷이름이 없으면 ""를 리턴한다.
	"""
	hasRnum = re.findall("([ABCDEFGH][0-9]{4})_([a-zA-Z0-9]+)_([a-zA-Z]*[0-9]+)", path)
	if hasRnum: # 롤넘버가 존재할때(최대8권)
		return hasRnum[0][1] + "_" + hasRnum[0][2], None
	hasShot = re.findall("([a-zA-Z0-9]+)_([a-zA-Z]*[0-9]+)", path)
	if hasShot:
		return hasShot[0][0] + "_" + hasShot[0][1], None
	return "", "샷이름을 추출할 수 없습니다."

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
