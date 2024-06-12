#!/bin/bash

# 获取定时列表
# 创建定时任务
# 更新定时任务
# 上线定时任务
# 下线定时任务

DIR_PATH=$(cd $(dirname $0);pwd)

function help() {
    echo "USAGE: scheduler.sh [OPTIONS]"
    echo "Process Definition Scheduler options, OPTIONS is one of:"
    echo "    list                  get scheduler list"
    echo "    create CODE           create scheduler for process, CODE is process code, run [bin/process.sh list] get it"
    echo "                          please modify ${DIR_PATH}/../scheduler.json first, it contains scheduler content"
    echo "    update COED           update scheduler for process, CODE is process code, run [bin/process.sh list] get it."
    echo "                          please modify ${DIR_PATH}/../scheduler.json first, it contains scheduler content"
    echo "    online COED           online scheduler for process, CODE is process code, run [bin/process.sh list] get it"
    echo "    offline COED          offline scheduler for process, CODE is process code, run [bin/process.sh list] get it"
    exit 0
}

case $1 in
  "list")
    python ${DIR_PATH}/../main.py --scheduler -l
    ;;
  "create")
    if [ -z "$2" ];then
      help
    fi
    python ${DIR_PATH}/../main.py --scheduler --create $2
    ;;
  "update")
    if [ -z "$2" ];then
      help
    fi
    python ${DIR_PATH}/../main.py --scheduler --update $2
    ;;
  "online")
    if [ -z "$2" ];then
      help
    fi
    python ${DIR_PATH}/../main.py --scheduler --online $2
    ;;
  "offline")
    if [ -z "$2" ];then
      help
    fi
    python ${DIR_PATH}/../main.py --scheduler --offline $2
    ;;
  *)
    help
    ;;
esac
