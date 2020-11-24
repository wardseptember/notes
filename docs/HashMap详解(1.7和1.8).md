# HashMap 1.7

使用数组加链表实现hashmap。

hashmap初始容量为16，装载因子为0.75，hashmap里面的元素达到阈值(阈值=容量 * 装载因子)时，就会进行扩容，每次扩容2倍。

## put方法

```java
    public V put(K key, V value) {
        // 当第一次往里面放元素时才真正地申请空间
        if (table == EMPTY_TABLE) {
            inflateTable(threshold);
        }
        if (key == null)
            return putForNullKey(value);
        // 计算hash值
        int hash = hash(key);
        // 计算索引值，大小为0到table.length - 1
        int i = indexFor(hash, table.length);
        // 如果已经存在这个key，则更新value值
        for (Entry<K,V> e = table[i]; e != null; e = e.next) {
            Object k;
            if (e.hash == hash && ((k = e.key) == key || key.equals(k))) {
                V oldValue = e.value;
                e.value = value;
                e.recordAccess(this);
                return oldValue;
            }
        }
		
        modCount++;
        // 不存在这个key,就新增
        addEntry(hash, key, value, i);
        return null;
    }
```

### hash方法

将hashcode的高位和低位混合求hash值，减少冲突

```java
    final int hash(Object k) {
        int h = hashSeed;
        if (0 != h && k instanceof String) {
            return sun.misc.Hashing.stringHash32((String) k);
        }

        h ^= k.hashCode();

        // This function ensures that hashCodes that differ only by
        // constant multiples at each bit position have a bounded
        // number of collisions (approximately 8 at default load factor).
        h ^= (h >>> 20) ^ (h >>> 12);
        return h ^ (h >>> 7) ^ (h >>> 4);
    }
```

### indexFor方法

hash & (length -1)可以将所有hash值映射到0到length-1范围内，这也解释了为什么hashmap的容量必须是2的倍数。

```java
    static int indexFor(int h, int length) {
        // assert Integer.bitCount(length) == 1 : "length must be a non-zero power of 2";
        return h & (length-1);
    }
```

### addEntry方法

```java
    void addEntry(int hash, K key, V value, int bucketIndex) {
        // 扩容
        if ((size >= threshold) && (null != table[bucketIndex])) {
            resize(2 * table.length);
            hash = (null != key) ? hash(key) : 0;
            bucketIndex = indexFor(hash, table.length);
        }
		// 添加新元素
        createEntry(hash, key, value, bucketIndex);
    }
```

### resize方法——扩容

```java
    void resize(int newCapacity) {
        Entry[] oldTable = table;
        int oldCapacity = oldTable.length;
        if (oldCapacity == MAXIMUM_CAPACITY) {
            threshold = Integer.MAX_VALUE;
            return;
        }

        Entry[] newTable = new Entry[newCapacity];
        transfer(newTable, initHashSeedAsNeeded(newCapacity));
        table = newTable;
        threshold = (int)Math.min(newCapacity * loadFactor, MAXIMUM_CAPACITY + 1);
    }
```

### initHashSeedAsNeeded方法

initHashSeedAsNeeded方法判断是否需要rehash

```java
    final boolean initHashSeedAsNeeded(int capacity) {
        // hashSeed降低hash碰撞的hash种子，初始值为0
        boolean currentAltHashing = hashSeed != 0;
        //ALTERNATIVE_HASHING_THRESHOLD： 当map的capacity容量大于这个值的时候并满足其他条件时候进行重新hash
        boolean useAltHashing = sun.misc.VM.isBooted() && (capacity >= Holder.ALTERNATIVE_HASHING_THRESHOLD);
        //TODO 异或操作，二者满足一个条件即可rehash
        boolean switching = currentAltHashing ^ useAltHashing;
        if (switching) {
            // 更新hashseed的值
            hashSeed = useAltHashing ? sun.misc.Hashing.randomHashSeed(this) : 0;
        }
        return switching;
    }
```

### transfer方法

将原始table中元素复制到newTable

```java
    void transfer(Entry[] newTable, boolean rehash) {
        int newCapacity = newTable.length;
        for (Entry<K,V> e : table) {
            while(null != e) {
                Entry<K,V> next = e.next;
                if (rehash) {
                    e.hash = null == e.key ? 0 : hash(e.key);
                }
                int i = indexFor(e.hash, newCapacity);
                e.next = newTable[i];
                newTable[i] = e;
                e = next;
            }
        }
    }
```

### createEntry方法

如果没有超过阈值，则直接存入table

```java
    void createEntry(int hash, K key, V value, int bucketIndex) {
        Entry<K,V> e = table[bucketIndex];
        table[bucketIndex] = new Entry<>(hash, key, value, e);
        size++;
    }
```

