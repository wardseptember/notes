# 简介

数组队列，本质上还是一个数组，但不一定是Object数组，任何数组都可以，可以用自定义的类。所有数组的属性它都有，有特点的地方是，这个队列，有个队头和队尾指针，所有不用存索引0开始存储元素，最后一个元素也不一定是数组最后一个位置，类似环形队列。

这个数组队列必须指定初始容量，没有空构造方法。它不是一个动态数组，不会自动扩容，除非调用其resize方法。队列满了就直接抛异常

<div align="center"> <img src="https://gitee.com/wardseptember/images/raw/master/imgs/20201205230045.png" width="600"/> </div><br>

# 源码

源码都比较简单，没啥可说的，应该都能看懂。

```java

package com.sun.jmx.remote.internal;

import java.util.AbstractList;
import java.util.Iterator;

public class ArrayQueue<T> extends AbstractList<T> {
    public ArrayQueue(int capacity) {
        this.capacity = capacity + 1;
        this.queue = newArray(capacity + 1);
        this.head = 0;
        this.tail = 0;
    }

    public void resize(int newcapacity) {
        int size = size();
        if (newcapacity < size)
            throw new IndexOutOfBoundsException("Resizing would lose data");
        newcapacity++;
        if (newcapacity == this.capacity)
            return;
        T[] newqueue = newArray(newcapacity);
        for (int i = 0; i < size; i++)
            newqueue[i] = get(i);
        this.capacity = newcapacity;
        this.queue = newqueue;
        this.head = 0;
        this.tail = size;
    }

    @SuppressWarnings("unchecked")
    private T[] newArray(int size) {
        return (T[]) new Object[size];
    }

    public boolean add(T o) {
        // 添加到队尾
        queue[tail] = o;
        // 环形的，兄弟，需要求余，你懂的
        int newtail = (tail + 1) % capacity;
        // 队列满了
        if (newtail == head)
            throw new IndexOutOfBoundsException("Queue full");
        tail = newtail;
        return true; // we did add something
    }

    public T remove(int i) {
        if (i != 0)
            throw new IllegalArgumentException("Can only remove head of queue");
        if (head == tail)
            throw new IndexOutOfBoundsException("Queue empty");
        T removed = queue[head];
        queue[head] = null;
        head = (head + 1) % capacity;
        return removed;
    }

    public T get(int i) {
        // 每次都要动态求其元素个数
        int size = size();
        // 检查i是否合法
        if (i < 0 || i >= size) {
            final String msg = "Index " + i + ", queue size " + size;
            throw new IndexOutOfBoundsException(msg);
        }
        int index = (head + i) % capacity;
        return queue[index];
    }

    public int size() {
        // Can't use % here because it's not mod: -3 % 2 is -1, not +1.
        int diff = tail - head;
        if (diff < 0)
            diff += capacity;
        return diff;
    }

    private int capacity;
    private T[] queue;
    private int head;
    private int tail;
}

```

