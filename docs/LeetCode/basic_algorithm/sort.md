# 排序

## 常考排序

### 快速排序

```java
public class Solution {
    public int[] quickSort(int[] nums) {
        // 思路：把一个数组分为左右两段，左段小于右段，类似分治法没有合并过程
        quickSort(nums, 0 , nums.length - 1);
        return nums;
    }

    private void quickSort(int[] nums, int start, int end) {
        if (start < end) {
            // pivot 是分割点，pivot左边的比nums[pivot]小，右边的比nums[pivot]大
            int pivot = partition(nums, start, end);
            quickSort(nums, 0, pivot - 1);
            quickSort(nums, pivot + 1, end);
        }
    }

    private int partition(int[] nums, int start, int end) {
        int target = nums[end];
        int i = start;
        // 将小于target移到数组前面
        for (int j = start; j < end; j++) {
            if (nums[j] < target) {
                swap(nums, i, j);
                i++;
            }
        }
        // 把中间的值换为用于比较的基准值
        swap(nums, i, end);
        return i;
    }

    private void swap(int[] nums, int i, int j) {
        int tmp = nums[j];
        nums[j] = nums[i];
        nums[i] = tmp;
    }
}
```

### 归并排序

```java
public class Solution {
    public int[] mergeSortRoot(int[] nums) {
        mergeSort(nums, 0 , nums.length - 1);
        return nums;
    }

    private void mergeSort(int[] nums, int l, int r) {
        if (l < r) {
            int mid = (l + r) / 2;
            // 分治
            mergeSort(nums, l, mid);
            mergeSort(nums, mid + 1, r);
            // 合并
            merge(nums, l, mid, r);
        }
    }

    private void merge(int[] nums, int l, int mid, int r) {
        int i = l, j = mid + 1, k = l;
        int[] tmp = new int[nums.length];
        while (i <= mid && j <= r) {
            if (nums[i] > nums[j]) {
                tmp[k++] = nums[j++];
            } else {
                tmp[k++] = nums[i++];
            }
        }
        while (i <= mid) {
            tmp[k++] = nums[i++];
        }
        while (j <= r) {
            tmp[k++] = nums[j++];
        }
        for (i = l; i <= r; i++) {
            nums[i] = tmp[i];
        }
    }
}
```

### 堆排序

用数组表示的完美二叉树 complete binary tree

> 完美二叉树 VS 其他二叉树

![](http://wardseptember.club/FlkDKfdlFhktC-Aum9D2TcWW-Uxd)

[动画展示](https://www.bilibili.com/video/av18980178/)

![](http://wardseptember.club/Fs4uTASjU1EJwP6662TMri7OfGtJ)
核心代码

```java
public class Solution {
    // 本函数完成在数组a[low]和a[high]的范围内对位置low上的结点进行调整
    void move(int[] nums, int low, int high) {
        // a[]中是一棵完全二叉树 ，所以关键字的存储必须从0开始或者从1开始都可以，从1开始做孩子为2*
        int i = low, j = 2 * i + 1;     //a[j]是a[i]的左孩子结点
        int temp = nums[i];
        while (j <= high) {
            if (j < high && nums[j] < nums[j + 1]) { //若右孩子较大，则把j指向右孩子
                ++j;                      // j变为2*i+1
            }
            if (temp < nums[j]) {
                nums[i] = nums[j];  //将a[j]调整到双亲结点的位置上
                i = j;                    //修改i和j的值，以便继续向下调整
                j = 2 * i + 1;
            }
            else {
                break;
            }
        }
        nums[i] = temp;                     //被调整结点的值放入最终位置
    }

    // 堆排序函数
    void heapSort(int[] nums) {
        int i;
        int temp;
        int n = nums.length - 1;
        for (i = n / 2; i >= 0; --i) { //建立初始堆,使跟结点最大也就是a[0]最大
            move(nums, i, n);
        }
        for (i = n; i >= 1; --i) {       //进行n-1次循环，完成堆排序
            // 以下3句换出了根结点中的关键字，将其放入最终位置
            temp = nums[0];
            nums[0] = nums[i];
            nums[i] = temp;
            move(nums, 0, i - 1);       //在减少了一个关键字的无序序列中进行调整
        }
    }
}
```

## 参考

[十大经典排序](https://www.cnblogs.com/onepixel/p/7674659.html)

[二叉堆](https://labuladong.gitbook.io/algo/shu-ju-jie-gou-xi-lie/er-cha-dui-xiang-jie-shi-xian-you-xian-ji-dui-lie)

## 练习

- [ ] 手写快排、归并、堆排序
