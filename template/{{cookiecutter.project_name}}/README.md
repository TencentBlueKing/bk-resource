# {{ cookiecutter.app_id }}

## 一、概述


## 二、快速开始
 
### 1、安装依赖

#### 环境依赖

Python 3.6、MySQL 5.7+、Redis 3.2+

#### PIP源

``` pip.conf
[global]
index-url=https://mirrors.tencent.com/repository/pypi/tencent_pypi/simple
extra-index-url=http://mirrors.cloud.tencent.com/pypi/simple/
trusted-host = mirrors.tencent.com, mirrors.cloud.tencent.com
```

PIP 版本需要满足 `pip==20.2.3`，在 PaaS 中增加环境变量 `PIP_VERSION=20.2.3` 声明，本地可以使用 `pip install --upgrade pip==20.2.3` 安装指定版本

#### 安装依赖
   
``` bash
pip install -r requirements.txt
pip install -r requirements_dev.txt
```

### 2、安装配置pre-commit

pre-commit 是一款本地的代码规范检查工具，配置pre-commit，有助于代码质量的提升，
详细配置可在此文件中查看：.pre-commit-config.yaml

```bash
pip install pre-commit
pre-commit install --allow-missing-config
pre-commit install --hook-type commit-msg --allow-missing-config
```

### 3、配置环境变量

可以直接复制 `.env.template` 为 `.env`，快速初始化环境变量，`.env` 文件中配置的环境变量优先级低于已有的环境变量

```bash
DJANGO_SETTINGS_MODULE=settings
BKPAAS_APP_ID=xxxx
BKPAAS_APP_SECRET=xxxx
BKPAAS_ENGINE_REGION=default/ieod
BKPAAS_LOGIN_URL=xxx
BKAPP_DEPLOY_MODULE=default
```

### 4、配置DB

创建本地数据库

```
CREATE DATABASE IF NOT EXISTS `{{ cookiecutter.app_id }}` DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
```

### 5、声明目录

<div style="color: red">如果使用IDE无法正常运行，需要将"apps"目录标记为"源代码根目录"，或者在 `PYTHONPATH` 环境变量中增加"apps"目录的绝对路径</div>

### 6、启动服务 

使用IDE或者在项目根目录执行(命令行启动需要提前配置好环境变量，export DJANGO_SETTINGS_MODULE=settings):

```bash
python manage.py migrate
python manage.py runserver
```

当看到以下的输出的时候，证明我们的应用已经成功跑起来了：

```bash
System check identified no issues (0 silenced).
August 18, 2021 - 16:11:45
Django version 2.2.6, using settings 'settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

## 三、目录结构

```
- api                           # 第三方 API 集成
- bin                           # 脚本命令
    - post_compile              # 部署前置命令，更多请查看蓝鲸官方文档《部署前置命令》
- config                        # 应用配置目录
    - __init__.py               # 应用 RUN_VER（ieod/clouds/qcloud）、APP_CODE 和 SECRET_KEY 等配置
    - dev.py                    # 本地开发配置（开发团队共享）
    - default.py                # 全局配置
    - prod.py                   # 生产环境配置
    - stag.py                   # 预发布环境配置
- core                          # Blueapps Restful Pedestal    
    - exceptions.py             # 项目异常处理基类
    - models.py                 # Model基类
    - permissions.py            # 常用权限控制
- dev                           # 开发环境配置
- locale                        # 国际化文件
- modules                       # 各模块文件
    - web                       # Django application目录
        - entry                 # 项目入口
        - example               # 简单示例
        - __init__.py
        - settings.py           # 模块配置文件
        - urls.py               # 模块路由文件
- static                        # 公共静态文件
- templates                     # 公共模板文件
    - admin                     # admin模板文件
        - base_site.html
        - login.html
    - base.html                 # Django 模板基础文件，其他的页面可以从这里继承
    - 400.html                  # 400页面
    - 500.html                  # 500页面
- .coveragerc                   # Coverage配置
- .flake8                       # flake8
- .gitignore                    
- .pre-commit-config.yaml       # pre-commit配置文件
- __init__.py                   
- Aptfile                       # 在蓝鲸平台部署安装的系统组件
- CHANGELOG.md                  # 项目更新日志
- manage.py                     # Django 工程 manage
- Procfile                      # 应用进程管理文件，如果使用 Celery 需要修改
- requirements.txt              # 依赖的 python 包列表
- requirements_env.txt          # 不同环境扩展的依赖
- requirements_dev.txt          # 本地开发依赖
- runtime.txt                   # PaaS平台运行项目使用的Python解析器
- settings.py                    # Django工程 settings
- urls.py                       # Django工程主路由 URL 配置
- wsgi.py                       # WSG I配置
```

### 3.1 配置文件覆盖顺序

```
config.default -> config.{env} -> module.setting
    默认配置    ->    环境配置    ->    模块配置
    
INSTALLED_APPS 应在模块的配置中进行覆盖式声明 
所有需要对用户开放的配置都建议使用 os.getenv 或 get_env_or_raise 获取
```

### 3.2 初始化新模块

1. 在 `modules` 目录下新建模块目录，目录名须为英文小写，即满足正则 `[a-z]*`
2. 在目录下创建 app，可以使用 `python manage.py start_resource xxx` 来新建
3. 新建 `settings.py` 文件，并声明 `INSTALLED_APPS`，可参考 web 模块的声明方式
4. 更新环境变量 `BKAPP_DEPLOY_MODULE` 为对应的模块名后重启服务

## 四、常见问题 


### 4.1 blueapps 安装异常

Q：pip install blueapps 4.1.2 安装异常：'openssl/opensslv.h' file not found

```
build/temp.macosx-11.6-x86_64-3.6/_openssl.c:575:10: fatal error: 'openssl/opensslv.h' file not found
```

A：https://stackoverflow.com/questions/66035003/installing-cryptography-on-an-apple-silicon-m1-mac

```
LDFLAGS="-L$(brew --prefix openssl@1.1)/lib" CFLAGS="-I$(brew --prefix openssl@1.1)/include" pip install cryptography==3.3.2
```

### 4.2 运行提示 NameError: name '_mysql' is not defined

在 config/local_settings.py 文件中增加如下内容

```python
import pymysql
pymysql.install_as_MySQLdb()
```

