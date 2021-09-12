# SEU_Action_Report

本项目是 [Quzard/SEU_Action_Report](https://github.com/Quzard/SEU_Action_Report) 的分支，仍使用 headless browser 而不是模拟请求完成健康上报。

利用 GitHub Actions 进行健康上报，支持定时上报以及 star 上报（star 一下自己 fork 后的项目就会启动上报 action）

**没有更新疫苗信息的请手动上报一次更新自己的疫苗信息**

**fork 后记得添加变量，并去 Actions 那 Enable Workflow。可以 star 一下自己 fork 后的项目测试 action 是否可以正常启动**

如有使用问题，请发 issue 或邮件。

## 使用步骤

1. 首先 fork 本项目到自己的仓库

2. 去 Actions 那 Enable Workflow

3. 进入自己 fork 的仓库，点击 Settings -> Secrets -> New repository secret，它们将作为配置项，在应用启动时传入程序。

**所有的可用 Secrets 及说明**

| Secret     | 解释                                                         |
| ---------- | ------------------------------------------------------------ |
| ID         | 一卡通号                                                     |
| PASSWORD   | 一卡通密码                                                   |

4. 如果需要修改上报时间，修改 `.github/workflows/auto_temperature.yml`
