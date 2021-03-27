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

1. 首先对key进行第一次hash，通过hash值确定segment的位置

2. 然后在segment内进行操作，获取锁

3. 接着获取当前segment的HashEntry数组，然后对key进行第二次hash，通过hash值确定在HashEntry数组的索引位置。

4. 然后对当前索引的HashEntry链进行遍历，如果有重复的key，则替换；如果没有重复的，则插入

5. 关闭锁
     可见，在整个put过程中，进行了2次hash操作，才最终确定key的位置。

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

## 求hash

```java
    static final int HASH_BITS = 0x7fffffff; // usable bits of normal node hash
	static final int spread(int h) {
        return (h ^ (h >>> 16)) & HASH_BITS;
    }
```

`spread(key.hashCode());`跟hashmap类似，高16位和低16位做异或操作，增加随机性减少冲突，这里还把hash值限制在Integer.MAX_VALUE之内。

## tabAt

```java
    private static final sun.misc.Unsafe U;
	// 直接操作内存
    U = sun.misc.Unsafe.getUnsafe();
	/**
     * 寻找指定数组在内存中i位置的数据
     */
    @SuppressWarnings("unchecked")
    static final <K,V> Node<K,V> tabAt(Node<K,V>[] tab, int i) {
        return (Node<K,V>)U.getObjectVolatile(tab, ((long)i << ASHIFT) + ABASE);
    }
```

## casTabAt和setTabAt

```java
/**
 * 将结点v插入tab[i]，采用cas的方法，c是期望值，如果当前值不等于期望值就一直循环尝试插入
 * @param tab
 * @param i
 * @param c
 * @param v
 * @param <K>
 * @param <V>
 * @return
 */
static final <K,V> boolean casTabAt(Node<K,V>[] tab, int i,
                                    Node<K,V> c, Node<K,V> v) {
    return U.compareAndSwapObject(tab, ((long)i << ASHIFT) + ABASE, c, v);
}

/**
 * 将结点v设置到tab[i]的位置
 * @param tab
 * @param i
 * @param v
 * @param <K>
 * @param <V>
 */
static final <K,V> void setTabAt(Node<K,V>[] tab, int i, Node<K,V> v) {
    U.putObjectVolatile(tab, ((long)i << ASHIFT) + ABASE, v);
}
```

setTabAt都是在加锁的代码里面调用的，不然就使用casTabAt，无锁操作。

## put方法

1. 如果没有初始化就先调用initTable()方法来进行初始化过程
2. 如果没有hash冲突就直接CAS插入
3. 如果还在进行扩容操作就先进行协作扩容
4. 如果存在hash冲突，就加锁来保证线程安全，这里有两种情况，一种是链表形式就直接遍历到尾端插入，一种是红黑树就按照红黑树结构插入，
5. 最后一个如果Hash冲突时会形成Node链表，在链表长度超过8，Node数组超过64时会将链表结构转换为红黑树的结构，break退出循环
6. 如果添加成功就调用addCount()方法统计size，并且检查是否需要扩容

