package dipath_test

import (
	"fmt"

	"github.com/digital-idea/dipath"
)

func ExampleLin2win() {
	fmt.Println(dipath.Lin2win("/show/TEMP/tmp"))
	// Output: \\10.0.200.100\show_TEMP\tmp
}

func ExampleWin2lin() {
	fmt.Println(dipath.Win2lin("\\\\10.0.200.100\\show_TEMP\\tmp"))
	// Output: /show/TEMP/tmp
}
