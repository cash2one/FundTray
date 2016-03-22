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

/*Table structure for table `accept_help` */

DROP TABLE IF EXISTS `accept_help`;

CREATE TABLE `accept_help` (
  `accept_order` varchar(32) COLLATE utf8_bin NOT NULL COMMENT '接受帮助订单id',
  `accept_uid` int(11) unsigned NOT NULL COMMENT '接受帮助玩家id',
  `accept_stime` int(11) unsigned NOT NULL COMMENT '接受帮助开始时间',
  `accept_money` int(11) unsigned NOT NULL COMMENT '接受帮助金额',
  `accept_lmoney` int(11) unsigned NOT NULL COMMENT '剩余接受帮助金额',
  `accept_stat` tinyint(2) unsigned NOT NULL COMMENT '接受帮助状态:0匹配中, 1完成',
  PRIMARY KEY (`accept_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='接受帮助';

/*Data for the table `accept_help` */

insert  into `accept_help`(`accept_order`,`accept_uid`,`accept_stime`,`accept_money`,`accept_lmoney`,`accept_stat`) values ('8888',18888,UNIX_TIMESTAMP(NOW()),4294967295,4294967295,0);

/*Table structure for table `accept_help_req` */

DROP TABLE IF EXISTS `accept_help_req`;

CREATE TABLE `accept_help_req` (
  `id` varchar(32) COLLATE utf8_bin NOT NULL COMMENT '请求id,没有意义',
  `accept_req_uid` int(11) unsigned NOT NULL COMMENT '接受帮助请求玩家id',
  `accept_req_time` int(11) unsigned NOT NULL COMMENT '接受帮助请求时间',
  `accept_req_money` int(11) unsigned NOT NULL COMMENT '接受帮助请求金额',
  `accept_req_stat` tinyint(2) unsigned NOT NULL COMMENT '接受帮助请求状态:0申请, 1完成',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='接受帮助请求';

/*Data for the table `accept_help_req` */

/*Table structure for table `apply_help` */

DROP TABLE IF EXISTS `apply_help`;

CREATE TABLE `apply_help` (
  `apply_sorder` varchar(32) COLLATE utf8_bin NOT NULL COMMENT '申请帮助子订单id',
  `accept_order` varchar(32) COLLATE utf8_bin NOT NULL COMMENT '接收帮助订单id',
  `apply_order` varchar(32) COLLATE utf8_bin NOT NULL COMMENT '申请帮助订单id',
  `apply_uid` int(11) unsigned NOT NULL COMMENT '申请帮助玩家id',
  `apply_money` int(11) unsigned NOT NULL COMMENT '申请帮助金额',
  `apply_stime` int(11) unsigned NOT NULL COMMENT '申请帮助开始时间',
  `apply_ptime` int(11) unsigned DEFAULT NULL COMMENT '申请帮助支付时间',
  `apply_interest` int(11) unsigned NOT NULL COMMENT '申请帮助利息',
  `apply_piture` tinytext COLLATE utf8_bin COMMENT '申请帮助支付截图',
  `apply_message` tinytext COLLATE utf8_bin COMMENT '申请帮助留言',
  `apply_stat` tinyint(2) unsigned NOT NULL COMMENT '申请帮助状态:0等待支付, 1已经支付,2确认支付,3取消,4完成',
  PRIMARY KEY (`apply_sorder`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='申请帮助';

/*Data for the table `apply_help` */

/*Table structure for table `apply_help_req` */

DROP TABLE IF EXISTS `apply_help_req`;

CREATE TABLE `apply_help_req` (
  `id` varchar(32) COLLATE utf8_bin NOT NULL COMMENT '请求id,没有意义',
  `apply_req_uid` int(11) unsigned NOT NULL COMMENT '申请帮助请求玩家id',
  `apply_req_time` int(11) unsigned NOT NULL COMMENT '申请帮助请求时间',
  `apply_req_money` int(11) unsigned NOT NULL COMMENT '申请帮助请求金额',
  `apply_req_stat` tinyint(2) unsigned NOT NULL COMMENT '申请帮助请求状态:0申请, 1匹配中,2 完成',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='申请帮助请求';

/*Data for the table `apply_help_req` */

/*Table structure for table `server_info` */

DROP TABLE IF EXISTS `server_info`;

CREATE TABLE `server_info` (
  `start_time` int(11) unsigned NOT NULL COMMENT '开始时间',
  `apply_match_min_days` tinyint(1) NOT NULL COMMENT '申请帮助至少匹配时间(天)',
  `apply_match_max_days` tinyint(1) NOT NULL COMMENT '申请帮助最多匹配时间(天)',
  `apply_pay_max_days` tinyint(1) NOT NULL COMMENT '申请帮助最多支付时间(天)',
  `accept_match_min_days` tinyint(1) NOT NULL COMMENT '接受帮助至少匹配时间(天)',
  `apply_interest` tinyint(1) NOT NULL COMMENT '申请帮助利息(百分比)',
  `pay_timely_rwd_hours` tinyint(1) NOT NULL COMMENT '及时打款奖励区间(小时)',
  `pay_timely_rwd_int` tinyint(1) NOT NULL COMMENT '及时打款利息奖励(百分比)',
  `cfmd_timely_rwd_hours` tinyint(1) NOT NULL COMMENT '及时打款奖励区间(小时)',
  `cfmd_timely_rwd_int` tinyint(1) NOT NULL COMMENT '及时收款确认利息奖励(百分比)',
  `day_seconds` int(11) NOT NULL COMMENT '一天的秒数',
  PRIMARY KEY (`start_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Data for the table `server_info` */

insert  into `server_info`(`start_time`,`apply_match_min_days`,`apply_match_max_days`,`apply_pay_max_days`,`accept_match_min_days`,`apply_interest`,`pay_timely_rwd_hours`,`pay_timely_rwd_int`,`cfmd_timely_rwd_hours`,`cfmd_timely_rwd_int`,`day_seconds`) values (UNIX_TIMESTAMP(NOW()),3,7,1,2,3,4,1,4,1,86400);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