```java
    public V put(K key, V value) {
        return putVal(key, value, false);
    }

    /** Implementation for put and putIfAbsent */
    final V putVal(K key, V value, boolean onlyIfAbsent) {
        if (key == null || value == null) throw new NullPointerException();
        int hash = spread(key.hashCode());
        // 统计桶中数量
        int binCount = 0;
        for (Node<K,V>[] tab = table;;) {
            Node<K,V> f; int n, i, fh;
            // tab=null，就初始化table
            if (tab == null || (n = tab.length) == 0)
                tab = initTable();
            // tab[i]=null,就cas插入key、value
            else if ((f = tabAt(tab, i = (n - 1) & hash)) == null) {
                if (casTabAt(tab, i, null,
                             new Node<K,V>(hash, key, value, null)))
                    break;                   // no lock when adding to empty bin
            }
            // 如果正在扩容，就当前线程就去协助扩容
            else if ((fh = f.hash) == MOVED)
                tab = helpTransfer(tab, f);
            // 存在hash冲突
            else {
                V oldVal = null;
                synchronized (f) {
                    if (tabAt(tab, i) == f) {
                        if (fh >= 0) {
                            binCount = 1;
                            for (Node<K,V> e = f;; ++binCount) {
                                K ek;
                                // 更新value值
                                if (e.hash == hash &&
                                    ((ek = e.key) == key ||
                                     (ek != null && key.equals(ek)))) {
                                    oldVal = e.val;
                                    if (!onlyIfAbsent)
                                        e.val = value;
                                    break;
                                }
                                // 不存在这个key，就插入一个新结点，尾插法
                                // pred是e的前驱结点
                                Node<K,V> pred = e;
                                if ((e = e.next) == null) {
                                    pred.next = new Node<K,V>(hash, key,
                                                              value, null);
                                    break;
                                }
                            }
                        }
                        // 红黑树操作，不看
                        else if (f instanceof TreeBin) {
                            Node<K,V> p;
                            binCount = 2;
                            if ((p = ((TreeBin<K,V>)f).putTreeVal(hash, key,
                                                           value)) != null) {
                                oldVal = p.val;
                                if (!onlyIfAbsent)
                                    p.val = value;
                            }
                        }
                    }
                }
                if (binCount != 0) {
                    // 桶中结点大于等于8就变成红黑树
                    if (binCount >= TREEIFY_THRESHOLD)
                        treeifyBin(tab, i);
                    // 如果是更新操作，就返回旧值
                    if (oldVal != null)
                        return oldVal;
                    break;
                }
            }
        }
        // 结点数加1
        addCount(1L, binCount);
        return null;
    }
```

## initTable

初始化数组，只允许一个数组进行初始化，实现原理，利用sizeCtl，sizeCtl默认为0，

1. while循环判断数组是否为null，且数组长度是否为0
2. 在while内部，先判断sizeCtl是否小于0，如果小于0就让出cpu，说明别的线程正在初始化
3. 如果sizeCtl不小于0，就进行cas操作，就sizeCtl设置为-1，设置成功就再判断数组是否为null，且数组长度是否为0，如果满足条件，就进行初始化，并且把sizeCtl设置为n/2；如果不满足就退出循环
4. 初始化完数组，别的线程如果还在initTable函数里，就会尝试把sizeCtl设置为-1，设置成功，判断数组不为null，退出循环。

```java
    /**
     * Initializes table, using the size recorded in sizeCtl.
     * 初始化数组
     */
    private final Node<K,V>[] initTable() {
        Node<K,V>[] tab; int sc;
        // 如果当前table数组是空的
        while ((tab = table) == null || tab.length == 0) {
            // sizeCtl默认为0，如果sizeCtl<0，表示有线程正在初始化，当前线程让出cpu，
            // 而且此时sizeCtl=-1，因为此时在initTable函数里，看下面代码
            if ((sc = sizeCtl) < 0)
                Thread.yield(); // lost initialization race; just spin
            // compareAndSwapInt，cas操作，当前sizeCtl如果等于期望值sc,就将sizeCtl设置为-1
            // 此时就可以看到，只能有一个线程进行初始化，别的线程再调用initTable，就会进入第一个
            // if让出cpu
            else if (U.compareAndSwapInt(this, SIZECTL, sc, -1)) {
                try {
                    // 这里再判断table是否为null,相当于DCL双重检查
                    if ((tab = table) == null || tab.length == 0) {
                        // 如果sc=0，就会使用默认容量
                        int n = (sc > 0) ? sc : DEFAULT_CAPACITY;
                        @SuppressWarnings("unchecked")
                        Node<K,V>[] nt = (Node<K,V>[])new Node<?,?>[n];
                        table = tab = nt;
                        // sc=n/2
                        sc = n - (n >>> 2);
                    }
                } finally {
                    // 此时sizeCtl记录的是扩容阈值
                    sizeCtl = sc;
                }
                break;
            }
        }
        return tab;
    }

```

