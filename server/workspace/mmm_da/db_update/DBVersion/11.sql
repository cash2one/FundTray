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
  ADD COLUMN `active_coin_loss` INT(3) NOT NULL  COMMENT '激活币每次激活消耗(整形)' AFTER `notice`,
  ADD COLUMN `match_coin_loss` INT(3) NOT NULL  COMMENT '排单币每次排单消耗(百分比)' AFTER `active_coin_loss`,
  ADD COLUMN `apply_paid_reward` INT(3) NOT NULL  COMMENT '申请帮助完成奖励(百分比)' AFTER `match_coin_loss`,
  ADD COLUMN `apply_unpaid_punish` INT(3) NOT NULL  COMMENT '申请帮助未完成惩罚(百分比)' AFTER `apply_paid_reward`,
  ADD COLUMN `system_balance` INT(11) NOT NULL  COMMENT '系统净差额= 申请帮助总额-接受帮助总额' AFTER `apply_unpaid_punish`,
  ADD COLUMN `total_apply_money` INT(11) DEFAULT 0  NOT NULL  COMMENT '申请帮助总额' AFTER `system_balance`,
  ADD COLUMN `total_accept_money` INT(11) DEFAULT 0  NOT NULL  COMMENT '接受帮助总额' AFTER `total_apply_money`;

UPDATE `server_info` SET `active_coin_loss` =1, `match_coin_loss`=5, `apply_paid_reward`=5, `apply_unpaid_punish`=20, `system_balance`= 2000000, `apply_interest`=1,`pay_timely_rwd_hours`=3, `pay_timely_rwd_int`=1;
  
ALTER TABLE `account`   
  ADD COLUMN `match_coin` INT(11) DEFAULT 0  NOT NULL  COMMENT '排单币' AFTER `active_coin`,
  ADD COLUMN `max_apply_money` INT(11) DEFAULT 1000  NOT NULL  COMMENT '当前最大的申请帮助金额' AFTER `finished_accept`;
  
  
UPDATE `account` SET `match_coin` = 1000000000 WHERE id = '18888';


/*Table structure for table `bonus_log` */

DROP TABLE IF EXISTS `bonus_log`;

CREATE TABLE `bonus_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id,无意义',
  `afctd_uid` varchar(20) COLLATE utf8_bin NOT NULL COMMENT '被奖励的uid',
  `afct_uid` varchar(20) COLLATE utf8_bin NOT NULL COMMENT '奖励的uid',
  `afct_bonus` int(11) NOT NULL COMMENT '奖金',
  `afct_time` int(11) NOT NULL COMMENT '奖励时间',
  `afct_type` int(3) NOT NULL COMMENT '奖金类型',
  PRIMARY KEY (`id`),
  KEY `afct_relations` (`afctd_uid`,`afct_uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Data for the table `bonus_log` */


/*Table structure for table `history_noticce` */

DROP TABLE IF EXISTS `history_noticce`;

CREATE TABLE `history_noticce`(  
  `id` INT NOT NULL AUTO_INCREMENT COMMENT 'id,没有意义',
  `notice` TEXT NOT NULL COMMENT '公告',
  `time` INT(11) NOT NULL COMMENT '公告时间',
  PRIMARY KEY (`id`)
) ENGINE=INNODB CHARSET=utf8 COLLATE=utf8_bin
COMMENT='历史公告';


/*Data for the table `history_noticce` */


/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
