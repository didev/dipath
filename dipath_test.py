#!/usr/bin/env python
#coding:utf-8
import unittest
from dipath import *

class Test_dipath(unittest.TestCase):
	def test_Project(self):
		self.assertEqual(Project("/show/TEMP"), ("TEMP",None))
		self.assertEqual(Project("/lustre3/show/TEMP/seq"), ("TEMP",None))
		self.assertEqual(Project("/lustre2/show/TEMP/seq"), ("TEMP",None))
		self.assertEqual(Project("/lustre/show/TEMP/seq"), ("TEMP",None))
		self.assertEqual(Project("//10.0.200.101/lustre/show_TEMP/seq"), ("TEMP",None))
		self.assertEqual(Project("\\\\10.0.200.101\\lustre\\show_TEMP\\seq"), ("TEMP",None))
		self.assertEqual(Project("\\\\10.0.200.101\\lustre2\\show_TEMP\\seq"), ("TEMP",None))
		self.assertEqual(Project("\\\\10.0.200.101\\lustre3\\show_TEMP\\seq"), ("TEMP",None))
		self.assertEqual(Project("//10.0.200.101/lustr2/show_TEMP/seq"), ("TEMP",None))
		self.assertEqual(Project("//10.0.200.101/lustre3/show_TEMP/seq"), ("TEMP",None))
		self.assertEqual(Project("//10.0.200.100/show_TEMP/seq"), ("TEMP",None))
		self.assertEqual(Project("\\\\10.0.200.100\\show_TEMP\\seq"), ("TEMP",None))
		self.assertEqual(Project("/fxdata/cache/show/TEMP/seq"), ("TEMP",None))
		self.assertEqual(Project("/backup/2016/TEMP/org_fin"), ("TEMP",None))
		self.assertEqual(Project("/lustre/INHouse/CentOS/bin"), ("","경로에서 프로젝트를 가지고 올 수 없습니다."))

	def test_Seq(self):
		self.assertEqual(Seq("/show/TEMP/seq/SS"), ("SS",None))
		self.assertEqual(Seq("/lustre3/show/TEMP/seq/SS/"), ("SS",None))
		self.assertEqual(Seq("/lustre2/show/TEMP/seq/BNS/"), ("BNS",None))
		self.assertEqual(Seq("/lustre/show/TEMP/seq/BNS/"), ("BNS",None))
		self.assertEqual(Seq("//10.0.200.101/lustre/show_TEMP/seq/SS/"), ("SS",None))
		self.assertEqual(Seq("/lustre/INHouse/CentOS/bin"), ("","경로에서 시퀀스를 가지고 올 수 없습니다."))

	def test_Shot(self):
		self.assertEqual(Shot("/show/TEMP/seq/S001/S001_0010"), ("0010",None))
		self.assertEqual(Shot("/lustre3/show/TEMP/seq/SS/SS_0040/"), ("0040",None))
		self.assertEqual(Shot("/lustre2/show/TEMP/seq/BNS/BNS_0060"), ("0060",None))
		self.assertEqual(Shot("/lustre/show/TEMP/seq/BNS/Bns_0060/comp"), ("0060",None))
		self.assertEqual(Shot("//10.0.200.101/lustre/show_TEMP/seq/SS/SS_0070/comp/dev"), ("0070",None))
		self.assertEqual(Shot("/lustre/INHouse/CentOS/bin"), ("","경로에서 샷을 가지고 올 수 없습니다."))

	def test_Task(self):
		self.assertEqual(Task("/show/TEMP/seq/S001/S001_0010/comp"), ("","경로에서 Task를 가지고 올 수 없습니다."))
		self.assertEqual(Task("/show/mrsunshine/assets/char/crow/lookdev/dev"), ("lookdev",None))
		self.assertEqual(Task("/lustre3/show/TEMP/seq/SS/SS_0040/ani/dev"), ("ani",None))
		self.assertEqual(Task("/lustre3/show/TEMP/seq/SS/SS_0040/ani/pub/preview/SS_0040_ani_v04"), ("ani",None))
		self.assertEqual(Task("/show/TEMP/seq/SS/SS_0010/ani/dev/hongjoo/preview"), ("ani",None))

	def test_ShotFromBaseName(self):
		self.assertEqual(ShotFromBaseName("A0000_SS_0010_comp_v01"), ("SS_0010",None)) # 롤넘버가 존재하는 형태
		self.assertEqual(ShotFromBaseName("A0000_SS_0010_v01"), ("SS_0010",None)) # 롤넘버가 존재하는 형태
		self.assertEqual(ShotFromBaseName("A000_SS_0010_v01"), ("SS_0010",None)) # 롤넘버형식이 아닌 포멧을 일부러 추가함.
		self.assertEqual(ShotFromBaseName("SS_0010_v01"), ("SS_0010",None))
		self.assertEqual(ShotFromBaseName("SS_0010"), ("SS_0010",None))
		self.assertEqual(ShotFromBaseName("R1VFX_sh033_comp_v01"), ("R1VFX_sh033",None))
		self.assertEqual(ShotFromBaseName("JYN_1640_comp_L_v01"), ("JYN_1640",None))
		self.assertEqual(ShotFromBaseName("JYN_1640_comp_left_v01"), ("JYN_1640",None))
		self.assertEqual(ShotFromBaseName("/show/TEMP/seq/R1VFX/R1VFX_sh033/comp/dev/R1VFX_sh033_comp_v01"), ("R1VFX_sh033",None)) # 상위경로는 파이프라인툴로 제작된다. 하위보다는 상위경로를 더 신뢰하도록 한다.
		self.assertEqual(ShotFromBaseName("/show/TEMP/product/out/confirm/170522/R1VFX_sh033_comp_v01"), ("R1VFX_sh033",None))
		self.assertEqual(ShotFromBaseName("SS_0010_00_previz_v001.mov"), ("SS_0010",None))
		self.assertEqual(ShotFromBaseName("thesea2_SS_0010_00_previz_v001.mov"), ("SS_0010",None))
		self.assertEqual(ShotFromBaseName("SDF"), ("","파일 경로에서 샷을 가지고 올 수 없습니다."))
	
	def test_Seqnum(self):
		self.assertEqual(Seqnum("SS_0010_comp_v01.1036.dpx"), (1036,None))
		self.assertEqual(Seqnum("SS_0010_comp1036.dpx"), (1036,None))
		self.assertEqual(Seqnum("/show/test/SS_0010_comp_v01.1036.dpx"), (1036,None))
		self.assertEqual(Seqnum("/show/test/SS_0010_comp1036.dpx"), (1036,None))
		self.assertEqual(Seqnum("/show/test/SS_0010_comp_motion1036.dpx"), (1036,None))	
		self.assertEqual(Seqnum("/show/test/SS_0010_v01.dddd.dpx"), (-1,"시퀀스 파일이 아닙니다."))
		self.assertEqual(Seqnum("SS_0010_comp_v01.1036...dpx"), (-1,"시퀀스 파일이 아닙니다."))
		self.assertEqual(Seqnum(""), (-1,"시퀀스 파일이 아닙니다."))

	def test_Vernum(self):
		self.assertEqual(Vernum("SS_0010_ani_v01_w02.mb"), (1,2,None))
		self.assertEqual(Vernum("SS_0010_ani_V01_w02.mb"), (1,2,None))
		self.assertEqual(Vernum("SS_0010_ani_v001_w002.mb"), (1,2,None))
		self.assertEqual(Vernum("SS_0010_comp_v01.0001.jpg"), (1,-1,None))
		self.assertEqual(Vernum("SS_0010_comp_V01.0001.jpg"), (1,-1,None))
		self.assertEqual(Vernum("SS_0010_comp_vvv.0001.jpg"), (-1,-1,"버전 정보를 가지고 올 수 없습니다."))
		self.assertEqual(Vernum("SS_0010_ani_v001_www.mb"), (1,-1,None))
		self.assertEqual(Vernum(""), (-1,-1,"버전 정보를 가지고 올 수 없습니다."))

	def test_Lin2win(self):
		self.assertEqual(Lin2win("/show/habaek/seq/SS/SS_0010"), "//10.0.200.100/show_habaek/seq/SS/SS_0010")
		self.assertEqual(Lin2win("/lustre/show/habaek/seq/SS/SS_0010"), "//10.0.200.100/show_habaek/seq/SS/SS_0010")
		self.assertEqual(Lin2win("/lustre2/show/habaek/seq/SS/SS_0010"), "//10.0.200.100/show_habaek/seq/SS/SS_0010")
		self.assertEqual(Lin2win("/lustre3/show/habaek/seq/SS/SS_0010"), "//10.0.200.100/show_habaek/seq/SS/SS_0010")
		self.assertEqual(Lin2win("/clib/src/src1422934591789"), "//10.0.200.100/clib/src/src1422934591789")
		self.assertEqual(Lin2win("/backup/2009"), "//10.0.200.100/_IDEA_BackUP/2009")
		self.assertEqual(Lin2win("/lustre/INHouse/nukedev/lut/AlexaV3_K1S1_LogC2Video_Rec709_EE_nuke3d.cube"), "//10.0.200.100/_lustre_INHouse/nukedev/lut/AlexaV3_K1S1_LogC2Video_Rec709_EE_nuke3d.cube")
		self.assertEqual(Lin2win("aa"), "aa")

	def test_Rmlustre(self):
		self.assertEqual(Rmlustre("/lustre/show/habaek/seq"), "/show/habaek/seq")
		self.assertEqual(Rmlustre("/lustre2/show/habaek/seq"), "/show/habaek/seq")
		self.assertEqual(Rmlustre("/lustre3/show/habaek/seq"), "/show/habaek/seq")
		self.assertEqual(Rmlustre("/show/habaek/seq"), "/show/habaek/seq")

	def test_ToNetapp(self):
		self.assertEqual(ToNetapp("/lustre/show/habaek/seq"), ("/netapp/show/habaek/seq",None))
		self.assertEqual(ToNetapp("/show/habaek/seq"), ("/netapp/show/habaek/seq",None))
		self.assertEqual(ToNetapp("/lustre3/show/habaek/seq"), ("/netapp/show/habaek/seq",None))
		self.assertEqual(ToNetapp("/home/d10191/test"), ("/home/d10191/test","netapp 경로로 바꿀 수 없습니다."))

	def test_Rnum(self):
		self.assertEqual(Rnum("/show/TEMP/seq/S001/A0000_S001_0010"), ("A0000", None))
		self.assertEqual(Rnum("A0000_SS_0010_comp_v01"), ("A0000", None)) # 롤넘버가 존재하는 형태
		self.assertEqual(Rnum("A0000_SS_0010_v01"), ("A0000", None)) # 롤넘버가 존재하는 형태
		self.assertEqual(Rnum("SS_0010_v01"), ("", "파일 경로에서 롤넘버를 가지고 올 수 없습니다."))


if __name__ == "__main__":
	unittest.main()
