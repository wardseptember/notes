# 回溯法

## 背景

回溯法（backtrack）常用于遍历列表所有子集，是 DFS 深度搜索一种，一般用于全排列，穷尽所有可能，遍历的过程实际上是一个决策树的遍历过程。时间复杂度一般 O(N!)，它不像动态规划存在重叠子问题可以优化，回溯算法就是纯暴力穷举，复杂度一般都很高。

## 模板

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


核心就是从选择列表里做一个选择，然后一直递归往下搜索答案，如果遇到路径不通，就返回来撤销这次选择。

## 示例

### [subsets](https://leetcode-cn.com/problems/subsets/)

> 给定一组不含重复元素的整数数组 nums，返回该数组所有可能的子集（幂集）。

遍历过程

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


### [subsets-ii](https://leetcode-cn.com/problems/subsets-ii/)

> 给定一个可能包含重复元素的整数数组 nums，返回该数组所有可能的子集（幂集）。说明：解集不能包含重复的子集。

重复的解不添加进去，并用一个数组visited标记某个元素是否被访问过
```java
class Solution {
    private void backtracking(List<List<Integer>> result, List<Integer> temp, boolean[] visited, int[] nums, int start, int size) {
        if (temp.size() == size) {
            result.add(new ArrayList<>(temp));
            return;
        }
        for (int i = start; i < nums.length; ++i) {
            if (i != 0 && nums[i] == nums[i - 1] && !visited[i - 1]) {
                continue;
            }
            temp.add(nums[i]);
            visited[i] = true;
            backtracking(result, temp, visited, nums, i + 1, size);
            visited[i] = false;
            temp.remove(temp.size() - 1);
        }
    }
    public List<List<Integer>> subsetsWithDup(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        Arrays.sort(nums);
        List<Integer> temp = new ArrayList<>();
        for (int i = 0; i <= nums.length; ++i) {
            backtracking(result, temp, new boolean[nums.length], nums, 0, i);
        }
        return result;
    }
}
```

### [permutations](https://leetcode-cn.com/problems/permutations/)

> 给定一个   没有重复   数字的序列，返回其所有可能的全排列。

思路：需要记录已经选择过的元素，满足条件的结果才进行返回

```java
class Solution {
    private void backtrack(List<Integer> permute, List<List<Integer>> permutes, boolean[] visited, int[] nums) {
        if (permute.size() == nums.length) {
            permutes.add(new ArrayList<>(permute));
            return;
        }
        for (int i = 0; i < visited.length; ++i) {
            if (visited[i]) {
                continue;
            }
            visited[i] = true;
            permute.add(nums[i]);
            backtrack(permute, permutes, visited, nums);
            permute.remove(permute.size() - 1);
            visited[i] = false;
        }
    }
    public List<List<Integer>> permute(int[] nums) {
        List<List<Integer>> permutes = new ArrayList<>();
        List<Integer> permute = new ArrayList<>();
        boolean[] visited = new boolean[nums.length];
        backtrack(permute, permutes, visited, nums);
        return permutes;
    }
}


```

### [permutations-ii](https://leetcode-cn.com/problems/permutations-ii/)

> 给定一个可包含重复数字的序列，返回所有不重复的全排列。

```java
class Solution {
    private void backtrack(List<List<Integer>> permutes, List<Integer> permute, boolean[] visited, int[] nums) {
        if (permute.size() == nums.length) {
            permutes.add(new ArrayList<>(permute));
            return;
        }
        for (int i = 0; i < nums.length; ++i){
            if (i != 0 && nums[i] == nums[i - 1] && !visited[i - 1]) {
                continue;
            }
            if (visited[i]) {
                continue;
            }
            visited[i] = true;
            permute.add(nums[i]);
            backtrack(permutes, permute, visited, nums);
            permute.remove(permute.size() - 1);
            visited[i] = false;
        }
    }
    public List<List<Integer>> permuteUnique(int[] nums) {
        List<List<Integer>> permutes = new ArrayList<>();
        List<Integer> permute = new ArrayList<>();
        Arrays.sort(nums);
        boolean[] visited = new boolean[nums.length];
        backtrack(permutes, permute, visited, nums);
        return permutes;
    }
}
```

## 练习

- [ ] [subsets](https://leetcode-cn.com/problems/subsets/)
- [ ] [subsets-ii](https://leetcode-cn.com/problems/subsets-ii/)
- [ ] [permutations](https://leetcode-cn.com/problems/permutations/)
- [ ] [permutations-ii](https://leetcode-cn.com/problems/permutations-ii/)

挑战题目

- [ ] [combination-sum](https://leetcode-cn.com/problems/combination-sum/)
- [ ] [letter-combinations-of-a-phone-number](https://leetcode-cn.com/problems/letter-combinations-of-a-phone-number/)
- [ ] [palindrome-partitioning](https://leetcode-cn.com/problems/palindrome-partitioning/)
- [ ] [restore-ip-addresses](https://leetcode-cn.com/problems/restore-ip-addresses/)
- [ ] [permutations](https://leetcode-cn.com/problems/permutations/)
