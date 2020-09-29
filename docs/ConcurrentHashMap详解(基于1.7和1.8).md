# ConcurrentHashMap 1.7

首先将数据分为一段一段的存储，然后给每一段数据配一把锁，当一个线程占用锁访问其中一个段数据 时，其他段的数据也能被其他线程访问。

**ConcurrentHashMap** 是由 **Segment** 数组结构和 **HashEntry** 数组结构组成。

Segment 继承了 ReentrantLock,所以 Segment 是一种可重入锁，扮演锁的⻆色。HashEntry 用于存储 键值对数据。

![](https://gitee.com/wardseptember/images/raw/master/imgs/20200928220201.png)

一个 ConcurrentHashMap 里包含一个 Segment 数组。Segment 的结构和 HashMap 类似，是一种数组 和链表结构，一个 Segment 包含一个 HashEntry 数组，每个 HashEntry 是一个链表结构的元素，每 个 Segment 守护着一个 HashEntry 数组里的元素，当对 HashEntry 数组的数据进行修改时，必须首 先获得对应的 Segment 的锁。

![](https://gitee.com/wardseptember/images/raw/master/imgs/20200928221841.png)

## put操作

对于ConcurrentHashMap的数据插入，这里要进行两次Hash去定位数据的存储位置

```dart
static class  Segment<K,V> extends  ReentrantLock implements  Serializable {
}
```

从上Segment的继承体系可以看出，Segment实现了ReentrantLock,也就带有锁的功能，当执行put操作时，会进行第一次key的hash来定位Segment的位置，如果该Segment还没有初始化，即通过CAS操作进行赋值，然后进行第二次hash操作，找到相应的HashEntry的位置，这里会利用继承过来的锁的特性，在将数据插入指定的HashEntry位置时（链表的尾端），会通过继承ReentrantLock的tryLock（）方法尝试去获取锁，如果获取成功就直接插入相应的位置，如果已经有线程获取该Segment的锁，那当前线程会以自旋的方式去继续的调用tryLock（）方法去获取锁，超过指定次数就挂起，等待唤醒。

## get操作

ConcurrentHashMap的get操作跟HashMap类似，只是ConcurrentHashMap第一次需要经过一次hash定位到Segment的位置，然后再hash定位到指定的HashEntry，遍历该HashEntry下的链表进行对比，成功就返回，不成功就返回null。

## size操作

第一种方案他会使用不加锁的模式去尝试多次计算ConcurrentHashMap的size，最多三次，比较前后两次计算的结果，结果一致就认为当前没有元素加入，计算的结果是准确的

第二种方案是如果第一种方案不符合，他就会给每个Segment加上锁，然后计算ConcurrentHashMap的size返回

# ConcurrentHashMap 1.8

ConcurrentHashMap不允许空值空键

ConcurrentHashMap 取消了 Segment 分段锁，采用 CAS 和 synchronized 来保证并发安全。数据结构 跟 HashMap1.8 的结构类似，数组+链表/红黑二叉树。Java 8 在链表⻓度超过一定阈值(8)时将链表 (寻址时间复杂度为 O(N))转换为红黑树(寻址时间复杂度为 O(log(N)))

![](https://gitee.com/wardseptember/images/raw/master/imgs/20200928220802.png)

synchronized 只锁定当前链表或红黑二叉树的首节点，这样只要 hash 不冲突，就不会产生并发，效 率又提升 N 倍。

## sizeCtl含义

```java
private transient volatile int sizeCtl;
```

sizeCtl在初始化时一直出现，在扩容的时候也有使用。

* sizeCtl为0，代表数组未初始化，且数组的初始容量为16
* sizeCtl为正数，如果数组未初始化，那么其记录的是数组的初始容量，如果数组已经初始化，那么其记录的是数组的扩容阈值。
* sizeCtl为-1，表示数组正在进行初始化
* sizeCtl小于0，并且不是-1，表示数组正在扩容，-(1 + n)表示此时有n个线程正在共同完成数组的扩容操作。

## put方法

1. 如果没有初始化就先调用initTable（）方法来进行初始化过程
2. 如果没有hash冲突就直接CAS插入
3. 如果还在进行扩容操作就先进行扩容
4. 如果存在hash冲突，就加锁来保证线程安全，这里有两种情况，一种是链表形式就直接遍历到尾端插入，一种是红黑树就按照红黑树结构插入，
5. 最后一个如果Hash冲突时会形成Node链表，在链表长度超过8，Node数组超过64时会将链表结构转换为红黑树的结构，break再一次进入循环
6. 如果添加成功就调用addCount（）方法统计size，并且检查是否需要扩容

## get操作

1. 计算hash值，定位到该table索引位置，如果是首节点符合就返回

2. 如果遇到扩容的时候，会调用标志正在扩容节点ForwardingNode的find方法，查找该节点，匹配就返回

3. 以上都不符合的话，就往下遍历节点，匹配就返回，否则最后就返回null

## 扩容

ConcurrentHashMap是多线程动态扩容，一个线程负责一段数组，将老数组里面的元素添加到新数组里面。

## 计算容量

添加容量并没有加锁，而是使用cas方式，往一个数组里面的+1，最后将整个数组求和，就是当前ConcurrentHashMap的大小。

```java
    private transient volatile CounterCell[] counterCells;

    @sun.misc.Contended static final class CounterCell {
        volatile long value;
        CounterCell(long x) { value = x; }
    }
```



```java
    final long sumCount() {
        CounterCell[] as = counterCells; CounterCell a;
        long sum = baseCount;
        if (as != null) {
            for (int i = 0; i < as.length; ++i) {
                if ((a = as[i]) != null)
                    sum += a.value;
            }
        }
        return sum;
    }
```

## TODO

* 更详细的ConcurrentHashMap笔记

