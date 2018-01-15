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

// Project 함수는 경로를 받아서 프로젝트 이름을 반환한다.
func Project(path string) (string, error) {
	if path == "" {
		return path, errors.New("빈 문자열 입니다.")
	}
	p := strings.Replace(path, "\\", "/", -1)
	regRule := `/show[/_](\S[^/]+)`
	if strings.HasPrefix(p, "/backup/") {
		regRule = `/backup/\d+?/(\S[^/]+)`
	}
	re, err := regexp.Compile(regRule)
	if err != nil {
		return "", err
	}

	results := re.FindStringSubmatch(p)
	if results == nil {
		return "", errors.New(path + " 경로에서 프로젝트 정보를 가지고 올 수 없습니다.")
	}
	return results[len(results)-1], nil
}

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
	} else if strings.HasPrefix(path, "/lustre") { // lustre, lustre2, lustre3, lustre4 로 시작할 때..
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
	} else if strings.HasPrefix(path, "/lustre4/show") {
		return "\\\\10.0.200.100\\show_" + strings.Replace(path[14:], "/", "\\", len(path[14:]))
	} else {
		return path
	}
}

// 웹에서 파일을 드레그시 붙는 file:// 형태의 프로토콜 문자열을 제거한다.
func RmProtocol(path string) string {
	prefix := []string{"file://", "http://", "ftp://"}
	for _, p := range prefix {
		if strings.HasPrefix(path, p) {
			return path[len(p):]
		}
	}
	return path
}

//경로를 받아서 시퀀스넘버를 반환한다.
//만약 리턴할 시컨스넘버가 없으면 -1과 에러를 반환한다.
func Seqnum(path string) (int, error) {
	re, err := regexp.Compile("([0-9]+)\\.[a-zA-Z]+$")
	if err != nil {
		return -1, errors.New("정규 표현식이 잘못되었습니다.")
	}

	//예를 들어 "SS_0010_comp_v01.0001.jpg"값이 들어오면
	//results리스트는 다음값을 가집니다. [0]:"0001.jpg", [1]:"0001"
	results := re.FindStringSubmatch(path)
	if results == nil {
		return -1, errors.New("시퀀스 파일이 아닙니다.")
	}
	seq := results[1]
	seqNum, err := strconv.Atoi(seq)
	if err != nil {
		return -1, errors.New("시퀀스 파일이 아닙니다")
	}
	return seqNum, nil
}

//파일을 받아서 파일 버젼과 서브버전을   반환한다.
//만약 리턴할 버전과 서브버전이  없으면 -1과 에러를 반환한다.
func Vernum(path string) (int, int, error) {
	re, err := regexp.Compile(`_[vV]([0-9]+)(_[wW]([0-9]+))*`)
	if err != nil {
		return -1, -1, errors.New("레귤러 익스프레션이 잘못되었습니다.")
	}

	//예를 들어 "S_0010_ani_v01_w02.mb"값이 들어오면
	//results리스트는 다음값을 가집니다. [0]:"v01_w02.mb", [1]:"01", [3]:"02"
	results := re.FindStringSubmatch(path)
	if results == nil {
		return -1, -1, errors.New("버전 정보를 가지고 올 수 없습니다.")
	}
	verNum, err := strconv.Atoi(results[1])
	if err != nil {
		return -1, -1, errors.New("버전 정보를 가지고 올 수 없습니다.")
	}
	//버전은 값이 있고 서브버전에 값이 없다면 -1을 반환
	subNum, err := strconv.Atoi(results[3])
	if err != nil {
		subNum = -1
	}

	return verNum, subNum, nil
}

// Ideapath함수는 입력받은 경로가 idea 소유주, idea 그룹, 0775권한을 가지도록 설정한다.
// 이 권한은 전 사원이 읽고 쓸 수 있는 권한을 가지게된다.
func Ideapath(path string) error {
	err := os.Chmod(path, 0775)
	if err != nil {
		return err
	}
	err = os.Chown(path, 500, 500)
	if err != nil {
		return err
	}
	return nil
}

// Safepath 함수는 입력받은 경로가 idea 소유주, idea 그룹, 555권한을 가지도록 설정한다.
// 이 권한은 전 사원이 읽고 실행만 가능하다. 삼바서버에서 마우스 드레그사고를 방지한다.
// 회사는 seq 폴더를 이 권한으로 설정하고 폴더권한을 보호한다.
func Safepath(path string) error {
	err := os.Chmod(path, 0555)
	if err != nil {
		return err
	}
	err = os.Chown(path, 500, 500)
	if err != nil {
		return err
	}
	return nil
}

// Seq 함수는 경로를 받아서 시퀀스를 반환한다.
func Seq(path string) (string, error) {
	if path == "" {
		return path, errors.New("빈 문자열 입니다.")
	}
	p := strings.Replace(path, "\\", "/", -1)
	regRule := `/show[/_]\S+?/seq/(\S[^/]+)`
	if strings.HasPrefix(p, "/backup/") {
		regRule = `/backup/\d+?/\S+?/\S+?/seq/(\S[^/]+)`
	}
	re, err := regexp.Compile(regRule)
	if err != nil {
		return "", err
	}
	results := re.FindStringSubmatch(p)
	if results == nil {
		return "", errors.New(path + " 경로에서 시퀀스 정보를 가지고 올 수 없습니다.")
	}
	return results[len(results)-1], nil
}

// Shot 함수는 경로를 받아서 샷을 반환한다.
func Shot(path string) (string, error) {
	if path == "" {
		return path, errors.New("빈 문자열 입니다.")
	}
	p := strings.Replace(path, "\\", "/", -1)
	regRule := `/show[/_]\S+?/seq/\S+?/\S+?_(\S[^/]+)`
	if strings.HasPrefix(p, "/backup/") {
		regRule = `/backup/\d+?/\S+?/\S+?/seq/\S+?/\S+?_(\S[^/]+)`
	}
	re, err := regexp.Compile(regRule)
	if err != nil {
		return "", err
	}
	results := re.FindStringSubmatch(p)
	if results == nil {
		return "", errors.New(path + " 경로에서 샷 정보를 가지고 올 수 없습니다.")
	}
	return results[len(results)-1], nil
}
