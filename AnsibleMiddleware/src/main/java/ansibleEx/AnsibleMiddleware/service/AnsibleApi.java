package ansibleEx.AnsibleMiddleware.service;

/**
 * created by wangml
 * date 2018.06.21
 * ansible接口调用操作方法，密码加密、解密入口
 * */
public interface AnsibleApi {
	
	public String ApiEntrance(String  user , String passwd , String host , String module , String cmd);
}
