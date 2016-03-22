mmm_da
#############################

版本: 0.0.1

1.简介
=============

mmm_da 管理mmm后台逻辑+db访问


2.接口介绍
==============

2.1 注册:	
------------------------------------------
	HTTPS post /register:	
	
		body(ujson){
			id: 账号id, 需要使用通过2.20new_account_id获取一个新账号id
		
			account:账号
			
			passwd: 密码
			
			id_card: 身份证号码

			email: 邮箱
			
			phone: 手机号码
			
			leader_id: 领导人id, 必须是真实存在的id， 需要使用通过2.20random_leader_id获取一个新账号id
			
			bank: 开户银行
			
			bank_address: 开户支行
			
			bank_account: 开户账号
			
			bank_name: 开户名称
			
			wechat: 微信，  可选
			
			alipay: 支付宝， 可选
			
		}
		
	Response:
		'result':请见错误码说明
		
		
2.2 登陆:	
------------------------------------------
	HTTPS post /login:	
	
		body(ujson){
			id:账号id
		
			passwd: 密码	
			
		}
		
	Response:
		'result':请见错误码说明, 
	
		'account_info': 详见4数据模板 ACCOUNT_INFO
		
		'access_token': 访问token
		
2.3 账号修改:	
------------------------------------------
	HTTPS post /account/<id>:	
		headers{
			'Authorization': access_token
			
			'id' = id
			
		}
		
		body(ujson){
		
			passwd: 密码
			
			...
			
		}
				
	Response:
		'result':请见错误码说明, 
		

2.4获取他人账号信息:		
------------------------------------------
	HTTPS get /account/<view_id>:	
		headers{
			'Authorization': access_token
			
			'id' = id
			
		}
				
	Response:
		'result':请见错误码说明, 
		
		'account_info': 详见4数据模板 ACCOUNT_INFO
		
		
		
2.5 密码修改:	
------------------------------------------
	HTTPS post /passwd_change:	
		headers{
			'Authorization': access_token
			
			'id' = id
			
		}
		
		body(ujson){
		
			old_passwd: 老密码
			
			new_passwd: 新密码
			
		}
				
	Response:
		'result':请见错误码说明, 
		
		
2.6 激活账号:		
------------------------------------------
	HTTPS get /active/<active_id>:	
		headers{
			'Authorization': access_token
			
			'id' = id
			
		}
				
	Response:
		'result':请见错误码说明, 
		
2.8 我的团队概要信息:
-------------------------
	HTTPS get/post /summary:	
		headers{
			'Authorization': access_token
			
			'id' = id
			
		}
				
	Response:
		'result':请见错误码说明,
		
		'summary': [{u'unactived': 第一层未激活数量, u'actived': 第一层激活数量, u'sum': 第一层总数量}, 
		
				{u'unactived': 第二层未激活数量, u'actived': 第二层激活数量, u'sum': 第二层总数量},
				
				,
				
				,
				
				{u'unactived': 第N层未激活数量, u'actived': 第N层激活数量, u'sum': 第N层总数量}]
				
				
2.9 申请帮助:
--------------------
	HTTPS post /apply_help:	
		headers{
			'Authorization': access_token
			
			'id' = id
			
		}
		
		body(ujson){
		
			apply_money: 提供金额
			
		}
		
		
				
	Response:

		
2.9.1 删除申请帮助:
--------------------
	HTTPS post /del_apply_help:	
		headers{
			'Authorization': access_token
			
			'id' = id
			
		}
		
		body(ujson){
		
			apply_order:申请帮助订单
			
		}
		
		
				
	Response:
		'result':请见错误码说明
		
		
