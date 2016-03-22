/*
SQLyog Ultimate v11.28 (64 bit)
MySQL - 5.5.41-0ubuntu0.14.04.1-log : Database - mmm_db
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

/*Table structure for table `account` */

DROP TABLE IF EXISTS `account`;

CREATE TABLE `account` (
  `id` int(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `account` varchar(50) COLLATE utf8_bin NOT NULL COMMENT '账号',
  `passwd` varchar(50) COLLATE utf8_bin NOT NULL COMMENT '密码',
  `id_card` varchar(20) COLLATE utf8_bin NOT NULL COMMENT '身份证号码',
  `email` varchar(50) COLLATE utf8_bin NOT NULL COMMENT '邮箱',
  `phone` varchar(11) COLLATE utf8_bin NOT NULL COMMENT '手机号码',
  `leader_id` varchar(50) COLLATE utf8_bin NOT NULL COMMENT '领导人账号',
  `bank` varchar(20) COLLATE utf8_bin NOT NULL COMMENT '开户行',
  `bank_address` varchar(100) COLLATE utf8_bin NOT NULL COMMENT '开户支行',
  `bank_account` varchar(20) COLLATE utf8_bin NOT NULL COMMENT '开户账号',
  `bank_name` varchar(20) COLLATE utf8_bin NOT NULL COMMENT '开户名称',
  `wechat` varchar(50) COLLATE utf8_bin DEFAULT NULL COMMENT '微信',
  `alipay` varchar(50) COLLATE utf8_bin DEFAULT NULL COMMENT '支付宝',
  `create_time` int(11) NOT NULL COMMENT '创建时间',
  `active_coin` int(11) DEFAULT '0' COMMENT '激活币',
  `active_time` int(11) DEFAULT NULL COMMENT '激活时间',
  `active_stat` tinyint(1) DEFAULT '0' COMMENT '激活状态：0未激活,1激活',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=80000 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='账号表';

/*Data for the table `account` */
insert  into `account`(`id`,`account`,`passwd`,`id_card`,`email`,`phone`,`leader_id`,`bank`,`bank_address`,`bank_account`,`bank_name`,`wechat`,`alipay`,`create_time`,`active_coin`,`active_time`,`active_stat`) values (18888,'admin01','!Admin01','350481198604321234','jnijichanch@163.com','18610234567','0000','中国建设银行','中国建设银行厦门江头支行','62216800111198763','杜若飞','niamgeb','jnijichanch@163.com',1450230011,1000000000,1450230011,1);

/*Table structure for table `db_version` */

DROP TABLE IF EXISTS `db_version`;

CREATE TABLE `db_version` (
  `db_version` int(11) NOT NULL DEFAULT '1' COMMENT '数据库版本'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Data for the table `db_version` */

insert  into `db_version`(`db_version`) values (1);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
