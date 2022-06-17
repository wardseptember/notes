[TOC]

# 简介

AQS是AbstractQueuedSynchronizer，是用来构建锁或者其它同步器组件的重量级基础框架及整个JUC体系的基石，通过内置的FIFO队列来完成资源获取线程的排队工作，并通过一个int类型变量表示持有锁的状态。

AQS使用一个volatile的int类型的成员变量来表示同步状态，通过内置的FIFO队列来完成资源获取的排队工作将每条要去抢占资源的线程封装成一个Node结点来实现锁的分配，通过CAS完成对State值的修改。

它维护了一个volatile int state（代表共享资源）和一个FIFO线程等待队列（多线程争用资源被阻塞时会进入此队列）。

<div align="center"> <img src="https://raw.githubusercontent.com/wardseptember/notes/master/imgs/20201208192923.png" width="600"/> </div><br>

AQS定义两种资源共享方式：Exclusive（独占，只有一个线程能执行，如ReentrantLock）和Share（共享，多个线程可同时执行，如Semaphore/CountDownLatch）。

不同的自定义同步器争用共享资源的方式也不同。**自定义同步器在实现时只需要实现共享资源state的获取与释放方式即可**，至于具体线程等待队列的维护（如获取资源失败入队/唤醒出队等），AQS已经在顶层实现好了。自定义同步器实现时主要实现以下几种方法：

- isHeldExclusively()：该线程是否正在独占资源。只有用到condition才需要去实现它。
- tryAcquire(int)：独占方式。尝试获取资源，成功则返回true，失败则返回false。
- tryRelease(int)：独占方式。尝试释放资源，成功则返回true，失败则返回false。
- tryAcquireShared(int)：共享方式。尝试获取资源。负数表示失败；0表示成功，但没有剩余可用资源；正数表示成功，且有剩余资源。
- tryReleaseShared(int)：共享方式。尝试释放资源，如果释放后允许唤醒后续等待结点返回true，否则返回false。

以ReentrantLock为例，state初始化为0，表示未锁定状态。A线程lock()时，会调用tryAcquire()独占该锁并将state+1。此后，其他线程再tryAcquire()时就会失败，直到A线程unlock()到state=0（即释放锁）为止，其它线程才有机会获取该锁。当然，释放锁之前，A线程自己是可以重复获取此锁的（state会累加），这就是可重入的概念。但要注意，获取多少次就要释放多么次，这样才能保证state是能回到零态的。

再以CountDownLatch以例，任务分为N个子线程去执行，state也初始化为N（注意N要与线程个数一致）。这N个子线程是并行执行的，每个子线程执行完后countDown()一次，state会CAS减1。等到所有子线程都执行完后(即state=0)，会unpark()主调用线程，然后主调用线程就会从await()函数返回，继续后余动作。

一般来说，自定义同步器要么是独占方法，要么是共享方式，他们也只需实现tryAcquire-tryRelease、tryAcquireShared-tryReleaseShared中的一种即可。但AQS也支持自定义同步器同时实现独占和共享两种方式，如ReentrantReadWriteLock。

# 源码

源码是有点复杂的，也不算太复杂。

## 队列结点状态

队列结点状态用waitStatus表示。

Node结点是对每一个等待获取资源的线程的封装，其包含了需要同步的线程本身及其等待状态，如是否被阻塞、是否等待唤醒、是否已经被取消等。变量waitStatus则表示当前Node结点的等待状态，共有5种取值CANCELLED、SIGNAL、CONDITION、PROPAGATE、0。

- **CANCELLED**(1)：表示当前结点已取消调度。当timeout或被中断（响应中断的情况下），会触发变更为此状态，进入该状态后的结点将不会再变化。
- **SIGNAL**(-1)：表示后继结点在等待当前结点唤醒。后继结点入队时，会将前继结点的状态更新为SIGNAL。
- **CONDITION**(-2)：表示结点等待在Condition上，当其他线程调用了Condition的signal()方法后，CONDITION状态的结点将**从等待队列转移到同步队列中**，等待获取同步锁。
- **PROPAGATE**(-3)：共享模式下，前继结点不仅会唤醒其后继结点，同时也可能会唤醒后继的后继结点。
- **0**：新结点入队时的默认状态。

