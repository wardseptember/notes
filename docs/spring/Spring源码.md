# IOC

IOC（Inverse of Control: 反转控制）是一种**设计思想**，就是 **将原本在程序中手动创建对象的控制权，交由Spring框架来管理。** IOC 在其他语言中也有应用，并非 Spring 特有。 **IOC 容器是 Spring 用来实现 IOC 的载体， IOC 容器实际上就是个Map（key，value）,Map 中存放的是各种对象。**

将对象之间的相互依赖关系交给 IOC 容器来管理，并由 IOC 容器完成对象的注入。这样可以很大程度上简化应用的开发，把应用从复杂的依赖关系中解放出来。 **IOC 容器就像是一个工厂一样，当我们需要创建一个对象的时候，只需要配置好配置文件/注解即可，完全不用考虑对象是如何被创建出来的。**

**DI(Dependecy Inject,依赖注入)是实现控制反转的一种设计模式，依赖注入就是将实例变量传入到一个对象中去。**

### IOC好处

第一，资源集中管理，实现资源的可配置和易管理。第二，降低了使用资源双方的依赖程度。

## Spring 缺点

- Spring明明一个很轻量级的框架，却给人感觉大而全
- Spring依赖反射，反射影响性能
- 使用门槛升高，入门Spring需要较长时间

## 组件添加

基于注解的，往IOC添加组件的方式有哪些？

### @ComponentScan

```java
//@ComponentScan  value:指定要扫描的包
//excludeFilters = Filter[] ：指定扫描的时候按照什么规则排除那些组件
//includeFilters = Filter[] ：指定扫描的时候只需要包含哪些组件
//FilterType.ANNOTATION：按照注解
//FilterType.ASSIGNABLE_TYPE：按照给定的类型；
//FilterType.ASPECTJ：使用ASPECTJ表达式
//FilterType.REGEX：使用正则指定
//FilterType.CUSTOM：使用自定义规则
@ComponentScans(
		value = {
				@ComponentScan(value="com.atguigu",includeFilters = {
						@Filter(type=FilterType.ANNOTATION,classes={Controller.class}),
						@Filter(type=FilterType.ASSIGNABLE_TYPE,classes={BookService.class}),
						@Filter(type=FilterType.CUSTOM,classes={MyTypeFilter.class})
				},useDefaultFilters = false)	
		}
		)
```

### @Bean

一般放在方法上，告诉Spring，注册一个Bean对象

### @Scope

调整作用域

* prototype：多实例的：ioc容器启动并不会去调用方法创建对象放在容器中。每次获取的时候才会调用方法创建对象；
* singleton：单实例的（默认值），ioc容器启动会调用方法创建对象放到ioc容器中。以后每次获取就是直接从容器（map.get()）中拿。
* request：同一次请求创建一个实例
* session：同一个session创建一个实例

### @Configuration

用于声明配置类

### @Service

业务层，使用@Service注解在一个类上，表示将此类标记为Spring容器中的一个Bean。

### @Controller

控制层，使用@Controller注解在一个类上，表示将此类标记为Spring容器中的一个Bean。

### @Repository

数据层，使用@Repository注解在一个类上，表示将此类标记为Spring容器中的一个Bean。

### @Component

标注Spring管理的Bean，使用@Component注解在一个类上，表示将此类标记为Spring容器中的一个Bean。Repository、Controller、Service注解上都被标注@Component。

### @Conditional

可以按照条件装配Bean，条件类需要实现Condition接口。

### @Import

@Import导入组件，id默认是组件的全类名

### @Primary

自动装配时当出现多个Bean候选者时，被注解为@Primary的Bean将作为首选者，否则将抛出异常 

### @Lazy

被@Lazy标注的bean，使用时才创建。单实例bean：默认在容器启动的时候创建对象。

### 实现ImportSelector接口

实现ImportSelector接口，也可以注册Bean.

```java
package com.atguigu.condition;

import org.springframework.context.annotation.ImportSelector;
import org.springframework.core.type.AnnotationMetadata;

// 自定义逻辑返回需要导入的组件
public class MyImportSelector implements ImportSelector {

	// 返回值，就是到导入到容器中的组件全类名
	// AnnotationMetadata:当前标注@Import注解的类的所有注解信息
	@Override
	public String[] selectImports(AnnotationMetadata importingClassMetadata) {
		// TODO Auto-generated method stub
		// importingClassMetadata
		// 方法不要返回null值
		return new String[]{"com.atguigu.bean.Blue","com.atguigu.bean.Yellow"};
	}

}
```

### 实现FactoryBean接口

实现FactoryBean接口，也可以注册Bean，FactoryBean一般用于注册复杂的Bean，其方法getObject()返回创建的Bean，而不是实现FactoryBean接口的Bean，&beanName获取Factory本身。

### @PostConstruct

JSR250规范，在bean创建完成并且属性赋值完成；来执行初始化方法

### @PreDestory

JSR250规范，跟@PostConstruct是一对，在容器销毁bean之前通知我们进行清理工作