2.10 获取当前申请帮助(申请状态为未确认的):
--------------------------------------------------
	HTTPS post /cur_apply_help:	
		headers{
			'Authorization': access_token
			
			'id' = id
			
		}
				
	Response:
		'result':请见错误码说明, 
		
		'apply_help_ls': [{accept_order:接受帮助订单, accept_uid:接受帮助玩家id, accept_account:接受帮助玩家账号, bank_name:接受帮助玩家银行卡名称
		
						apply_order:申请帮助订单, apply_sorder:申请帮助子订单, apply_time:申请时间, apply_money:申请金额, apply_stat:申请状态}
						
						,,,
						
						]
		
		'apply_help': {apply_order:申请帮助订单, apply_time:申请时间, apply_money:申请金额, apply_stat:申请状态]
		
								

2.11 申请帮助支付信息上传(前端):
------------------------------------
	及时支付给申请帮助的人加息，加息幅度可配置

	HTTP post http://52.77.234.86/apply_help_pay:
		body(){
			id: 用户id
			
			access_token = access_token
		
			apply_sorder:申请帮助子订单id
			
			pay_msg: 支付留言
			
			file: 选择文件
			
		}		
				
	Response:
		'result':请见错误码说明
		
		'apply_help': {apply_sorder:申请帮助子订单, apply_stat:申请状态}
		
		
2.12 申请帮助支付信息转存(nginx)
----------------------------------
	注意：前端不需要开发，这个接口是nginx调用的

	HTTP post /apply_help_paid:			
		body(){
			id: 用户id
			
			access_token = access_token
		
			apply_sorder:申请帮助子订单id
			
			pay_msg: 支付留言
			
			file_content_type: 文件类型,如'image/jpeg', 
			
			file_md5: 文件md5,'fafa5efeaf3cbe3b23b2748d13e629a1', 
			
			submit: 'Upload', 

			file_name: 文件名称,如'Tulips.jpg', 
			
			file_path: 文件存储路径,'/tmp/nginx_upload/0000000001',
			
			file_size: 文件大小,'620888',
			
		}		
				
	Response:
		'result':请见错误码说明
		
		'apply_help': {apply_sorder:申请帮助子订单, apply_stat:申请状态}
		
2.13 申请帮助拒绝:
--------------------
	HTTPS post /apply_help_refuse:	
		headers{
			'Authorization': access_token
			
			'id' = id
			
		}
		
		body(ujson){
		
			apply_sorder:申请帮助子订单
			
		}		
				
	Response:
		'result':请见错误码说明					
		
		
2.15 接受帮助:
-------------------------------------
	申请帮助4-7天后才能开始接收帮助
	
	类似于提现帮助本息,接收帮助后，本息一次性算完，到此为止，不在提供利息
	
	接受帮助需要在24小时内匹配完成

	HTTPS post /accept_help:	
		headers{
			'Authorization': access_token
			
			'id' = id
			
		}
		
		body(ujson){
		
			'mafuluo': 需要提取的马夫罗，整形
			
		}	
				
	Response:
		'result':请见错误码说明,	
		
		
2.15.1 删除接受帮助:
-------------------------------------

	HTTPS post /del_accept_help:	
		headers{
			'Authorization': access_token
			
			'id' = id
			
		}
		
		body(ujson){
		
			'accept_order': 接受帮助订单ID
			
		}	
				
	Response:
		'result':请见错误码说明		
		
		
2.16 获取当前接受帮助:
------------------------
	HTTPS post /cur_accept_help:	
		headers{
			'Authorization': access_token
			
			'id' = id
			
		}
		
				
	Response:
		'result':请见错误码说明, 
		
		'apply_help_ls': [{apply_order:申请帮助订单ID, apply_sorder:申请帮助子订单, apply_uid:申请帮助玩家id, bank_name:申请帮助玩家银行卡名称, apply_money:申请金额,  apply_stat:申请状态, apply_piture:支付截图, apply_message:支付留言},,,]
		
		'accept_help': {accept_order:接受帮助订单ID, accept_stime:接受帮助开始日期, accept_money:接受帮助金额, accept_lmoney:接受帮助剩余金额, accept_stat:接受帮助状态}		
		
		# 注意：如果是匹配状态下， accept_help只有以下字段： {accept_order:接受帮助订单ID, accept_stime:接受帮助开始日期, accept_money:接受帮助金额,  accept_stat:接受帮助状态}
		
