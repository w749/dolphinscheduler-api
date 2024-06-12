#!/bin/bash

# 实例列表
# 实例重跑/停止
# 任务列表
# 任务重跑


DIR_PATH=$(cd $(dirname $0);pwd)

function help() {
    echo "USAGE: instance.sh [OPTIONS]"
    echo "Process Instance options, OPTIONS is one of:"
    echo "    list [PROCESS_CODE]           get instance list, default get all process instance, can gets instance list for PROCESS_CODE"
    echo "    tasks INSTANCE_ID             get instance tasks for INSTANCE_ID, run [bin/instance.sh list] get it"
    echo "    rerun INSTANCE_ID             rerun instance for INSTANCE_ID, run [bin/instance.sh list] get it"
    echo "    failure INSTANCE_ID           run failure tasks for INSTANCE_ID, run [bin/instance.sh list] get it"
    echo "    stop INSTANCE_ID              stop instance for INSTANCE_ID, run [bin/instance.sh list] get it"
    echo "    task INSTANCE_ID TASK_CODE    rerun single task for INSTANCE_ID AND TASK_CODE, run [bin/instance.sh tasks INSTANCE_ID] get TASK_CODE"
    exit 0
}

function get_instance_id() {
    if [ $# -ge 2 ];then
      instance_id="--id ${2}"
    else
      help
    fi
}

case $1 in
  "list")
    if [ $# -ge 2 ];then
      process_code="--process-code ${2}"
    fi
    commands="python ${DIR_PATH}/../main.py --instance list ${process_code}"
    echo ${commands}
    eval ${commands}
    ;;
  "tasks")
    get_instance_id $@
    commands="python ${DIR_PATH}/../main.py --instance tasks ${instance_id}"
    echo ${commands}
    eval ${commands}
    ;;
  "rerun")
    get_instance_id $@
    commands="python ${DIR_PATH}/../main.py --instance instance ${instance_id} --type 1"
    echo ${commands}
    eval ${commands}
    ;;
  "failure")
    get_instance_id $@
    commands="python ${DIR_PATH}/../main.py --instance instance ${instance_id} --type 2"
    echo ${commands}
    eval ${commands}
    ;;
  "stop")
    get_instance_id $@
    commands="python ${DIR_PATH}/../main.py --instance instance ${instance_id} --type 3"
    echo ${commands}
    eval ${commands}
    ;;
  "task")
    get_instance_id $@
    if [ $# -ge 3 ];then
      task_code="--code ${3}"
    else
      help
    fi
    commands="python ${DIR_PATH}/../main.py --instance run ${instance_id} ${task_code}"
    echo ${commands}
    eval ${commands}
    ;;
  *)
    help
    ;;
esac