## 组件赋值

对组件的属性赋值

### @Value

使用@Value赋值；

* 基本数值
* 可以写SpEL； #{}
* 可以写${}；取出配置文件【properties】中的值（在运行环境变量里面的值）

### @Autowired

自动注入，默认按照类型装配

### @Qualifier

限定注入，可与@Autowired结合使用

* 通过 Bean 名称限定

* 通过分组限定

### @Resources

JSR250的规则，@Resource的作用相当于@Autowired，只不过@Autowired按byType自动注入，而@Resource默认按 byName自动注入罢了。@Resource有两个属性是比较重要的，分是name和type，Spring将@Resource注解的name属性解析为bean的名字，而type属性则解析为bean的类型。所以如果使用name属性，则使用byName的自动注入策略，而使用type属性时则使用byType自动注入策略。如果既不指定name也不指定type属性，这时将通过反射机制使用byName自动注入策略。

#### @Resource装配顺序

　　1. 如果同时指定了name和type，则从Spring上下文中找到唯一匹配的bean进行装配，找不到则抛出异常
　　2. 如果指定了name，则从上下文中查找名称（id）匹配的bean进行装配，找不到则抛出异常
　　3. 如果指定了type，则从上下文中找到类型匹配的唯一bean进行装配，找不到或者找到多个，都会抛出异常
　　4. 如果既没有指定name，又没有指定type，则自动按照byName方式进行装配；如果没有匹配，则回退为一个原始类型进行匹配，如果匹配则自动装配；

#### @Autowired 与@Resource的区别：

1. @Autowired与@Resource都可以用来装配bean. 都可以写在字段上,或写在setter方法上。

2. @Autowired默认按类型装配（这个注解是属业spring的），默认情况下必须要求依赖对象必须存在，如果要允许null值，可以设置它的required属性为false，如：@Autowired(required=false) ，如果我们想使用名称装配可以结合@Qualifier注解进行使用
3. Resource（这个注解属于J2EE的），默认按照名称进行装配，名称可以通过name属性进行指定，如果没有指定name属性，当注解写在字段上时，默认取字段名进行安装名称查找，如果注解写在setter方法上默认取属性名进行装配。当找不到与名称匹配的bean时才按照类型进行装配。但是需要注意的是，如果name属性一旦指定，就只会按照名称进行装配。

### @Inject

如果 JSR-330 存在于 ClassPath 中，复用 AutowiredAnnotationBeanPostProcessor 实现

### @PropertySource

使用@PropertySource可以引入一个文件到Spring环境中，被@Configuration标注的类可以使用这个文件中的内容。

### @PropertySources

可以导入多个文件

### @Profile

* 指定组件在哪个环境的情况下才能被注册到容器中，不指定，任何环境下都能注册这个组件
* Spring为我们提供的可以根据当前环境，动态的激活和切换一系列组件的功能；

例如可以动态切换数据源

```
-Dspring.profiles.active=test
```

## 依赖注入

* 构造器注入
* Setter注入
* 字段注入
* 方法注入
* 接口回调注入(XXXAware)

## Refresh方法详解

