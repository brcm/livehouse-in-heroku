## LiveHouse 反向代理（Heroku版）

### 已知该版本存在无法登录问题，请移步 NGINX 版本 livehouse-in-nginx !!! 
部署在 Heroku 中即可立即获得一个非常方便访问谷歌的方式。源代码基于 @Hsiny 的 ```google-in-heroku``` 修改而来。

### 如何部署

在 Windows 的 Git Bash 或者 Linux 的终端中运行如下命令即可。

```bash
git clone https://github.com/brcm/livehouse-in-heroku
cd livehouse-in-heroku
heroku create
git add -A
git commit -m "init"
git push heroku master
heroku open
```

### 更新内容

1. 完善 HTTP 请求头，HTTP 响应头添加缓存字段
2. 对 Google Firebase 库单独本地缓存
3. 强行移除多余 Javascript 脚本，例如 Facebook SDK、广告等
4. 添加页面繁体中文转简体中文 JS 库，默认启用
5. Web 服务器添加 POST 与 Cookies 支持

### 已知问题

1. 用户无法登录，永远处于未登录状态
2. 本地 Firebase 读取速度过慢
3. NGINX 版本相对完善请使用 NGINX 版本