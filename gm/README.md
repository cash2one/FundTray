
### 生产过程

本目录下的dist文件，为生产所需的全部文件，请将其放置于服务器的静态文件目录,如果需要重新构建，请参考《源码转换过程》，务必注意，重新构建将会覆盖dist文件,出于谨慎考虑，可以备份dist文件,在进行生产转换.

### 源码转换过程

1. 安装nodejs

2. 在命令行中，输入npm --version 查看npm的版本号; 确认npm正常可用

3. cd /to/current_dir 将命令行切换号当前目录

4. 确保当前目录下，有package.json

5. 在命令行中，输入 npm install 安装项目所需要的插件（过程根据网络环境，可能需要几十分钟）

6. 在命令行中，输入 grunt --version 查看是否成功安装grunt插件

7. 在命令行中，输入 grunt build 进行 * 生产版本构建 *

8. 部分cdn进行手动替换：
    把
    `<link rel="stylesheet" href="bower_components/bootstrap/dist/css/bootstrap.css" />`
    替换为
    `<link href="//cdn.bootcss.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet">`
    把
    `<link rel="stylesheet" href="bower_components/font-awesome/css/font-awesome.css" />`
    替换为
    `<link href="//cdn.bootcss.com/font-awesome/4.5.0/css/font-awesome.css" rel="stylesheet">`
9. 转换完成
