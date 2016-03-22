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
  `accept_order` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '接受订单id',
  `accept_uid` int(11) unsigned NOT NULL COMMENT '接受玩家id',
  `accept_time` int(11) unsigned NOT NULL COMMENT '申请接受时间',
  `accept_money` int(11) unsigned NOT NULL COMMENT '接受金额',
  `left_accept_money` int(11) unsigned NOT NULL COMMENT '剩余接受金额',
  PRIMARY KEY (`accept_order`)
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='接受帮助';

/*Data for the table `accept_help` */

/* 初始化系统默认接受帮助信息 */

insert  into `accept_help`(`accept_order`,`accept_uid`,`accept_time`,`accept_money`,`left_accept_money`) values (8888,18888,UNIX_TIMESTAMP(NOW()),4294967295,4294967295);

/*Table structure for table `apply_help` */

DROP TABLE IF EXISTS `apply_help`;

CREATE TABLE `apply_help` (
  `apply_id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '帮助id',
  `apply_uid` int(11) unsigned NOT NULL COMMENT '帮助玩家id',
  `apply_money` int(11) unsigned NOT NULL COMMENT '帮助金额',
  `apply_start_time` int(11) unsigned NOT NULL COMMENT '帮助开始时间',
  `apply_pay_time` int(11) unsigned NOT NULL COMMENT '帮助支付时间',
  `apply_interest` int(11) unsigned NOT NULL COMMENT '帮助利息',
  `stat` tinyint(2) unsigned NOT NULL COMMENT '帮助状态:0未支付, 1支付完成，2未确认,3确认,4本息提取,5取消',
  `message` tinytext COLLATE utf8_bin COMMENT '帮助留言',
  PRIMARY KEY (`apply_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='申请帮助';

/*Data for the table `apply_help` */

/*Table structure for table `help_relations` */

DROP TABLE IF EXISTS `help_relations`;

CREATE TABLE `help_relations` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id，没有意义',
  `accept_order` int(11) unsigned NOT NULL COMMENT '接收帮助订单id',
  `apply_order` int(11) unsigned NOT NULL COMMENT '申请帮助订单id',
  `apply_id` int(11) unsigned NOT NULL COMMENT '申请帮助id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='订单关系表';

/*Data for the table `help_relations` */

/*Table structure for table `server_info` */

DROP TABLE IF EXISTS `server_info`;

CREATE TABLE `server_info` (
  `start_time` int(11) unsigned NOT NULL COMMENT '开始时间',
  `pay_max_days` tinyint(1) NOT NULL COMMENT '申请帮助的时间上限为7天，如果超过7天不打款，封号（天）',
  `apple_interest` tinyint(1) NOT NULL COMMENT '申请帮助利息(百分比)',
  `accept_help_interval` tinyint(1) NOT NULL COMMENT '接收帮助间隔(小时)',
  `pay_timely_rwd_hours` tinyint(1) NOT NULL COMMENT '及时打款奖励区间(小时)',
  `pay_timely_rwd_int` tinyint(1) NOT NULL COMMENT '及时打款利息奖励(百分比)',
  `cfmd_timely_rwd_hours` tinyint(1) NOT NULL COMMENT '及时打款奖励区间(小时)',
  `cfmd_timely_rwd_int` tinyint(1) NOT NULL COMMENT '及时收款确认利息奖励(百分比)',
  PRIMARY KEY (`start_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Data for the table `server_info` */

/* 初始化系统启动时间为执行脚本的当前时间 */
insert  into `server_info`(`start_time`,`pay_max_days`,`apple_interest`,`accept_help_interval`,`pay_timely_rwd_hours`,`pay_timely_rwd_int`,`cfmd_timely_rwd_hours`,`cfmd_timely_rwd_int`) values (UNIX_TIMESTAMP(NOW()),7,3,48,4,1,4,1);



/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
