# 快速开始

## 数据结构与算法

数据结构是一种数据的表现形式，如链表、二叉树、栈、队列等都是内存中一段数据表现的形式。
算法是一种通用的解决问题的模板或者思路，大部分数据结构都有一套通用的算法模板，所以掌握这些通用的算法模板即可解决各种算法问题。

后面会分专题讲解各种数据结构、基本的算法模板、和一些高级算法模板，每一个专题都有一些经典练习题，完成所有练习的题后，你对数据结构和算法会有新的收获和体会。

先介绍两个算法题，试试感觉~

示例 1

[strStr](https://leetcode-cn.com/problems/implement-strstr/)

> 给定一个  haystack 字符串和一个 needle 字符串，在 haystack 字符串中找出 needle 字符串出现的第一个位置 (从 0 开始)。如果不存在，则返回  -1。

思路：核心点遍历给定字符串字符，判断以当前字符开头字符串是否等于目标字符串

```java
class Solution {
    public int strStr(String haystack, String needle) {
        int L = needle.length(), n = haystack.length();
        for (int start = 0; start < n - L + 1; ++start) {
            if (haystack.substring(start, start + L).equals(needle)) {
                return start;
            }
        }
        return -1;
    }
}
```

需要注意点

- 循环时，i 不需要到 len-1
- 如果找到目标字符串，len(needle)==j

示例 2

[subsets](https://leetcode-cn.com/problems/subsets/)

> 给定一组不含重复元素的整数数组 nums，返回该数组所有可能的子集（幂集）。

思路：这是一个典型的应用回溯法的题目，简单来说就是穷尽所有可能性，算法模板如下

```
int[] result = new int[size];
void backtrack(选择列表,路径): {
    if 满足结束条件: {
        result.add(路径)
        return
    }
    for (选择 : 选择列表): {
        做选择
        backtrack(选择列表,路径)
        撤销选择
    }
}
```

通过不停的选择，撤销选择，来穷尽所有可能性，最后将满足条件的结果返回

答案代码

```java
class Solution {
    List<List<Integer>> output = new ArrayList();
    int n, k; // k表示某个子集内的元素个数
    private void backtrack(int first, ArrayList<Integer> cur, int[] nums) {
        if (cur.size() == k) {
            output.add(new ArrayList(cur));
        }
        for (int i = first; i < n; ++i) {
            cur.add(nums[i]);
            backtrack(i + 1, cur, nums);
            // 删除最后添加的一个数
            cur.remove(cur.size() - 1);
        }
    }
    public List<List<Integer>> subsets(int[] nums) { 
        n = nums.length;
        for (k = 0; k <= n; ++k) {
            backtrack(0, new ArrayList<Integer>(), nums);
        }
        return output;
    }
}
```

说明：后面会深入讲解几个典型的回溯算法问题，如果当前不太了解可以暂时先跳过

## 面试注意点

我们大多数时候，刷算法题可能都是为了准备面试，所以面试的时候需要注意一些点

- 快速定位到题目的知识点，找到知识点的**通用模板**，可能需要根据题目**特殊情况做特殊处理**。
- 先去朝一个解决问题的方向！**先抛出可行解**，而不是最优解！先解决，再优化！
- 代码的风格要统一，熟悉各类语言的代码规范。
  - 命名尽量简洁明了，尽量不用数字命名如：i1、node1、a1、b2
- 常见错误总结
  - 访问下标时，不能访问越界
  - 空值 null 问题 run time error

## 练习

- [ ] [strStr](https://leetcode-cn.com/problems/implement-strstr/)
- [ ] [subsets](https://leetcode-cn.com/problems/subsets/)