注意，**负值表示结点处于有效等待状态，而正值表示结点已被取消。所以源码中很多地方用>0、<0来判断结点的状态是否正常**。

## 队列的结点类型

```java
static final class Node {
/** Marker to indicate a node is waiting in shared mode */
static final Node SHARED = new Node();
/** Marker to indicate a node is waiting in exclusive mode */
static final Node EXCLUSIVE = null;

/** waitStatus value to indicate thread has cancelled
* 表示当前结点已取消调度。当timeout或被中断（响应中断的情况下），会触发变更为此状态，进入该状态后的结点将不会再变化。*/
static final int CANCELLED =  1;
/** waitStatus value to indicate successor's thread needs unparking
* 表示后继结点在等待当前结点唤醒。后继结点入队时，会将前继结点的状态更新为SIGNAL。*/
static final int SIGNAL    = -1;
/** waitStatus value to indicate thread is waiting on condition
* 表示结点等待在Condition上，当其他线程调用了Condition的signal()方法后，CONDITION状态的结点将从等待队列转移到同步队列中，等待获取同步锁。*/
static final int CONDITION = -2;
/**
* 共享模式下，前继结点不仅会唤醒其后继结点，同时也可能会唤醒后继的后继结点。
*/
static final int PROPAGATE = -3;

// 注意，负值表示结点处于有效等待状态，而正值表示结点已被取消。所以源码中很多地方用>0、<0来判断结点的状态是否正常。
volatile int waitStatus;

// 前驱结点
volatile Node prev;

// 后继结点
volatile Node next;

// 等待中的线程
volatile Thread thread;

/**
* Link to next node waiting on condition, or the special
* value SHARED.  Because condition queues are accessed only
* when holding in exclusive mode, we just need a simple
* linked queue to hold nodes while they are waiting on
* conditions. They are then transferred to the queue to
* re-acquire. And because conditions can only be exclusive,
* we save a field by using special value to indicate shared
* mode.
* 链接上下一个等待在相同条件下的结点或者存上SHARED值
*/
Node nextWaiter;

/**
* 返回true,代表是共享模式
*/
final boolean isShared() {
return nextWaiter == SHARED;
}

/**
* 返回前驱结点
* @return the predecessor of this node
*/
final Node predecessor() throws NullPointerException {
Node p = prev;
if (p == null)
throw new NullPointerException();
else
return p;
}

Node() {    // Used to establish initial head or SHARED marker
}

Node(Thread thread, Node mode) {     // Used by addWaiter
this.nextWaiter = mode;
this.thread = thread;
}

Node(Thread thread, int waitStatus) { // Used by Condition
this.waitStatus = waitStatus;
this.thread = thread;
}
}
```

## State

跟state相关的操作只有三个方法。

```java
/**
* Head of the wait queue, lazily initialized.  Except for
* initialization, it is modified only via method setHead.  Note:
* If head exists, its waitStatus is guaranteed not to be
* CANCELLED.
* 阻塞队列的头，head不为null,他的waitStatus一定不是CANCELLED
*/
private transient volatile Node head;

/**
* Tail of the wait queue, lazily initialized.  Modified only via
* method enq to add new wait node.
* 阻塞队列的尾结点
*/
private transient volatile Node tail;

/**
* The synchronization state.
*/
private volatile int state;

/**
* Returns the current value of synchronization state.
* This operation has memory semantics of a {@code volatile} read.
* @return current state value
*/
protected final int getState() {
return state;
}

/**
* Sets the value of synchronization state.
* This operation has memory semantics of a {@code volatile} write.
* @param newState the new state value
*/
protected final void setState(int newState) {
state = newState;
}

/**
* cas操作，读取传入对象o在内存中偏移量为offset位置的值与期望值expected作比较。
* 如果state的值是期望值expect，就将state修改成update，如果不相等就不修改返回false
* @param expect the expected value
* @param update the new value
* @return {@code true} if successful. False return indicates that the actual
*         value was not equal to the expected value.
*/
protected final boolean compareAndSetState(int expect, int update) {
// See below for intrinsics setup to support this
return unsafe.compareAndSwapInt(this, stateOffset, expect, update);
}
```

