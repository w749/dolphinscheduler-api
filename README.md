- [dolphinscheduler-api](#dolphinscheduler-api)
  - [功能](#功能)
  - [操作说明](#操作说明)
    - [配置文件](#配置文件)
    - [创建token](#创建token)
    - [项目操作](#项目操作)
    - [租户操作](#租户操作)
    - [队列操作](#队列操作)
    - [资源操作](#资源操作)
    - [工作流操作](#工作流操作)
    - [定时任务操作](#定时任务操作)
    - [补数](#补数)
    - [实例操作](#实例操作)

# dolphinscheduler-api
使用python脚本封装dolphinscheduler api，实现在命令行初始化项目，管理、运行作业等等，开发测试版本为Dolphin Scheduler3.2.1版本

## 功能
- 根据admin用户名密码创建token
- 项目创建/删除/查看
- 租户创建/删除/查看
- 队列创建/删除/查看
- 资源创建/更新/删除/查看
- 工作流上传/下载/更新/上下线/删除/查看
- 定时任务创建/更新/上下线
- 补数
- 实例重跑/运行失败任务/停止/获取任务列表/运行单独的任务/查看

## 部署
开发测试使用到了`Python 2.7.5`和`Python 3.11.9`两个版本，其他版本未测试，第三方包分别对应`requirements-2.7.txt`和`requirements.txt`

如果使用Python 3.11.9版本那么执行`pip install -r requirements.txt`安装所需依赖

如果使用Python 2.7.5版本，执行`deploy.sh`离线安装

## 操作说明
bin目录下的shell脚本将常用的ds接口再次封装以便快速操作
### 配置文件
项目下的`settings.json`文件
- username: 用户名，必须是admin
- password: admin密码
- baseUrl: ds api基础url，需要修改ip和端口
- tokenExpireTime: token过期时间，配置一次后不要再次修改
- project: 默认项目
- queue: 默认队列
- tenant: 默认租户
- token: 默认为空，配置其他参数后执行[创建token](#创建token)操作会创建token并赋值
- schedulerFile: 定时任务配置文件，不需要修改

### 创建token
`python main.py --token --create`

创建token命令，根据`settings.json`中的`tokenExpireTime`参数值判断是否存在token，不存在则创建，随后将token赋值给`token`参数

### 项目操作
1. 获取项目列表
    
   `python main.py --project --list`

2. 创建项目

   `python main.py --project --create`
   
   创建`settings.json`配置文件`project`参数对应的项目

3. 删除项目
    
   `python main.py --project --delete PROJECT_NAME`
   
   删除名称为PROJECT_NAME的项目

### 租户操作
1. 获取租户列表
    
   `python main.py --tenant --list`

2. 创建租户

   `python main.py --tenant --create`
   
   创建`settings.json`配置文件`tenant`参数对应的项目

3. 删除租户
    
   `python main.py --tenant --delete TENANT_NAME`
   
   删除名称为TENANT_NAME的租户

### 队列操作
1. 获取队列列表
    
   `python main.py --queue --list`

2. 创建队列

   `python main.py --queue --create`
   
   创建`settings.json`配置文件`queue`参数对应的项目

3. 删除队列
    
   `python main.py --queue --delete QUEUE_NAME`
   
   删除名称为QUEUE_NAME的队列

### 资源操作
1. 获取资源列表
    
   `python main.py --resource --list`

2. 上传资源

   `python main.py --resource --upload FILEPATH`
   
   将本地文件上传到ds资源中心，需提供文件路径FILEPATH，资源名称就是本地文件名称

3. 更新资源
    
   `python main.py --resource --update FILEPATH`
   
   更新资源中心的资源，需提供文件路径FILEPATH，通过本地文件名称确定需要更新的ds资源

4. 删除资源
    
   `python main.py --resource --delete RESOURCE_NAME`
   
   删除名称为RESOURCE_NAME的资源

### 工作流操作
1. 获取工作流列表
    
   `python main.py --process --list`

2. 上传工作流

   `python main.py --process --import FILEPATH`
   
   将本地工作流json文件上传到ds，需提供文件路径FILEPATH

3. 下载工作流
    
   `python main.py --process --export PROCESS_CODE`
   
   下载PROCESS_CODE对应的工作流到本地文件，PROCESS_CODE为工作流列表中的code字段

4. 更新工作流
    
   `python main.py --process --update FILEPATH`
   
   更新工作流，将本地文件FILEPATH中的部分内容更新到ds工作流。需要先下载待更新的工作流到本地文件，在此文件上修改后再执行更新命令。查看更新步骤`python main.py --process --update-help`

5. 上线工作流
    
   `python main.py --process --online PROCESS_CODE`
   
   上线PROCESS_CODE对应的工作流，PROCESS_CODE为工作流列表中的code字段

6. 下线工作流
    
   `python main.py --process --offline PROCESS_CODE`
   
   下线PROCESS_CODE对应的工作流，PROCESS_CODE为工作流列表中的code字段

7. 删除工作流
    
   `python main.py --process --delete PROCESS_CODE`
   
   删除PROCESS_CODE对应的工作流，PROCESS_CODE为工作流列表中的code字段

### 定时任务操作
1. 获取定时任务列表
    
   `python main.py --scheduler --list`

2. 创建定时任务
    
   `python main.py --scheduler --create PROCESS_CODE`
   
   创建PROCESS_CODE工作流的定时任务，PROCESS_CODE为工作流列表中的code字段。定时任务详细内容在`settings.json`中`schedulerFile`参数值对应的文件内

3. 更新定时任务
    
   `python main.py --scheduler --update PROCESS_CODE`
   
   更新PROCESS_CODE工作流的定时任务，PROCESS_CODE为工作流列表中的code字段。定时任务详细内容在`settings.json`中`schedulerFile`参数值对应的文件内

4. 上线工作流
    
   `python main.py --scheduler --online PROCESS_CODE`
   
   上线PROCESS_CODE工作流的定时任务，PROCESS_CODE为工作流列表中的code字段

5. 下线工作流
    
   `python main.py --scheduler --offline PROCESS_CODE`
   
   下线PROCESS_CODE工作流的定时任务，PROCESS_CODE为工作流列表中的code字段

### 补数
`python main.py --run --code PROCESS_CODE --start [START_TIME] --end [END_TIME] --tenant-code [TENANT]`

- PROCESS_CODE: 待运行的工作流code，PROCESS_CODE为工作流列表中的code字段
- START_TIME: 补数开始时间，默认当前时间
- END_TIME: 补数结束时间，默认当前时间
- TENANT: 作业提交队列，默认使用`settings.json`中`tenant`参数值

### 实例操作
1. 获取实例列表
    
   `python main.py --instance list --code [PROCESS_CODE] --page-no [PAGE_NO] --page-size [PAGE_SIZE] --state [STATE] --start [START] --end [END]`
   
   - PROCESS_CODE: 查看某个工作流下的实例，PROCESS_CODE为工作流列表中的code字段。默认为空，表示所有工作流实例
   - PAGE_NO: 查询的实例页面页数，默认为1
   - PAGE_SIZE: 查询的实例页面大小，默认为10。还有30和50两个选项
   - STATE: 查看的实例状态，默认所有状态。{"1": "SUCCESS", "2": "RUNNING_EXECUTION", "3": "FAILURE", "4": "STOP"}
   - START: 实例开始时间，默认所有时间。eg: '2024-05-01 00:00:00'
   - END: 实例结束时间，默认所有时间。eg: '2024-05-01 00:00:00'

2. 获取实例变量列表
    
   `python main.py --instance vars --id INSTANCE_ID`
   
   获取INSTANCE_ID实例的变量列表，INSTANCE_ID为实例列表中的id字段

3. 获取实例任务列表
    
   `python main.py --instance tasks --id INSTANCE_ID`
   
   获取INSTANCE_ID实例的任务列表，INSTANCE_ID为实例列表中的id字段

4. 实例操作
    
   `python main.py --instance instance --id INSTANCE_ID --type EXECUTE_TYPE`
   
   - INSTANCE_ID: 实例ID，实例列表中的id字段
   - EXECUTE_TYPE: 操作类型。1表示重跑实例，2表示重跑失败作业，3表示停止实例

5. 实例任务重跑
    
   `python main.py --instance run --id INSTANCE_ID --code TASK_CODE`
   
   - INSTANCE_ID: 实例ID，实例列表中的id字段
   - TASK_CODE: 任务code，TASK_CODE为实例任务列表中的taskCode字段
