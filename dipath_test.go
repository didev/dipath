package dipath_test

import (
	"di/dipath"
	"errors"
	"testing"
)

func Test_Lin2win(t *testing.T) {
	cases := []struct {
		in   string
		want string
	}{{
		in:   "/lustre2/Digitalidea_source/flib/ai/14",
		want: "\\\\10.0.200.100\\lustre_Digitalidea_source\\flib\\ai\\14",
	}, {
		in:   "/lustre/Digitalidea_source/flib/ai/14",
		want: "\\\\10.0.200.100\\lustre_Digitalidea_source\\flib\\ai\\14",
	}, {
		in:   "/show/ghost/seq",
		want: "\\\\10.0.200.100\\show_ghost\\seq",
	}, {
		in:   "/lustre/show/ghost/seq",
		want: "\\\\10.0.200.100\\show_ghost\\seq",
	}, {
		in:   "/lustre4/show/thesea2/seq",
		want: "\\\\10.0.200.100\\show_thesea2\\seq",
	}, {
		in:   "/lustre2/Marketing/2015Brochure/Creature/0911_confirm",
		want: "/lustre2/Marketing/2015Brochure/Creature/0911_confirm",
	}}
	for _, c := range cases {
		got := dipath.Lin2win(c.in)
		if got != c.want {
			t.Fatalf("Win2lin(%v): 얻은 값 %v, 원하는 값 %v", c.in, got, c.want)
		}
	}
}

func Test_Win2lin(t *testing.T) {
	cases := []struct {
		in   string
		want string
	}{{
		in:   "\\\\10.0.200.100\\lustre_Digitalidea_source\\flib\\ai\\14",
		want: "/lustre2/Digitalidea_source/flib/ai/14",
	}, {
		in:   "\\\\10.0.200.100\\show_ghost\\seq",
		want: "/show/ghost/seq",
	}, {
		in:   "/lustre2/Marketing/2015Brochure/Creature/0911_confirm",
		want: "/lustre2/Marketing/2015Brochure/Creature/0911_confirm",
	}, {
		in:   "/lustre3/show/TEMP/tmp",
		want: "/lustre3/show/TEMP/tmp",
	}}
	for _, c := range cases {
		got := dipath.Win2lin(c.in)
		if got != c.want {
			t.Fatalf("Win2lin(%v): 얻은 값 %v, 원하는 값 %v", c.in, got, c.want)
		}
	}
}

func Test_RmProtocol(t *testing.T) {
	cases := []struct {
		in   string
		want string
	}{{
		in:   "",
		want: "",
	}, {
		in:   "file:///show/test",
		want: "/show/test",
	}, {
		in:   "http:///show/test",
		want: "/show/test",
	}, {
		in:   "ftp:///show/test",
		want: "/show/test",
	}, {
		in:   "file://\\\\10.0.200.100\\show_test",
		want: "\\\\10.0.200.100\\show_test",
	}}
	for _, c := range cases {
		got := dipath.RmProtocol(c.in)
		if got != c.want {
			t.Fatalf("RmProtocol(%v): 얻은 값 %v, 원하는 값 %v", c.in, got, c.want)
		}
	}
}

