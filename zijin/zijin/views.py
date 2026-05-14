from django.shortcuts import render
from django.http import  StreamingHttpResponse, HttpResponse, Http404,HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_protect,requires_csrf_token
from urllib.parse import quote
import subprocess
import os
from datetime import datetime


#判断客户端类型
def ismobile(requestmeta):
    if "HTTP_USER_AGENT" in requestmeta: 
        useragent1 = requestmeta['HTTP_USER_AGENT']
        useragent1 = useragent1.lower()  # 把useragent1里所有大写转换为小写
        if 'mobile' in useragent1 or 'android' in useragent1 or 'phone' in useragent1 or 'ipad' in useragent1:
            return 1
        else:
            return 0  


@csrf_protect
@requires_csrf_token
def index(request):
    meta1 = request.META
    mobile_flag = ismobile(meta1)
    if request.method == 'POST':
        passwd = request.POST.get('passwd','')
        if passwd == "ooo000#@!":
            grades = request.POST.getlist('grade', '')
            grades_string = ", ".join(f"'{g}'" for g in grades)
            # 获取当前时间
            current_time = datetime.now().strftime("%H:%M:%S")
            if current_time < "16:00:00":
                con = "午休"
            else:
                con = "晚休"
            
            file_date = datetime.now().strftime("%m.%d")
            file_name = f"{con}就寝未归考勤明细表({file_date}).xlsx"
        
            # 构建执行 sheetout.py 的命令
            script_path = os.path.join('E:\\', 'pxg','zijin', 'zijin', 'sheetout.py')
            command = ['python', script_path, grades_string]
            print(command)
            
            try:
                # 调用 sheetout.py 脚本
                process = subprocess.run(command, capture_output=True, text=True, check=True)
                
                # 检查 sheetout.py 执行结果
                if process.returncode == 0:
                    context = {'file_name': file_name}  # 将文件名传递给模板
                    d_type = 'm_download.html' if mobile_flag == 1 else 'download.html'
                    return render(request, d_type, context)
                else:
                    return HttpResponse(f"执行sheetout时出错: {process.stderr}")
            except subprocess.CalledProcessError as e:
                return HttpResponse(f"执行脚本时发生错误: {e}")
        else:
            return HttpResponse("密码错误，请重新输入。")
    
    # 根据设备类型选择不同的模板
    i_type = 'm_index.html' if mobile_flag == 1 else 'index.html'
    return render(request, i_type)



def download_file(request):
    current_time = datetime.now().strftime("%H:%M:%S")
    if current_time < "16:00:00":
        con = "午休"
    else:
        con = "晚休"
        
    file_date = datetime.now().strftime("%m.%d")
    filename = f"{con}就寝未归考勤明细表({file_date}).xlsx"
    
    # 使构建文件路径
    file_path = os.path.join('E:\\', 'pxg','zijin', 'xlsx', filename)
    
    print(f"尝试从路径下载文件: {file_path}")
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print("File does not exist!")
        raise Http404("File does not exist")

    # 打开文件并创建一个文件响应对象
    def file_iterator(file_path, chunk_size=512):
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    response = StreamingHttpResponse(file_iterator(file_path))
    
    # 设置Content-Type头部，以便浏览器知道如何处理文件
    response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    
    # 进行文件名编码
    encoded_filename = quote(filename)
    response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{encoded_filename}'

    return response