## acquire方法

```java
/**
* Acquires in exclusive mode, ignoring interrupts.  Implemented
* by invoking at least once {@link #tryAcquire},
* returning on success.  Otherwise the thread is queued, possibly
* repeatedly blocking and unblocking, invoking {@link
* #tryAcquire} until success.  This method can be used
* to implement method {@link Lock#lock}.
*
* @param arg the acquire argument.  This value is conveyed to
*        {@link #tryAcquire} but is otherwise uninterpreted and
*        can represent anything you like.
* 在排他模式下获取资源
*/
public final void acquire(int arg) {
if (!tryAcquire(arg) &&
acquireQueued(addWaiter(Node.EXCLUSIVE), arg))
selfInterrupt();
}
```

### tryAcquire

tryAcquire是独占方式。尝试获取资源，成功则返回true，失败则返回false。可以看到这个方法直接抛出异常，这个方法是留个子类实现的，ReentrantLock和ReentrantReadWriteLock等都实现了这个方法。

```java
protected boolean tryAcquire(int arg) {
throw new UnsupportedOperationException();
}
```

### addWaiter

addWaiter是为当前线程创建一个Node结点，并把这个结点加入到等待队列里面。流程如下

1. 为当前线程创建一个Node结点
2. 判断队列是否null，如果不为null，就将创建的Node结点加到队列尾部
3. 如果队列对null，就会新创建一个傀儡结点当做队列的头结点，然后把node结点添加到队列尾部

```java
/**
* Creates and enqueues node for current thread and given mode.
*  为当前线程创建一个Node结点，并把这个结点加入到等待队列里面
* @param mode Node.EXCLUSIVE for exclusive, Node.SHARED for shared
* @return the new node
*/
private Node addWaiter(Node mode) {
Node node = new Node(Thread.currentThread(), mode);
// Try the fast path of enq; backup to full enq on failure
Node pred = tail;
// pred!=null 说明当前队列不为null,尝试入队
if (pred != null) {
node.prev = pred;
// compareAndSetTail尝试将node添加到pred尾部，返回true，添加成功，返回false添加失败
if (compareAndSetTail(pred, node)) {
// 返回当前结点
pred.next = node;
return node;
}
}
// 走到这说明当前队列为null
enq(node);
return node;
}
/**
* CAS tail field. Used only by enq.
*/
private final boolean compareAndSetTail(Node expect, Node update) {
return unsafe.compareAndSwapObject(this, tailOffset, expect, update);
}

/**
* CAS head field. Used only by enq.
*/
private final boolean compareAndSetHead(Node update) {
return unsafe.compareAndSwapObject(this, headOffset, null, update);
}
/**
* Inserts node into queue, initializing if necessary. See picture above.
*
* 将node结点入队
* @param node the node to insert
* @return node's predecessor
*/
private Node enq(final Node node) {
// 自选方式
for (;;) {
Node t = tail;
// 第一次循环，t=null，就会设置队列头，可以看到是新创建了一个Node结点，
// 把这个新创建的结点当做头结点，这个结点也叫做傀儡结点
if (t == null) { // Must initialize
if (compareAndSetHead(new Node()))
tail = head;
} else {
// 第二次循环，t!=null，因为已经有傀儡结点了，就会进入这个语句块中
// 然后将node添加到傀儡结点的后面
node.prev = t;
if (compareAndSetTail(t, node)) {
t.next = node;
return t;
}
}
}
}
```

### acquireQueued

