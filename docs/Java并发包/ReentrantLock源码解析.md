# 简介

ReentrantLock默认是非公平锁，也可以是公平锁，也是独占锁、可重入锁。有尝试加锁的功能，需要用户去手动去释放锁，加锁多少次，必须解锁多少次。

Reentrantlock可以用来实现分组唤醒需要唤醒的线程们，可以精确唤醒，而不是像synchronized要么随机唤醒一个线程要么唤醒全部线程。

Reentranlock 可中断：

1. 设置超时方法 trylock(long timeout, TimeUnit unit)
2. lockInterruptibly放代码块中，调用interrupt()方法可中断

# 源码

ReentrantLock有个内部类sync，sync继承了AbstractQueuedSynchronizer，通过AQS实现的，AQS源码不熟悉的可以去看我之前写的[笔记](https://wardseptember.gitee.io/mynotes/#/docs/Java%E5%B9%B6%E5%8F%91%E5%8C%85/AQS%E6%BA%90%E7%A0%81%E8%AF%A6%E8%A7%A3)。

主要是通过AQS实现的，state=0代表没有线程占有锁，state=1代表有一个线程占有锁，state>1代表同一线程多次获取锁，释放锁时也要多次释放，一次释放state减一。

有非公平模式和公平模式，非公平锁不管队列里有没有线程，都尝试去获取锁，并发程度相对高；公平锁是轮到它，才去获取锁。

## 内部类

```java
    abstract static class Sync extends AbstractQueuedSynchronizer {
        private static final long serialVersionUID = -5179523762034025860L;

        /**
         * Performs {@link Lock#lock}. The main reason for subclassing
         * is to allow fast path for nonfair version.
         * 给子类覆写的
         */
        abstract void lock();

        /**
         * Performs non-fair tryLock.  tryAcquire is implemented in
         * subclasses, but both need nonfair try for trylock method.
         * 尝试获取锁
         */
        final boolean nonfairTryAcquire(int acquires) {
            final Thread current = Thread.currentThread();
            int c = getState();
            if (c == 0) {
                if (compareAndSetState(0, acquires)) {
                    setExclusiveOwnerThread(current);
                    return true;
                }
            }
            // 可重入
            else if (current == getExclusiveOwnerThread()) {
                int nextc = c + acquires;
                if (nextc < 0) // overflow
                    throw new Error("Maximum lock count exceeded");
                setState(nextc);
                return true;
            }
            return false;
        }

        // 尝试释放锁，从这里就可以看到，加锁多少次就必须释放锁多少次，state=0才返回true
        protected final boolean tryRelease(int releases) {
            int c = getState() - releases;
            if (Thread.currentThread() != getExclusiveOwnerThread())
                throw new IllegalMonitorStateException();
            boolean free = false;
            if (c == 0) {
                free = true;
                setExclusiveOwnerThread(null);
            }
            setState(c);
            return free;
        }

        // 判断是否是独占式，是否拥有锁
        protected final boolean isHeldExclusively() {
            // While we must in general read state before owner,
            // we don't need to do so to check if current thread is owner
            return getExclusiveOwnerThread() == Thread.currentThread();
        }

        // 可以实现分组唤醒
        final ConditionObject newCondition() {
            return new ConditionObject();
        }

        // Methods relayed from outer class

        final Thread getOwner() {
            return getState() == 0 ? null : getExclusiveOwnerThread();
        }

        final int getHoldCount() {
            return isHeldExclusively() ? getState() : 0;
        }

        final boolean isLocked() {
            return getState() != 0;
        }

        /**
         * Reconstitutes the instance from a stream (that is, deserializes it).
         */
        private void readObject(java.io.ObjectInputStream s)
            throws java.io.IOException, ClassNotFoundException {
            s.defaultReadObject();
            setState(0); // reset to unlocked state
        }
    }
```

## 非公平锁

可以看到之前我们在AQS源码分析里提到的tryAcquire就在这里覆写了。

```java
    /**
     * Sync object for non-fair locks
     * 非公平模式
     */
    static final class NonfairSync extends Sync {
        private static final long serialVersionUID = 7316153563782823691L;

        /**
         * Performs lock.  Try immediate barge, backing up to normal
         * acquire on failure.
         */
        final void lock() {
            // 没抢到锁，才去排队
            if (compareAndSetState(0, 1))
                setExclusiveOwnerThread(Thread.currentThread());
            else
                acquire(1);
        }

        protected final boolean tryAcquire(int acquires) {
            return nonfairTryAcquire(acquires);
        }
    }
```

## 公平锁

```java
    /**
     * Sync object for fair locks
     * 公平锁模式
     */
    static final class FairSync extends Sync {
        private static final long serialVersionUID = -3000897897090466540L;

        final void lock() {
            acquire(1);
        }

        /**
         * Fair version of tryAcquire.  Don't grant access unless
         * recursive call or no waiters or is first.
         */
        protected final boolean tryAcquire(int acquires) {
            final Thread current = Thread.currentThread();
            int c = getState();
            if (c == 0) {
                // hasQueuedPredecessors判断排在当前线程前面有没有线程，没有的话才尝试获取锁
                if (!hasQueuedPredecessors() &&
                    compareAndSetState(0, acquires)) {
                    setExclusiveOwnerThread(current);
                    return true;
                }
            }
            else if (current == getExclusiveOwnerThread()) {
                int nextc = c + acquires;
                if (nextc < 0)
                    throw new Error("Maximum lock count exceeded");
                setState(nextc);
                return true;
            }
            return false;
        }
    }
```

## 构造方法和lock

```java
    /**
     * Creates an instance of {@code ReentrantLock}.
     * This is equivalent to using {@code ReentrantLock(false)}.
     * 默认非公平锁
     */
    public ReentrantLock() {
        sync = new NonfairSync();
    }

    /**
     * Creates an instance of {@code ReentrantLock} with the
     * given fairness policy.
     *
     * @param fair {@code true} if this lock should use a fair ordering policy
     */
    public ReentrantLock(boolean fair) {
        sync = fair ? new FairSync() : new NonfairSync();
    }

    /**
     * Acquires the lock.
     *
     * <p>Acquires the lock if it is not held by another thread and returns
     * immediately, setting the lock hold count to one.
     *
     * <p>If the current thread already holds the lock then the hold
     * count is incremented by one and the method returns immediately.
     *
     * <p>If the lock is held by another thread then the
     * current thread becomes disabled for thread scheduling
     * purposes and lies dormant until the lock has been acquired,
     * at which time the lock hold count is set to one.
     */
    public void lock() {
        sync.lock();
    }
```

## lockInterruptibly

```java
 /** lockInterruptibly可以对interrupt方法做出响应
 */
public void lockInterruptibly() throws InterruptedException {
    sync.acquireInterruptibly(1);
}
```

## tryLock

```java
/** 尝试获取锁，如果锁被其他线程占有，立即返回false
 */
public boolean tryLock() {
    return sync.nonfairTryAcquire(1);
}
/** 尝试获取锁，如果锁被其他线程占有，在timeout时间里，还没获取到锁就返回false
*/
public boolean tryLock(long timeout, TimeUnit unit)
    throws InterruptedException {
    return sync.tryAcquireNanos(1, unit.toNanos(timeout));
}
```

## unlock

```java
/** 释放锁
 */
public void unlock() {
    sync.release(1);
}
```