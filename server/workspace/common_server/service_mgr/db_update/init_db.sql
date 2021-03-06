/*
SQLyog Ultimate v11.28 (64 bit)
MySQL - 5.5.44-0ubuntu0.14.04.1-log : Database - fund_tray_service_mgr
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

/*Table structure for table `tp_service` */

DROP TABLE IF EXISTS `tp_service`;

CREATE TABLE `tp_service` (
  `id` varchar(50) COLLATE utf8_bin NOT NULL COMMENT 'id',
  `service_group` varchar(20) COLLATE utf8_bin NOT NULL COMMENT '服务器组id',
  `ip` varchar(200) COLLATE utf8_bin NOT NULL COMMENT 'IP',
  `port` varchar(200) COLLATE utf8_bin NOT NULL COMMENT '端口,字典形式:{"http_port":1,"tcp_port":2}',
  `params` tinytext COLLATE utf8_bin COMMENT '附加参数,字典形式:{K:V}',
  PRIMARY KEY (`id`),
  KEY `tp_service_group` (`service_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='第三方服务表';

/*Data for the table `tp_service` */

insert  into `tp_service`(`id`,`service_group`,`ip`,`port`,`params`) values ('10.24.6.7_mysql_01','tp_mysql','10.24.6.7','{\"tcp\":3306}','{\"db_password\":\"!System\",\"db_user\":\"system\"}');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
