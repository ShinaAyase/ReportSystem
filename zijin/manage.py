#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import schedule
import time
import shutil

def delete_xlsx_folder():
    xlsx_folder = 'xlsx'
    if os.path.exists(xlsx_folder):
        shutil.rmtree(xlsx_folder)
        print(f"{xlsx_folder} 文件夹已删除。")
    else:
        print(f"{xlsx_folder} 文件夹不存在。")

def run_scheduled_tasks():
    # 每月第一天的 00:00 执行删除任务
    schedule.every().month.at("00:00").do(delete_xlsx_folder)
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zijin.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    import threading
    # 启动定时任务线程
    task_thread = threading.Thread(target=run_scheduled_tasks)
    task_thread.daemon = True
    task_thread.start()

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()