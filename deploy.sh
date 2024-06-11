#!/bin/bash

# For offline python2.7

function init() {
  DIR_PATH=$(cd $(dirname $0);pwd)
  PYTHON_VERSION=`python -c "import platform; print(platform.python_version())"`
  PACKAGE_PATH=${DIR_PATH}/depend/package
  WHL_PATH=${DIR_PATH}/depend/whl

  if [[ ${PYTHON_VERSION} != "2.7"* ]];then
    echo "Only python2.7 deployment is supported."
    exit -1
  fi
}

function install_package() {
  cd ${PACKAGE_PATH}
  for file in `ls ${PACKAGE_PATH}`
  do
    if [ -f "${file}" ];then
      echo "start install ${PACKAGE_PATH}/${file}"
      if [[ ${file} == *.tar.gz ]];then
        local dir_name=$(tar -tzf "${file}" | head -1 | cut -f1 -d"/")
        if [ ! -d "${dir_name}" ];then
          tar -zxvf "${file}"
        fi
        cd "${dir_name}"
        python setup.py install
        cd -
      elif [[ ${file} == *.zip ]];then
        local dir_name=$(unzip -qql "${file}" | head -1 | awk '{print $4}' | cut -f1 -d"/")
        if [ ! -d "${dir_name}" ];then
          unzip -o "${file}"
          echo "${dir_name} not exits."
        fi
        cd "${dir_name}"
        python setup.py install
        cd -
      else
        echo "Decompression of ${PACKAGE_PATH}/${file} is not supported."
      fi
    fi
  done
}

function install_whl() {
  pip install --no-index --find-links=${WHL_PATH} -r requirements-2.7.txt
}

init
install_package
install_whl