2.17 接受帮助确认:
------------------------
	及时确认给申请帮助的人加息，加息幅度可配置

	HTTPS post /accept_help_confirm:	
		headers{
			'Authorization': access_token
			
			'id' = id
			
		}
		
		body(ujson){
		
			apply_sorder:申请帮助子订单, 
			
		}	
				
	Response:
		'result':请见错误码说明, 
		
		'apply_help': {apply_sorder:申请帮助子订单, apply_stat:申请状态}
		

2.17.1 接受帮助未收到:
--------------------------
	申请帮助支付之后，接受帮助者确认没有收到，这时候处理订单异常状态，系统不处理，等待客服处理

	HTTPS post /accept_help_notreceived:	
		headers{
			'Authorization': access_token
			
			'id' = id
			
		}
		
		body(ujson){
		
			apply_sorder:申请帮助子订单, 
			
		}	
				
	Response:
		'result':请见错误码说明,
				
				
2.20 分配账号id:	
-------------------------
	HTTPS get /new_account_id:
				
	Response:
		'result':请见错误码说明, 
		
		'new_account_id': 新账号id
				
2.20.1 检测账号id是否存在:	
-----------------------------
	HTTPS get /check_id:
		id: 账号id
				
	Response:
		
2.21 随机分配领导id:	
-------------------------
	HTTPS get /random_leader_id:
				
	Response:
		'result':请见错误码说明, 
		
		'leader_id': 领导id
		

2.22 系统信息:	
-------------------------
	HTTPS get /system_info:
				
	Response:
		'apply_req_count': 提供援助人数
		
		'accept_req_count': 等待援助人数
		
		'notice': 系统公告
		
		
2.24 获取奖金日志：
-------------------------
	HTTPS post /get_bonus_logs:	
		headers{
			'Authorization': access_token
			
			'id' = id
			
		}
		
		body(ujson){
		
			page_idx: 页数索引,没有的话默认为1
			
		}	
		
				
	Response:
		'result':请见错误码说明, 
		
		'bonus_logs': [{afctd_uid:被奖励的uid, afct_uid:奖励的uid, afct_bonus:奖金, afct_time:奖励时间, afct_type:奖金类型}]
		
2.25 检测手机号码是否存在:	
-----------------------------
	HTTPS get /check_phone:
		phone: 手机号码
				
	Response:
	
	
2.26 激活币转账:
------------------------
	HTTPS post /active_coin_transfer:	
		headers{
			'Authorization': access_token
			
			'id' = id
			
		}
		
		body(ujson){
		
			tgt_id: 目标用户id,
			
			tgt_coin: 转账激活币个数
			
		}	
		
	Response:
		'result':请见错误码说明, 
		
		
2.27 排单币转账:
------------------------
	HTTPS post /match_coin_transfer:	
		headers{
			'Authorization': access_token
			
			'id' = id
			
		}
		
		body(ujson){
		
			tgt_id: 目标用户id,
			
			tgt_coin: 转账排单币个数
			
		}	
		
	Response:
		'result':请见错误码说明, 
		

3. 错误码说明
===============

ERROR_SUCCESS = 0                           # 操作成功

ERROR_UNKNOWN_ERROR = 1                     # 未知错误

ERROR_PARAMS_ERROR = 2                      # 参数格式错误

ERROR_DB_ERROR = 3                          # 数据库操作错误

ERROR_ACCESS_TOKEN_ERROR = 4                # AccessToken错误

ERROR_VERIFY_CODE_ERROR = 5                 # 验证码错误

ERROR_SIGN_ERROR = 6                        # 参数签名出错





ERROR_PARAM = 440                           # 参数格式错误

ERROR_UID_NOT_EXIST = 441                   # uid不存在

