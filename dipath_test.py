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

if __name__ == "__main__":
	unittest.main()
