/*
SQLyog Ultimate v11.28 (64 bit)
MySQL - 5.5.40-0ubuntu0.14.04.1-log : Database - mmm_db
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


/*Table structure for table `accept_help` */

DROP TABLE IF EXISTS `accept_help`;

CREATE TABLE `accept_help` (
  `accept_id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '接受id',
  `accept_uid` int(11) unsigned NOT NULL COMMENT '接受玩家id',
  `accept_time` int(11) unsigned NOT NULL COMMENT '申请接受时间',
  `accept_money` int(11) unsigned NOT NULL COMMENT '接受金额',
  `left_accept_money` int(11) unsigned NOT NULL COMMENT '剩余接受金额',
  PRIMARY KEY (`accept_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='接受帮助';

/*Data for the table `accept_help` */

/*Table structure for table `apply_help` */

DROP TABLE IF EXISTS `apply_help`;

CREATE TABLE `apply_help` (
  `apply_id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '帮助id',
  `apply_uid` int(11) unsigned NOT NULL COMMENT '帮助玩家id',
  `accept_id` int(11) unsigned NOT NULL COMMENT '申请帮助id',
  `apply_money` int(11) unsigned NOT NULL COMMENT '帮助金额',
  `apply_start_time` int(11) unsigned NOT NULL COMMENT '帮助开始时间',
  `apply_pay_time` int(11) unsigned NOT NULL COMMENT '帮助支付时间',
  `apply_interest` int(11) unsigned NOT NULL COMMENT '帮助利息',
  `stat` tinyint(2) unsigned NOT NULL COMMENT '帮助状态:0未支付, 1支付完成，2未确认,3确认,4取消',
  PRIMARY KEY (`apply_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='申请帮助';

/*Data for the table `apply_help` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