func Test_Project(t *testing.T) {
	cases := []struct {
		in   string
		want string
	}{{
		in:   "",
		want: "",
	}, {
		in:   "/show/TEMP",
		want: "TEMP",
	}, {
		in:   "/show/TEMP/test.txt",
		want: "TEMP",
	}, {
		in:   "/lustre3/show/TEMP/seq",
		want: "TEMP",
	}, {
		in:   "/lustre3/show/프로젝트/seq",
		want: "프로젝트",
	}, {
		in:   "/lustre3/show/项目/seq",
		want: "项目",
	}, {
		in:   "/lustre3/show/プロジェクト/seq",
		want: "プロジェクト",
	}, {
		in:   "/lustre2/show/TEMP/seq",
		want: "TEMP",
	}, {
		in:   "//10.0.200.101/lustre/show_TEMP/seq",
		want: "TEMP",
	}, {
		in:   "\\\\10.0.200.101\\lustre3\\show_TEMP\\seq",
		want: "TEMP",
	}, {
		in:   "//10.0.200.100/show_TEMP/seq01",
		want: "TEMP",
	}, {
		in:   "/fxdata/cache/show/TEMP/seq",
		want: "TEMP",
	}, {
		in:   "/backup/2016/TEMP/org_fin",
		want: "TEMP",
	}, {
		in:   "/lustre2/show/TEMP/seq",
		want: "TEMP",
	}, {
		in:   "file:///show/test/",
		want: "test",
	}, {
		in:   "http://10.0.90.98/show/test/",
		want: "test",
	}, {
		in:   "http://10.0.90.98/test/",
		want: "",
	}, {
		in:   "file://\\\\10.0.200.100\\show_test\\",
		want: "test",
	}}
	for _, c := range cases {
		got, _ := dipath.Project(c.in)
		if got != c.want {
			t.Fatalf("Project(%v): 얻은 값 %v, 원하는 값 %v", c.in, got, c.want)
		}
	}
}

func Test_Seqnum(t *testing.T) {
	cases := []struct {
		in   string
		want int
	}{{
		in:   "",
		want: -1,
	}, {
		in:   "SS_0010_comp_v01.1036.dpx",
		want: 1036,
	}, {
		in:   "SS_0010_comp1036.dpx",
		want: 1036,
	}, {
		in:   "/show/test/SS_0010_comp_v01.1036.dpx",
		want: 1036,
	}, {
		in:   "/show/test/SS_0010_comp1036.dpx",
		want: 1036,
	}, {
		in:   "/show/test/SS_0010_comp_motion1036.dpx",
		want: 1036,
	}, {
		in:   "SS_0010_comp_v01.1036...dpx",
		want: -1,
	}, {
		in:   "/show/test/SS_0010_v01.dddd.dpx",
		want: -1,
	}}
	for _, c := range cases {
		got, _ := dipath.Seqnum(c.in)
		if got != c.want {
			t.Fatalf("SeqNumber(%v): 얻은 값 %v, 원하는 값 %v", c.in, got, c.want)
		}
	}
}

func Test_Vernum(t *testing.T) {
	cases := []struct {
		in      string
		want    int
		subwant int
	}{{
		in:      "",
		want:    -1,
		subwant: -1,
	}, {
		in:      "SS_0010_ani_v01_w02.mb",
		want:    1,
		subwant: 2,
	}, {
		in:      "SS_0010_ani_V01_w02.mb",
		want:    1,
		subwant: 2,
	}, {
		in:      "SS_0010_ani_v001_w002.mb",
		want:    1,
		subwant: 2,
	}, {
		in:      "SS_0010_comp_v01.0001.jpg",
		want:    1,
		subwant: -1,
	}, {
		in:      "SS_0010_comp_V01.0001.jpg",
		want:    1,
		subwant: -1,
	}, {
		in:      "SS_0010_comp_vvv.0001.jpg",
		want:    -1,
		subwant: -1,
	}, {
		in:      "SS_0010_ani_v001_www.mb",
		want:    1,
		subwant: -1,
	}}
	for _, c := range cases {
		got, subgot, _ := dipath.Vernum(c.in)
		if got != c.want {
			t.Fatalf("Vernum(%v): 얻은 값 %v, 원하는 값 %v", c.in, got, c.want)
		} else if subgot != c.subwant {
			t.Fatalf("vernum(%v): 얻은 값 %v, 원하는 값 %v", c.in, subgot, c.subwant)
		}
	}
}

