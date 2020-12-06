# hashtable简介

hashtable是线程安全的，代码里面加的synchronized。他实现了Map接口，继承Dictionary类，不过hashtable已经基本不使用了，他是遗留类。

不要求线程安全的程序可以使用hashmap，要求线程安全的程序可用使用ConcurrentHashMap，这二者效率更高。

hashtable默认大小为11，装填因子为0.75，也是基于数组和链表的方式实现的。

hashmap的value可以为null，hashtable的key不能为null。

HashTable是基于数组和链表实现的，存在hash冲突，就采用头插法，将新结点插入到链表的头部。

如果你看我的[hashmap详解](https://wardseptember.github.io/notes/#/README)，hashtable还是比较简单的。

多线程高并发教程也可以[我的笔记](https://wardseptember.github.io/notes/#/README)。

> 本教程基于jdk 1.8。别的版本也不想看了，遗留类了，还有啥可看的。



# 源码

源码比较简单，加的全局锁，进行put的时候就不能get，进行get的时候就不能put，你想想效率低不低。

## put方法

```java
    public synchronized V put(K key, V value) {
        // Make sure the value is not null
        if (value == null) {
            throw new NullPointerException();
        }

        // Makes sure the key is not already in the hashtable.
        Entry<?,?> tab[] = table;
        // 计算hash也比较简单，直接把key的hashcode编码作为hash值
        int hash = key.hashCode();
        // 计算索引，直接把hash与int最大值做与运算，然后对tab.length求余
        int index = (hash & 0x7FFFFFFF) % tab.length;
        @SuppressWarnings("unchecked")
        Entry<K,V> entry = (Entry<K,V>)tab[index];
        // 如果key已经存在，则更新value值
        for(; entry != null ; entry = entry.next) {
            if ((entry.hash == hash) && entry.key.equals(key)) {
                V old = entry.value;
                entry.value = value;
                return old;
            }
        }
		// 添加这个key、value
        addEntry(hash, key, value, index);
        return null;
    }
```

### addEntry

```java
    private void addEntry(int hash, K key, V value, int index) {
        modCount++;

        Entry<?,?> tab[] = table;
        if (count >= threshold) {
            // Rehash the table if the threshold is exceeded
            // 如果超过阈值，则会重新hash
            rehash();

            tab = table;
            hash = key.hashCode();
            index = (hash & 0x7FFFFFFF) % tab.length;
        }

        // Creates the new entry.
        @SuppressWarnings("unchecked")
        Entry<K,V> e = (Entry<K,V>) tab[index];
        tab[index] = new Entry<>(hash, key, value, e);
        count++;
    }
```

### rehash

rehash方法就是hashtable扩容的方法，也比较简单，直接把new 一个新的Entry数组，把原table里面的元素重新计算hash值，放到新的table里面。相比hashmap，效率低。

```java
    protected void rehash() {
        int oldCapacity = table.length;
        Entry<?,?>[] oldMap = table;

        // overflow-conscious code
        int newCapacity = (oldCapacity << 1) + 1;
        if (newCapacity - MAX_ARRAY_SIZE > 0) {
            if (oldCapacity == MAX_ARRAY_SIZE)
                // Keep running with MAX_ARRAY_SIZE buckets
                return;
            newCapacity = MAX_ARRAY_SIZE;
        }
        Entry<?,?>[] newMap = new Entry<?,?>[newCapacity];

        modCount++;
        threshold = (int)Math.min(newCapacity * loadFactor, MAX_ARRAY_SIZE + 1);
        table = newMap;

        for (int i = oldCapacity ; i-- > 0 ;) {
            for (Entry<K,V> old = (Entry<K,V>)oldMap[i] ; old != null ; ) {
                Entry<K,V> e = old;
                old = old.next;

                int index = (e.hash & 0x7FFFFFFF) % newCapacity;
                e.next = (Entry<K,V>)newMap[index];
                newMap[index] = e;
            }
        }
    }
```

## get方法

直接取就完事了。

```java
    public synchronized V get(Object key) {
        Entry<?,?> tab[] = table;
        int hash = key.hashCode();
        int index = (hash & 0x7FFFFFFF) % tab.length;
        for (Entry<?,?> e = tab[index] ; e != null ; e = e.next) {
            if ((e.hash == hash) && e.key.equals(key)) {
                return (V)e.value;
            }
        }
        return null;
    }
```

## remove方法

```java
    public synchronized V remove(Object key) {
        Entry<?,?> tab[] = table;
        int hash = key.hashCode();
        int index = (hash & 0x7FFFFFFF) % tab.length;
        @SuppressWarnings("unchecked")
        Entry<K,V> e = (Entry<K,V>)tab[index];
        // prev是e的前驱结点，删除e，就设置prev.next = e.next
        for(Entry<K,V> prev = null ; e != null ; prev = e, e = e.next) {
            if ((e.hash == hash) && e.key.equals(key)) {
                modCount++;
                // prev =null 说明e是首结点
                if (prev != null) {
                    prev.next = e.next;
                } else {
                    tab[index] = e.next;
                }
                count--;
                V oldValue = e.value;
                e.value = null;
                return oldValue;
            }
        }
        return null;
    }
```

