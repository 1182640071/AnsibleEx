package ansibleEx.AnsibleMiddleware.service.imp;


import java.net.URLEncoder;
import java.util.List;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicHeader;
import org.apache.http.protocol.HTTP;
import org.apache.http.util.EntityUtils;
/*
 * 利用HttpClient进行post请求的工具类
 */
public class HttpClientUtil {
	
	private static final String APPLICATION_JSON = "application/json";
    
    private static final String CONTENT_TYPE_TEXT_JSON = "text/json";
	
	public String doPost(String url,String json, String charset) throws Exception{
		HttpClient httpClient = null;
		HttpPost httpPost = null;
		String result = null;
//		String encoderJson = URLEncoder.encode(json, HTTP.UTF_8);
		
		try{
			httpClient = new SSLClient();
			httpPost = new HttpPost(url);
//			httpPost.addHeader(HTTP.CONTENT_TYPE, APPLICATION_JSON);
//			httpPost.setHeader("Accept", "application/x-yaml");

			StringEntity se = new StringEntity(json , "utf-8");
//	        se.setContentType(CONTENT_TYPE_TEXT_JSON);
//	        se.setContentEncoding(new BasicHeader(HTTP.CONTENT_TYPE, APPLICATION_JSON));
			se.setContentEncoding("UTF-8");    
			se.setContentType("application/json"); 
	        httpPost.setEntity(se);
			HttpResponse response = httpClient.execute(httpPost);
			if(response != null){
				HttpEntity resEntity = response.getEntity();
				if(resEntity != null){
					result = EntityUtils.toString(resEntity,"utf-8");
				}
			}
		}catch(Exception ex){
			ex.printStackTrace();
		}
		return result;
	}
}