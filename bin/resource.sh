#!/bin/bash

# 资源列表
# 上传资源
# 更新资源
# 删除资源

DIR_PATH=$(cd $(dirname $0);pwd)

function help() {
    echo "USAGE: resource.sh [OPTIONS]"
    echo "Resource options, OPTIONS is one of:"
    echo "    list                  get resource list"
    echo "    upload FILEPATH       upload resource, FILEPATH is local filepath"
    echo "    update FILENAME       update resource, must upload first, FILENAME is resource name"
    echo "    delete FILENAME       delete resource, FILENAME is resource name"
    exit 0
}

case $1 in
  "list")
    python ${DIR_PATH}/../main.py --resource -l
    ;;
  "upload")
    if [ ! -f "$2" ];then
      help
    fi
    python ${DIR_PATH}/../main.py --resource --upload $2
    ;;
  "update")
    if [ -z "$2" ];then
      help
    fi
    python ${DIR_PATH}/../main.py --resource --update $2
    ;;
  "delete")
    if [ -z "$2" ];then
      help
    fi
    python ${DIR_PATH}/../main.py --resource --delete $2
    ;;
  *)
    help
    ;;
esac
