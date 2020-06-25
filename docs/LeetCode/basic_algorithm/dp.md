# 动态规划

## 背景

先从一道题目开始~

如题  [triangle](https://leetcode-cn.com/problems/triangle/)

> 给定一个三角形，找出自顶向下的最小路径和。每一步只能移动到下一行中相邻的结点上。

例如，给定三角形：

```text
[
     [2],
    [3,4],
   [6,5,7],
  [4,1,8,3]
]
```

自顶向下的最小路径和为  11（即，2 + 3 + 5 + 1 = 11）。

使用 DFS（遍历 或者 分治法）

超时
```java
public class Solution {
    int row;
    
    public int minimumTotal(List<List<Integer>> triangle) {
        row=triangle.size();
        return helper(0,0, triangle);
    }
    
    private int helper(int level, int c, List<List<Integer>> triangle){
        if (level==row-1){
            return triangle.get(level).get(c);
        }
        int left = helper(level+1, c, triangle);
        int right = helper(level+1, c+1, triangle);
        return Math.min(left, right) + triangle.get(level).get(c);
    }
}
```

优化 DFS，缓存已经被计算的值（称为：记忆化搜索 本质上：动态规划）
自顶向下
```java
public class Solution {
    int row;
    Integer[][] memo;
    
    public int minimumTotal(List<List<Integer>> triangle) {
        row = triangle.size();
        memo = new Integer[row][row];
        return helper(0,0, triangle);
    }
    
    private int helper(int level, int c, List<List<Integer>> triangle){
        if (memo[level][c]!=null)
            return memo[level][c];
        if (level==row-1){
            return memo[level][c] = triangle.get(level).get(c);
        }
        int left = helper(level+1, c, triangle);
        int right = helper(level+1, c+1, triangle);
        return memo[level][c] = Math.min(left, right) + triangle.get(level).get(c);
    }
}
```
动态规划就是把大问题变成小问题，并解决了小问题重复计算的方法称为动态规划

动态规划和 DFS 区别

- 二叉树 子问题是没有交集，所以大部分二叉树都用递归或者分治法，即 DFS，就可以解决
- 像 triangle 这种是有重复走的情况，**子问题是有交集**，所以可以用动态规划来解决

**动态规划三个特性**：
* 最优子结构

    最优子结构指的是，问题的最优解包含子问题的最优解。反过来说就是，我们可以通过子问题的最优解，推导出问题的最优解。如果我们把最优子结构，对应到我们前面定义的动态规划问题模型上，那我们也可以理解为，后面阶段的状态可以通过前面阶段的状态推导出来。
* 无后效性

    无后效性有两层含义，第一层含义是，在推导后面阶段的状态的时候，我们只关心前面阶段的状态值，不关心这个状态是怎么一步一步推导出来的。第二层含义是，某阶段状态一旦确定，就不受之后阶段的决策影响。无后效性是一个非常“宽松”的要求。只要满足前面提到的动态规划问题模型，其实基本上都会满足无后效性。
* 重复子问题

    如果用一句话概括一下，那就是，不同的决策序列，到达某个相同的阶段时，可能会产生重复的状态。所以才会用一个数组记录中间结果，避免重复计算。


动态规划，自底向上
这里变成一位数组，因为层号实际上可以不用记录，每次记录上一层的值，到当前层就把以前的覆盖到，动态规划运用场景其中一条就是最优子结构，往下走不用回头一定是最优的

```java
class Solution {
    public int minimumTotal(List<List<Integer>> triangle) {
        int row = triangle.size();
        int[] dp = new int[row + 1];
        for (int level = row - 1; level >= 0; level--) {
            for (int i = 0; i <= level; i++) {  // 第i行有i个数
                // 这里变成一位数组，因为层号实际上可以不用记录，每次记录上一层的值，到当前层就把以前的覆盖到，动态规划运用场景其中一条就是最优子结构，往下走不用回头一定是最优的
                dp[i] = Math.min(dp[i], dp[i + 1]) + triangle.get(level).get(i);
            }
        }
        return dp[0];
    }
}

```

## 递归和动规关系

递归是一种程序的实现方式：函数的自我调用

```go
Function(x) {
	...
	Funciton(x-1);
	...
}
```

动态规划：是一种解决问 题的思想，大规模问题的结果，是由小规模问 题的结果运算得来的。动态规划可用递归来实现(Memorization Search)

## 使用场景

满足三个条件：最优子结构，无后效性，重复子问题

简单来说就是：

- 满足以下条件之一
  - 求最大/最小值（Maximum/Minimum ）
  - 求是否可行（Yes/No ）
  - 求可行个数（Count(\*) ）
- 满足不能排序或者交换（Can not sort / swap ）

如题：[longest-consecutive-sequence](https://leetcode-cn.com/problems/longest-consecutive-sequence/)  位置可以交换，所以不用动态规划

## 四点要素

1. **状态 State**
   - 灵感，创造力，存储小规模问题的结果
2. 方程 Function
   - 状态之间的联系，怎么通过小的状态，来算大的状态
3. 初始化 Intialization
   - 最极限的小状态是什么, 起点
4. 答案 Answer
   - 最大的那个状态是什么，终点

## 常见四种类型

1. Matrix DP (10%)
1. Sequence (40%)
1. Two Sequences DP (40%)
1. Backpack (10%)

> 注意点
>
> - 贪心算法大多题目靠背答案，所以如果能用动态规划就尽量用动规，不用贪心算法

## 1、矩阵类型（10%）

### [minimum-path-sum](https://leetcode-cn.com/problems/minimum-path-sum/)

> 给定一个包含非负整数的  *m* x *n*  网格，请找出一条从左上角到右下角的路径，使得路径上的数字总和为最小。
```
思路：动态规划
1、state: f[x][y]从起点走到 x,y 的最短路径
2、function: f[x][y] = min(f[x-1][y], f[x][y-1]) + A[x][y]
3、intialize: f[0][0] = A[0][0]、f[i][0] = sum(0,0 -> i,0)、 f[0][i] = sum(0,0 -> 0,i)
4、answer: f[n-1][m-1]
```
自顶向下

```java
class Solution {
    public int minPathSum(int[][] grid) {
        if (grid == null || grid.length == 0 || grid[0].length == 0) {
            return 0;
        }
        int m = grid.length, n = grid[0].length;
        if (n == 1) {
            return grid[0][0];
        }
        int[][] result = new int[m][n];
        result[0][0] = grid[0][0];
        // 处理边界
        for (int i = 1; i < n; ++i) {
            result[0][i] = grid[0][i] + result[0][i-1];
        }
        for (int i = 1; i < m; ++i) {
            result[i][0] = grid[i][0] + result[i-1][0];
        }
        for (int i = 1; i < m; ++i) {
            for (int j = 1; j < n; ++j) {
                result[i][j] = Math.min(grid[i][j] + result[i-1][j], grid[i][j] + result[i][j-1]); 
            }
        }
        return result[m-1][n-1];
    }
}
```

### [unique-paths](https://leetcode-cn.com/problems/unique-paths/)

> 一个机器人位于一个 m x n 网格的左上角 （起始点在下图中标记为“Start” ）。
> 机器人每次只能向下或者向右移动一步。机器人试图达到网格的右下角（在下图中标记为“Finish”）。
> 问总共有多少条不同的路径？

每一个位置只能从左边一格或者上方一格走到，所以动态方程为dp[i][j] = dp[i-1][j] + dp[i][j-1]
又因为二维dp数组，可以被一维dp数组代替，之前的数据可以不保存，动态方程优化为dp[i]=dp[i]+d[i-1].
```java
class Solution {
    public int uniquePaths(int m, int n) {
        int[] dp = new int[n];
        Arrays.fill(dp, 1);
        for (int i = 1; i < m; ++i) {
            for (int j = 1; j < n; ++j) {
                dp[j] = dp[j] + dp[j - 1];
            }
        }
        return dp[n - 1];
    }
}
```

### [unique-paths-ii](https://leetcode-cn.com/problems/unique-paths-ii/)

> 一个机器人位于一个 m x n 网格的左上角 （起始点在下图中标记为“Start” ）。
> 机器人每次只能向下或者向右移动一步。机器人试图达到网格的右下角（在下图中标记为“Finish”）。
> 问总共有多少条不同的路径？
> 现在考虑网格中有障碍物。那么从左上角到右下角将会有多少条不同的路径？

动态规划，直接在原数组上操作，空间复杂度为O(1)
```
如果第一个格点 obstacleGrid[0,0] 是 1，说明有障碍物，那么机器人不能做任何移动，我们返回结果 0。
否则，如果 obstacleGrid[0,0] 是 0，我们初始化这个值为 1 然后继续算法。
遍历第一行，如果有一个格点初始值为 1 ，说明当前节点有障碍物，没有路径可以通过，设值为 0 ；否则设这个值是前一个节点的值 obstacleGrid[i,j] = obstacleGrid[i,j-1]。
遍历第一列，如果有一个格点初始值为 1 ，说明当前节点有障碍物，没有路径可以通过，设值为 0 ；否则设这个值是前一个节点的值 obstacleGrid[i,j] = obstacleGrid[i-1,j]。
现在，从 obstacleGrid[1,1] 开始遍历整个数组，如果某个格点初始不包含任何障碍物，就把值赋为上方和左侧两个格点方案数之和 obstacleGrid[i,j] = obstacleGrid[i-1,j] + obstacleGrid[i,j-1]。
如果这个点有障碍物，设值为 0 ，这可以保证不会对后面的路径产生贡献。
```

```java
class Solution {
    public int uniquePathsWithObstacles(int[][] obstacleGrid) {
        int rows = obstacleGrid.length;
        int cols = obstacleGrid[0].length;
        if (obstacleGrid[0][0] == 1) {
            return 0;
        }
        obstacleGrid[0][0] = 1;
        // 初始化边界
        for (int i = 1; i < rows; ++i) {
            obstacleGrid[i][0] = (obstacleGrid[i][0] == 0 && obstacleGrid[i - 1][0] == 1) ? 1 : 0;
        }
        for (int j = 1; j < cols; ++j) {
            obstacleGrid[0][j] = (obstacleGrid[0][j] == 0 && obstacleGrid[0][j - 1] == 1) ? 1 : 0;
        }
        for (int i = 1; i < rows; ++i) {
            for (int j = 1; j < cols; ++j) {
                if (obstacleGrid[i][j] == 0) {
                    obstacleGrid[i][j] = obstacleGrid[i - 1][j] + obstacleGrid[i][j - 1];
                } else {
                    obstacleGrid[i][j] = 0;
                }
            }
        }
        return obstacleGrid[rows - 1][cols - 1];
    }
}
```

## 2、序列类型（40%）

### [climbing-stairs](https://leetcode-cn.com/problems/climbing-stairs/)

> 假设你正在爬楼梯。需要  *n*  阶你才能到达楼顶。

定义一个数组 dp 存储上楼梯的方法数（为了方便讨论，数组下标从 1 开始），dp[i] 表示走到第 i 个楼梯的方法数目。

第 i 个楼梯可以从第 i-1 和 i-2 个楼梯再走一步到达，走到第 i 个楼梯的方法数为走到第 i-1 和第 i-2 个楼梯的方法数之和。
动态转移方程为：
`dp[i] = dp[i-1] + dp[i-2]`

考虑到 dp[i] 只与 dp[i - 1] 和 dp[i - 2] 有关，因此可以只用两个变量来存储 dp[i - 1] 和 dp[i - 2]，使得原来的 O(N) 空间复杂度优化为 O(1) 复杂度。

```java
class Solution {
    public int climbStairs(int n) {
        if (n <= 2) {
            return n;
        }
        int pre1 = 1, pre2 = 2;
        for (int i = 2; i < n; ++i) {
            int cur = pre1 + pre2;
            pre1 = pre2;
            pre2 = cur;
        }
        return pre2;
    }
}
```

### [jump-game](https://leetcode-cn.com/problems/jump-game/)

> 给定一个非负整数数组，你最初位于数组的第一个位置。
> 数组中的每个元素代表你在该位置可以跳跃的最大长度。
> 判断你是否能够到达最后一个位置。

对于当前遍历到的位置 ，如果它在最远可以到达的位置的范围内，那么我们就可以从起点通过若干次跳跃到达该位置， 因此我们可以用 x+nums[x]更新最远可以到达的位置。if (i <= rightmost) 这句判断就是起到了题解中这句话的作用。举个例子，nums=[1,0,2,3]，那么当i=2时rightmost=1，此时i>rightmost，表明我们无法到达index=2的位置，也就无法更新rightmost了。
```java
class Solution {
    public boolean canJump(int[] nums) {
        int n = nums.length;
        int rightMost = 0;
        for (int i = 0; i < n; ++i) {
            if (i <= rightMost) {  // 如果i > rightMost，说明到不了rightMost，不更新
                rightMost = Math.max(rightMost, i + nums[i]);
                if (rightMost >= n - 1) {
                    return true;
                }
            }
        }
        return false;
    }
}
```

### [jump-game-ii](https://leetcode-cn.com/problems/jump-game-ii/)

> 给定一个非负整数数组，你最初位于数组的第一个位置。
> 数组中的每个元素代表你在该位置可以跳跃的最大长度。
> 你的目标是使用最少的跳跃次数到达数组的最后一个位置。

对于数组 [2,3,1,2,4,2,3]，初始位置是下标 0，从下标 0 出发，最远可到达下标 2。下标 0 可到达的位置中，下标 1 的值是 3，从下标 1 出发可以达到更远的位置，因此第一步到达下标 1。
从下标 1 出发，最远可到达下标 4。下标 1 可到达的位置中，下标 4 的值是 4 ，从下标 4 出发可以达到更远的位置，因此第二步到达下标 4。

我们维护当前能够到达的最大下标位置，记为边界。我们从左到右遍历数组，到达边界时，更新边界并将跳跃次数增加 1。     
```java
class Solution {
    public int jump(int[] nums) {
        int len = nums.length;
        int end = 0;  // 判断是否到达上一个最大边界
        int maxPosition = 0;  // 当前能跳到的最大位置
        int steps = 0;  // 记录跳的次数，
        for (int i = 0; i < len - 1; ++i) {
            maxPosition = Math.max(maxPosition, i + nums[i]); // 更新最大边界
            if (i == end) { // 如果到达上一个最大边界，更新数据，说明从上个位置一步可以跳到这里
                end = maxPosition;
                steps++;
            }
        }
        return steps;
    }
}
```

### [palindrome-partitioning-ii](https://leetcode-cn.com/problems/palindrome-partitioning-ii/)

> 给定一个字符串 _s_，将 _s_ 分割成一些子串，使每个子串都是回文串。
> 返回符合要求的最少分割次数。

```java
class Solution {
    public int minCut(String s) {
        int n = s.length();
        int[] dp = new int[n];
        // 假设没有任何的回文串，初始化 dp
        for (int i = 0; i < n; ++i) {
            dp[i] = i;
        }
        // 把第i个字符当做中心，向两边扩散，考虑每个中心
        for (int i = 0; i < n; ++i) {
            // j 表示某一个方向扩展的个数
            int j = 0;
            // 考虑奇数的情况
            while (true) {
                if (i - j < 0 || i + j > n - 1) {
                    break;
                } else if (s.charAt(i - j) == s.charAt(i + j)) {
                    if (i - j == 0) {
                        dp[i + j] = 0;
                    } else {
                        dp[i + j] = Math.min(dp[i + j], dp[i - j - 1] + 1);
                    }
                }
                else {
                    break;
                }
                j++;
            }
            j = 1;
            // 考虑偶数的情况
            while (true) {
                if (i - j + 1 < 0 || i + j > n - 1) {
                    break;
                } else if (s.charAt(i - j + 1) == s.charAt(i + j)) {
                    if (i - j + 1 == 0) {
                        dp[i + j] = 0;
                    } else {
                        // dp[i - j] = dp[i - j + 1 - 1]
                        dp[i + j] = Math.min(dp[i + j], dp[i - j] + 1);
                    }
                } else {
                    break;
                }
                j++;
            }
        }
        return dp[n - 1];
    }
}
```

注意点

- 判断回文字符串时，可以提前用动态规划算好，减少时间复杂度

### [longest-increasing-subsequence](https://leetcode-cn.com/problems/longest-increasing-subsequence/)

> 给定一个无序的整数数组，找到其中最长上升子序列的长度。

```
定义一个 tails 数组，其中 tails[i] 存储长度为 i + 1 的最长递增子序列的最后一个元素。对于一个元素 x，

如果它大于 tails 数组所有的值，那么把它添加到 tails 后面，表示最长递增子序列长度加 1；
如果 tails[i-1] < x <= tails[i]，那么更新 tails[i] = x。
例如对于数组 [4,3,6,5]，有：
tails      len      num
[]         0        4
[4]        1        3
[3]        1        6
[3,6]      2        5
[3,5]      2        null
```
可以看出 tails 数组保持有序，因此在查找 Si 位于 tails 数组的位置时就可以使用二分查找。
```java
class Solution {
    public int lengthOfLIS(int[] nums) {
        int n = nums.length;
        if (nums == null || n == 0) {
            return 0;
        }
        int[] tails = new int[n];
        int maxLength = 0;
        for (int num : nums) {
            int index = binarySearch(tails, maxLength, num);
            tails[index] = num;
            if (index == maxLength) {
                maxLength++;
            }
        }
        return maxLength;
    }
    private int binarySearch(int[] tails, int len, int key) {
        int left = 0, right = len;
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (tails[mid] == key) {
                return mid;
            } else if (tails[mid] > key) {
                right = mid;
            } else {
                left = mid + 1;
            }
        }
        return left;
    }
}
```

### [word-break](https://leetcode-cn.com/problems/word-break/)

> 给定一个**非空**字符串  *s*  和一个包含**非空**单词列表的字典  *wordDict*，判定  *s*  是否可以被空格拆分为一个或多个在字典中出现的单词。


dict 中的单词没有使用次数的限制，因此这是一个完全背包问题。

该问题涉及到字典中单词的使用顺序，也就是说物品必须按一定顺序放入背包中，例如下面的 dict 就不够组成字符串 “leetcode”：
["lee", "tc", "cod"]

求解顺序的完全背包问题时，对物品的迭代应该放在最里层，对背包的迭代放在外层，只有这样才能让物品按一定顺序放入背包中。
```java
class Solution {
    public boolean wordBreak(String s, List<String> wordDict) {
        int n = s.length();
        boolean[] dp = new boolean[n + 1];
        dp[0] = true;
        for (int i = 0; i <= n; i++) {
            for (String word : wordDict) {
                int len = word.length();
                if (len <= i && word.equals(s.substring(i - len, i))) {
                    dp[i] = dp[i] || dp[i - len];
                }
            }
        }
        return dp[n];
    }
}
```

小结

常见处理方式是给 0 位置占位，这样处理问题时一视同仁，初始化则在原来基础上 length+1，返回结果 f[n]

- 状态可以为前 i 个
- 初始化 length+1
- 取值 index=i-1
- 返回值：f[n]或者 f[m][n]

## Two Sequences DP（40%）

### [longest-common-subsequence](https://leetcode-cn.com/problems/longest-common-subsequence/)

> 给定两个字符串  text1 和  text2，返回这两个字符串的最长公共子序列。
> 一个字符串的   子序列   是指这样一个新的字符串：它是由原字符串在不改变字符的相对顺序的情况下删除某些字符（也可以不删除任何字符）后组成的新字符串。
> 例如，"ace" 是 "abcde" 的子序列，但 "aec" 不是 "abcde" 的子序列。两个字符串的「公共子序列」是这两个字符串所共同拥有的子序列。


详解见[https://leetcode-cn.com/problems/longest-common-subsequence/solution/dong-tai-gui-hua-zhi-zui-chang-gong-gong-zi-xu-lie/
](https://leetcode-cn.com/problems/longest-common-subsequence/solution/dong-tai-gui-hua-zhi-zui-chang-gong-gong-zi-xu-lie/
)
```java
class Solution {
    public int longestCommonSubsequence(String text1, String text2) {
        int m = text1.length(), n = text2.length();
        int[][] dp = new int[m + 1][n + 1];
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; ++j) {
                if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        return dp[m][n];
    }
}
```


### [edit-distance](https://leetcode-cn.com/problems/edit-distance/)

> 给你两个单词  word1 和  word2，请你计算出将  word1  转换成  word2 所使用的最少操作数  
> 你可以对一个单词进行如下三种操作：
> 插入一个字符
> 删除一个字符
> 替换一个字符

思路：和上题很类似，相等则不需要操作，否则取删除、插入、替换最小操作次数的值+1

```java
class Solution {
    public int minDistance(String word1, String word2) {
        if (word1 == null || word2 == null) {
            return 0;
        }
        int m = word1.length(), n = word2.length();
        int[][] dp = new int[m + 1][n + 1];
        for (int i = 1; i <= m; i++) {
            dp[i][0] = i;
        }
        for (int i = 1; i <= n; ++i) {
            dp[0][i] = i;
        }
        for (int i = 1; i <= m; ++i) {
            for (int j = 1; j <= n; ++j) {
                if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = Math.min(dp[i - 1][j - 1], Math.min(dp[i][j - 1], dp[i - 1][j])) + 1;
                }
            }
        }
        return dp[m][n];
    }
}
```

说明

> 另外一种做法：MAXLEN(a,b)-LCS(a,b)

## 零钱和背包（10%）

### [coin-change](https://leetcode-cn.com/problems/coin-change/)

> 给定不同面额的硬币 coins 和一个总金额 amount。编写一个函数来计算可以凑成总金额所需的最少的硬币个数。如果没有任何一种硬币组合能组成总金额，返回  -1。

思路：
因为硬币可以重复使用，因此这是一个完全背包问题。完全背包只需要将 0-1 背包的逆序遍历 dp 数组改为正序遍历即可。
```java
class Solution {
    public int coinChange(int[] coins, int amount) {
        if (coins == null || coins.length == 0) {
            return -1;
        }
        if (amount == 0) {
            return 0;
        }
        int[] dp = new int[amount + 1];
        int coinMin = 0;
        for (int coin : coins) {
            for (int i = coin; i <= amount; ++i) {
                if (i == coin) {
                    dp[i] = 1;
                } else if (dp[i] == 0 && dp[i - coin] != 0) { 
                    dp[i] = dp[i - coin] + 1;
                } else if (dp[i - coin] != 0) {
                    dp[i] = Math.min(dp[i], dp[i - coin] + 1);
                }
            }
            if (coin < coinMin) {
                coinMin = coin;
            }
        }
        if (coinMin > amount) {
            return -1;
        }
        return dp[amount] == 0 ? -1 : dp[amount];
    }
}
```

注意

> dp[i-a[j]] 决策 a[j]是否参与

### [backpack](https://www.lintcode.com/problem/backpack/description)

> 在 n 个物品中挑选若干物品装入背包，最多能装多满？假设背包的大小为 m，每个物品的大小为 A[i]

```java
public class Solution {
    /**
     * @param m: An integer m denotes the size of a backpack
     * @param A: Given n items with size A[i]
     * @return: The maximum size
     */
    public int backPack(int m, int[] A) {
        // write your code here
        int n = A.length;
        boolean[] states = new boolean[m + 1]; // 默认值false
        states[0] = true;  // 第一行的数据要特殊处理，可以利用哨兵优化
        if (A[0] <= m) {
            states[A[0]] = true;
        }
        for (int i = 1; i < n; ++i) { // 动态规划
            for (int j = m - A[i]; j >= 0; --j) { //把第i个物品放入背包
                if (states[j] == true) {
                    states[j + A[i]] = true;
                }
            }
        }
        for (int i = m; i >= 0; --i) { // 输出结果
            if (states[i] == true) return i;
        }
        return 0;
    }
}
```

### [backpack-ii](https://www.lintcode.com/problem/backpack-ii/description)

> 有 `n` 个物品和一个大小为 `m` 的背包. 给定数组 `A` 表示每个物品的大小和数组 `V` 表示每个物品的价值.
> 问最多能装入背包的总价值是多大?


常规思路
```java
public class Solution {
    /**
     * @param m: An integer m denotes the size of a backpack
     * @param A: Given n items with size A[i]
     * @param V: Given n items with V V[i]
     * @return: The maximum V
     */
    public int backPackII(int m, int[] A, int[] V) {
        int n = A.length;
        int[][] states = new int[n][m + 1];
        for (int i = 0; i < n; ++i) { // 初始化states
            for (int j = 0; j < m + 1; ++j) {
                states[i][j] = -1;
            }
        }
        states[0][0] = 0;
        if (A[0] <= m) {
            states[0][A[0]] = V[0];
        }
        for (int i = 1; i < n; ++i) {  // 动态规划，状态转移
            for (int j = 0; j <= m; ++j) {  // 不选择第i个物品
                if (states[i - 1][j] >= 0) {
                    states[i][j] = states[i - 1][j];
                }
            }
            for (int j = 0; j <= m - A[i]; ++j) { // 选择第i个物品
                if (states[i - 1][j] >= 0) {
                    int v = states[i - 1][j] + V[i];
                    if (v > states[i][j + A[i]]) {
                        states[i][j + A[i]] = v;
                    }
                }
            }
        }
        // 找出最大值
        int maxV = -1;
        for (int j = 0; j <= m; ++j) {
            if (states[n - 1][j] > maxV) {
                maxV = states[n - 1][j];
            }
        }
        return maxV;
    }
}
```

优化解法
```java
public class Solution {
    /**
     * @param m: An integer m denotes the size of a backpack
     * @param A: Given n items with size A[i]
     * @param V: Given n items with value V[i]
     * @return: The maximum value
     */
    public int backPackII(int m, int[] A, int[] V) {
        return backPack(m, A, V);
    }
    
    private int backPack(int maxVolume, int[] volumes, int[] values) {
        int objectAmount = volumes.length;
        if (objectAmount == 0) {
            return 0;
        }
        int[] maxValuePerVolume = new int[maxVolume + 1];
        for (int cAmount = 0; cAmount < objectAmount; cAmount++) {
            for (int cVolume = maxVolume; cVolume > 0; cVolume--) {
                if (cVolume >= volumes[cAmount]) {
                    maxValuePerVolume[cVolume] = Math.max(maxValuePerVolume[cVolume], maxValuePerVolume[cVolume - volumes[cAmount]] + values[cAmount]);
                }
            }
        }
        return maxValuePerVolume[maxVolume];
    }
}
```
## 练习

Matrix DP (10%)

- [ ] [triangle](https://leetcode-cn.com/problems/triangle/)
- [ ] [minimum-path-sum](https://leetcode-cn.com/problems/minimum-path-sum/)
- [ ] [unique-paths](https://leetcode-cn.com/problems/unique-paths/)
- [ ] [unique-paths-ii](https://leetcode-cn.com/problems/unique-paths-ii/)

Sequence (40%)

- [ ] [climbing-stairs](https://leetcode-cn.com/problems/climbing-stairs/)
- [ ] [jump-game](https://leetcode-cn.com/problems/jump-game/)
- [ ] [jump-game-ii](https://leetcode-cn.com/problems/jump-game-ii/)
- [ ] [palindrome-partitioning-ii](https://leetcode-cn.com/problems/palindrome-partitioning-ii/)
- [ ] [longest-increasing-subsequence](https://leetcode-cn.com/problems/longest-increasing-subsequence/)
- [ ] [word-break](https://leetcode-cn.com/problems/word-break/)

Two Sequences DP (40%)

- [ ] [longest-common-subsequence](https://leetcode-cn.com/problems/longest-common-subsequence/)
- [ ] [edit-distance](https://leetcode-cn.com/problems/edit-distance/)

Backpack & Coin Change (10%)

- [ ] [coin-change](https://leetcode-cn.com/problems/coin-change/)
- [ ] [backpack](https://www.lintcode.com/problem/backpack/description)
- [ ] [backpack-ii](https://www.lintcode.com/problem/backpack-ii/description)
