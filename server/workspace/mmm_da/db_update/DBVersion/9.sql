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

ALTER TABLE `account`   
  ADD COLUMN `mafuluo` INT(11) DEFAULT 0  NOT NULL  COMMENT '钱包余额，马夫罗' AFTER `stat`,
  ADD COLUMN `finished_apply` INT(11) DEFAULT 0  NOT NULL  COMMENT '完成的申请帮助订单数' AFTER `mafuluo`,
  ADD COLUMN `finished_accept` INT(11) DEFAULT 0  NOT NULL  COMMENT '完成的接受帮助订单数' AFTER `finished_apply`;
  
ALTER TABLE `account`
  CHANGE `id` `id` VARCHAR(20) NOT NULL  COMMENT 'ID';
  
ALTER TABLE `apply_help_req`   
  CHANGE `apply_req_uid` `apply_req_uid` VARCHAR(20) NOT NULL  COMMENT '申请帮助请求玩家id';
  
ALTER TABLE `apply_help`   
  CHANGE `apply_uid` `apply_uid` VARCHAR(20) NOT NULL  COMMENT '申请帮助玩家id';
  
ALTER TABLE `accept_help_req`   
  CHANGE `accept_req_uid` `accept_req_uid` VARCHAR(20) NOT NULL  COMMENT '接受帮助请求玩家id';
  
ALTER TABLE `accept_help`   
  CHANGE `accept_uid` `accept_uid` VARCHAR(20) NOT NULL  COMMENT '接受帮助玩家id';

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
