/*
SQLyog Ultimate v11.28 (64 bit)
MySQL - 5.5.44-0ubuntu0.14.04.1-log : Database - mmm_db
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

/*Table structure for table `apply_help_wait` */

DROP TABLE IF EXISTS `apply_help_wait`;

CREATE TABLE `apply_help_wait` (
  `apply_wait_uid` varchar(20) COLLATE utf8_bin NOT NULL COMMENT '等待申请帮助玩家id',
  `apply_wait_time` int(11) unsigned NOT NULL COMMENT '等待申请帮助开始时间',
  PRIMARY KEY (`apply_wait_uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

ALTER TABLE `server_info`   
  ADD COLUMN `apply_aft_accept_hour` INT(11) DEFAULT 1  NOT NULL  COMMENT '接受帮助后必须申请帮助的时间间隔' AFTER `total_accept_factor`;

/*Data for the table `apply_help_wait` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
