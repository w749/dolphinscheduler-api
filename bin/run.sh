#!/bin/bash

# 补数

DIR_PATH=$(cd $(dirname $0);pwd)

function help() {
    echo "USAGE: run.sh [CODE] [START_TIME] [END_TIME] [TENANT]"
    echo "Complement Data options, OPTIONS is:"
    echo "    CODE           require         process code, run [bin/process.sh list] get it"
    echo "    START_TIME     default now     complement data start time, need use quotation marks, eg: '2024-05-01 00:00:00'"
    echo "    END_TIME       default now     complement data end time, need use quotation marks, eg: '2024-05-01 00:00:00'"
    echo "    TENANT         default hdfs    complement data tenant"
    exit 0
}
if [ $# -ge 1 ];then
  code=$1
  if [ $# -ge 2 ];then
    start_time="--start '${2}'"
  fi
  if [ $# -ge 3 ];then
    end_time="--end '${3}'"
  fi
  if [ $# -ge 4 ];then
    tenant="--tenant-code ${4}"
  fi
  commands="python ${DIR_PATH}/../main.py --run -c ${code} ${start_time} ${end_time} ${tenant}"
  echo ${commands}
  eval ${commands}
else
  help
fi
