package dipath_test

import (
	"dipath"
	"testing"
)

type testpair struct {
	values string
	result string
}

var tests_lin2win = []testpair {
	{ "/lustre2/Digitalidea_source/flib/ai/14", "\\\\10.0.200.100\\lustre_Digitalidea_source\\flib\\ai\\14" },
	{ "/lustre/Digitalidea_source/flib/ai/14", "\\\\10.0.200.100\\lustre_Digitalidea_source\\flib\\ai\\14" },
	{ "/show/ghost/seq", "\\\\10.0.200.100\\show_ghost\\seq"},
	{ "/lustre/show/ghost/seq", "\\\\10.0.200.100\\show_ghost\\seq"},
	{ "/lustre2/show/ghost/seq", "\\\\10.0.200.100\\show_ghost\\seq"},
	{ "/lustre2/show/ghost/seq", "\\\\10.0.200.100\\show_ghost\\seq"},
	{ "/lustre2/Marketing/2015Brochure/Creature/0911_confirm", "/lustre2/Marketing/2015Brochure/Creature/0911_confirm"}, //마운트포인트가 없음.
}



var tests_win2lin = []testpair {
	{ "\\\\10.0.200.100\\lustre_Digitalidea_source\\flib\\ai\\14", "/lustre2/Digitalidea_source/flib/ai/14" },
	{ "\\\\10.0.200.100\\show_ghost\\seq", "/show/ghost/seq" },
	{ "\\\\10.0.200.100\\show_ghost\\seq", "/show/ghost/seq" },
	{ "\\\\10.0.200.100\\show_ghost\\seq", "/show/ghost/seq" },
	{ "\\\\10.0.200.100\\show_ghost\\seq", "/show/ghost/seq", },
	{ "/lustre2/Marketing/2015Brochure/Creature/0911_confirm", "/lustre2/Marketing/2015Brochure/Creature/0911_confirm" }, //마운트포인트가 없음.
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