## 扩容

ConcurrentHashMap是多线程动态扩容，一个线程负责一段数组，将老数组里面的元素添加到新数组里面。

### helpTransfer

```java
    /**
     * Helps transfer if a resize is in progress.
     * 协助扩容函数
     */
    final Node<K,V>[] helpTransfer(Node<K,V>[] tab, Node<K,V> f) {
        Node<K,V>[] nextTab; int sc;
        // 如果 table 不是空 且 node 节点是转移类型，数据检验
        // 且 node 节点的 nextTable（新 table） 不是空，同样也是数据校验
        // 尝试帮助扩容
        if (tab != null && (f instanceof ForwardingNode) &&
            (nextTab = ((ForwardingNode<K,V>)f).nextTable) != null) {
            // 这个方法的返回一个与table容量n大小有关的扩容标记
            int rs = resizeStamp(tab.length);
            // 如果 nextTab 没有被并发修改 且 tab 也没有被并发修改
            // 且 sizeCtl  < 0 （说明还在扩容）
            while (nextTab == nextTable && table == tab &&
                   (sc = sizeCtl) < 0) {
                // 如果 sizeCtl 无符号右移  16 不等于 rs （ sc前 16 位如果不等于标识符，则标识符变化了）
                // 或者 sizeCtl == rs + 1  （扩容结束了，不再有线程进行扩容）（默认第一个线程设置 sc ==rs 左移 16 位 + 2，当第一个线程结束扩容了，就会将 sc 减一。这个时候，sc 就等于 rs + 1）
                // 或者 sizeCtl == rs + 65535  （如果达到最大帮助线程的数量，即 65535）
                // 或者转移下标正在调整 （扩容结束）
                // 结束循环，返回 table
                if ((sc >>> RESIZE_STAMP_SHIFT) != rs || sc == rs + 1 ||
                    sc == rs + MAX_RESIZERS || transferIndex <= 0)
                    break;
                // 如果以上都不是, 将 sizeCtl + 1, （表示增加了一个线程帮助其扩容）
                if (U.compareAndSwapInt(this, SIZECTL, sc, sc + 1)) {
                    // 进行转移
                    transfer(tab, nextTab);
                    break;
                }
            }
            return nextTab;
        }
        return table;
    }
```

### transfer

