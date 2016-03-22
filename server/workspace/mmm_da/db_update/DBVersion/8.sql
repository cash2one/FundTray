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
  ADD COLUMN `notice` TEXT NULL  COMMENT '网站公告' AFTER `min_account_id`;
  
UPDATE `server_info` SET `notice` = '固定收益都是30%利息！  当有人需要资金帮助时，你就可以把你的资金打给对方！ 当你需要资金帮助时，你就可以在平台内提出申请，等待别人帮助。就这样，不断的提供帮助和接受帮助，每个月30%的收益你就可以赚到。资金不经过互助系统平台，而是会员之间相互转账，没有任何风险。';

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