```java
/**
* Acquires in exclusive uninterruptible mode for thread already in
* queue. Used by condition wait methods as well as acquire.
* 排他模式下使用的方法，尝试获取资源，此时线程结点已经在队列里面了
* 这个方法返回node结点中的线程是否被中断过
* @param node the node
* @param arg the acquire argument
* @return {@code true} if interrupted while waiting
*/
final boolean acquireQueued(final Node node, int arg) {
boolean failed = true;
try {
// 标识线程是否被中断过, 中断过，中断标志位就变成true了，到外面acquire会再中断一次
// 此时中断标志位会切换成false，不会唤醒等待中的线程，
// 如果interrupted=false，就不会进入selfInterrupt依然不会唤醒等待中的线程
boolean interrupted = false;
// 自旋方式
for (;;) {
// p是node的前驱结点
final Node p = node.predecessor();
// p=head就再尝试获取资源，获取成功就重新设置队列头，并完全断开傀儡结点
if (p == head && tryAcquire(arg)) {
setHead(node);
p.next = null; // help GC
failed = false;
return interrupted;
}
// 再次获取资源失败
if (shouldParkAfterFailedAcquire(p, node) &&
parkAndCheckInterrupt())
// 走到这，说明被中断过
interrupted = true;
}
} finally {
// 如果等待过程中没有成功获取资源（如timeout，或者可中断的情况下被中断了），那么取消结点在队列中的等待。
if (failed)
cancelAcquire(node);
}
}


/**
* Checks and updates status for a node that failed to acquire.
* Returns true if thread should block. This is the main signal
* control in all acquire loops.  Requires that pred == node.prev.
* 获取资源失败，检查和更新node结点状态，如果返回true，表示pred已经就绪了，可以将node结点的线程阻塞
* pred是node的前驱结点
* @param pred node's predecessor holding status
* @param node the node
* @return {@code true} if thread should block
*/
private static boolean shouldParkAfterFailedAcquire(Node pred, Node node) {
// pred结点状态
int ws = pred.waitStatus;
// 如果是第一次调用shouldParkAfterFailedAcquire,pred是傀儡结点，ws默认是0
if (ws == Node.SIGNAL)
// ws=Node.SIGNAL，说明这是第二次调用shouldParkAfterFailedAcquire
// 此时pred已经就绪了，可以将可以将node结点的线程阻塞
/*
* This node has already set status asking a release
* to signal it, so it can safely park.
*/
return true;
if (ws > 0) {
// ws>0说明pred被取消，往前遍历找到waitStatus<=0的
/*
* Predecessor was cancelled. Skip over predecessors and
* indicate retry.
*/
do {
node.prev = pred = pred.prev;
} while (pred.waitStatus > 0);
pred.next = node;
} else {
/*
* waitStatus must be 0 or PROPAGATE.  Indicate that we
* need a signal, but don't park yet.  Caller will need to
* retry to make sure it cannot acquire before parking.
* 将pred的结点状态设置为Node.SIGNAL，表示后继结点在等待当前结点唤醒
*/
compareAndSetWaitStatus(pred, ws, Node.SIGNAL);
}
return false;
}

/**
* Convenience method to park and then check if interrupted
* pred结点就绪了，可以将node结点的线程阻塞
* @return {@code true} if interrupted
*/
private final boolean parkAndCheckInterrupt() {
// 阻塞node结点的线程
LockSupport.park(this);
// 检查当前线程是否被中断
return Thread.interrupted();
}


```

#### cancelAcquire

