import sys,time,os
sys.path.append('C:/Users/work/Desktop/uplode/main.py')
from com.ftp_c import *
from com.email_send import send_email

  
def config_update():
    #version_old.ini 
    #version_new.ini
    #下载最新的ini文件
    #1.删除本地的version_old.ini文件，把本地的version_new.ini文件名改成version_old.ini
    #2.从ftp 下载version.ini到本地，下载后命名为version_new.ini
    ftp=ftp_connect('192.168.1.6','public','share')              #链接1.6
    remot_version_file='Linux_Packets/version.ini'
    local_version_file='./config/version_new.ini'
    if os.path.exists('./config/version_old.ini')==True:
        os.remove('./config/version_old.ini')  #删除文件
        print('旧配置文件删除成功')
    if os.path.exists('./config/version_new.ini')==True:
        os.rename('./config/version_new.ini', './config/version_old.ini') #更改文件名(要修改的目录名 ,修改后的目录名) 
        print('配置文件改名成功')
    print('开始下载新的version_new.ini')
    downloadfile(ftp,remot_version_file,local_version_file)
    ftp.quit()
    
   #涉密包上传
def SM_uplode(field):
    #field='LocalizationSecret'
    version_new='./config/version_new.ini'       
    version_old='./config/version_old.ini'
    SM_up_pakg=diff_package(version_new,version_old,field)#找出哪个版本变了 
    for i in SM_up_pakg:
        print('%s 的 %s 需要更新包'%(field,i))
        #从ftp下载到本地
        ftp=ftp_connect('192.168.1.6','public','share')              #链接1.6
        #获取新包的路径
        test_ftp=read_config(version_new,field,i)                      
        #print('%s包所在的位置为：%s'%(i,test_ftp))       
        #获取包名
        filepath,package_name = os.path.split(test_ftp)
        #拼接包的本地路径
        down_local='./config/down_local.ini'
        local_path=read_config(down_local,field,i)
        local_file_path=os.path.join(local_path,package_name) #下载到本地的地址
        print('%s包下载到本地路径：%s'%(i,local_file_path))
        #下载到本地
        downloadfile(ftp,test_ftp,local_file_path)                 #下载   

        #提测包的大小：
        test_packege_size=ftp.size(test_ftp)
        print('提测包的大小为：%s'%(test_packege_size))
        #内网1.6路径
        nw_path_ini='./config/neiwang.ini'
        remot_pa=read_config(nw_path_ini,field,i)
        now_time=time.strftime('%Y-%m-%d-%H-%M',time.localtime(time.time()))
        ftp.cwd(remot_pa)
        ftp.mkd(now_time)
        ftp.cwd(now_time)

       
        name,suffix=os.path.splitext(package_name)  #分离包名和后缀，取包名，生成q7的文件名
        q7=name+'.q7'                                #q7文件名
        local_path_q7=os.path.join(local_path,q7)   #拼接路径
        print(local_path_q7)
    
        #本地包和q7文件大小
        local_package_size=os.path.getsize(local_file_path)
        local_q7_size=os.path.getsize(local_path_q7)
        print('本地包大小:%s,本地q7文件大小:%s'%(local_package_size,local_q7_size))

        if local_package_size !=test_packege_size:
            print('%s下载到本地出错，请重新操作'% (i))
        else:
            #上传packege到路径下
            uploadfile(ftp,package_name,local_file_path)#上传packege到pa路径下
            #上传q7到pa路径下
            uploadfile(ftp,q7,local_path_q7)  

            #计算包和q7的md5
            packageMd5=get_md5(local_file_path)
            print(packageMd5)
            q7Md5=get_md5(local_path_q7)
            print(q7Md5)
            #包和q7的内网路径
            nwlj_package='ftp://192.168.1.6/public/'+remot_pa+now_time+'/'+package_name #包的内网路径
            nwlj_q7='ftp://192.168.1.6/public/'+remot_pa+now_time+'/'+q7               #q7的内网路径
            write_config('./log/version_path.ini',field,i,nwlj_package)

            nw_path_package=remot_pa+now_time+'/'+package_name
            print(nw_path_package)
            nw_path_q7=remot_pa+now_time+'/'+q7
            print(nw_path_q7)

            #获取内网包和q7文件大小
            nw_packege_size=ftp.size(package_name)
            nw_q7_size=ftp.size(q7)
            print('内网release包大小:%s,内网release签名q7大小:%s'%(nw_packege_size,nw_q7_size))
            ftp.quit()
            if nw_packege_size!=local_package_size or nw_q7_size!=local_q7_size:
                print('上传到内网文件不一致，请删除手动上传')
            else:
                #上传到外网 
                ftp2=ftp_connect('120.133.1.35','jingyun','cx2016jy!@')
                ww_path_ini='./config/waiwang.ini'
                ww_path=read_config(ww_path_ini,field,i)            #读取配置文件的外网地址
                package_ww_path=os.path.join(ww_path,package_name)    #包文件外网的上传地址
                q7_ww_path=os.path.join(ww_path,q7)                   #q7外网上传地址
                
                #remot_file=ww_path,package_name


                #ftp2.cwd(ww_path)
                uploadfile(ftp2,package_ww_path,local_file_path)      #上传包到外网路径下
                time.sleep(3)
                uploadfile(ftp2,q7_ww_path,local_path_q7)           #上传q7到外网路径下

                #print(package_ww_path,q7_ww_path)
                #获取外网包和q7文件大小
                ww_package_size=ftp2.size(package_ww_path)
                ww_q7_size=ftp2.size(q7_ww_path)
                print('外网release包大小:%s,外网release 签名q7大小:%s'%(ww_package_size,ww_q7_size))
                ftp2.quit()
                if local_package_size!= ww_package_size or local_q7_size!=ww_q7_size:
                    print('上传到外网大小不一致，请手动重新上传')
                else:
                    wwlj_package='ftp://120.133.1.35/'+package_ww_path
                    wwlj_q7='ftp://120.133.1.35/'+q7_ww_path
                    fp=open('./log/uplode.txt','a+',encoding="utf-8")
                    
                    #将时间-包和q7的内外网路径和MD5写入log
                    fp.write('\n''%s: %s的%s包内网路径:%s\nMD5:%s'%(now_time,field,i,nwlj_package,packageMd5))         
                    fp.write('\n''%s: %s的%sQ7内网路径:%s\nMD5:%s'%(now_time,field,i,nwlj_q7,q7Md5))  
                    fp.write('\n''%s: %s的%s包外网路径:%s'%(now_time,field,i,wwlj_package))
                    fp.write('\n''%s: %s的%sQ7外网路径:%s\n'%(now_time,field,i,wwlj_q7))   
                    fp.close()
                    connect='%s的%s包测试通过\n内网路径:\n%s\n%s\n包MD5%s\nQ7MD5:%s\n外网路径\n%s\n%s'%(field,i,nwlj_package,nwlj_q7,packageMd5,q7Md5,wwlj_package,wwlj_q7)
                    subject='%s的%s包测试结果'%(field,i)
                    send_email(subject,connect)



    '''      
                                                    #下载到本地
                                                    #上传到内网ftp
                                                    #输出内网路径
                                                    #输出MD5
                                                    #上传到外网ftp
                                                    #输出外网路径
                                                    #写入将内外网包和q7的路径和MD5写入log                                         
  
'''
      

