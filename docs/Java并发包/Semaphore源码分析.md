# 简介

Semaphore也是基于AQS实现的，用于限流，控制访问资源的线程数量。支持公平锁和非公平锁。默认是非公平锁

# 源码

Semaphore有一个内部类sync继承了AbstractQueuedSynchronizer，通过更改state的值，控制对资源的访问，例如state=n，表示有n个线程可以同时访问某个资源，多出的线程只能等待别的线程释放锁，释放一次，state加一。

## 内部类

```java
abstract static class Sync extends AbstractQueuedSynchronizer {
        private static final long serialVersionUID = 1192457210091910933L;

        Sync(int permits) {
            setState(permits);
        }

        final int getPermits() {
            return getState();
        }

        final int nonfairTryAcquireShared(int acquires) {
            for (;;) {
                int available = getState();
                int remaining = available - acquires;
                if (remaining < 0 ||
                    compareAndSetState(available, remaining))
                    return remaining;
            }
        }

        protected final boolean tryReleaseShared(int releases) {
            for (;;) {
                int current = getState();
                int next = current + releases;
                if (next < current) // overflow
                    throw new Error("Maximum permit count exceeded");
                if (compareAndSetState(current, next))
                    return true;
            }
        }

        final void reducePermits(int reductions) {
            for (;;) {
                int current = getState();
                int next = current - reductions;
                if (next > current) // underflow
                    throw new Error("Permit count underflow");
                if (compareAndSetState(current, next))
                    return;
            }
        }

        final int drainPermits() {
            for (;;) {
                int current = getState();
                if (current == 0 || compareAndSetState(current, 0))
                    return current;
            }
        }
    }
```

## 公平和非公平

```java
    /**
     * NonFair version
     * 非公平模式
     */
    static final class NonfairSync extends Sync {
        private static final long serialVersionUID = -2694183684443567898L;

        NonfairSync(int permits) {
            super(permits);
        }

        protected int tryAcquireShared(int acquires) {
            return nonfairTryAcquireShared(acquires);
        }
    }

    /**
     * Fair version
     * 公平模式
     */
    static final class FairSync extends Sync {
        private static final long serialVersionUID = 2014338818796000944L;

        FairSync(int permits) {
            super(permits);
        }

        protected int tryAcquireShared(int acquires) {
            for (;;) {
                // 先检查是否轮到了当前线程
                if (hasQueuedPredecessors())
                    return -1;
                int available = getState();
                int remaining = available - acquires;
                if (remaining < 0 ||
                    compareAndSetState(available, remaining))
                    return remaining;
            }
        }
    }
```

## 构造方法

```java
    /** 默认是非公平锁
     */
    public Semaphore(int permits) {
        sync = new NonfairSync(permits);
    }
    public Semaphore(int permits, boolean fair) {
        sync = fair ? new FairSync(permits) : new NonfairSync(permits);
    }
```

## 获取锁

```java
    /** 可以响应线程中断状态，获取锁的线程中断，其他没有获取锁的线程可以获取锁
     * @throws InterruptedException if the current thread is interrupted
     */
    public void acquire() throws InterruptedException {
        sync.acquireSharedInterruptibly(1);
    }
    /** 是使等待进入acquire()方法的线程，不允许被中断。
     */
    public void acquireUninterruptibly() {
        sync.acquireShared(1);
    }
```

## 释放锁

```java
    public void release() {
        sync.releaseShared(1);
    }
    public void release(int permits) {
        if (permits < 0) throw new IllegalArgumentException();
        sync.releaseShared(permits);
    }
```

