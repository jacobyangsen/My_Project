# 关闭原来表中的主外键约束功能
set FOREIGN_KEY_CHECKS=0;
# 清空原有的课程分类表信息
truncate table ly_course_category;
# 添加导航信息
insert into ly_course_category (name,orders,is_show,is_delete,create_time,update_time) VALUES
("python",1,1,0,"2019-11-11 12:00:00","2019-11-11 12:00:00"),
("python进阶",2,1,0,"2019-11-11 12:00:00","2019-11-11 12:00:00"),
("java",3,1,0,"2019-11-11 12:00:00","2019-11-11 12:00:00"),
("前端开发",4,1,0,"2019-11-11 12:00:00","2019-11-11 12:00:00");

# 开启原来表中的主外键约束功能
set FOREIGN_KEY_CHECKS=1;