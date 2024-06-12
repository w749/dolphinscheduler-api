#!/bin/bash

# 创建token
# 初始化DS项目，队列，租户

DIR_PATH=$(cd $(dirname $0);pwd)

case $1 in
  "token")
    python ${DIR_PATH}/../main.py --token -c
    ;;
  "init")
    python ${DIR_PATH}/../main.py --project -c
    python ${DIR_PATH}/../main.py --queue -c
    python ${DIR_PATH}/../main.py --tenant -c
    ;;
  *)
    echo "USAGE: init.sh [OPTIONS]"
    echo "Initialize project, OPTIONS is one of:"
    echo "    token       create token"
    echo "    init        create project,queue,tenant, edit ${DIR_PATH}/../settings.json first."
    exit 0
    ;;
esac
