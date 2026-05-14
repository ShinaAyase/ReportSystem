
import mysql.connector
from datetime import datetime
import sys,json

yesr =  []

def main():
    global yesr
    # 从标准输入读取 JSON 数据
    input_data = sys.stdin.read()
    form_data = json.loads(input_data)

    # 处理表单数据
    grade1 = form_data.get('grade1')
    grade2 = form_data.get('grade2')
    grade3 = form_data.get('grade3')
    yesr = [grade1,grade2,grade3]



# 连接到 MySQL 数据库
conn = mysql.connector.connect(
    host='36.212.25.208', 
    port='33398',       
    user='root',     
    password='wwwyibu2008',
    database='schooloa', 
    charset='gbk'
)


today = datetime.now().strftime("%Y-%m-%d")
now_time = datetime.now().strftime("%H:%M:%S")

# 判断当前时间是午休还是晚休
# 用于查询请假时间
if now_time < "16:00:00":
    e_time = "11:00:00"
    b_time = "12:50:00"
else:
	e_time = "21:00:00"
	b_time = "23:00:00"

# yesr = "高一","高二","高三"


sql = """
SELECT
	s.`name` AS '姓名',
	s.sex AS '性别',
	s.`status` AS '状态',
	s.out_type AS '住宿类型',
	s.stu_no AS '学号',
	s.yesr AS '年级',
	s.class AS '班级',
	h.hostel_name AS '宿舍',
	r.hostel_room_name AS '房间',
	d.bed_code AS '床位',
	k.kq_date AS '考勤时间',
	k.r_d_Time AS '刷脸时间',
	k.is_in AS '类型', 
	e.STATUS AS '审核状态',
	CONCAT( e.begin_date, ' ', e.begin_time ) AS '请假开始时间',
	CONCAT( e.end_date, ' ', e.end_time ) AS '请假结束时间',
	e.xj_time AS '销假时间',
	t.`name`,
	t.phone
FROM
	student s
	JOIN hostel_bed d ON d.str_id = s.ID
	JOIN hostel_room r ON r.ID = d.hostel_room_id
	JOIN hostel h ON h.ID = d.hostel_Id
	JOIN room_kq_detail k ON k.stu_no = s.stu_no
	LEFT JOIN stu_leave e ON e.stu_no = s.stu_no 
	AND CONCAT( e.end_date, ' ', e.end_time ) >= '%s %s' 
	AND CONCAT( e.begin_date, ' ', e.begin_time ) <= '%s %s' 
	AND e.`status` IN ( '3', '4' )
	LEFT JOIN teacher_subject b ON b.class_id = s.class_id 
	AND ( b.`status` = '0' )
	LEFT JOIN teacher t ON t.ID = b.Teacher_id 
	AND ( t.`status` = '0' ) 
WHERE
	s.out_type = '住宿生' 
	AND k.kq_date = CURDATE( ) 
	AND k.r_d_Time IS NULL or k.status = '1' 
	AND s.yesr in %s
GROUP BY
	s.stu_no 
ORDER BY
	h.hostel_name,
	r.hostel_room_name,
	d.bed_code ASC
""" % (today,e_time,today,b_time,yesr)

if __name__ == "__main__":
    main()