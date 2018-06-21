package ansibleEx.AnsibleMiddleware.service.imp;

import java.io.UnsupportedEncodingException;

import com.alibaba.dubbo.config.annotation.Service;

import ansibleEx.AnsibleMiddleware.service.AnsibleApi;
import ansibleEx.AnsibleMiddleware.util.Secret;
import net.sf.json.JSONObject;



/**
 * created by wangml
 * date 2018.06.21
 * ansible接口调用操作方法，密码加密、解密入口方法实现
 * */
@Service
public class AnsibleApiImp implements AnsibleApi{
	//ansible接口地址
	private String url = "https://172.16.22.24/ansible/api1.0";
	private String charset = "utf-8";
	private HttpClientUtil httpClientUtil = null;

	public AnsibleApiImp(){
		httpClientUtil = new HttpClientUtil();
	}
	

	public String ApiEntrance(String user, String passwd, String host, String module, String cmd) {
		String httpOrgCreateTest = url;
		if(""!=passwd && !"".equals(passwd)&&passwd != null){
			passwd = Secret.decryptBasedDes(passwd);
		}
		
		
        JSONObject obj = new JSONObject();
        obj.element("user",user);
        obj.element("passwd",passwd);
        obj.element("host", host);
        obj.element("module", module);
        obj.element("arg", cmd);
		
		String httpOrgCreateTestRtn = "";
		try {
			httpOrgCreateTestRtn = httpClientUtil.doPost(httpOrgCreateTest,obj.toString(),charset);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		try {
			System.out.println(new String(httpOrgCreateTestRtn.getBytes() , charset));
		} catch (UnsupportedEncodingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return null;
	}

	public static void main(String[] args){
		AnsibleApiImp main = new AnsibleApiImp();
		main.ApiEntrance("root" , "HUiUK5ekqrNUDSR/T0XZZw==" , "172.16.22.23,172.16.22.25","shell","uptime");
	}
}
