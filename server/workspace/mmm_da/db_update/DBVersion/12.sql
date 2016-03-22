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
  DROP COLUMN `pay_timely_rwd_hours`, 
  DROP COLUMN `pay_timely_rwd_int`, 
  DROP COLUMN `cfmd_timely_rwd_hours`, 
  DROP COLUMN `cfmd_timely_rwd_int`, 
  ADD COLUMN `pay_reward_dic` TINYTEXT NOT NULL  COMMENT '打款奖励{小时:奖励百分比}' AFTER `apply_interest`,
  ADD COLUMN `cfmd_reward_dic` TINYTEXT NOT NULL  COMMENT '打款确认奖励{小时:奖励百分比}' AFTER `pay_reward_dic`;
  
  
UPDATE server_info SET pay_reward_dic = '{"3":1,"5":0.5}', cfmd_reward_dic = '{"4":1}';


/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