def FM_uplode(field):
    #field='LocalizationSecret'
    version_new='./config/version_new.ini'       
    version_old='./config/version_old.ini'
    SM_up_pakg=diff_package(version_new,version_old,field)#找出哪个版本变了 
    for i in SM_up_pakg:
        print('%s 的 %s 需要更新包'%(field,i))
        #从ftp下载到本地
        ftp=ftp_connect('192.168.1.6','public','share')              #链接1.6
        #获取新包的路径
        test_ftp=read_config(version_new,field,i)                      
        #print('%s包所在的位置为：%s'%(i,test_ftp))       
        #获取包名
        filepath,package_name = os.path.split(test_ftp)
        #拼接包的本地路径
        down_local='./config/down_local.ini'
        local_path=read_config(down_local,field,i)
        local_file_path=os.path.join(local_path,package_name) #下载到本地的地址
        print('%s包下载到本地路径：%s'%(i,local_file_path))
        #下载到本地
        downloadfile(ftp,test_ftp,local_file_path)                 #下载   
        #提测包的大小：
        test_packege_size=ftp.size(test_ftp)
        print('提测包的大小为：%s'%(test_packege_size))
        #内网1.6路径
        nw_path_ini='./config/neiwang.ini'
        remot_pa=read_config(nw_path_ini,field,i)
        now_time=time.strftime('%Y-%m-%d-%H-%M',time.localtime(time.time()))
        ftp.cwd(remot_pa)
        #上传packege到路径下
        uploadfile(ftp,package_name,local_file_path)#上传packege到pa路径下       
        #本地包文件大小
        local_package_size=os.path.getsize(local_file_path)        
        print('本地包大小:%s'%(local_package_size))
        if local_package_size !=test_packege_size:
            print('%s下载到本地出错，请重新操作'% (i))
        else:
            #计算包的md5
            packageMd5=get_md5(local_file_path)
            print(packageMd5)
            
            #包的内网路径
            nwlj_package='ftp://192.168.1.6/public/'+remot_pa+package_name #包的内网路径    
            write_config('./log/version_path.ini',field,i,nwlj_package)
            nw_path_package=remot_pa+package_name
            print(nw_path_package)
            
            #获取内网包文件大小
            nw_packege_size=ftp.size(package_name)
            print('内网release包大小:%s'%(nw_packege_size))
            ftp.quit()
            if nw_packege_size!=local_package_size:
                print('上传到内网文件不一致，请删除手动上传')
            else:
                #上传到外网 
                ftp2=ftp_connect('120.133.1.35','jingyun','cx2016jy!@')
                ww_path_ini='./config/waiwang.ini'
                ww_path=read_config(ww_path_ini,field,i)            #读取配置文件的外网地址
                package_ww_path=os.path.join(ww_path,package_name)    #包文件外网的上传地址              
                uploadfile(ftp2,package_ww_path,local_file_path)      #上传包到外网路径下                
                #print(package_ww_path,q7_ww_path)
                #获取外网包和q7文件大小
                ww_package_size=ftp2.size(package_ww_path)               
                print('外网release包大小:%s'%(ww_package_size))
                ftp2.quit()
                if local_package_size!= ww_package_size:
                    print('上传到外网大小不一致，请手动上传')
                else:
                    wwlj_package='ftp://120.133.1.35/'+package_ww_path                    
                    fp=open('./log/uplode.txt','a+',encoding="utf-8")
                    
                    #将时间-包和q7的内外网路径和MD5写入log
                    fp.write('\n''%s: %s的%s包内网路径:%s\nMD5:%s'%(now_time,field,i,nwlj_package,packageMd5))                            
                    fp.write('\n''%s: %s的%s包外网路径:%s\n'%(now_time,field,i,wwlj_package))                    
                    fp.close()
                    
                    connect='%s的%s包测试通过：\n内网路径:%s\nMD5:%s\n外网路径%s'%(field,i,nwlj_package,packageMd5,wwlj_package)
                    subject='%s的%s包测试结果'%(field,i)
                    send_email(subject,connect)
                    
if __name__ == "__main__":
    config_update()   
    
    #SM_uplode('LocalizationSecret')
    #FM_uplode('LocalizationNormal')
    FM_uplode('LinuxNormalbin')
    #FM_uplode('LinuxNormalrpm')
    #FM_uplode('LinuxNormaldeb')