```java
Spring容器的refresh()【创建刷新】;
1、prepareRefresh()刷新前的预处理;
   1）、initPropertySources()初始化一些属性设置;子类自定义个性化的属性设置方法；
   2）、getEnvironment().validateRequiredProperties();检验属性的合法等
   3）、earlyApplicationEvents= new LinkedHashSet<ApplicationEvent>();保存容器中的一些早期的事件；
2、obtainFreshBeanFactory();获取BeanFactory；
   1）、refreshBeanFactory();刷新【创建】BeanFactory；
         创建了一个this.beanFactory = new DefaultListableBeanFactory();
         设置id；
   2）、getBeanFactory();返回刚才GenericApplicationContext创建的BeanFactory对象；
   3）、将创建的BeanFactory【DefaultListableBeanFactory】返回；
3、prepareBeanFactory(beanFactory);BeanFactory的预准备工作（BeanFactory进行一些设置）；
   1）、设置BeanFactory的类加载器、支持表达式解析器...
   2）、添加部分BeanPostProcessor【ApplicationContextAwareProcessor】
   3）、设置忽略的自动装配的接口EnvironmentAware、EmbeddedValueResolverAware、xxx；
   4）、注册可以解析的自动装配；我们能直接在任何组件中自动注入：
         BeanFactory、ResourceLoader、ApplicationEventPublisher、ApplicationContext
   5）、添加BeanPostProcessor【ApplicationListenerDetector】
   6）、添加编译时的AspectJ；
   7）、给BeanFactory中注册一些能用的组件；
      environment【ConfigurableEnvironment】、
      systemProperties【Map<String, Object>】、
      systemEnvironment【Map<String, Object>】
4、postProcessBeanFactory(beanFactory);BeanFactory准备工作完成后进行的后置处理工作；
   1）、子类通过重写这个方法来在BeanFactory创建并预准备完成以后做进一步的设置
======================以上是BeanFactory的创建及预准备工作==================================
5、invokeBeanFactoryPostProcessors(beanFactory);执行BeanFactoryPostProcessor的方法；
   BeanFactoryPostProcessor：BeanFactory的后置处理器。在BeanFactory标准初始化之后执行的；
   两个接口：BeanFactoryPostProcessor、BeanDefinitionRegistryPostProcessor
      先执行BeanDefinitionRegistryPostProcessor
      1）、获取所有的BeanDefinitionRegistryPostProcessor；
      2）、看先执行实现了PriorityOrdered优先级接口的BeanDefinitionRegistryPostProcessor、
         postProcessor.postProcessBeanDefinitionRegistry(registry)
      3）、在执行实现了Ordered顺序接口的BeanDefinitionRegistryPostProcessor；
         postProcessor.postProcessBeanDefinitionRegistry(registry)
      4）、最后执行没有实现任何优先级或者是顺序接口的BeanDefinitionRegistryPostProcessors；
         postProcessor.postProcessBeanDefinitionRegistry(registry)
         
      
      再执行BeanFactoryPostProcessor的方法
      1）、获取所有的BeanFactoryPostProcessor
      2）、看先执行实现了PriorityOrdered优先级接口的BeanFactoryPostProcessor、
         postProcessor.postProcessBeanFactory()
      3）、在执行实现了Ordered顺序接口的BeanFactoryPostProcessor；
         postProcessor.postProcessBeanFactory()
      4）、最后执行没有实现任何优先级或者是顺序接口的BeanFactoryPostProcessor；
         postProcessor.postProcessBeanFactory()

6、registerBeanPostProcessors(beanFactory);注册BeanPostProcessor（Bean的后置处理器）【 intercept bean creation】
      不同接口类型的BeanPostProcessor；在Bean创建前后的执行时机是不一样的
      BeanPostProcessor、
      DestructionAwareBeanPostProcessor、
      InstantiationAwareBeanPostProcessor、
      SmartInstantiationAwareBeanPostProcessor、
      MergedBeanDefinitionPostProcessor【internalPostProcessors】、
      
      1）、获取所有的 BeanPostProcessor;后置处理器都默认可以通过PriorityOrdered、Ordered接口来执行优先级
      2）、先注册PriorityOrdered优先级接口的BeanPostProcessor；
         把每一个BeanPostProcessor；添加到BeanFactory中
         beanFactory.addBeanPostProcessor(postProcessor);
      3）、再注册Ordered接口的
      4）、最后注册没有实现任何优先级接口的
      5）、最终注册MergedBeanDefinitionPostProcessor；
      6）、注册一个ApplicationListenerDetector；来在Bean创建完成后检查是否是ApplicationListener，如果是
         applicationContext.addApplicationListener((ApplicationListener<?>) bean);
7、initMessageSource();初始化MessageSource组件（做国际化功能；消息绑定，消息解析）；
      1）、获取BeanFactory
      2）、看容器中是否有id为messageSource的，类型是MessageSource的组件
         如果有赋值给messageSource，如果没有自己创建一个DelegatingMessageSource；
            MessageSource：取出国际化配置文件中的某个key的值；能按照区域信息获取；
      3）、把创建好的MessageSource注册在容器中，以后获取国际化配置文件的值的时候，可以自动注入MessageSource；
         beanFactory.registerSingleton(MESSAGE_SOURCE_BEAN_NAME, this.messageSource);   
         MessageSource.getMessage(String code, Object[] args, String defaultMessage, Locale locale);
8、initApplicationEventMulticaster();初始化事件派发器；
      1）、获取BeanFactory
      2）、从BeanFactory中获取applicationEventMulticaster的ApplicationEventMulticaster；
      3）、如果上一步没有配置；创建一个SimpleApplicationEventMulticaster
      4）、将创建的ApplicationEventMulticaster添加到BeanFactory中，以后其他组件直接自动注入
9、onRefresh();留给子容器（子类）
      1、子类重写这个方法，在容器刷新的时候可以自定义逻辑；
10、registerListeners();给容器中将所有项目里面的ApplicationListener注册进来；
      1、从容器中拿到所有的ApplicationListener
      2、将每个监听器添加到事件派发器中；
         getApplicationEventMulticaster().addApplicationListenerBean(listenerBeanName);
      3、派发之前步骤产生的事件；
11、finishBeanFactoryInitialization(beanFactory);初始化所有剩下的单实例bean；
   1、beanFactory.preInstantiateSingletons();初始化后剩下的单实例bean
      1）、获取容器中的所有Bean，依次进行初始化和创建对象
      2）、获取Bean的定义信息；RootBeanDefinition
      3）、Bean不是抽象的，是单实例的，是懒加载；
         1）、判断是否是FactoryBean；是否是实现FactoryBean接口的Bean；
         2）、不是工厂Bean。利用getBean(beanName);创建对象
            0、getBean(beanName)； ioc.getBean();
            1、doGetBean(name, null, null, false);
            2、先获取缓存中保存的单实例Bean。如果能获取到说明这个Bean之前被创建过（所有创建过的单实例Bean都会被缓存起来）
               从private final Map<String, Object> singletonObjects = new ConcurrentHashMap<String, Object>(256);获取的
            3、缓存中获取不到，开始Bean的创建对象流程；
            4、标记当前bean已经被创建
            5、获取Bean的定义信息；
            6、【获取当前Bean依赖的其他Bean;如果有按照getBean()把依赖的Bean先创建出来；】
            7、启动单实例Bean的创建流程；
               1）、createBean(beanName, mbd, args);
               2）、Object bean = resolveBeforeInstantiation(beanName, mbdToUse);让BeanPostProcessor先拦截返回代理对象；
                  【InstantiationAwareBeanPostProcessor】：提前执行；
                  先触发：postProcessBeforeInstantiation()；
                  如果有返回值：触发postProcessAfterInitialization()；
               3）、如果前面的InstantiationAwareBeanPostProcessor没有返回代理对象；调用4）
               4）、Object beanInstance = doCreateBean(beanName, mbdToUse, args);创建Bean
                   1）、【创建Bean实例】；createBeanInstance(beanName, mbd, args);
                     利用工厂方法或者对象的构造器创建出Bean实例；
                   2）、applyMergedBeanDefinitionPostProcessors(mbd, beanType, beanName);
                     调用MergedBeanDefinitionPostProcessor的postProcessMergedBeanDefinition(mbd, beanType, beanName);
                   3）、【Bean属性赋值】populateBean(beanName, mbd, instanceWrapper);
                     赋值之前：
                     1）、拿到InstantiationAwareBeanPostProcessor后置处理器；
                        postProcessAfterInstantiation()；
                     2）、拿到InstantiationAwareBeanPostProcessor后置处理器；
                        postProcessPropertyValues()；
                     =====赋值之前：===
                     3）、应用Bean属性的值；为属性利用setter方法等进行赋值；
                        applyPropertyValues(beanName, mbd, bw, pvs);
                   4）、【Bean初始化】initializeBean(beanName, exposedObject, mbd);
                     1）、【执行Aware接口方法】invokeAwareMethods(beanName, bean);执行xxxAware接口的方法
                        BeanNameAware\BeanClassLoaderAware\BeanFactoryAware
                     2）、【执行后置处理器初始化之前】applyBeanPostProcessorsBeforeInitialization(wrappedBean, beanName);
                        BeanPostProcessor.postProcessBeforeInitialization();
                     3）、【执行初始化方法】invokeInitMethods(beanName, wrappedBean, mbd);
                        1）、是否是InitializingBean接口的实现；执行接口规定的初始化；
                        2）、是否自定义初始化方法；
                     4）、【执行后置处理器初始化之后】applyBeanPostProcessorsAfterInitialization
                        BeanPostProcessor.postProcessAfterInitialization()；
                   5）、注册Bean的销毁方法；
               5）、将创建的Bean添加到缓存中singletonObjects；
            ioc容器就是这些Map；很多的Map里面保存了单实例Bean，环境信息。。。。；
      所有Bean都利用getBean创建完成以后；
         检查所有的Bean是否是SmartInitializingSingleton接口的；如果是；就执行afterSingletonsInstantiated()；
12、finishRefresh();完成BeanFactory的初始化创建工作；IOC容器就创建完成；
      1）、initLifecycleProcessor();初始化和生命周期有关的后置处理器；LifecycleProcessor
         默认从容器中找是否有lifecycleProcessor的组件【LifecycleProcessor】；如果没有new DefaultLifecycleProcessor();
         加入到容器；
         
         写一个LifecycleProcessor的实现类，可以在BeanFactory
            void onRefresh();
            void onClose();    
      2）、    getLifecycleProcessor().onRefresh();
         拿到前面定义的生命周期处理器（BeanFactory）；回调onRefresh()；
      3）、publishEvent(new ContextRefreshedEvent(this));发布容器刷新完成事件；
      4）、liveBeansView.registerApplicationContext(this);
   
   ======总结===========
   1）、Spring容器在启动的时候，先会保存所有注册进来的Bean的定义信息；
      1）、xml注册bean；<bean>
      2）、注解注册Bean；@Service、@Component、@Bean、xxx
   2）、Spring容器会合适的时机创建这些Bean
      1）、用到这个bean的时候；利用getBean创建bean；创建好以后保存在容器中；
      2）、统一创建剩下所有的bean的时候；finishBeanFactoryInitialization()；
   3）、后置处理器；BeanPostProcessor
      1）、每一个bean创建完成，都会使用各种后置处理器进行处理；来增强bean的功能；
         AutowiredAnnotationBeanPostProcessor:处理自动注入
         AnnotationAwareAspectJAutoProxyCreator:来做AOP功能；
         xxx....
         增强的功能注解：
         AsyncAnnotationBeanPostProcessor
         ....
   4）、事件驱动模型；
      ApplicationListener；事件监听；
      ApplicationEventMulticaster；事件派发：
```