```java
    /**
     * Moves and/or copies the nodes in each bin to new table. See
     * above for explanation.
     * 复制结点到一个新数组
     */
    private final void transfer(Node<K,V>[] tab, Node<K,V>[] nextTab) {
        int n = tab.length, stride;
        // stride表示每个线程处理的槽个数。同时基于性能考虑，stride不能比16小。
        if ((stride = (NCPU > 1) ? (n >>> 3) / NCPU : n) < MIN_TRANSFER_STRIDE)
            stride = MIN_TRANSFER_STRIDE; // subdivide range
        if (nextTab == null) {            // initiating
            try {
                // 如果nextTab=null就新建一个table
                @SuppressWarnings("unchecked")
                Node<K,V>[] nt = (Node<K,V>[])new Node<?,?>[n << 1];
                nextTab = nt;
            } catch (Throwable ex) {      // try to cope with OOME
                // 数组扩容的时候有可能出现OOME，这时需要将sizeCtl设置为Integer.MAX_VALUE，用以表示这个异常
                sizeCtl = Integer.MAX_VALUE;
                return;
            }
            nextTable = nextTab;
            // transferIndex用以标识扩容总的进度，默认设置为原数组长度。
            // 因为扩容时候的元素迁移是从最末的元素开始的，所以迁移的时候下标是递减的，从下面的`--i`就能看出来了
            transferIndex = n;
        }
        int nextn = nextTab.length;
        // 扩容时准备的特殊节点
        ForwardingNode<K,V> fwd = new ForwardingNode<K,V>(nextTab);
        // 用于表示table里面单个元素是否迁移完毕，初始为true是为了进入while循环。
        // 1. true表示还未迁移完
        // 2. false表示已经迁移完
        boolean advance = true;
        // 用于表示table里面的所有元素是否迁移完毕
        boolean finishing = false; // to ensure sweep before committing nextTab
        // 这儿又是自旋，bound表示槽的边界
        for (int i = 0, bound = 0;;) {
            Node<K,V> f; int fh;
            while (advance) {
                int nextIndex, nextBound;
                // 倒序迁移旧元素的下标已达到槽的边界，或者整个table已经迁移完毕，说明迁移完成了
                if (--i >= bound || finishing)
                    advance = false;
                // 扩容总进度<=0，说明迁移完成了
                else if ((nextIndex = transferIndex) <= 0) {
                    i = -1;
                    advance = false;
                }
                // transferIndex减去每个线程处理的槽个数，将这个值设置为即将迁移的边界
                else if (U.compareAndSwapInt
                         (this, TRANSFERINDEX, nextIndex,
                          nextBound = (nextIndex > stride ?
                                       nextIndex - stride : 0))) {
                    bound = nextBound;
                    i = nextIndex - 1;
                    advance = false;
                }
            }
            // 判断是否迁移完成
            if (i < 0 || i >= n || i + n >= nextn) {
                int sc;
                if (finishing) {
                    nextTable = null;
                    table = nextTab;
                    // sizeCtl=扩容阈值
                    sizeCtl = (n << 1) - (n >>> 1);
                    return;
                }
                if (U.compareAndSwapInt(this, SIZECTL, sc = sizeCtl, sc - 1)) {
                    if ((sc - 2) != resizeStamp(n) << RESIZE_STAMP_SHIFT)
                        return;
                    finishing = advance = true;
                    i = n; // recheck before commit
                }
            }
            // 数组元素所在的位置没有值，则直接设置ForwordNode
            else if ((f = tabAt(tab, i)) == null)
                advance = casTabAt(tab, i, null, fwd);
            // 数组元素所在位置节点为ForwordNode，表示已经被迁移过了
            else if ((fh = f.hash) == MOVED)
                advance = true; // already processed
            else {
                // 其他情况，需要对元素首结点进行加锁，然后将该元素所在槽里面的每个结点都进行迁移
                synchronized (f) {
                    if (tabAt(tab, i) == f) {
                        // ln表示扩容后索引位置不变的情况，hn表示扩容后索引位置要变成当前位置+原容量的情况
                        Node<K,V> ln, hn;
                        if (fh >= 0) {
                            // runBit = 0表示扩容后索引位置不变，runBit=1表示扩容后索引位置要变成当前位置+原容量的情况
                            int runBit = fh & n;
                            // 用lastRun记录下最后一个需要遍历的结点，注意，lastRun不一定是最后一个结点，lastRun后面的结点
                            // 跟lastRun扩容后的位置是一样的，所以直接把这个小链表插入到新数组就行，不用再挨个遍历后面的结点
                            Node<K,V> lastRun = f;
                            for (Node<K,V> p = f.next; p != null; p = p.next) {
                                int b = p.hash & n;
                                // 这if语句，用于判断b和runBit是否相同，如果相同，就不用记录了，因为之前可能已经记录过lastRun了
                                // 如果不同，则更改lastRun。lastRun结点到尾结点这段结点的扩容后索引位置相同
                                if (b != runBit) {
                                    runBit = b;
                                    lastRun = p;
                                }
                            }
                            // ln表示扩容后索引位置不变的情况
                            if (runBit == 0) {
                                ln = lastRun;
                                hn = null;
                            }
                            // hn表示扩容后索引位置要变成当前位置+原容量的情况
                            else {
                                hn = lastRun;
                                ln = null;
                            }
                            // 这个for循环只用遍历到lastRun结点，因为lastRun后面的结点跟lastRun结点插入位置相同
                            for (Node<K,V> p = f; p != lastRun; p = p.next) {
                                int ph = p.hash; K pk = p.key; V pv = p.val;
                                // 头插法
                                if ((ph & n) == 0)
                                    ln = new Node<K,V>(ph, pk, pv, ln);
                                else
                                    hn = new Node<K,V>(ph, pk, pv, hn);
                            }
                            // 将ln链表插入到nextTab[i]位置
                            setTabAt(nextTab, i, ln);
                            // 将hn链表插入到nextTab[i + n]位置
                            setTabAt(nextTab, i + n, hn);
                            // TODO 我觉得这句代码可能是处理ln=null情况，将fwd插入到tab[i]
                            setTabAt(tab, i, fwd);
                            advance = true;
                        }
                        else if (f instanceof TreeBin) {
                            TreeBin<K,V> t = (TreeBin<K,V>)f;
                            TreeNode<K,V> lo = null, loTail = null;
                            TreeNode<K,V> hi = null, hiTail = null;
                            int lc = 0, hc = 0;
                            for (Node<K,V> e = t.first; e != null; e = e.next) {
                                int h = e.hash;
                                TreeNode<K,V> p = new TreeNode<K,V>
                                    (h, e.key, e.val, null, null);
                                if ((h & n) == 0) {
                                    if ((p.prev = loTail) == null)
                                        lo = p;
                                    else
                                        loTail.next = p;
                                    loTail = p;
                                    ++lc;
                                }
                                else {
                                    if ((p.prev = hiTail) == null)
                                        hi = p;
                                    else
                                        hiTail.next = p;
                                    hiTail = p;
                                    ++hc;
                                }
                            }
                            ln = (lc <= UNTREEIFY_THRESHOLD) ? untreeify(lo) :
                                (hc != 0) ? new TreeBin<K,V>(lo) : t;
                            hn = (hc <= UNTREEIFY_THRESHOLD) ? untreeify(hi) :
                                (lc != 0) ? new TreeBin<K,V>(hi) : t;
                            setTabAt(nextTab, i, ln);
                            setTabAt(nextTab, i + n, hn);
                            setTabAt(tab, i, fwd);
                            advance = true;
                        }
                    }
                }
            }
        }
    }
```