## get方法

```java
    public V get(Object key) {
        if (key == null)
            return getForNullKey();
        // 调用getEntry方法
        Entry<K,V> entry = getEntry(key);

        return null == entry ? null : entry.getValue();
    }
```

### getEntry方法

```java
    final Entry<K,V> getEntry(Object key) {
        if (size == 0) {
            return null;
        }

        int hash = (key == null) ? 0 : hash(key);
        // 先找到在那个table[i]，然后遍历链表找到这个key
        for (Entry<K,V> e = table[indexFor(hash, table.length)];
             e != null;
             e = e.next) {
            Object k;
            if (e.hash == hash &&
                ((k = e.key) == key || (key != null && key.equals(k))))
                return e;
        }
        return null;
    }
```

## 存在的问题

* 并发环境中易死锁

* 可以通过精心构造的恶意请求引发DOS

# HashMap 1.8

`HashMap`结构图：

![](http://wardseptember.top/FjO6pGCUZafcw5DGVmQnv0-kPrL5)

 HashMap：它根据键的hashCode值存储数据，大多数情况下可以直接定位到它的值，因而具有很快的访问速度，但遍历顺序却是不确定的。 HashMap最多只允许一条记录的键为null，允许多条记录的值为null。HashMap非线程安全，即任一时刻可以有多个线程同时写HashMap，可能会导致数据的不一致。如果需要满足线程安全，可以用 Collections的synchronizedMap方法使HashMap具有线程安全的能力，或者使用ConcurrentHashMap。

默认的初始容量是16
默认的负载因子0.75
当桶上的结点数大于8会转成红黑树
当桶上的结点数小于6红黑树转链表
Node<k,v>[] table //存储元素的哈希桶数组，总是2的幂次倍

## 为什么哈希数组table的大小必须是2的倍数（合数）？

1. 当数组长度为2的幂次方时，可以使用位运算来计算元素在数组中的下标
2. 增加hash值的随机性，减少hash冲突

看一下hashmap的源码：

```java
//计算hash值
static final int hash(Object key) {
int h;
return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
}
```

`h >>> 16`表示无符号右移16位，低位挤走，高位补0；^ 为按位异或，即转成二进制后，相异为1，相同为0；由此可发现，当传入的值小于 2的16次方-1 时，调用这个方法返回的值，都是自身的值。

右位移16位，正好是32bit的一半，自己的高半区和低半区做异或，就是为了混合原始哈希码的高位和低位，以此来加大低位的随机性。而且混合后的低位掺杂了高位的部分特征，这样高位的信息也被变相保留下来。
假如没有进行高位运算，那最后参与运算的永远只是取模运算的最后几位，相似性会比较大。

[JDK 源码中 HashMap 的 hash 方法原理](https://link.jianshu.com/?t=https%3A%2F%2Fwww.zhihu.com%2Fquestion%2F20733617%2Fanswer%2F111577937)

![](http://wardseptember.top/FviYD1i2KPPm7G3Ocar06b8y7gi5)

*hash函数的主要作用就是：增大随机性，减少碰撞。*

hashmap中put的源码:

```java
//put源码
public V put(K key, V value) {
	return putVal(hash(key), key, value, false, true);
}
final V putVal(int hash, K key, V value, boolean onlyIfAbsent,
                   boolean evict) {
        Node<K,V>[] tab; Node<K,V> p; int n, i;
        if ((tab = table) == null || (n = tab.length) == 0)
            n = (tab = resize()).length;
        if ((p = tab[i = (n - 1) & hash]) == null)
            tab[i] = newNode(hash, key, value, null);
        else {
            Node<K,V> e; K k;
            if (p.hash == hash &&
                ((k = p.key) == key || (key != null && key.equals(k))))
                e = p;
            else if (p instanceof TreeNode)
                e = ((TreeNode<K,V>)p).putTreeVal(this, tab, hash, key, value);
            else {
                for (int binCount = 0; ; ++binCount) {
                    if ((e = p.next) == null) {
                        p.next = newNode(hash, key, value, null);
                        if (binCount >= TREEIFY_THRESHOLD - 1) // -1 for 1st
                            treeifyBin(tab, hash);
                        break;
                    }
                    if (e.hash == hash &&
                        ((k = e.key) == key || (key != null && key.equals(k))))
                        break;
                    p = e;
                }
            }
            if (e != null) { // existing mapping for key
                V oldValue = e.value;
                if (!onlyIfAbsent || oldValue == null)
                    e.value = value;
                afterNodeAccess(e);
                return oldValue;
            }
        }
        ++modCount;
        if (++size > threshold)
            resize();
        afterNodeInsertion(evict);
        return null;
    }
```

里面非常巧妙的代码是`p = tab[i = (n - 1) & hash]`，tab是hashmap存放存放元素的数组，`(n - 1) & hash`也解释了为什么table的大小要是2的倍数。

如果n是默认大小16，没有扩容，`(n - 1) & hash`的计算结果就是hash值本身；见下图：

![](http://wardseptember.top/FnoOXwzol6IFaNzkiZtRkKr5H32a)

如果n扩容，扩容大小是原大小*2，为什么n一定要是2的倍数？举个例子：

```java
设：oldCap=16 二进制为：0001 0000  // oldCap是扩容之前的table大小
oldCap-1=15 二进制为：0000 1111   // 如果oldCap是2的倍数，低位就全部是1，与hash进行&运算，hash值不变
e1.hash=10 二进制为：0000 1010
e2.hash=26 二进制为：0101 1010
e1在扩容前的位置为：e1.hash & oldCap-1  结果为：0000 1010 
e2在扩容前的位置为：e2.hash & oldCap-1  结果为：0000 1010 
结果相同，所以e1和e2在扩容前在同一个链表上，这是扩容之前的状态。
        
现在扩容后，需要重新计算元素的位置，在扩容前的链表中计算地址的方式为e.hash & oldCap-1
那么在扩容后应该也这么计算呀，扩容后的容量为oldCap*2=32 0010 0000 newCap=32，新的计算
方式应该为
e1.hash & newCap-1 
即：0000 1010 & 0001 1111 
结果为0000 1010与扩容前的位置完全一样。
e2.hash & newCap-1 
即：0101 1010 & 0001 1111 
结果为0001 1010,为扩容前位置+oldCap。
```

由此可见，扩容后的hashmap本来存在的数据位置不用改变，新增的数据的存储位置是扩容前位置+oldCap，直接可以计算出扩容后的位置，减少了一次求hash值的次数(不需要像JDK1.7的实现那样重新计算hash)；而且将有冲突的数据均匀的分散到新的空间上；而且&运算比%取模运算要快；

当桶上的结点数大于8会转成红黑树：

![](http://wardseptember.club/FilCh0t268Fot12pqsnGGsw3YVG-)

红黑树的查找速度更快，查找速度优化为O(logn)。

红黑树知识可以查看我的另一篇教程，[红黑树](https://wardseptember.github.io/notes/#/docs/红黑树)。或者下面的教程

- [30张图带你彻底理解红黑树](https://www.jianshu.com/p/e136ec79235c)
- [关于红黑树(R-B tree)原理，看这篇如何](https://www.cnblogs.com/LiaHon/p/11203229.html)
- [可视化动态生成红黑树](https://www.cs.usfca.edu/~galles/visualization/RedBlack.html)

## 如何扩容

HashMap每次扩容都是建立一个新的table数组，长度和容量阈值都变为原来的两倍，然后把原数组元素重新映射到新数组上，具体步骤如下：

1. 首先会判断table数组长度，如果大于0说明已被初始化过，那么`按当前table数组长度的2倍进行扩容，阈值也变为原来的2倍`
2. 若table数组未被初始化过，且threshold(阈值)大于0说明调用了`HashMap(initialCapacity, loadFactor)`构造方法，那么就把数组大小设为threshold
3. 若table数组未被初始化，且threshold为0说明调用`HashMap()`构造方法，那么就把数组大小设为`16`，threshold设为`16*0.75`
4. 接着需要判断如果不是第一次初始化，那么扩容之后，要重新计算键值对的位置，并把它们移动到合适的位置上去，如果节点是红黑树类型的话则需要进行红黑树的拆分。

这里有一个需要注意的点就是在JDK1.8 HashMap扩容阶段重新映射元素时不需要像1.7版本那样重新去一个个计算元素的hash值，而是**通过`hash & oldCap`的值来判断，若为0则索引位置不变，不为0则新索引=原索引+旧数组长度**，为什么呢？具体原因如下：

**因为我们使用的是2次幂的扩展(指长度扩为原来2倍)，所以，元素的位置要么是在原位置，要么是在原位置再移动2次幂的位置。因此，我们在扩充HashMap的时候，不需要像JDK1.7的实现那样重新计算hash，只需要看看原来的hash值新增的那个bit是1还是0就好了，是0的话索引没变，是1的话索引变成“原索引+oldCap**

![](https://gitee.com/wardseptember/images/raw/master/imgs/20200928143909.png)

为什么用hash & oldCap做判断，假设oldCap=16，二进制是10000，15的二进制是1111，hash & (length - 1)用了四位二进制可以得到所在的索引，如果需要扩容，就是原容量*2，也就是取5位二进制与hash做与算法，这里用hash & oldCap这种非常巧妙的方法，判断hash的倒数第五位二进制是不是1，如果是1，说明应该索引变成“原索引+oldCap”，为什么不用重新hash?因为重新hash的结果也是原索引+oldCap，无非就是用五位二进制算一下，通过hash & oldCap这种方式已经判断了；如果是hash & oldCap= 0，说明原位置不用动。这里非常巧妙，如果还不懂，我也没办法了，你们仔细想想。

扩容代码：

```java
final Node<K,V>[] resize() {
    Node<K,V>[] oldTab = table;
    int oldCap = (oldTab == null) ? 0 : oldTab.length;
    int oldThr = threshold;
    int newCap, newThr = 0;

    //1、若oldCap>0 说明hash数组table已被初始化
    if (oldCap > 0) {
        if (oldCap >= MAXIMUM_CAPACITY) {
            threshold = Integer.MAX_VALUE;
            return oldTab;
        }//按当前table数组长度的2倍进行扩容，阈值也变为原来的2倍
        else if ((newCap = oldCap << 1) < MAXIMUM_CAPACITY && oldCap >= DEFAULT_INITIAL_CAPACITY)
            newThr = oldThr << 1;
    }//2、若数组未被初始化，而threshold>0说明调用了HashMap(initialCapacity)和HashMap(initialCapacity, loadFactor)构造器
    else if (oldThr > 0)
        newCap = oldThr;//新容量设为数组阈值
    else { //3、若table数组未被初始化，且threshold为0说明调用HashMap()构造方法
        newCap = DEFAULT_INITIAL_CAPACITY;//默认为16
        newThr = (int)(DEFAULT_LOAD_FACTOR * DEFAULT_INITIAL_CAPACITY);//16*0.75
    }

    //若计算过程中，阈值溢出归零，则按阈值公式重新计算
    if (newThr == 0) {
        float ft = (float)newCap * loadFactor;
        newThr = (newCap < MAXIMUM_CAPACITY && ft < (float)MAXIMUM_CAPACITY ?
                  (int)ft : Integer.MAX_VALUE);
    }
    threshold = newThr;
    //创建新的hash数组，hash数组的初始化也是在这里完成的
    Node<K,V>[] newTab = (Node<K,V>[])new Node[newCap];
    table = newTab;
    //如果旧的hash数组不为空，则遍历旧数组并映射到新的hash数组
    if (oldTab != null) {
        for (int j = 0; j < oldCap; ++j) {
            Node<K,V> e;
            if ((e = oldTab[j]) != null) {
                oldTab[j] = null;//GC
                if (e.next == null)//如果只链接一个节点，重新计算并放入新数组
                    newTab[e.hash & (newCap - 1)] = e;
                //若是红黑树，则需要进行拆分
                else if (e instanceof TreeNode)
                    ((TreeNode<K,V>)e).split(this, newTab, j, oldCap);
                else {
                    //rehash————>重新映射到新数组
                    Node<K,V> loHead = null, loTail = null;
                    Node<K,V> hiHead = null, hiTail = null;
                    Node<K,V> next;
                    do {
                        next = e.next;
                        /*注意这里使用的是：e.hash & oldCap，若为0则索引位置不变，不为0则新索引=原索引+旧数组长度*/
                        if ((e.hash & oldCap) == 0) {
                            if (loTail == null)
                                loHead = e;
                            else
                                loTail.next = e;
                            loTail = e;
                        }
                        else {
                            if (hiTail == null)
                                hiHead = e;
                            else
                                hiTail.next = e;
                            hiTail = e;
                        }
                    } while ((e = next) != null);
                    if (loTail != null) {
                        loTail.next = null;
                        newTab[j] = loHead;
                    }
                    if (hiTail != null) {
                        hiTail.next = null;
                        newTab[j + oldCap] = hiHead;
                    }
                }
            }
        }
    }
    return newTab;
}
```

## 为什么链表长度大于8才变为红黑树

因为容器中节点分布在hash桶中的频率遵循lambda=0.5的泊松分布，桶的长度超过8的概率非常非常小，约0.00000006。所以一般情况下都不会转为红黑树，如果你自己写的类当做hashmap的key，实现了hashcode和equals方法，hashcode写的太烂，就有可能导致hash桶中元素超过8，避免查找、删除效率太低，所以要转为红黑树。

## 为什么不直接使用红黑树，而是链表长度大于8才专为红黑树

因为红黑树占用空间是链表的两倍，而且当链表长度短时，红黑树不一定比链表快。

### 参考链接

- https://www.jianshu.com/p/dc13f825b71f
- https://www.cnblogs.com/duodushuduokanbao/p/9492952.html
- https://blog.csdn.net/qq_37113604/article/details/81353626
- https://www.zhihu.com/question/20733617/answer/111577937