```java
/**
* Cancels an ongoing attempt to acquire.
*  取消node结点在队列里的等待
* @param node the node
*/
private void cancelAcquire(Node node) {
// Ignore if node doesn't exist
if (node == null)
return;

node.thread = null;

// Skip cancelled predecessors
// 跳过node前驱结点中被取消的结点
Node pred = node.prev;
while (pred.waitStatus > 0)
node.prev = pred = pred.prev;

// predNext is the apparent node to unsplice. CASes below will
// fail if not, in which case, we lost race vs another cancel
// or signal, so no further action is necessary.
Node predNext = pred.next;

// Can use unconditional write instead of CAS here.
// After this atomic step, other Nodes can skip past us.
// Before, we are free of interference from other threads.
node.waitStatus = Node.CANCELLED;

// If we are the tail, remove ourselves.
// node是尾结点，并且将pred设置成尾结点成功，将pred.next置null
if (node == tail && compareAndSetTail(node, pred)) {
compareAndSetNext(pred, predNext, null);
} else {
// If successor needs signal, try to set pred's next-link
// so it will get one. Otherwise wake it up to propagate.
int ws;
// 将pred.next设置为node.next
if (pred != head &&
((ws = pred.waitStatus) == Node.SIGNAL ||
(ws <= 0 && compareAndSetWaitStatus(pred, ws, Node.SIGNAL))) &&
pred.thread != null) {
Node next = node.next;
if (next != null && next.waitStatus <= 0)
compareAndSetNext(pred, predNext, next);
} else {
/**此方法用于唤醒等待队列中下一个线程
这里为什么要唤醒等待队列中的下一个线程？因为这个方法也是在lock方法中调用的，

final void lock() {
acquire(1);
}
当前线程被取消了，当然要唤醒下一个线程咯
*/
unparkSuccessor(node);
}

node.next = node; // help GC
}
}
```

acquireQueued总结

1. 结点进入队尾后，检查状态，找到安全休息点；
2. 调用park()进入waiting状态，等待unpark()或interrupt()唤醒自己；
3. 被唤醒后，看自己是不是有资格能拿到号。如果拿到，head指向当前结点，并返回从入队到拿到号的整个过程中是否被中断过；如果没拿到，继续流程1。

### acquire总结

```java
public final void acquire(int arg) {
if (!tryAcquire(arg) &&
acquireQueued(addWaiter(Node.EXCLUSIVE), arg))
selfInterrupt();
}
/**
* Convenience method to interrupt current thread.
* 中断当前线程
*/
static void selfInterrupt() {
Thread.currentThread().interrupt();
}
```

1. 调用自定义同步器的tryAcquire()尝试直接去获取资源，如果成功则直接返回；
2. 没成功，则addWaiter()将该线程加入等待队列的尾部，并标记为独占模式；
3. acquireQueued()使线程在等待队列中休息，有机会时（轮到自己，会被unpark()）会去尝试获取资源。获取到资源后才返回。如果在整个等待过程中被中断过，则返回true，否则返回false。
4. 如果线程在等待过程中被中断过，它是不响应的。只是获取资源后才再进行自我中断selfInterrupt()，将中断补上。

如果tryAcquire返回true，表示成功获取到了资源，此时调用selfInterrupt()就会唤醒等待中的线程，如果线程本来就在运行，调用Thread.currentThread().interrupt();依然不会影响运行；如果tryAcquire返回false，acquireQueued返回true表示中断过，此时中断标志位为true，再调用selfInterrupt会把中断标志位设置为false，依然不会唤醒等待中的线程。

## release方法

此方法是独占模式下线程释放共享资源的顶层入口。它会释放指定量的资源，如果彻底释放了（即state=0）,它会唤醒等待队列里的其他线程来获取资源。这也正是unlock()的语义，当然不仅仅只限于unlock()。下面是release()的源码：

```java
public final boolean release(int arg) {
if (tryRelease(arg)) {
Node h = head;
// 唤醒等待中的线程
if (h != null && h.waitStatus != 0)
unparkSuccessor(h);
return true;
}
return false;
}
```

tryRelease(arg)是给子类覆写的，尝试释放资源，释放成功返回true，释放失败返回false。

### unparkSuccessor

唤醒等待中的结点。

