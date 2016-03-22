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



DROP TABLE IF EXISTS `help_relations`;

/*Table structure for table `apply_help` */

DROP TABLE IF EXISTS `apply_help`;

CREATE TABLE `apply_help` (
  `apply_order` varchar(32) COLLATE utf8_bin NOT NULL COMMENT '申请帮助订单id',
  `apply_uid` varchar(20) COLLATE utf8_bin NOT NULL COMMENT '申请帮助玩家id',
  `apply_stime` int(11) unsigned NOT NULL COMMENT '申请帮助开始时间',
  `apply_money` int(11) unsigned NOT NULL COMMENT '申请帮助金额',
  `apply_lmoney` int(11) unsigned NOT NULL COMMENT '申请帮助剩余金额',
  `apply_stat` tinyint(2) unsigned NOT NULL COMMENT '申请帮助状态:0匹配中, 1完成',
  PRIMARY KEY (`apply_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='申请帮助';

/*Data for the table `apply_help` */


/*Table structure for table `apply_help_pay` */

DROP TABLE IF EXISTS `apply_help_pay`;

CREATE TABLE `apply_help_pay` (
  `apply_sorder` varchar(32) COLLATE utf8_bin NOT NULL COMMENT '申请帮助子订单id',
  `accept_order` varchar(32) COLLATE utf8_bin NOT NULL COMMENT '接收帮助订单id',
  `apply_order` varchar(32) COLLATE utf8_bin NOT NULL COMMENT '申请帮助订单id',
  `apply_pmoney` int(11) unsigned NOT NULL COMMENT '申请帮助支付金额',
  `apply_pstat` tinyint(2) unsigned NOT NULL COMMENT '申请帮助支付状态:0等待支付, 1已经支付,2确认支付,3支付异常,4支付取消',
  `apply_ptime` int(11) unsigned DEFAULT NULL COMMENT '申请帮助支付时间',
  `apply_interest` int(11) unsigned NOT NULL COMMENT '申请帮助利息',
  `apply_piture` tinytext COLLATE utf8_bin COMMENT '申请帮助支付截图',
  `apply_message` tinytext COLLATE utf8_bin COMMENT '申请帮助留言',
  PRIMARY KEY (`apply_sorder`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='申请帮助支付信息表';

/*Data for the table `apply_help_pay` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
