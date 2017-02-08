#coding:utf8

def GetProject(path):
	"""
	경로를 받아서 프로젝트 문자열을 리턴한다.
	만약 리턴할 프로젝트 문자열이 없으면 ""를 리턴한다.

	아래는 예상패턴이다. 사용자가 가장 많이 사용하는 순서이다.
	/show/{{project}}/seq
	/lustre3/show/{{project}}/seq
	/lustre/show/{{project}}/seq
	/lustre2/show/{{project}}/seq
	\\\\10.0.200.100\\show_{{project}}\\seq
	//10.0.200.100/show_{{project}}/seq
	/fxdata/cache/show/{{project}}/seq
	/backup/2016/{{project}}/org_fin
	\\\\10.0.200.101\\lustre_show\\{{project}}\\seq
	\\\\10.0.200.101\\lustre2_show\\{{project}}\\seq
	\\\\10.0.200.101\\lustre3_show\\{{project}}\\seq
	//10.0.200.101/lustre_show/{{project}}/seq
	//10.0.200.101/lustre2_show/{{project}}/seq
	//10.0.200.101/lustre3_show/{{project}}/seq
	"""
	pass


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
