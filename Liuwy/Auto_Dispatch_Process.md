[TOC]

## 自动派工过程
> 点击自动派工界面中的自动派工按钮


1. 请求地址： ```http://114.55.33.101/Dispatch_Process_Implement```


2. 请求类型：``` GET 请求```


3. 示例参数：
	
		UserId=ZQ09

4. 请求参数：

		UserId:表示派工人员登录账号

		该参数必须输入,不能为空


5. 返回值：

		msg:派工消息,success表示派工成功,error表示派工失败

		code:派工消息码,1表示成功,0表示失败

6. 返回格式：

		{
    			'msg': 'success',
    			'code': 1
		}
7. 说明:
		
		若返回的参数为{'msg': 'success', 'code': 1}时,则前端再调用自动派工结果查询接口 http://114.55.33.101/AutoTask/Result ；若返回的参数为{'msg': 'error', 'code': 0}时,则前端可以抛出异常

		自动派工过程复杂,处理时间长,我们测试自动派工过程所花时间为70秒,针对这个接口,前端需要考虑把响应时间调大些