```java
/**
* Wakes up node's successor, if one exists.
*
* @param node the node
*/
private void unparkSuccessor(Node node) {
/*
* If status is negative (i.e., possibly needing signal) try
* to clear in anticipation of signalling.  It is OK if this
* fails or if status is changed by waiting thread.
*/
int ws = node.waitStatus;
if (ws < 0)
compareAndSetWaitStatus(node, ws, 0);

/*
* Thread to unpark is held in successor, which is normally
* just the next node.  But if cancelled or apparently null,
* traverse backwards from tail to find the actual
* non-cancelled successor.
*/
Node s = node.next;
if (s == null || s.waitStatus > 0) {
s = null;
// 从后往前找有效的node结点
for (Node t = tail; t != null && t != node; t = t.prev)
if (t.waitStatus <= 0)
s = t;
}
if (s != null)
// 唤醒s
LockSupport.unpark(s.thread);
}
```

这个函数并不复杂。一句话概括：**用unpark()唤醒等待队列中最前边的那个未放弃线程**，这里我们也用s来表示吧。此时，再和acquireQueued()联系起来，s被唤醒后，进入if (p == head && tryAcquire(arg))的判断（即使p!=head也没关系，它会再进入shouldParkAfterFailedAcquire()寻找一个安全点。这里既然s已经是等待队列中最前边的那个未放弃线程了，那么通过shouldParkAfterFailedAcquire()的调整，s也必然会跑到head的next结点，下一次自旋p==head就成立啦），然后s把自己设置成head标杆结点，表示自己已经获取到资源了，acquire()也返回了！！

## acquireShared

此方法是共享模式下线程获取共享资源的顶层入口。它会获取指定量的资源，获取成功则直接返回，获取失败则进入等待队列，直到获取到资源为止，整个过程忽略中断。

```java
/**
* Acquires in shared mode, ignoring interrupts.  Implemented by
* first invoking at least once {@link #tryAcquireShared},
* returning on success.  Otherwise the thread is queued, possibly
* repeatedly blocking and unblocking, invoking {@link
* #tryAcquireShared} until success.
*  在共享模式下，尝试获取资源
* @param arg the acquire argument.  This value is conveyed to
*        {@link #tryAcquireShared} but is otherwise uninterpreted
*        and can represent anything you like.
*/
public final void acquireShared(int arg) {
if (tryAcquireShared(arg) < 0)
doAcquireShared(arg);
}

```

这里tryAcquireShared()依然需要自定义同步器去实现。但是AQS已经把其返回值的语义定义好了：负值代表获取失败；0代表获取成功，但没有剩余资源；正数表示获取成功，还有剩余资源，其他线程还可以去获取。所以这里acquireShared()的流程就是：

1. tryAcquireShared()尝试获取资源，成功则直接返回；
2. 失败则通过doAcquireShared()进入等待队列，直到获取到资源为止才返回。

### doAcquireShared

此方法用于将当前线程加入等待队列尾部休息，直到其他线程释放资源唤醒自己，自己成功拿到相应量的资源后才返回。

```java
private void doAcquireShared(int arg) {
// 加入队列尾部
final Node node = addWaiter(Node.SHARED);
boolean failed = true;
try {
// 等待过程中是否被中断过的标志
boolean interrupted = false;
for (;;) {
// 前驱结点
final Node p = node.predecessor();
if (p == head) {
// p = head说明轮到node了，尝试获取资源
int r = tryAcquireShared(arg);
if (r >= 0) {
// r >= 0 将node设置为head,还有剩余资源可以再唤醒之后的线程
setHeadAndPropagate(node, r);
p.next = null; // help GC
// 如果等待过程中被打断过，此时将中断补上。
if (interrupted)
selfInterrupt();
failed = false;
return;
}
}
// 判断状态，寻找安全点，进入waiting状态，等着被unpark()或interrupt()
if (shouldParkAfterFailedAcquire(p, node) &&
parkAndCheckInterrupt())
interrupted = true;
}
} finally {
if (failed)
cancelAcquire(node);
}
}
```

### setHeadAndPropagate

此方法在setHead()的基础上多了一步，就是自己苏醒的同时，如果条件符合（比如还有剩余资源），还会去唤醒后继结点，毕竟是共享模式！

