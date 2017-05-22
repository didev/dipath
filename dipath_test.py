#!/usr/bin/env python
#coding:utf-8
import unittest
from dipath import *

class Test_dipath(unittest.TestCase):
	def test_Project(self):
		self.assertEqual(Project("/show/TEMP/seq"), ("TEMP",None))
		self.assertEqual(Project("/lustre3/show/TEMP/seq"), ("TEMP",None))
		self.assertEqual(Project("/lustre2/show/TEMP/seq"), ("TEMP",None))
		self.assertEqual(Project("/lustre/show/TEMP/seq"), ("TEMP",None))
		self.assertEqual(Project("/lustre/show/TEMP/seq"), ("TEMP",None))
		self.assertEqual(Project("//10.0.200.101/lustre/show_TEMP/seq"), ("TEMP",None))
		self.assertEqual(Project("\\\\10.0.200.101\\lustre\\show_TEMP\\seq"), ("TEMP",None))
		self.assertEqual(Project("\\\\10.0.200.101\\lustre2\\show_TEMP\\seq"), ("TEMP",None))
		self.assertEqual(Project("\\\\10.0.200.101\\lustre3\\show_TEMP\\seq"), ("TEMP",None))
		self.assertEqual(Project("//10.0.200.101/lustr2/show_TEMP/seq"), ("TEMP",None))
		self.assertEqual(Project("//10.0.200.101/lustre3/show_TEMP/seq"), ("TEMP",None))
		self.assertEqual(Project("/fxdata/cache/show/TEMP/seq"), ("TEMP",None))
		self.assertEqual(Project("/backup/2016/TEMP/org_fin"), ("TEMP",None))
		self.assertEqual(Project("/lustre/INHouse/CentOS/bin"), ("","경로에서 프로젝트를 가지고 올 수 없습니다."))

	def test_Shot(self):
		self.assertEqual(Shot("A0000_SS_0010_comp_v01"), ("SS_0010",None)) # 롤넘버가 존재하는 형태
		self.assertEqual(Shot("A0000_SS_0010_v01"), ("SS_0010",None)) # 롤넘버가 존재하는 형태
		self.assertEqual(Shot("SS_0010_v01"), ("SS_0010",None))
		self.assertEqual(Shot("SS_0010"), ("SS_0010",None))
		self.assertEqual(Shot("R1VFX_sh033_comp_v01"), ("R1VFX_sh033",None))
		self.assertEqual(Shot("/show/TEMP/seq/R1VFX/R1VFX_sh033/comp/dev/R1VFX_sh033_comp_v01"), ("R1VFX_sh033",None)) # 상위경로는 파이프라인툴로 제작된다. 하위보다는 상위경로를 더 신뢰하도록 한다.
		self.assertEqual(Shot("/show/TEMP/product/out/confirm/170522/R1VFX_sh033_comp_v01"), ("R1VFX_sh033",None))
		self.assertEqual(Shot("SS_0010_00_previz_v001.mov"), ("SS_0010",None))
		self.assertEqual(Shot("SDF"), ("","샷이름을 추출할 수 없습니다."))

if __name__ == "__main__":
	unittest.main()
