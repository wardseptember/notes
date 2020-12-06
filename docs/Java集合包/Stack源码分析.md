# 简介

Stack是栈，先入后出，继承自Vector，所以是线程安全的。遗留类，不推荐使用，可用Deque模拟战。本质上还是用数组实现的，数组尾部就是栈顶。

```java
Deque<Integer> stack = new LinkedList<>();
stack.addFirst(12);
stack.pollFirst();
```

<div align="center"> <img src="https://gitee.com/wardseptember/images/raw/master/imgs/20201206215001.png" width="600"/> </div><br>

# 源码

源码比较简单

```java
package java.util;


public
class Stack<E> extends Vector<E> {
    /**
     * Creates an empty Stack.
     */
    public Stack() {
    }

    public E push(E item) {
        // 添加到数组尾部
        addElement(item);

        return item;
    }

    public synchronized E pop() {
        E       obj;
        int     len = size();
        // 获得数组最后一个元素
        obj = peek();
        // 删除数组最后一个元素
        removeElementAt(len - 1);

        return obj;
    }

    /**
     * Looks at the object at the top of this stack without removing it
     * from the stack.
     *
     * @return  the object at the top of this stack (the last item
     *          of the <tt>Vector</tt> object).
     * @throws  EmptyStackException  if this stack is empty.
     */
    public synchronized E peek() {
        int     len = size();

        if (len == 0)
            throw new EmptyStackException();
        return elementAt(len - 1);
    }

    /**
     * Tests if this stack is empty.
     *
     * @return  <code>true</code> if and only if this stack contains
     *          no items; <code>false</code> otherwise.
     */
    public boolean empty() {
        return size() == 0;
    }

	// 返回o所在的索引位置
    public synchronized int search(Object o) {
        int i = lastIndexOf(o);

        if (i >= 0) {
            return size() - i;
        }
        return -1;
    }

    /** use serialVersionUID from JDK 1.0.2 for interoperability */
    private static final long serialVersionUID = 1224463164541339165L;
}

```

