# NJU-health-report
![](https://img.shields.io/badge/language-python-brightgreen)

南京大学每日健康填报自动打卡脚本。

## 说明
- 本项目仅供学习交流使用。开发者对项目造成产生的后果不负任何责任，也不保证本方案一直有效。请使用者对自己负责。
- 使用前须将项目 Fork 至自己的仓库，此时密钥只有自己才知道，可以保证信息的安全，请放心使用。 
- 因统一身份认证的特性，在输错一次密码之后会要求输入验证码。因此请在密码错误之后手动登录来去除验证码的限制。

## 更新
- 2020-10-19 之前使用的方案实测已经无法正常使用，目前已回退旧方案。已 fork 的用户请更新后使用。

## 使用方法
1. 将本项目 Fork 到自己的仓库。
2. 打开自己 Fork 之后的仓库，因为没有填写账户信息，此时若触发打卡，一定会失败。
3. 进入 `Settings` 选项，点击 `Secret`，并选择 `New Repository Secret`。依次添加以下变量：
   - `username`: 学号
   - `password`: 南京大学统一认证的密码
   - `location`: 你希望打卡的地理位置。比如南京大学仙林校区可以填 `中国江苏省南京市栖霞区九乡河东路`

![](img/1.png)

4. 回到 `Action` 选项卡，重新运行 Action，或者静待自动打卡。
5. 项目默认是在 13:00（UTC 时间）自动打卡，可以根据需要修改 `.github/workflows/report.yml` 中 `cron` 项。
6. 建议设置 GitHub Actions 通知为 `Send notifications for failed workflows only` 以接收构建失败的通知。这通常是默认设置项。

当 Action 启动之后，可以通过进入 Summary 来查看具体的记录。一次正常的打卡显示效果如下：

![](img/2.png)

若构建失败，请遵循 Log 中的提示进行相应操作。

## 待办
- [ ] 自动识别验证码