## Bean生命周期

Bean生命周期主要为四个阶段

* 实例化
* 属性赋值
* 初始化
* 销毁

在初始化和销毁阶段，有三对可以执行初始化方法和销毁方法。

1. 通过@Bean指定initMethod和destroyMethod
2. 通过让Bean实现InitializingBean（定义初始化逻辑），DisposableBean（定义销毁逻辑）;
3. 使用JSR250；@PostConstruct：在bean创建完成并且属性赋值完成，来执行初始化方法； @PreDestroy：在容器销毁bean之前通知我们进行清理工作

如果同时使用上面三种方法和实现BeanPostProcessor，他们的执行顺序如下图：

<div align="center"> <img src="https://gitee.com/wardseptember/images/raw/master/imgs/Xnip2021-01-22_18-34-41.jpg" width="600" height = "1500"/> </div><br>

### Bean生命周期

1. 读取BeanDefinition信息
2. 注册各种BeanPostProcessor
3. 实例化之前先执行InstantiationAwareBeanPostProcessor，执行applyBeanPostProcessorsBeforeInstantiation方法，可以返回Bean的代理对象
4. 利用反射实例化Bean
5. 实例化完成后，调用MergedBeanDefinitionPostProcessor的postProcessMergedBeanDefinition(mbd, beanType, beanName);
6. 然后调用InstantiationAwareBeanPostProcessor的postProcessAfterInstantiation方法
7. 执行populateBean方法，对Bean进行属性赋值
8. 如果Bean实现了XXXAware接口，就为Bean设置上这些属性，首先执行的是BeanNameAware、BeanClassLoaderAware、BeanFactoryAware
9. 执行BeanPostProcessor.postProcessBeforeInitialization方法
10. 如果标注了@PostConstruct就先执行这个初始化方法；如果实现了InitializingBean，就再执行这个初始化方法；然后执行自定义的初始化方法。
11. 初始化完成后，执行BeanPostProcessor.postProcessAfterInitialization()
12. 如果容器关闭，就依次执行@PreDestory、DisposableBean、destroyMethod等销毁方法

