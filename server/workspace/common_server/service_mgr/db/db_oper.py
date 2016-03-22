# coding=utf-8
"""
Created on 2015-4-22

@author: Jay
"""
from utils.data.db.mysql_manual import SchemaTable
from utils.service_control.cacher import ParamCacher
from utils.service_control.parser import ArgumentParser
from utils.meta.instance_pool import InstancePool


class DBSchemaTable(SchemaTable):
    __metaclass__ = InstancePool

    def __init__(self, table_name):
        super(DBSchemaTable, self).__init__(ParamCacher().db_instance, ArgumentParser().args.db_name, table_name)


DBGrantMachineInst = DBSchemaTable.instance("grant_machine")
DBTpServiceInst = DBSchemaTable.instance("tp_service")
DBServiceGroupInst = DBSchemaTable.instance("service_group")
DBServiceInst = DBSchemaTable.instance("service")
