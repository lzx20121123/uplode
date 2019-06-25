import os,sys,time,hashlib,configparser,ftplib


def ftp_connect(host,username,password):
    '''
    获取ftp连接
    :return:ftp
    '''
    try:
        ftp = ftplib.FTP(host)
        #ftp.encoding = "GB2312"
        ftp.encoding = "utf-8"
        ftp.login(username,password)#登录，参数user，password，acct均是可选参数，
         #f.login(user="user", passwd="password")
        #ftp.encoding = "GB2312"
        
        print('已连接到： "%s"' % host)
        return ftp 
    except:
        print("FTP登陆失败，请检查主机号、用户名、密码是否正确")
        #sys.exit(0)

def uploadfile(ftp,file_remote,file_local):
    '''
    以二进制形式上传文件
    file_remote:ftp文件名
    file_local:要下载到哪里，文件名是什么
    '''
    try:
        #ftp.set_pasv(False)
        bufsize = 1024  # 设置缓冲器大小
        fp = open(file_local, 'rb')
        ftp.storbinary('STOR '+file_remote, fp, bufsize)
        #fp.close()
        print('%s上传到成功'%(file_remote))
        fp.close()
    except Exception as e:
        print('%s上传失败'%(file_remote))
        print(e)

def downloadfile(ftp,file_remote,file_local):
    '''
    以二进制形式下载文件
    file_remote:ftp文件
    file_local:要上传的文件路径和文件名
    '''
    try:
        print('开始下载%s'%(file_remote))
        bufsize = 1024  # 设置缓冲器大小
        fp = open(file_local, 'wb')
        ftp.retrbinary('RETR ' + file_remote, fp.write, bufsize)
        fp.close()
        print('%s下载成功'%(file_remote))
    except Exception as e:
        print(e)
        print('%s下载失败'%(file_remote))


#定义计算md5函数
def get_md5(path_file):
    '''
    计算文件的md5值
    path_file:文件的地址
    '''
    try:
        m = hashlib.md5() 
        f = open(path_file,'rb')  #以二进制只读方式打开文件，生成一个文件对象
        str = f.read()            #读取整个文件，内容赋值给变量 
        m.update(str)             #用md5对象的update方法指定一个字符串，前面的b是转换为二进制，否则显示不 了。
        md5_num=m.hexdigest()
        #print(m.hexdigest())      #用md5对象的hexdigest()方法进行十六进制显示 。
        return md5_num
    except:
        print('获取%s的MD5失败'%(path_file))

#读取ini文件
def read_config(config_file_path, field, key):
    '''
    config_file_path:ini文件路径
    field: 领域
    key：关键字
    return:value(版本号)
    ''' 
    cf = configparser.ConfigParser()
    try:
        cf.read(config_file_path,encoding="utf-8-sig")
        result = cf.get(field, key)
        #print('%s对应的版本为%s'%(key,result))
        return result
    except Exception as e:
        print('%s读取失败'%(config_file_path))
        print(e)


#写入ini文件
def write_config(config_file_path, field, key,value):
    '''
    config_file_path:ini文件路径
    field: 领域(SM or FM)
    key：关键字(客户端名称)
    value:key对应的值(对应包新的版本号)
    
    ''' 
    cf = configparser.ConfigParser()
    try:
        cf.read(config_file_path,encoding="utf-8-sig")
        cf.set(field,key,value)
        cf.write(open(config_file_path,'w',encoding='utf-8-sig'))
        print('%s已经更新为%s'%(key,value))

    except Exception as e:
        print('%s写入异常'%(config_file_path))
        print(e)
    

def diff_package(ini_remote,ini_local,field):
    '''
    对比两个ini文件，输出有改变的value对应的key
    ini_remote:ftp上的ftp文件
    ini_local:本地的ini文件
    field:领域
    return更改的列表
    '''
    try:
        #获取第一个ini文件的key,value列表
        cf = configparser.ConfigParser()
        cf.read(ini_remote,encoding="utf-8-sig")
        l=cf.items(field)
        #print(cf.items(field))

        #获取第二个ini文件的key,value列表
        cf2=configparser.ConfigParser()
        cf2.read(ini_local,encoding="utf-8-sig")
        l2=cf2.items(field) 
        #print(cf2.items(field))


        l3=[]
        diff_pag=[]
        for i in l:
            if i in l2:
                #print('%s 的%s未更新'%(field,i[0]))
                print('')
            else:
                l3.append(i)
        #print(l3)
        for i in l3:
            diff_pag.append(i[0])
            print('%s 的 %s包已经更新'%(field,i[0]))
        print(diff_pag)
        return diff_pag
    except Exception as e:
        print('文件对比失败')
        print(e)
if __name__ == "__main__":
    
    write_config('./log/version_path.ini','LocalizationNormal','中科方德(非密)','nwlj_package')
   