```java
private void setHeadAndPropagate(Node node, int propagate) {
Node h = head; // Record old head for check below
setHead(node);
/*
* Try to signal next queued node if:
*   Propagation was indicated by caller,
*     or was recorded (as h.waitStatus either before
*     or after setHead) by a previous operation
*     (note: this uses sign-check of waitStatus because
*      PROPAGATE status may transition to SIGNAL.)
* and
*   The next node is waiting in shared mode,
*     or we don't know, because it appears null
*
* The conservatism in both of these checks may cause
* unnecessary wake-ups, but only when there are multiple
* racing acquires/releases, so most need signals now or soon
* anyway.
*/
// 如果还有剩余量，继续唤醒下一个邻居线程
if (propagate > 0 || h == null || h.waitStatus < 0 ||
(h = head) == null || h.waitStatus < 0) {
Node s = node.next;
if (s == null || s.isShared())
doReleaseShared();
}
}
```

### acquireShared小结

至此，acquireShared()也要告一段落了。让我们再梳理一下它的流程：

1. tryAcquireShared()尝试获取资源，成功则直接返回；
2. 失败则通过doAcquireShared()进入等待队列park()，直到被unpark()/interrupt()并成功获取到资源才返回。整个等待过程也是忽略中断的。

其实跟acquire()的流程大同小异，只不过多了个**自己拿到资源后，还会去唤醒后继队友的操作（这才是共享嘛）**。

## releaseShared

此方法是共享模式下线程释放共享资源的顶层入口。它会释放指定量的资源，如果成功释放且允许唤醒等待线程，它会唤醒等待队列里的其他线程来获取资源。

```java
public final boolean releaseShared(int arg) {
// 尝试释放资源，释放成功可以唤醒后面等待中的线程
if (tryReleaseShared(arg)) {
// 释放成功可以唤醒后面等待中的线程
doReleaseShared();
return true;
}
return false;
}
```

跟独占模式下的release()相似，但有一点稍微需要注意：独占模式下的tryRelease()在完全释放掉资源（state=0）后，才会返回true去唤醒其他线程，这主要是基于独占下可重入的考量；而共享模式下的releaseShared()则没有这种要求，共享模式实质就是控制一定量的线程并发执行，那么拥有资源的线程在释放掉部分资源时就可以唤醒后继等待结点。例如，资源总量是13，A（5）和B（7）分别获取到资源并发运行，C（4）来时只剩1个资源就需要等待。A在运行过程中释放掉2个资源量，然后tryReleaseShared(2)返回true唤醒C，C一看只有3个仍不够继续等待；随后B又释放2个，tryReleaseShared(2)返回true唤醒C，C一看有5个够自己用了，然后C就可以跟A和B一起运行。而ReentrantReadWriteLock读锁的tryReleaseShared()只有在完全释放掉资源（state=0）才返回true，所以自定义同步器可以根据需要决定tryReleaseShared()的返回值。

### doReleaseShared

```java
private void doReleaseShared() {
/*
* Ensure that a release propagates, even if there are other
* in-progress acquires/releases.  This proceeds in the usual
* way of trying to unparkSuccessor of head if it needs
* signal. But if it does not, status is set to PROPAGATE to
* ensure that upon release, propagation continues.
* Additionally, we must loop in case a new node is added
* while we are doing this. Also, unlike other uses of
* unparkSuccessor, we need to know if CAS to reset status
* fails, if so rechecking.
*/
for (;;) {
Node h = head;
if (h != null && h != tail) {
int ws = h.waitStatus;
// ws=Node.SIGNAL说明下一个线程需要被唤醒
if (ws == Node.SIGNAL) {
if (!compareAndSetWaitStatus(h, Node.SIGNAL, 0))
continue;            // loop to recheck cases
unparkSuccessor(h);
}
else if (ws == 0 &&
!compareAndSetWaitStatus(h, 0, Node.PROPAGATE))
continue;                // loop on failed CAS
}
// h = head说明资源已经被占用
if (h == head)                   // loop if head changed
break;
}
}
```

### 参考链接

* https://www.cnblogs.com/waterystone/p/4920797.html
