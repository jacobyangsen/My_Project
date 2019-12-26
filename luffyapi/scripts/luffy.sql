-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
--
-- Host: localhost    Database: luffy
-- ------------------------------------------------------
-- Server version	5.7.25

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `codename` varchar(100) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry','add_logentry',1),(2,'Can change log entry','change_logentry',1),(3,'Can delete log entry','delete_logentry',1),(4,'Can view log entry','view_logentry',1),(5,'Can add permission','add_permission',2),(6,'Can change permission','change_permission',2),(7,'Can delete permission','delete_permission',2),(8,'Can view permission','view_permission',2),(9,'Can add group','add_group',3),(10,'Can change group','change_group',3),(11,'Can delete group','delete_group',3),(12,'Can view group','view_group',3),(13,'Can add content type','add_contenttype',4),(14,'Can change content type','change_contenttype',4),(15,'Can delete content type','delete_contenttype',4),(16,'Can view content type','view_contenttype',4),(17,'Can add session','add_session',5),(18,'Can change session','change_session',5),(19,'Can delete session','delete_session',5),(20,'Can view session','view_session',5),(21,'Can add User Widget','add_userwidget',6),(22,'Can change User Widget','change_userwidget',6),(23,'Can delete User Widget','delete_userwidget',6),(24,'Can view User Widget','view_userwidget',6),(25,'Can add User Setting','add_usersettings',7),(26,'Can change User Setting','change_usersettings',7),(27,'Can delete User Setting','delete_usersettings',7),(28,'Can view User Setting','view_usersettings',7),(29,'Can add log entry','add_log',8),(30,'Can change log entry','change_log',8),(31,'Can delete log entry','delete_log',8),(32,'Can view log entry','view_log',8),(33,'Can add Bookmark','add_bookmark',9),(34,'Can change Bookmark','change_bookmark',9),(35,'Can delete Bookmark','delete_bookmark',9),(36,'Can view Bookmark','view_bookmark',9),(37,'Can add revision','add_revision',10),(38,'Can change revision','change_revision',10),(39,'Can delete revision','delete_revision',10),(40,'Can view revision','view_revision',10),(41,'Can add version','add_version',11),(42,'Can change version','change_version',11),(43,'Can delete version','delete_version',11),(44,'Can view version','view_version',11),(45,'Can add 轮播图','add_banner',12),(46,'Can change 轮播图','change_banner',12),(47,'Can delete 轮播图','delete_banner',12),(48,'Can view 轮播图','view_banner',12),(49,'Can add 导航','add_nav',13),(50,'Can change 导航','change_nav',13),(51,'Can delete 导航','delete_nav',13),(52,'Can view 导航','view_nav',13),(53,'Can add 用户','add_user',14),(54,'Can change 用户','change_user',14),(55,'Can delete 用户','delete_user',14),(56,'Can view 用户','view_user',14),(57,'Can add 课程课时','add_courselesson',15),(58,'Can change 课程课时','change_courselesson',15),(59,'Can delete 课程课时','delete_courselesson',15),(60,'Can view 课程课时','view_courselesson',15),(61,'Can add 讲师导师','add_teacher',16),(62,'Can change 讲师导师','change_teacher',16),(63,'Can delete 讲师导师','delete_teacher',16),(64,'Can view 讲师导师','view_teacher',16),(65,'Can add 实战课程','add_course',17),(66,'Can change 实战课程','change_course',17),(67,'Can delete 实战课程','delete_course',17),(68,'Can view 实战课程','view_course',17),(69,'Can add 课程章节','add_coursechapter',18),(70,'Can change 课程章节','change_coursechapter',18),(71,'Can delete 课程章节','delete_coursechapter',18),(72,'Can view 课程章节','view_coursechapter',18),(73,'Can add 课程分类','add_coursecategory',19),(74,'Can change 课程分类','change_coursecategory',19),(75,'Can delete 课程分类','delete_coursecategory',19),(76,'Can view 课程分类','view_coursecategory',19);
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_ly_users_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_ly_users_id` FOREIGN KEY (`user_id`) REFERENCES `ly_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(17,'courses','course'),(19,'courses','coursecategory'),(18,'courses','coursechapter'),(15,'courses','courselesson'),(16,'courses','teacher'),(12,'home','banner'),(13,'home','nav'),(10,'reversion','revision'),(11,'reversion','version'),(5,'sessions','session'),(14,'users','user'),(9,'xadmin','bookmark'),(8,'xadmin','log'),(7,'xadmin','usersettings'),(6,'xadmin','userwidget');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2019-11-05 08:33:53.904303'),(2,'contenttypes','0002_remove_content_type_name','2019-11-05 08:33:54.016938'),(3,'auth','0001_initial','2019-11-05 08:33:54.072307'),(4,'users','0001_initial','2019-11-05 08:33:54.225575'),(5,'admin','0001_initial','2019-11-05 08:33:54.402930'),(6,'admin','0002_logentry_user','2019-11-05 08:33:54.456092'),(7,'home','0001_initial','2019-11-05 08:33:54.493782'),(8,'home','0002_auto_20191105_1127','2019-11-05 08:33:54.565645'),(9,'reversion','0001_initial','2019-11-05 08:33:54.612712'),(10,'sessions','0001_initial','2019-11-05 08:33:54.700743'),(11,'xadmin','0001_initial','2019-11-05 08:33:54.799863'),(12,'users','0002_user_wechat','2019-11-05 08:41:31.422893'),(13,'users','0003_auto_20191108_1053','2019-11-08 02:54:05.105426'),(14,'courses','0001_initial','2019-11-11 04:13:05.631444');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('c4o3b4lqc7k4o5kceb1nvhnk9zcklj2r','YjJkMTM1NTk2Mjg1NjJiM2UzMTFmZWUxNTc5Mjk4OWIyYTRlZTczMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudXRpbHMuVXNlcm5hbWVNb2JpbGVBdXRoQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjNmNjBlZmQ1MjZjYjQ1MGJlODgxOTdmNGUwMjg2Y2M5ZDljNTUzMWQiLCJMSVNUX1FVRVJZIjpbWyJ1c2VycyIsInVzZXIiXSwiIl19','2019-11-21 00:53:49.966277');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ly_banner`
--

