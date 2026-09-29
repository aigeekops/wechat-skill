# WeChat Skill

通过 **Mac 上的 Apple iPhone 镜像**，让具备电脑控制能力的 AI 助手操作 iPhone 微信。

A progressively loaded agent skill for WeChat on iPhone, controlled through Apple's iPhone Mirroring on macOS.

这是操作手册型技能：技能负责流程、目标核对与结果检查；宿主 AI 和电脑控制工具负责观察与执行。仅安装这些文件不会自动获得手机连接或电脑控制能力。项目与腾讯、微信、Apple 无官方关联。

## 能做什么

| 工作流 | 验证状态 |
| --- | --- |
| 给单个联系人发送文字 | 有手工实测记录 |
| 搜索并关注公众号 | 有手工实测记录 |
| 给第一条朋友圈点赞 | 有手工实测记录 |
| 文件传输助手保存图片，再发布带文案朋友圈 | 有手工实测记录 |
| 普通聊天图片、文件、视频；群聊与逐人发送 | 有操作指引，待验证 |
| 视频或纯文字朋友圈；文章阅读、点赞与转发 | 有操作指引，待验证 |

手工记录不等于跨版本兼容保证。环境记录缺项与测试方法见 [验证说明](docs/verification.md)。目前仅面向 Mac + iPhone 原生镜像，不包含桌面微信或公众号后台 API。

## 使用前准备

1. 按 [Apple 官方说明](https://support.apple.com/en-us/120421) 配置 iPhone 镜像，先确认能手动连接和操作手机。设备条件及地区可用性以官方说明为准。
2. 在 iPhone 微信登录需要操作的账号。
3. 使用支持加载技能文件、读取截图和操作 Mac 窗口的 AI 宿主。按电脑控制工具的要求设置权限；本项目不自动修改系统权限。

## 安装与调用

下载或克隆仓库后，保留目录名 `wechat-skill`。将包含 `SKILL.md` 的整个目录放入宿主支持的技能目录，或让助手直接读取该文件。不要只复制入口文件，工作流依赖相对路径引用。

例如，在支持 `CODEX_HOME/skills` 的本地宿主中，从本仓库根目录执行以下命令。目标已存在时会停止，请先比较现有版本：

```sh
skill_destination="${CODEX_HOME:-$HOME/.codex}/skills/wechat-skill"
if [ -e "$skill_destination" ] || [ -L "$skill_destination" ]; then
  echo "目标目录已存在，请先比较版本：$skill_destination"
else
  mkdir -p "$skill_destination"
  cp SKILL.md LICENSE THIRD_PARTY.md "$skill_destination/"
  cp -R agents references workflows "$skill_destination/"
fi
```

按宿主的技能刷新方式加载。支持 `$技能名` 调用的宿主可使用以下示例；花括号内容由你替换：

```text
使用 $wechat-skill，给「{联系人}」发送「{准确正文}」。
使用 $wechat-skill，搜索公众号「{公众号名称}」并关注。
使用 $wechat-skill，用「{图片路径}」和「{文案}」准备朋友圈草稿，先不发表。
```

## 结构与加载方式

```text
SKILL.md              技能入口与任务路由
agents/openai.yaml    宿主展示元数据
references/           连接、输入、滚动和媒体传输
workflows/            消息、公众号和朋友圈流程
docs/verification.md  验证范围与手工回归方法
scripts/validate.py   离线结构校验
```

执行时只读取所需工作流，遇到输入或媒体问题再加载对应说明。收件人、正文、窗口位置和文件路径来自本次任务。Phone Harness 是可选外部工具，见 [第三方说明](THIRD_PARTY.md)。

## 贡献与校验

欢迎贡献可复现的微信操作步骤和兼容性记录。先读 [贡献指南](CONTRIBUTING.md)，不要提交真实聊天、账号资料或未脱敏截图。隐私问题见 [安全说明](SECURITY.md)。

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
```

开发校验需要 Python 3.10 或更新版本。校验只检查技能结构、引用和元数据，不会连接手机；真实操作需要单独手工验证。

## 许可证

项目原创内容采用 [MIT License](LICENSE)。外部工具保留各自许可证，项目不分发微信或 Apple 软件。许可证标准文本来源：[Open Source Initiative](https://opensource.org/license/mit)。
