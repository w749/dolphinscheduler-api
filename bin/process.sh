#!/bin/bash

# 工作流列表
# 上传工作流
# 下载工作流
# 更新工作流
# 上线工作流
# 下线工作流
# 删除工作流

DIR_PATH=$(cd $(dirname $0);pwd)

function help() {
    echo "USAGE: process.sh [OPTIONS]"
    echo "Process Definition options, OPTIONS is one of:"
    echo "    list                  get process list"
    echo "    import FILEPATH       import process from file, FILEPATH is local json filepath"
    echo "    export COED           export process to file, CODE is process code, run [bin/process.sh list] get it"
    echo "    update FILEPATH       update process from file, FILEPATH is local json filepath, it must be a downloaded json file"
    echo "    online COED           online process, CODE is process code, run [bin/process.sh list] get it"
    echo "    offline COED          offline process, CODE is process code, run [bin/process.sh list] get it"
    echo "    delete COED           delete process, CODE is process code, run [bin/process.sh list] get it"
    exit 0
}

case $1 in
  "list")
    python ${DIR_PATH}/../main.py --process -l
    ;;
  "import")
    if [ ! -f "$2" ];then
      help
    fi
    python ${DIR_PATH}/../main.py --process --import $2
    ;;
  "export")
    if [ -z "$2" ];then
      help
    fi
    python ${DIR_PATH}/../main.py --process --export $2
    ;;
  "update")
    if [ ! -f "$2" ];then
      python ${DIR_PATH}/../main.py --process --update-help
      help
    fi
    python ${DIR_PATH}/../main.py --process --update $2
    ;;
  "online")
    if [ -z "$2" ];then
      help
    fi
    python ${DIR_PATH}/../main.py --process --online $2
    ;;
  "offline")
    if [ -z "$2" ];then
      help
    fi
    python ${DIR_PATH}/../main.py --process --offline $2
    ;;
  "delete")
    if [ -z "$2" ];then
      help
    fi
    python ${DIR_PATH}/../main.py --process --delete $2
    ;;
  *)
    help
    ;;
esac
