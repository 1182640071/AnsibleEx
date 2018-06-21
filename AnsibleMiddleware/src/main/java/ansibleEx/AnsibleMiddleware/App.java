package ansibleEx.AnsibleMiddleware;

import org.springframework.context.support.ClassPathXmlApplicationContext;

import com.alibaba.dubbo.container.Main;

/**
 * created by wangml
 * date 2018.06.21
 *程序启动，加在spring，dubbo配置文件
 */
public class App 
{
	
	public static ClassPathXmlApplicationContext context;
	
	static{
		try {
//			context = new ClassPathXmlApplicationContext("classpath:spring/spring.xml"); 
			context = new ClassPathXmlApplicationContext(new String[] {"classpath:spring/spring.xml","classpath:spring/dubbo.xml"});
		} catch (Exception e) {
			System.out.println(e);
		}
	}
	
    public static void main( String[] args )
    {
        System.out.println( "Hello World!" );
    	context.start();
		 // 使主线程等待以持续提供服务
        synchronized (Main.class) {
            while (true) {
                try {
                    Main.class.wait();
                } catch (Throwable e) {
                }
            }
        }
    }
}