## 自动注入的原理

```java
/**
 * 自动装配;
 * 		Spring利用依赖注入（DI），完成对IOC容器中中各个组件的依赖关系赋值；
 * 
 * 1）、@Autowired：自动注入：
 * 		1）、默认优先按照类型去容器中找对应的组件:applicationContext.getBean(BookDao.class);找到就赋值
 * 		2）、如果找到多个相同类型的组件，再将属性的名称作为组件的id去容器中查找
 * 							applicationContext.getBean("bookDao")
 * 		3）、@Qualifier("bookDao")：使用@Qualifier指定需要装配的组件的id，而不是使用属性名
 * 		4）、自动装配默认一定要将属性赋值好，没有就会报错；
 * 			可以使用@Autowired(required=false);
 * 		5）、@Primary：让Spring进行自动装配的时候，默认使用首选的bean；
 * 				也可以继续使用@Qualifier指定需要装配的bean的名字
 * 		BookService{
 * 			@Autowired
 * 			BookDao  bookDao;
 * 		}
 * 
 * 2）、Spring还支持使用@Resource(JSR250)和@Inject(JSR330)[java规范的注解]
 * 		@Resource:
 * 			可以和@Autowired一样实现自动装配功能；默认是按照组件名称进行装配的；
 * 			没有能支持@Primary功能没有支持@Autowired（reqiured=false）;
 * 		@Inject:
 * 			需要导入javax.inject的包，和Autowired的功能一样。没有required=false的功能；
 *  @Autowired:Spring定义的； @Resource、@Inject都是java规范
 * 	
 * AutowiredAnnotationBeanPostProcessor:解析完成自动装配功能；		
 * 
 * 3）、 @Autowired:构造器，参数，方法，属性；都是从容器中获取参数组件的值
 * 		1）、[标注在方法位置]：@Bean+方法参数；参数从容器中获取;默认不写@Autowired效果是一样的；都能自动装配
 * 		2）、[标在构造器上]：如果组件只有一个有参构造器，这个有参构造器的@Autowired可以省略，参数位置的组件还是可以自动从容器中获取
 * 		3）、放在参数位置：
 * 
 * 4）、自定义组件想要使用Spring容器底层的一些组件（ApplicationContext，BeanFactory，xxx）；
 * 		自定义组件实现xxxAware；在创建对象的时候，会调用接口规定的方法注入相关组件；Aware；
 * 		把Spring底层一些组件注入到自定义的Bean中；
 * 		xxxAware：功能使用xxxProcessor；
 * 			ApplicationContextAware==》ApplicationContextAwareProcessor；
 * 	
 * 		
 * 
 *
 */
```

## 循环依赖

* https://www.cnblogs.com/daimzh/p/13256413.html

