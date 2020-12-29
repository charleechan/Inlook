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
echo                     QRC资源文件转换工具
echo ------------------------------------------------------------                    
echo       将你的.qrc文件转换为Python Script文件                                     
echo ------------------------------------------------------------ 
@echo off
@echo off


set /p imagefolder=图片文件夹名:
set /p qssfolder=QSS文件夹名:
set /p qrcfilename=目标qrc文件名(不写后缀):
set /p pyfilename=目标Python脚本文件名(不写后缀):
echo=
echo 正在打包资源文件(图片和QSS)...
echo=
echo 正在生成QRC文件...
@python ./tool/res2py.py  %imagefolder% %qssfolder% %qrcfilename%.qrc
echo=
echo QRC文件生成完成,正在转换为Python文件...
@pyrcc5 -o %pyfilename%.py %qrcfilename%.qrc
echo=
echo Python文件生成完成！

echo ------------------------------------------------------------
echo 使用方法:                  
echo     1. 在主调Python中"import %pyfilename%"
echo     2. 在主调Python中":/imgfolder/xxx.png"
echo=
pause >
exit