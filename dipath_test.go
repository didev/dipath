package dipath_test

import (
	"di/dipath"
	"testing"
)

type testpair struct {
	values string
	result string
}

var tests_lin2win = []testpair{
	{"/lustre2/Digitalidea_source/flib/ai/14", "\\\\10.0.200.100\\lustre_Digitalidea_source\\flib\\ai\\14"},
	{"/lustre/Digitalidea_source/flib/ai/14", "\\\\10.0.200.100\\lustre_Digitalidea_source\\flib\\ai\\14"},
	{"/show/ghost/seq", "\\\\10.0.200.100\\show_ghost\\seq"},
	{"/lustre/show/ghost/seq", "\\\\10.0.200.100\\show_ghost\\seq"},
	{"/lustre2/show/ghost/seq", "\\\\10.0.200.100\\show_ghost\\seq"},
	{"/lustre2/show/ghost/seq", "\\\\10.0.200.100\\show_ghost\\seq"},
	{"/lustre3/show/ghost/seq", "\\\\10.0.200.100\\show_ghost\\seq"},
	{"/lustre2/Marketing/2015Brochure/Creature/0911_confirm", "/lustre2/Marketing/2015Brochure/Creature/0911_confirm"}, //마운트포인트가 없음.
}

var tests_win2lin = []testpair{
	{"\\\\10.0.200.100\\lustre_Digitalidea_source\\flib\\ai\\14", "/lustre2/Digitalidea_source/flib/ai/14"},
	{"\\\\10.0.200.100\\show_ghost\\seq", "/show/ghost/seq"},
	{"\\\\10.0.200.100\\show_ghost\\seq", "/show/ghost/seq"},
	{"\\\\10.0.200.100\\show_ghost\\seq", "/show/ghost/seq"},
	{"\\\\10.0.200.100\\show_ghost\\seq", "/show/ghost/seq"},
	{"/lustre2/Marketing/2015Brochure/Creature/0911_confirm", "/lustre2/Marketing/2015Brochure/Creature/0911_confirm"}, //마운트포인트가 없음.
	{"/lustre3/show/TEMP/tmp", "/lustre3/show/TEMP/tmp"},                                                               //마운트포인트가 없음.
}

func Test_lin2win(t *testing.T) {
	for _, pair := range tests_lin2win {
		v := dipath.Lin2win(pair.values)
		if pair.result != v {
			t.Error(
				"\n",
				"입력값:", pair.values, "\n",
				"예상값:", pair.result, "\n",
				"연산값:", v, "\n",
			)
		}
	}
}

func Test_win2lin(t *testing.T) {
	for _, pair := range tests_win2lin {
		v := dipath.Win2lin(pair.values)
		if pair.result != v {
			t.Error(
				"\n",
				"입력값:", pair.values, "\n",
				"예상값:", pair.result, "\n",
				"연산값:", v, "\n",
			)
		}
	}
}

func Test_RmFileProtocol(t *testing.T) {
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
		in:   "file://\\\\10.0.200.100\\show_test",
		want: "\\\\10.0.200.100\\show_test",
	}}
	for _, c := range cases {
		got := dipath.RmFileProtocol(c.in)
		if dipath.RmFileProtocol(c.in) != c.want {
			t.Fatalf("RmFileProtocol(%v): 얻은 값 %v, 원하는 값 %v", c.in, got, c.want)
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
			t.Fatalf("SeqNumber(%w): 얻은 값 %w, 원하는 값 %w", c.in, got, c.want)
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
			t.Fatalf("SeqNumber(%w): 얻은 값 %w, 원하는 값 %w", c.in, got, c.want)
		} else if subgot != c.subwant {
			t.Fatalf("SeqNumber(%w): 얻은 값 %w, 원하는 값 %w", c.in, subgot, c.subwant)
		}
	}
}