# AOP

AOP(Aspect-Oriented Programming:面向切面编程)能够将那些与业务无关，**却为业务模块所共同调用的逻辑或责任（例如事务处理、日志管理、权限控制等）封装起来**，便于**减少系统的重复代码**，**降低模块间的耦合度**，并**有利于未来的可拓展性和可维护性**。

**Spring AOP就是基于动态代理的**，如果要代理的对象，实现了某个接口，那么Spring AOP会使用**JDK Proxy**，去创建代理对象，而对于没有实现接口的对象，就无法使用 JDK Proxy 去进行代理了，这时候Spring AOP会使用**Cglib** ，这时候Spring AOP会使用 **Cglib** 生成一个被代理对象的子类来作为代理，如下图所示：

![](https://gitee.com/wardseptember/images/raw/master/imgs/20201013201004.png)

当然你也可以使用 AspectJ ,Spring AOP 已经集成了AspectJ ，AspectJ 应该算的上是 Java 生态系统中最完整的 AOP 框架了。

使用 AOP 之后我们可以把一些通用功能抽象出来，在需要用到的地方直接使用即可，这样大大简化了代码量。我们需要增加新功能时也方便，这样也提高了系统扩展性。日志功能、事务管理等等场景都用到了 AOP 。

## AOP原理

1. @EnableAspectJAutoProxy开启AOP功能，并会给容器注册一个AnnotationAwareAspectJAutoProxyCreator；AnnotationAwareAspectJAutoProxyCreator是一个后置处理器
2. 在registerBeanPostProcessors方法中创建AnnotationAwareAspectJAutoProxyCreator对象
3. 在finishBeanFactoryInitialization方法中，在创建业务逻辑组件和切面组件时，AnnotationAwareAspectJAutoProxyCreator拦截组件的创建过程；组件创建完之后，将切面的通知方法，包装成增强器（Advisor）;给业务逻辑组件创建一个代理对象（cglib）；
4. 代理对象执行目标方法：先得到目标方法的拦截器链，然后利用拦截器的链式机制，依次进入每一个拦截器进行执行；
    * 正常执行：前置通知-》目标方法-》后置通知-》返回通知
    * 出现异常：前置通知-》目标方法-》后置通知-》异常通知

### 详细

```java
/**
 * AOP：【动态代理】
 * 		指在程序运行期间动态的将某段代码切入到指定方法指定位置进行运行的编程方式；
 *
 * 1、导入aop模块；Spring AOP：(spring-aspects)
 * 2、定义一个业务逻辑类（MathCalculator）；在业务逻辑运行的时候将日志进行打印（方法之前、方法运行结束、方法出现异常，xxx）
 * 3、定义一个日志切面类（LogAspects）：切面类里面的方法需要动态感知MathCalculator.div运行到哪里然后执行；
 * 		通知方法：
 * 			前置通知(@Before)：logStart：在目标方法(div)运行之前运行
 * 			后置通知(@After)：logEnd：在目标方法(div)运行结束之后运行（无论方法正常结束还是异常结束）
 * 			返回通知(@AfterReturning)：logReturn：在目标方法(div)正常返回之后运行
 * 			异常通知(@AfterThrowing)：logException：在目标方法(div)出现异常以后运行
 * 			环绕通知(@Around)：动态代理，手动推进目标方法运行（joinPoint.procced()）
 * 4、给切面类的目标方法标注何时何地运行（通知注解）；
 * 5、将切面类和业务逻辑类（目标方法所在类）都加入到容器中;
 * 6、必须告诉Spring哪个类是切面类(给切面类上加一个注解：@Aspect)
 * [7]、给配置类中加 @EnableAspectJAutoProxy 【开启基于注解的aop模式】
 * 		在Spring中很多的 @EnableXXX;
 *
 * 三步：
 * 	1）、将业务逻辑组件和切面类都加入到容器中；告诉Spring哪个是切面类（@Aspect）
 * 	2）、在切面类上的每一个通知方法上标注通知注解，告诉Spring何时何地运行（切入点表达式）
 *  3）、开启基于注解的aop模式；@EnableAspectJAutoProxy
 *
 * AOP原理：【看给容器中注册了什么组件，这个组件什么时候工作，这个组件的功能是什么？】
 * 		@EnableAspectJAutoProxy；
 * 1、@EnableAspectJAutoProxy是什么？
 * 		@Import(AspectJAutoProxyRegistrar.class)：给容器中导入AspectJAutoProxyRegistrar
 * 			利用AspectJAutoProxyRegistrar自定义给容器中注册bean；BeanDefinetion
 * 			internalAutoProxyCreator=AnnotationAwareAspectJAutoProxyCreator
 *
 * 		给容器中注册一个AnnotationAwareAspectJAutoProxyCreator；
 *
 * 2、 AnnotationAwareAspectJAutoProxyCreator：
 * 		AnnotationAwareAspectJAutoProxyCreator
 * 			->AspectJAwareAdvisorAutoProxyCreator
 * 				->AbstractAdvisorAutoProxyCreator
 * 					->AbstractAutoProxyCreator
 * 							implements SmartInstantiationAwareBeanPostProcessor, BeanFactoryAware
 * 						关注后置处理器（在bean初始化完成前后做事情）、自动装配BeanFactory
 *
 * AbstractAutoProxyCreator.setBeanFactory()
 * AbstractAutoProxyCreator.有后置处理器的逻辑；
 *
 * AbstractAdvisorAutoProxyCreator.setBeanFactory()-》initBeanFactory()
 *
 * AnnotationAwareAspectJAutoProxyCreator.initBeanFactory()
 *
 *
 * 流程：
 * 		1）、传入配置类，创建ioc容器
 * 		2）、注册配置类，调用refresh（）刷新容器；
 * 		3）、registerBeanPostProcessors(beanFactory);注册bean的后置处理器来方便拦截bean的创建；
 * 			1）、先获取ioc容器已经定义了的需要创建对象的所有BeanPostProcessor
 * 			2）、给容器中加别的BeanPostProcessor
 * 			3）、优先注册实现了PriorityOrdered接口的BeanPostProcessor；
 * 			4）、再给容器中注册实现了Ordered接口的BeanPostProcessor；
 * 			5）、注册没实现优先级接口的BeanPostProcessor；
 * 			6）、注册BeanPostProcessor，实际上就是创建BeanPostProcessor对象，保存在容器中；
 * 				创建internalAutoProxyCreator的BeanPostProcessor【AnnotationAwareAspectJAutoProxyCreator】
 * 				1）、创建Bean的实例
 * 				2）、populateBean；给bean的各种属性赋值
 * 				3）、initializeBean：初始化bean；
 * 						1）、invokeAwareMethods()：处理Aware接口的方法回调
 * 						2）、applyBeanPostProcessorsBeforeInitialization()：应用后置处理器的postProcessBeforeInitialization（）
 * 						3）、invokeInitMethods()；执行自定义的初始化方法
 * 						4）、applyBeanPostProcessorsAfterInitialization()；执行后置处理器的postProcessAfterInitialization（）；
 * 				4）、BeanPostProcessor(AnnotationAwareAspectJAutoProxyCreator)创建成功；--》aspectJAdvisorsBuilder
 * 			7）、把BeanPostProcessor注册到BeanFactory中；
 * 				beanFactory.addBeanPostProcessor(postProcessor);
 * =======以上是创建和注册AnnotationAwareAspectJAutoProxyCreator的过程========
 *
 * 			AnnotationAwareAspectJAutoProxyCreator => InstantiationAwareBeanPostProcessor
 * 		4）、finishBeanFactoryInitialization(beanFactory);完成BeanFactory初始化工作；创建剩下的单实例bean
 * 			1）、遍历获取容器中所有的Bean，依次创建对象getBean(beanName);
 * 				getBean->doGetBean()->getSingleton()->
 * 			2）、创建bean
 * 				【AnnotationAwareAspectJAutoProxyCreator在所有bean创建之前会有一个拦截，InstantiationAwareBeanPostProcessor，会调用postProcessBeforeInstantiation()】
 * 				1）、先从缓存中获取当前bean，如果能获取到，说明bean是之前被创建过的，直接使用，否则再创建；
 * 					只要创建好的Bean都会被缓存起来
 * 				2）、createBean（）;创建bean；
 * 					AnnotationAwareAspectJAutoProxyCreator 会在任何bean创建之前先尝试返回bean的实例
 * 					【BeanPostProcessor是在Bean对象创建完成初始化前后调用的】
 * 					【InstantiationAwareBeanPostProcessor是在创建Bean实例之前先尝试用后置处理器返回对象的】
 * 					1）、resolveBeforeInstantiation(beanName, mbdToUse);解析BeforeInstantiation
 * 						希望后置处理器在此能返回一个代理对象；如果能返回代理对象就使用，如果不能就继续
 * 						1）、后置处理器先尝试返回对象；
 * 							bean = applyBeanPostProcessorsBeforeInstantiation（）：
 * 								拿到所有后置处理器，如果是InstantiationAwareBeanPostProcessor;
 * 								就执行postProcessBeforeInstantiation
 * 							if (bean != null) {
bean = applyBeanPostProcessorsAfterInitialization(bean, beanName);
}
 *
 * 					2）、doCreateBean(beanName, mbdToUse, args);真正的去创建一个bean实例；和3.6流程一样；
 * 					3）、
 *
 *
 * AnnotationAwareAspectJAutoProxyCreator【InstantiationAwareBeanPostProcessor】	的作用：
 * 1）、每一个bean创建之前，调用postProcessBeforeInstantiation()；
 * 		关心MathCalculator和LogAspect的创建
 * 		1）、判断当前bean是否在advisedBeans中（保存了所有需要增强bean）
 * 		2）、判断当前bean是否是基础类型的Advice、Pointcut、Advisor、AopInfrastructureBean，
 * 			或者是否是切面（@Aspect）
 * 		3）、是否需要跳过
 * 			1）、获取候选的增强器（切面里面的通知方法）【List<Advisor> candidateAdvisors】
 * 				每一个封装的通知方法的增强器是 InstantiationModelAwarePointcutAdvisor；
 * 				判断每一个增强器是否是 AspectJPointcutAdvisor 类型的；返回true
 * 			2）、永远返回false
 *
 * 2）、创建对象
 * postProcessAfterInitialization；
 * 		return wrapIfNecessary(bean, beanName, cacheKey);//包装如果需要的情况下
 * 		1）、获取当前bean的所有增强器（通知方法）  Object[]  specificInterceptors
 * 			1、找到候选的所有的增强器（找哪些通知方法是需要切入当前bean方法的）
 * 			2、获取到能在bean使用的增强器。
 * 			3、给增强器排序
 * 		2）、保存当前bean在advisedBeans中；
 * 		3）、如果当前bean需要增强，创建当前bean的代理对象；
 * 			1）、获取所有增强器（通知方法）
 * 			2）、保存到proxyFactory
 * 			3）、创建代理对象：Spring自动决定
 * 				JdkDynamicAopProxy(config);jdk动态代理；
 * 				ObjenesisCglibAopProxy(config);cglib的动态代理；
 * 		4）、给容器中返回当前组件使用cglib增强了的代理对象；
 * 		5）、以后容器中获取到的就是这个组件的代理对象，执行目标方法的时候，代理对象就会执行通知方法的流程；
 *
 *
 * 	3）、目标方法执行	；
 * 		容器中保存了组件的代理对象（cglib增强后的对象），这个对象里面保存了详细信息（比如增强器，目标对象，xxx）；
 * 		1）、CglibAopProxy.intercept();拦截目标方法的执行
 * 		2）、根据ProxyFactory对象获取将要执行的目标方法拦截器链；
 * 			List<Object> chain = this.advised.getInterceptorsAndDynamicInterceptionAdvice(method, targetClass);
 * 			1）、List<Object> interceptorList保存所有拦截器 5
 * 				一个默认的ExposeInvocationInterceptor 和 4个增强器；
 * 			2）、遍历所有的增强器，将其转为Interceptor；
 * 				registry.getInterceptors(advisor);
 * 			3）、将增强器转为List<MethodInterceptor>；
 * 				如果是MethodInterceptor，直接加入到集合中
 * 				如果不是，使用AdvisorAdapter将增强器转为MethodInterceptor；
 * 				转换完成返回MethodInterceptor数组；
 *
 * 		3）、如果没有拦截器链，直接执行目标方法;
 * 			拦截器链（每一个通知方法又被包装为方法拦截器，利用MethodInterceptor机制）
 * 		4）、如果有拦截器链，把需要执行的目标对象，目标方法，
 * 			拦截器链等信息传入创建一个 CglibMethodInvocation 对象，
 * 			并调用 Object retVal =  mi.proceed();
 * 		5）、拦截器链的触发过程;
 * 			1)、如果没有拦截器执行执行目标方法，或者拦截器的索引和拦截器数组-1大小一样（指定到了最后一个拦截器）执行目标方法；
 * 			2)、链式获取每一个拦截器，拦截器执行invoke方法，每一个拦截器等待下一个拦截器执行完成返回以后再来执行；
 * 				拦截器链的机制，保证通知方法与目标方法的执行顺序；
 *
 * 	总结：
 * 		1）、  @EnableAspectJAutoProxy 开启AOP功能
 * 		2）、 @EnableAspectJAutoProxy 会给容器中注册一个组件 AnnotationAwareAspectJAutoProxyCreator
 * 		3）、AnnotationAwareAspectJAutoProxyCreator是一个后置处理器；
 * 		4）、容器的创建流程：
 * 			1）、registerBeanPostProcessors（）注册后置处理器；创建AnnotationAwareAspectJAutoProxyCreator对象
 * 			2）、finishBeanFactoryInitialization（）初始化剩下的单实例bean
 * 				1）、创建业务逻辑组件和切面组件
 * 				2）、AnnotationAwareAspectJAutoProxyCreator拦截组件的创建过程
 * 				3）、组件创建完之后，判断组件是否需要增强
 * 					是：切面的通知方法，包装成增强器（Advisor）;给业务逻辑组件创建一个代理对象（cglib）；
 * 		5）、执行目标方法：
 * 			1）、代理对象执行目标方法
 * 			2）、CglibAopProxy.intercept()；
 * 				1）、得到目标方法的拦截器链（增强器包装成拦截器MethodInterceptor）
 * 				2）、利用拦截器的链式机制，依次进入每一个拦截器进行执行；
 * 				3）、效果：
 * 					正常执行：前置通知-》目标方法-》后置通知-》返回通知
 * 					出现异常：前置通知-》目标方法-》后置通知-》异常通知
 *
 *
 *
 */
```

