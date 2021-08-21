# NJU-health-report
## 说明
本项目仅供学习交流使用。开发者对项目造成产生的后果不负任何责任，也不保证本方案一直有效。请使用者对自己负责。

## 使用方法
1. 将本项目 Fork 到自己的仓库。
2. 打开自己 Fork 之后的仓库，此时可能会自动开始构建并尝试打卡，因为此时没有填写账户信息，所以一定会失败。
3. 进入 `Settings` 选项，点击 `Secret`，并选择 `New Repository Secret`。依次添加以下变量：
   - `username`: 学号
   - `password`: 南京大学统一认证的密码
   - `location`: 你希望打卡的地理位置。比如南京大学仙林校区可以填 `中国江苏省南京市栖霞区九乡河东路`
4. 回到 `Action` 选项卡，重新运行 Action。此时应当显示运行成功，即一次打卡成功。
5. 项目默认是在 12:00 与 21:00（UTC 时间）自动打卡，可以根据需要修改 `.github/workflows/report.yml` 中 `cron` 项。
6. 建议设置 GitHub Actions 通知为 `Send notifications for failed workflows only` 以接收构建失败的通知。