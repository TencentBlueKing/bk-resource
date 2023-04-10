![logo.png](assests/logo.png)

[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)](https://github.com/TencentBlueKing/bk-resource/blob/main/LICENSE.txt)
[![Release Version](https://img.shields.io/badge/release-0.4.0-brightgreen.svg)](https://github.com/TencentBlueKing/bk-resource/releases)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/TencentBlueKing/bk-resource/pulls)
[![codecov](https://codecov.io/gh/TencentBlueKing/bk-resource/branch/main/graph/badge.svg)](https://codecov.io/gh/TencentBlueKing/bk-resource)
[![Unittest Py3](https://github.com/TencentBlueKing/bk-resource/actions/workflows/unittest.yml/badge.svg)](https://github.com/TencentBlueKing/bk-resource/actions/workflows/unittest.yml)

[(English Documents Available)](readme_en.md)

## Overview

`bk_resource` 是基于 [Blueapps](https://github.com/TencentBlueKing/blueapps) & [Django Rest Framework](https://github.com/encode/django-rest-framework) ，快速生成符合 [`12-factor`](https://12factor.net/) 规范的 `WEB SaaS` 的脚本架

## Features

- [Basic] 基于 `Django` 进行封装，生成标准 `swagger API`
- [Basic] 基于 `django-environ` 适配环境变量与 `.env` 配置
- [Basic] 支持基于 `PEP-621` 的全工具链 (mypy\isort\flake8\black) 配置方案
- [Basic] 支持代码规范类工具整合：`pre-commit`、`code-cc`
- [Resource] 集成 `bk_resource` 组织工程目录结构，通过 `Resource` 的方式声明业务逻辑
- [Resource] 支持 `ApiResource` / `BkApiResource` 调用第三方 `API` 接口

## Getting started

### Installation

```bash
$ pip install cookiecutter
$ cookiecutter https://github.com/TencentBlueKing/bk-resource.git --checkout main --directory template
```

### Usage

- [快速开始](template/readme.md)
- [使用文档](docs/usage.md)

## Roadmap

- [版本日志](release.md)

## Support

- [蓝鲸论坛](https://bk.tencent.com/s-mart/community)
- [蓝鲸 DevOps 在线视频教程](https://bk.tencent.com/s-mart/video/)
- [蓝鲸社区版交流群](https://jq.qq.com/?_wv=1027&k=5zk8F7G)

## BlueKing Community

- [BK-CMDB](https://github.com/Tencent/bk-cmdb)：蓝鲸配置平台（蓝鲸 CMDB）是一个面向资产及应用的企业级配置管理平台。
- [BK-CI](https://github.com/Tencent/bk-ci)：蓝鲸持续集成平台是一个开源的持续集成和持续交付系统，可以轻松将你的研发流程呈现到你面前。
- [BK-BCS](https://github.com/Tencent/bk-bcs)：蓝鲸容器管理平台是以容器技术为基础，为微服务业务提供编排管理的基础服务平台。
- [BK-PaaS](https://github.com/Tencent/bk-paas)：蓝鲸 PaaS 平台是一个开放式的开发平台，让开发者可以方便快捷地创建、开发、部署和管理 SaaS 应用。
- [BK-SOPS](https://github.com/Tencent/bk-sops)：标准运维（SOPS）是通过可视化的图形界面进行任务流程编排和执行的系统，是蓝鲸体系中一款轻量级的调度编排类 SaaS 产品。
- [BK-JOB](https://github.com/Tencent/bk-job) 蓝鲸作业平台(Job)是一套运维脚本管理系统，具备海量任务并发处理能力。

## Contributing

如果你有好的意见或建议，欢迎给我们提 Issues 或 Pull Requests，为蓝鲸开源社区贡献力量。   
[腾讯开源激励计划](https://opensource.tencent.com/contribution) 鼓励开发者的参与和贡献，期待你的加入。

## License

基于 MIT 协议， 详细请参考 [LICENSE](LICENSE.txt)
