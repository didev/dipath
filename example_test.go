// 이 문서는 godoc 자동 생성시 예제로 추가되는 파일이다.
package dipath_test

import (
	"github.com/didev/dipath"
	"fmt"
)

func ExampleLin2win() {
	fmt.Println(dipath.Lin2win("/show/TEMP/tmp"))
	// Output: \\10.0.200.100\show_TEMP\tmp
}

func ExampleWin2lin() {
	fmt.Println(dipath.Win2lin("\\\\10.0.200.100\\show_TEMP\\tmp"))
	// Output: /show/TEMP/tmp
}