DROP TABLE IF EXISTS `ly_banner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ly_banner` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `image` varchar(100) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `link` varchar(512) DEFAULT NULL,
  `orders` int(11) NOT NULL,
  `is_show` tinyint(1) NOT NULL,
  `note` longtext NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ly_banner`
--

LOCK TABLES `ly_banner` WRITE;
/*!40000 ALTER TABLE `ly_banner` DISABLE KEYS */;
INSERT INTO `ly_banner` VALUES (1,'banner/banner1.png','小米的广告','http://www.baidu.com',1,1,'李老板的广告，电话：13355567778',0,'2019-11-05 03:27:17.149296','2019-11-05 03:27:17.214819'),(2,'banner/banner2.png','小明de广告','http://www.luffycity.com',2,1,'xxxx',0,'2019-11-05 03:27:17.149296','2019-11-05 03:27:17.214819');
/*!40000 ALTER TABLE `ly_banner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ly_course`
--

DROP TABLE IF EXISTS `ly_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ly_course` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `orders` int(11) NOT NULL,
  `is_show` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `name` varchar(128) NOT NULL,
  `course_img` varchar(255) DEFAULT NULL,
  `course_video` varchar(255) DEFAULT NULL,
  `course_type` smallint(6) NOT NULL,
  `brief` longtext,
  `level` smallint(6) NOT NULL,
  `pub_date` date NOT NULL,
  `period` int(11) NOT NULL,
  `attachment_path` varchar(128) DEFAULT NULL,
  `status` smallint(6) NOT NULL,
  `students` int(11) NOT NULL,
  `lessons` int(11) NOT NULL,
  `pub_lessons` int(11) NOT NULL,
  `price` decimal(6,2) NOT NULL,
  `course_category_id` int(11) DEFAULT NULL,
  `teacher_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ly_course_course_category_id_0fae919c_fk_ly_course_category_id` (`course_category_id`),
  KEY `ly_course_teacher_id_1a7162ce_fk_ly_teacher_id` (`teacher_id`),
  CONSTRAINT `ly_course_course_category_id_0fae919c_fk_ly_course_category_id` FOREIGN KEY (`course_category_id`) REFERENCES `ly_course_category` (`id`),
  CONSTRAINT `ly_course_teacher_id_1a7162ce_fk_ly_teacher_id` FOREIGN KEY (`teacher_id`) REFERENCES `ly_teacher` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ly_course`
--

