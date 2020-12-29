:@关闭本命令的回显
@echo off

:echo ___________________________________________________________
:echo 设置默认的控制台前景和背景颜色(color)。                        
:echo 指定控制台输出的颜色属性                                       
:echo 颜色属性由两个十六进制数字指定 -- 第一个为背景，第二个则为     
:echo 文字颜色。每个数字可以为以下任何值之一:                            
:echo    0 = 黑色        8 = 灰色                                                                       
:echo    1 = 蓝色        9 = 淡蓝色                                  
:echo    2 = 绿色        A = 淡绿色                                  
:echo    3 = 湖蓝色      B = 淡浅绿色                                
:echo    4 = 红色        C = 淡红色                                  
:echo    5 = 紫色        D = 淡紫色                                  
:echo    6 = 黄色        E = 淡黄色                                  
:echo    7 = 白色        F = 亮白色                                                             
:echo 例如: "COLOR fc" 亮白色背景，淡红色文字颜色。                          
:echo ____________________________________________________________
@color 2f
@echo off
@chcp 65001
@cls

echo ------------------------------------------------------------
echo                       UI转换工具
echo ------------------------------------------------------------                    
echo       将你的Qt Designer UI文件转换为Python Script文件                                     
echo ------------------------------------------------------------ 
echo=
echo=

set /p sourcefile=UI文件(去除后缀名):
echo=
set /p destfile=Python文件名(去除后缀名):
echo=
pyuic5 -o %destfile%.py %sourcefile%.ui
echo=
pause > nul
exit