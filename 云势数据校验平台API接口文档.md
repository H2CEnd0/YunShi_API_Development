# 云势数据接口

## 根据省和医院名精确匹配相应的医院信息
接口：http://182.92.96.114:1080/yunshi/getAccurateMatch
请求方式：POST

参数输入格式：{"id":"abc000001"}

注意:id是操作id,每次id输入是唯一的

返回的数据格式：


执行成功返回{"msg": "success", "code": "1"}
执行失败返回{"msg": "error", "code": "0"}


数据说明：code为1表示精确匹配成功,,后台通过程序将结果保存在excel文件中；code为0表示精确匹配失败程序报错，未生成excel文件

## 根据省和医院名模糊匹配相应的医院信息

接口：http://182.92.96.114:1080/yunshi/getBlurMatch
请求方式：POST

参数输入格式：{"id":"abc000001"}
注意:id是操作id,每次id输入是唯一的

返回的数据格式：

执行成功返回{"msg": "success", "code": "1"}
执行失败返回{"msg": "error", "code": "0"}


数据说明：code为1表示模糊匹配执行成功,后台通过程序将结果保存在excel文件中；code为0表示模糊匹配执行失败，程序报错，未生成excel文件



## 根据省、市、区以及筛选条件，查找相关医院信息,显示查询结果

接口：http://182.92.96.114:1080/yunshi/getAllData

请求方式：POST

参数格式：{"Province":"辽宁省","City":"大连市","County":"沙河口区","Page":1,"Pagesize":15,"Param1":"医院","Param2":"","id":"abc000014"}
注意:id是操作id,每次id输入是唯一的


参数说明:Province表示输入的省份,City表示输入的市,County表示输入的区 id表示任务编号,由前端输入
         page表示当前页
         pagesize表示显示条数
         Param1表示筛选条件1
         Param2表示筛选条件2

注意:Province City County id信息是必须输入的参数,否则程序报错

返回的数据格式：

执行失败返回:{"code": "0", "msg": "error"}
参数输入错误返回:{"code": "2", "msg": "Params Error"} 当Province City County id 四个参数中有一个参数没有输入程序就会报错
执行成功返回{
    "msg": "success",
    "content": [
        {
            "City": "大连市",
            "ApprovedDate": null,
            "Note": null,
            "State": "Active",
            "PostCode": "116021",
            "ApprovedDepartment": null,
            "MedicalOrgDesp": null,
            "Sort": null,
            "WarehouseAddress": null,
            "HospitalLevel": "未知",
            "OrganizationID": null,
            "ProfitNature": null,
            "MedicalOrgID": "HCO_0225146",
            "MedicalOrgAlias4": null,
            "Reason": "有效",
            "MedicalOrgAlias1": null,
            "MedicalOrgAlias3": null,
            "MedicalOrgAlias2": null,
            "AdministrationCode": null,
            "MedicalOrgName": "辽宁省大连市辽宁师范大学医院",
            "Town": null,
            "Province": "辽宁省",
            "Address": "地址待更新",
            "ExpiryDate": null,
            "GSPLicenseID": null,
            "AnestheticDrugBusinessQualification": null,
            "FoundingTime": null,
            "MedicalOrgSubType": "综合医院",
            "BusinessType": null,
            "Features": "Yunshi00865171",
            "Telephone": null,
            "County": "沙河口区",
            "Comprehensive/specialized_hospital": null,
            "MedicalOrgURL": null,
            "HospitalGrade": "未知"
        }
    ],
    "code": 1
}

 
## 根据医院特征ID,查找相关医院信息
接口：http://182.92.96.114:1080/yunshi/getById

请求方式：POST

参数格式：{"id":"abc000016"}
注意:id是操作id,每次id输入是唯一的


返回的数据格式：

执行成功返回{"msg": "success", "code": "1"}
执行失败返回{"msg": "error", "code": "0"}

数据说明：code为1表示执行成功,后台通过程序将结果保存在excel文件中；code为0表示执行失败，程序报错，未生成excel文件


## 导入数据








接口：http://182.92.96.114:1080/yunshi/InsertHospitalInfo
请求方式：POST

参数格式：{"id":"abc000016"}
注意:id是操作id,每次id输入是唯一的

返回的数据格式：

执行成功返回的数据格式：{"msg": "success", "code": "1"}
执行失败返回的数据格式：{"msg": "error", "code": "0"}


数据格式说明:code为1表示数据导入成功,code为0表示数据导入失败