## get操作

1. 计算hash值，定位到该table索引位置，如果是首节点符合就返回
2. 如果遇到扩容的时候，会调用标志正在扩容节点ForwardingNode的find方法，查找该节点，匹配就返回
3. 以上都不符合的话，就往下遍历节点，匹配就返回，否则最后就返回null

```java
    public V get(Object key) {
        Node<K,V>[] tab; Node<K,V> e, p; int n, eh; K ek;
        // 求key得hash值
        int h = spread(key.hashCode());
        if ((tab = table) != null && (n = tab.length) > 0 &&
            (e = tabAt(tab, (n - 1) & h)) != null) {
            // 判断tab[i]的第一个结点是不是要找的结点
            if ((eh = e.hash) == h) {
                if ((ek = e.key) == key || (ek != null && key.equals(ek)))
                    return e.val;
            }
            // eh < 0说明正在扩容，调用find方法查找，多态，有可能去链表中查找，也有可能去红黑树查找
            else if (eh < 0)
                return (p = e.find(h, key)) != null ? p.val : null;
            // 遍历链表
            while ((e = e.next) != null) {
                if (e.hash == h &&
                    ((ek = e.key) == key || (ek != null && key.equals(ek))))
                    return e.val;
            }
        }
        return null;
    }
```

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

## 注释版的ConcurrentHashMap

放在这里就太长了，我单独放在一个文件里面了。[注释版的ConcurrentHashMap](/docs/Java并发包/ConcurrentHashMap.java)