func Test_Seq(t *testing.T) {
	cases := []struct {
		in   string
		want string
	}{{
		in:   "",
		want: "",
	}, {
		in:   "/show/TEMP/seq/SS",
		want: "SS",
	}, {
		in:   "/show/TEMP/seq/BNS/test.txt",
		want: "BNS",
	}}
	for _, c := range cases {
		got, _ := dipath.Seq(c.in)
		if got != c.want {
			t.Fatalf("Seq(%v): 얻은 값 %v, 원하는 값 %v", c.in, got, c.want)
		}
	}
}

func Test_Shot(t *testing.T) {
	cases := []struct {
		in   string
		want string
	}{{
		in:   "",
		want: "",
	}, {
		in:   "/show/yeomryeok/seq/S001/S001_0010",
		want: "0010",
	}, {
		in:   "/show/yeomryeok/seq/S001/S001_0010/comp/dev/S001_0010_comp_v01.nk",
		want: "0010",
	}}
	for _, c := range cases {
		got, _ := dipath.Shot(c.in)
		if got != c.want {
			t.Fatalf("Seq(%v): 얻은 값 %v, 원하는 값 %v", c.in, got, c.want)
		}
	}
}

func Test_Task(t *testing.T) {
	cases := []struct {
		in   string
		want string
	}{{
		in:   "",
		want: "",
	}, {
		in:   "/show/yeomryeok/seq/S001/S001_0010",
		want: "",
	}, {
		in:   "/show/yeomryeok/seq/S001/S001_0010/comp/dev/S001_0010_comp_v01.nk",
		want: "comp",
	}}
	for _, c := range cases {
		got, _ := dipath.Task(c.in)
		if got != c.want {
			t.Fatalf("Seq(%v): 얻은 값 %v, 원하는 값 %v", c.in, got, c.want)
		}
	}
}

func Test_Element(t *testing.T) {
	cases := []struct {
		in   string
		want string
	}{{
		in:   "",
		want: "",
	}, {
		in:   "/show/yeomryeok/seq/S001/S001_0010/fx/dev/fire",
		want: "fire",
	}, {
		in:   "/show/yeomryeok/seq/S001/S001_0010/fx/dev/S001_0010_fx_v01.nk",
		want: "",
	}, {
		in:   "/show/yeomryeok/seq/S001/S001_0010/fx/dev/smoke",
		want: "smoke",
	}, {
		in:   "/show/yeomryeok/seq/S001/S001_0010/fx/dev/fire/S001_0010_fxsmoke_v01.nk",
		want: "fire",
	}}
	for _, c := range cases {
		got, _ := dipath.Element(c.in)
		if got != c.want {
			t.Fatalf("Seq(%v): 얻은 값 %v, 원하는 값 %v", c.in, got, c.want)
		}
	}
}

func Test_Seqnum2Sharp(t *testing.T) {
	cases := []struct {
		path   string
		result string
		num    int
		err    error
	}{{
		path:   "01김한웅woong漢雄か.0001.jpg",
		result: "01김한웅woong漢雄か.####.jpg",
		num:    1,
		err:    nil,
	}, {
		path:   "01김한웅woong漢雄か0000.jpg",
		result: "01김한웅woong漢雄か####.jpg",
		num:    0,
		err:    nil,
	}, {
		path:   "/show/test/01김한웅woong漢雄か0000.jpg",
		result: "/show/test/01김한웅woong漢雄か####.jpg",
		num:    0,
		err:    nil,
	}, {
		path:   "1.jpg",
		result: "#.jpg",
		num:    1,
		err:    nil,
	}, {
		path:   "a.jpg",
		result: "a.jpg",
		num:    -1,
		err:    errors.New("경로가 시퀀스 형식이 아닙니다."),
	}}
	for _, c := range cases {
		result, num, err := dipath.Seqnum2Sharp(c.path)
		if result != c.result || num != c.num {
			t.Fatalf("toSharp(%v): 얻은 값 %v,%v,%v 원하는 값 %v,%v,%v", c.path, result, num, err, c.result, c.num, c.err)
		}
	}
}