EEROR_ACCEPT_BALANCE = 442					# 接受帮助资金平衡，请改天再来申请

EEROR_MATCH_COIN_LACK = 443					# 排单币不足

ERROR_MAX_APPLY_HELP_LESS = 444             # 每次投资额不得低于上次投资额

ERROR_PHONE_EXISTED = 445                   # 手机号码已经存在

ERROR_PHONE_INVALID = 446                   # 手机号码无效

ERROR_ACCOUNT_SEALED = 447                  # 账号已经被封号，请联系管理员

ERROR_ACCOUNT_UNACTIVED = 448               # 账号未激活，请联系管理员

 


4.数据模板
==============

ACCOUNT_INFO = {id:账号id, account:账号, passwd: 密码, id_card: 身份证号码, email: 邮箱, phone: 手机号码, leader_id: 领导人id, 
		
		bank: 开户银行, bank_address: 开户支行, bank_account: 开户账号, bank_name: 开户名称, wechat: 微信, alipay: 支付宝, 
		
		create_time: 创建时间, active_coin:激活币, active_time:激活时间, stat:账号状态:0未激活,1激活,2封号,
		
		level:等级, mafuluo:钱包余额, team_count:团队人数,
		
		match_coin:排单币, max_apply_money:最大申请帮助金额,以后每次申请只能比此次更大金额}
		
		
SERVER_INFO =  {apply_match_min_days： 申请帮助至少匹配时间(天),
				
				apply_match_max_days: 申请帮助最多匹配时间(天),
				
				apply_pay_max_days:	申请帮助至少匹配时间(天),
				
				accept_match_min_days: 接受帮助至少匹配时间(天),
				
				apply_interest:申请帮助利息(百分比)
  
				pay_timely_rwd_hours:及时打款奖励区间(小时),
				
				pay_timely_rwd_int:及时打款利息奖励(百分比),
				
				cfmd_timely_rwd_hours:及时打款奖励区间(小时),
				
				cfmd_timely_rwd_int:及时收款确认利息奖励(百分比)
				
				day_seconds:一天的秒数}
				

				
# 申请帮助状态	
		
APPLY_STAT =[

	APYRS_REQUEST,        # 提供帮助请求提交(对于客户端来说，也是处理匹配状态)
	
	APYRS_MATCHING,       # 提供帮助请求匹配
	
	APYRS_FINISH,         # 提供帮助请求完成
	
	APYS_WAITING_PAY,     # 等待支付
	
    APYS_PAID,            # 已经支付
	
    APYS_CFRM_PAID,       # 确认支付
	
    APYS_UNUSUAL,         # 订单异常,联系客服处理
	
    APYS_CANCEL,          # 取消
	
] = [10,11,12, 0,1,2,3,4]


# 接受帮助状态

ACCEPT_STAT=[

	ACPRS_REQUEST,        # 接收帮助请求提交(对于客户端来说，也是处理匹配状态)
	
	ACPRS_FINISH,         # 接收帮助请求完成
	
	ACPS_MATCHING,        # 匹配中
	
	ACPS_FINISH,          # 完成
	
] = [10,11,  0,1]


# 账号状态

STAT =[

    UNACTIVED,  # 未激活
	
    ACTIVED,    # 激活
	
    SEALED      # 封号
	
] = xrange(0, 3)


# 等级级别

LEVEL = [

    NOT_LEVEL,      # 无职位
	
    MGR,            # 经理
	
    VICE_GEN_MGR,   # 副总经理
	
    GEN_MGR,        # 总经理
	
] = xrange(0, 4)


# BONUS 奖励类型

BONUS_REWARD_TYPE =[

    LAYER_APPLY_PAID_REWARD,        # 下线人员提供帮助奖励
	
] = xrange(10, 11)


# BONUS 惩罚类型

BONUS_PUNISH_TYPE =[

    LAYER_APPLY_UNPAID_PUNISH,      # 下线人员未支付提供帮助惩罚
	
] = xrange(20, 21)

