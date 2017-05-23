// Package dipath provides filepathAPI for Digitalidea.
//
// Author : kimhanwoong TD.
package dipath

import (
	"errors"
	"io/ioutil"
	"os"
	"regexp"
	"runtime"
	"sort"
	"strconv"
	"strings"
)

//프로젝트경로의 폴더를 문자열 리스트로 가지고 온다.
func Projectlist() []string {
	var dirlist []string
	projectpath := "/show"
	files, _ := ioutil.ReadDir(projectpath)
	for _, f := range files {
		fileInfo, _ := os.Lstat(projectpath + "/" + f.Name())
		if !strings.HasPrefix(f.Name(), ".") && fileInfo.Mode()&os.ModeSymlink == os.ModeSymlink {
			dirlist = append(dirlist, f.Name())
		} else if !strings.HasPrefix(f.Name(), ".") && fileInfo.IsDir() {
			dirlist = append(dirlist, f.Name())
		}
	}
	sort.Strings(dirlist)
	return dirlist
}

//서버의 temp경로를 반환한다.
func TEMP() string {
	switch runtime.GOOS {
	case "windows":
		return "\\\\10.0.200.100\\show_TEMP\\tmp\\"
	case "linux":
		return "/show/TEMP/tmp/"
	case "darwin":
		return "/show/TEMP/tmp/"
	default:
		return "/show/TEMP/tmp/"
	}
}

// 윈도우즈 경로를 리눅스 경로로 바꾼다.
// 만약, 변환되지 않으면 패스를 그대로 출력한다.
func Win2lin(path string) string {
	if strings.HasPrefix(path, "W:\\") {
		return "/show/" + strings.Replace(path[3:], "\\", "/", len(path[3:]))
	} else if strings.HasPrefix(path, "/show/") {
		return path
	} else if strings.HasPrefix(path, "/lustre") || strings.HasPrefix(path, "/lustre2") || strings.HasPrefix(path, "/lustre3") {
		return path
	} else if strings.HasPrefix(path, "\\\\10.0.200.100\\show_") {
		return "/show/" + strings.Replace(path[20:], "\\", "/", len(path[20:]))
	} else if strings.HasPrefix(path, "\\\\10.0.200.100\\lustre_Digitalidea_source\\") {
		return "/lustre2/Digitalidea_source/" + strings.Replace(path[41:], "\\", "/", len(path[41:]))
	} else {
		return path
	}
}

//리눅스 경로를 윈도우즈 경로로 바꾼다.
func Lin2win(path string) string {
	if strings.HasPrefix(path, "/lustre2/Digitalidea_source/flib") { //flib
		return "\\\\10.0.200.100\\lustre_Digitalidea_source\\flib" + strings.Replace(path[32:], "/", "\\", len(path[32:]))
	} else if strings.HasPrefix(path, "/lustre/Digitalidea_source/flib") { //flib
		return "\\\\10.0.200.100\\lustre_Digitalidea_source\\flib" + strings.Replace(path[31:], "/", "\\", len(path[31:]))
	} else if strings.HasPrefix(path, "/show") {
		return "\\\\10.0.200.100\\show_" + strings.Replace(path[6:], "/", "\\", len(path[6:]))
	} else if strings.HasPrefix(path, "/lustre/show") {
		return "\\\\10.0.200.100\\show_" + strings.Replace(path[13:], "/", "\\", len(path[13:]))
	} else if strings.HasPrefix(path, "/lustre2/show") {
		return "\\\\10.0.200.100\\show_" + strings.Replace(path[14:], "/", "\\", len(path[14:]))
	} else if strings.HasPrefix(path, "/lustre3/show") {
		return "\\\\10.0.200.100\\show_" + strings.Replace(path[14:], "/", "\\", len(path[14:]))
	} else {
		return path
	}
}

// 웹에서 파일을 드레그시 간혹 붙는 file:// 문자열을 제거한다.
func RmFileProtocol(path string) string {
	if strings.HasPrefix(path, "file://") {
		return path[7:]
	}
	return path
}

//시퀀스 넘버를 가져오는 함수
func Seqnum(path string) (int, error) {
	re, err := regexp.Compile("([0-9]+)(\\.[a-zA-Z]{3})$")
	if err != nil {
		return -1, errors.New("정규 표현식이 잘못되었습니다.")
	}
	file := re.FindStringSubmatch(path) //[0]: fullName, [1]: 시퀀스, [2]: .확장자
	if file == nil {
		return -1, errors.New("시퀀스 파일이 아닙니다.")
	}
	name := file[1]
	seq := strings.Split(name, ".")[0]
	seqNum, err := strconv.Atoi(seq)
	if err != nil {
		return -1, errors.New("시퀀스 파일이 아닙니다")
	}
	return seqNum, nil
}
