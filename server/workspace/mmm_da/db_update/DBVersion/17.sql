/*
SQLyog Ultimate v11.28 (64 bit)
MySQL - 5.5.41-0ubuntu0.14.04.1-log : Database - mmm
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

ALTER TABLE `server_info`   
  ADD COLUMN `total_apply_cnt` INT(11) DEFAULT 0  NOT NULL  COMMENT '申请帮助总数' AFTER `min_unique_id`,
  ADD COLUMN `total_accept_cnt` INT(11) DEFAULT 0  NOT NULL  COMMENT '接受帮助总数' AFTER `total_apply_cnt`,
  ADD COLUMN `total_apply_factor` INT(11) DEFAULT 10000  NOT NULL  COMMENT '申请帮助总数因子' AFTER `total_accept_cnt`,
  ADD COLUMN `total_accept_factor` INT(11) DEFAULT 200  NOT NULL  COMMENT '接受帮助总数因子' AFTER `total_apply_factor`;


/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