LOCK TABLES `ly_course` WRITE;
/*!40000 ALTER TABLE `ly_course` DISABLE KEYS */;
/*!40000 ALTER TABLE `ly_course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ly_course_category`
--

DROP TABLE IF EXISTS `ly_course_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ly_course_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `orders` int(11) NOT NULL,
  `is_show` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ly_course_category`
--

LOCK TABLES `ly_course_category` WRITE;
/*!40000 ALTER TABLE `ly_course_category` DISABLE KEYS */;
INSERT INTO `ly_course_category` VALUES (1,1,1,0,'2019-11-11 04:16:47.368781','2019-11-11 04:16:47.368821','python'),(2,1,1,0,'2019-11-11 04:16:52.647303','2019-11-11 04:16:52.647347','python进阶'),(3,1,1,0,'2019-11-11 04:16:57.121726','2019-11-11 04:16:57.121767','Linux运维'),(4,1,1,0,'2019-11-11 04:17:00.762881','2019-11-11 04:17:00.762934','go语言');
/*!40000 ALTER TABLE `ly_course_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ly_course_chapter`
--

DROP TABLE IF EXISTS `ly_course_chapter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ly_course_chapter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `orders` int(11) NOT NULL,
  `is_show` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `chapter` smallint(6) NOT NULL,
  `name` varchar(128) NOT NULL,
  `summary` longtext,
  `pub_date` date NOT NULL,
  `course_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ly_course_chapter_course_id_e677b55c_fk_ly_course_id` (`course_id`),
  CONSTRAINT `ly_course_chapter_course_id_e677b55c_fk_ly_course_id` FOREIGN KEY (`course_id`) REFERENCES `ly_course` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ly_course_chapter`
--

LOCK TABLES `ly_course_chapter` WRITE;
/*!40000 ALTER TABLE `ly_course_chapter` DISABLE KEYS */;
/*!40000 ALTER TABLE `ly_course_chapter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ly_course_lesson`
--

DROP TABLE IF EXISTS `ly_course_lesson`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ly_course_lesson` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `orders` int(11) NOT NULL,
  `is_show` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `name` varchar(128) NOT NULL,
  `lesson_type` smallint(6) NOT NULL,
  `lesson_link` varchar(255) DEFAULT NULL,
  `duration` varchar(32) DEFAULT NULL,
  `pub_date` datetime(6) NOT NULL,
  `free_trail` tinyint(1) NOT NULL,
  `recomment` tinyint(1) NOT NULL,
  `chapter_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ly_course_lesson_chapter_id_09ff8644_fk_ly_course_chapter_id` (`chapter_id`),
  KEY `ly_course_lesson_course_id_1e932817_fk_ly_course_id` (`course_id`),
  CONSTRAINT `ly_course_lesson_chapter_id_09ff8644_fk_ly_course_chapter_id` FOREIGN KEY (`chapter_id`) REFERENCES `ly_course_chapter` (`id`),
  CONSTRAINT `ly_course_lesson_course_id_1e932817_fk_ly_course_id` FOREIGN KEY (`course_id`) REFERENCES `ly_course` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ly_course_lesson`
--

LOCK TABLES `ly_course_lesson` WRITE;
/*!40000 ALTER TABLE `ly_course_lesson` DISABLE KEYS */;
/*!40000 ALTER TABLE `ly_course_lesson` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ly_nav`
--

DROP TABLE IF EXISTS `ly_nav`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ly_nav` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `orders` int(11) NOT NULL,
  `is_show` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `name` varchar(50) NOT NULL,
  `link` varchar(250) NOT NULL,
  `opt` smallint(6) NOT NULL,
  `is_http` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ly_nav`
--

LOCK TABLES `ly_nav` WRITE;
/*!40000 ALTER TABLE `ly_nav` DISABLE KEYS */;
INSERT INTO `ly_nav` VALUES (1,1,1,0,'2019-11-05 03:36:13.964197','2019-11-05 03:36:13.964232','免费课','/free',0,0),(2,1,1,0,'2019-11-05 03:36:29.554709','2019-11-05 03:36:29.554759','实战课','/courses',0,0),(3,1,1,0,'2019-11-05 03:36:49.294737','2019-11-05 03:36:49.294791','轻课','/light',0,0),(4,1,1,0,'2019-11-05 03:37:10.361508','2019-11-05 03:37:10.361552','老男孩教育','https://www.luffycity.com/home',0,1),(5,1,1,0,'2019-11-05 03:37:31.187057','2019-11-05 03:37:31.187098','关于我们','/about',1,0),(6,1,1,0,'2019-11-05 03:37:49.104235','2019-11-05 03:37:49.104271','联系我们','/concat',1,0),(7,1,1,0,'2019-11-05 03:38:02.798586','2019-11-05 04:21:52.525588','百度','http://www.baidu.com',1,1);
/*!40000 ALTER TABLE `ly_nav` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ly_teacher`
--

DROP TABLE IF EXISTS `ly_teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ly_teacher` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `orders` int(11) NOT NULL,
  `is_show` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `name` varchar(32) NOT NULL,
  `role` smallint(6) NOT NULL,
  `title` varchar(64) NOT NULL,
  `signature` varchar(255) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `brief` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ly_teacher`
--

LOCK TABLES `ly_teacher` WRITE;
/*!40000 ALTER TABLE `ly_teacher` DISABLE KEYS */;
/*!40000 ALTER TABLE `ly_teacher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ly_users`
--

DROP TABLE IF EXISTS `ly_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ly_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `mobile` varchar(15) NOT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `wechat` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `mobile` (`mobile`),
  UNIQUE KEY `wechat` (`wechat`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ly_users`
--

LOCK TABLES `ly_users` WRITE;
/*!40000 ALTER TABLE `ly_users` DISABLE KEYS */;
INSERT INTO `ly_users` VALUES (1,'pbkdf2_sha256$150000$mhMYhCwPtxEa$wsGhoIMa9MKCZWkuKSlOpPgBLqwkhu1YFK21KPxbxRg=','2019-11-08 02:15:25.853554',1,'root','','','',1,1,'2019-11-05 08:38:00.000000','13312341234','avatar/member.png',''),(8,'pbkdf2_sha256$150000$Z0OebuisJQb9$ilpZq8PMpY3W6OklXUEkyQCnGdZQpzjmnUOMxRqW07M=',NULL,0,'15910967252','','','',0,1,'2019-11-08 09:05:52.692620','15910967252','',NULL);
/*!40000 ALTER TABLE `ly_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ly_users_groups`
--

DROP TABLE IF EXISTS `ly_users_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ly_users_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ly_users_groups_user_id_group_id_e3b73a35_uniq` (`user_id`,`group_id`),
  KEY `ly_users_groups_group_id_7505a66d_fk_auth_group_id` (`group_id`),
  CONSTRAINT `ly_users_groups_group_id_7505a66d_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `ly_users_groups_user_id_b293b4e8_fk_ly_users_id` FOREIGN KEY (`user_id`) REFERENCES `ly_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ly_users_groups`
--

LOCK TABLES `ly_users_groups` WRITE;
/*!40000 ALTER TABLE `ly_users_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `ly_users_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ly_users_user_permissions`
--

DROP TABLE IF EXISTS `ly_users_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ly_users_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ly_users_user_permissions_user_id_permission_id_5b1027ec_uniq` (`user_id`,`permission_id`),
  KEY `ly_users_user_permis_permission_id_14148e4f_fk_auth_perm` (`permission_id`),
  CONSTRAINT `ly_users_user_permis_permission_id_14148e4f_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `ly_users_user_permissions_user_id_047a052d_fk_ly_users_id` FOREIGN KEY (`user_id`) REFERENCES `ly_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ly_users_user_permissions`
--

LOCK TABLES `ly_users_user_permissions` WRITE;
/*!40000 ALTER TABLE `ly_users_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `ly_users_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reversion_revision`
--

DROP TABLE IF EXISTS `reversion_revision`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reversion_revision` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_created` datetime(6) NOT NULL,
  `comment` longtext NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `reversion_revision_user_id_17095f45_fk_ly_users_id` (`user_id`),
  KEY `reversion_revision_date_created_96f7c20c` (`date_created`),
  CONSTRAINT `reversion_revision_user_id_17095f45_fk_ly_users_id` FOREIGN KEY (`user_id`) REFERENCES `ly_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reversion_revision`
--

LOCK TABLES `reversion_revision` WRITE;
/*!40000 ALTER TABLE `reversion_revision` DISABLE KEYS */;
/*!40000 ALTER TABLE `reversion_revision` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reversion_version`
--

DROP TABLE IF EXISTS `reversion_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reversion_version` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` varchar(191) NOT NULL,
  `db` varchar(191) NOT NULL,
  `format` varchar(255) NOT NULL,
  `serialized_data` longtext NOT NULL,
  `object_repr` longtext NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `revision_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `reversion_version_db_content_type_id_objec_b2c54f65_uniq` (`db`,`content_type_id`,`object_id`,`revision_id`),
  KEY `reversion_version_content_type_id_7d0ff25c_fk_django_co` (`content_type_id`),
  KEY `reversion_version_revision_id_af9f6a9d_fk_reversion_revision_id` (`revision_id`),
  CONSTRAINT `reversion_version_content_type_id_7d0ff25c_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `reversion_version_revision_id_af9f6a9d_fk_reversion_revision_id` FOREIGN KEY (`revision_id`) REFERENCES `reversion_revision` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reversion_version`
--

LOCK TABLES `reversion_version` WRITE;
/*!40000 ALTER TABLE `reversion_version` DISABLE KEYS */;
/*!40000 ALTER TABLE `reversion_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `xadmin_bookmark`
--

DROP TABLE IF EXISTS `xadmin_bookmark`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xadmin_bookmark` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(128) NOT NULL,
  `url_name` varchar(64) NOT NULL,
  `query` varchar(1000) NOT NULL,
  `is_share` tinyint(1) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `xadmin_bookmark_content_type_id_60941679_fk_django_co` (`content_type_id`),
  KEY `xadmin_bookmark_user_id_42d307fc_fk_ly_users_id` (`user_id`),
  CONSTRAINT `xadmin_bookmark_content_type_id_60941679_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `xadmin_bookmark_user_id_42d307fc_fk_ly_users_id` FOREIGN KEY (`user_id`) REFERENCES `ly_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `xadmin_bookmark`
--

LOCK TABLES `xadmin_bookmark` WRITE;
/*!40000 ALTER TABLE `xadmin_bookmark` DISABLE KEYS */;
/*!40000 ALTER TABLE `xadmin_bookmark` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `xadmin_log`
--

DROP TABLE IF EXISTS `xadmin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xadmin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `ip_addr` char(39) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` varchar(32) NOT NULL,
  `message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `xadmin_log_content_type_id_2a6cb852_fk_django_content_type_id` (`content_type_id`),
  KEY `xadmin_log_user_id_bb16a176_fk_ly_users_id` (`user_id`),
  CONSTRAINT `xadmin_log_content_type_id_2a6cb852_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `xadmin_log_user_id_bb16a176_fk_ly_users_id` FOREIGN KEY (`user_id`) REFERENCES `ly_users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `xadmin_log`
--

LOCK TABLES `xadmin_log` WRITE;
/*!40000 ALTER TABLE `xadmin_log` DISABLE KEYS */;
INSERT INTO `xadmin_log` VALUES (1,'2019-11-05 08:39:18.132472','127.0.0.1','1','root','change','修改 last_login，mobile 和 avatar',14,1),(2,'2019-11-11 04:16:47.370453','127.0.0.1','1','python','create','已添加。',19,1),(3,'2019-11-11 04:16:52.648700','127.0.0.1','2','python进阶','create','已添加。',19,1),(4,'2019-11-11 04:16:57.122333','127.0.0.1','3','Linux运维','create','已添加。',19,1),(5,'2019-11-11 04:17:00.766170','127.0.0.1','4','go语言','create','已添加。',19,1);
/*!40000 ALTER TABLE `xadmin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `xadmin_usersettings`
--

DROP TABLE IF EXISTS `xadmin_usersettings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xadmin_usersettings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(256) NOT NULL,
  `value` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `xadmin_usersettings_user_id_edeabe4a_fk_ly_users_id` (`user_id`),
  CONSTRAINT `xadmin_usersettings_user_id_edeabe4a_fk_ly_users_id` FOREIGN KEY (`user_id`) REFERENCES `ly_users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `xadmin_usersettings`
--

LOCK TABLES `xadmin_usersettings` WRITE;
/*!40000 ALTER TABLE `xadmin_usersettings` DISABLE KEYS */;
INSERT INTO `xadmin_usersettings` VALUES (1,'dashboard:home:pos','',1);
/*!40000 ALTER TABLE `xadmin_usersettings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `xadmin_userwidget`
--

DROP TABLE IF EXISTS `xadmin_userwidget`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xadmin_userwidget` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `page_id` varchar(256) NOT NULL,
  `widget_type` varchar(50) NOT NULL,
  `value` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `xadmin_userwidget_user_id_c159233a_fk_ly_users_id` (`user_id`),
  CONSTRAINT `xadmin_userwidget_user_id_c159233a_fk_ly_users_id` FOREIGN KEY (`user_id`) REFERENCES `ly_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `xadmin_userwidget`
--

LOCK TABLES `xadmin_userwidget` WRITE;
/*!40000 ALTER TABLE `xadmin_userwidget` DISABLE KEYS */;
/*!40000 ALTER TABLE `xadmin_userwidget` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-11-11 12:28:51
