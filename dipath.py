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
