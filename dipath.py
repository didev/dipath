#coding:utf8
import re
import os

def GetProject(path):
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
	return "", "실행경로에서 프로젝트를 인식할 수 없습니다."

def GetSeq(shotname):
	"""
	샷 네임에서 seq 이름을 가지고 온다.

	"""
	pass

def GetShot(shotstring):
	"""
	일반형태 SS_0010_comp_v01, 롤넘버가 붙은 형태 A0010_SS_0010_comp_v01 문자열에서 샷문자 SS_0010 을 반환한다.
	"""
	pass
