/*
SQLyog Ultimate v11.28 (64 bit)
MySQL - 5.5.41-0ubuntu0.14.04.1-log : Database - service_mgr
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`service_mgr` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;

/*Table structure for table `db_version` */

DROP TABLE IF EXISTS `db_version`;

CREATE TABLE `db_version` (
  `db_version` int(11) NOT NULL DEFAULT '1' COMMENT '数据库版本'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Data for the table `db_version` */

insert  into `db_version`(`db_version`) values (1);

/*Table structure for table `grant_machine` */

DROP TABLE IF EXISTS `grant_machine`;

CREATE TABLE `grant_machine` (
  `ip` varchar(20) COLLATE utf8_bin NOT NULL COMMENT 'IP',
  `os` varchar(20) COLLATE utf8_bin NOT NULL COMMENT '操作系统:windos/linux',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='授权机器信息';

/*Data for the table `grant_machine` */

insert  into `grant_machine`(`ip`,`os`,`create_time`) values ('10.24.6.170','WINDOWS','2015-05-27 17:55:32'),('10.24.6.187','WINDOWS','2015-07-02 13:45:33');

/*Table structure for table `service` */

DROP TABLE IF EXISTS `service`;

CREATE TABLE `service` (
  `id` int(11) NOT NULL COMMENT '服务id',
  `ip` varchar(200) COLLATE utf8_bin NOT NULL COMMENT '机器id,IP',
  `service_group` varchar(20) COLLATE utf8_bin NOT NULL COMMENT '服务器组id',
  `port` varchar(200) COLLATE utf8_bin NOT NULL COMMENT '端口,字典形式:{"http_port":1,"tcp_port":2}',
  `params` tinytext COLLATE utf8_bin NOT NULL COMMENT '附加参数,字典形式:{K:V}',
  `state` tinyint(3) NOT NULL DEFAULT '0' COMMENT '状态:0:free, 1:subscribe,2:running',
  `start_time` datetime DEFAULT NULL COMMENT '开始时间',
  PRIMARY KEY (`id`),
  KEY `service_service_group` (`service_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='服务启动实例表';

/*Data for the table `service` */

insert  into `service`(`id`,`ip`,`service_group`,`port`,`params`,`state`,`start_time`) values (1,'10.24.6.170','mmm','{\"https\":0,\"tcp\":0}','',0,'2015-11-19 16:52:51'),(2,'10.24.6.170','mmm_da','{\"https\":0,\"tcp\":0}','{\"db_name\":\"mmm_db\"}',0,'2015-11-19 16:52:47');

/*Table structure for table `service_group` */

DROP TABLE IF EXISTS `service_group`;

CREATE TABLE `service_group` (
  `id` varchar(20) COLLATE utf8_bin NOT NULL COMMENT '服务器组id=类型',
  `invisible` tinytext COLLATE utf8_bin COMMENT '不可以见的服务列表,list形式,[service,,,,]',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='服务组信息';

/*Data for the table `service_group` */

insert  into `service_group`(`id`,`invisible`) values ('mmm',''),('mmm_da','');

/*Table structure for table `tp_service` */

DROP TABLE IF EXISTS `tp_service`;

CREATE TABLE `tp_service` (
  `id` varchar(50) COLLATE utf8_bin NOT NULL COMMENT 'id',
  `service_group` varchar(20) COLLATE utf8_bin NOT NULL COMMENT '服务器组id',
  `ip` varchar(200) COLLATE utf8_bin NOT NULL COMMENT 'IP',
  `port` varchar(200) COLLATE utf8_bin NOT NULL COMMENT '端口,字典形式:{"http_port":1,"tcp_port":2}',
  `params` tinytext COLLATE utf8_bin COMMENT '附加参数,字典形式:{K:V}',
  PRIMARY KEY (`id`),
  KEY `tp_service_group` (`service_group`),
  CONSTRAINT `tp_service_group` FOREIGN KEY (`service_group`) REFERENCES `service_group` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='第三方服务表';

/*Data for the table `tp_service` */

insert  into `tp_service`(`id`,`service_group`,`ip`,`port`,`params`) values ('10.24.6.5_mysql_01','tp_mysql','10.24.6.5','{\"tcp\":3306}','{\"db_password\":\"!System\",\"db_user\":\"system\"}');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
