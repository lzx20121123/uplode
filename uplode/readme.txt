1.此工具为自动上传包的脚本。
2.main.py为主函数。
3.ftp_c.py为定义的一些通用函数。
4.脚本会比对提测路径包的大小，本地包的大小，内网包的大小以及外网包的大小，如果大小不一致，则会输出一些错误信息，需要手动重新上传。
5./log/uplode.txt 下面记录每次上传的内网地址，外网地址和MD5
6.config\waiwang.ini 里是外网路径
7.config\neiwang.ini 里是内网路径
8.config\down_local.ini 是本地路径
9.config\version_new.ini 是最新的版本信息
10.config\version_old.ini 是上一次上传的版本信息.
11.log\version_path.ini 每次上传之后，把最新的版本信息更新到上面
12.执行时修改一下要上传的包的类型：
例：
if __name__ == "__main__":
    config_update() 
    #SM_uplode('LocalizationSecret')
    #FM_uplode('LocalizationNormal')
    #FM_uplode('LinuxNormalbin')
    #FM_uplode('LinuxNormalrpm')
    FM_uplode('LinuxNormaldeb')
如只需要上传deb的包，则只需要上图两个函数，其余的注掉。
如果需要上传SM的专用机的包，需要先把测试完成的签名包放在本地的路径下。如中标龙芯涉密包。需要先放在C:/linux_package/client/zblx/zyj/下，再操作。
