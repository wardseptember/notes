# 二叉树

## 知识点

### 二叉树遍历

**前序遍历**：**先访问根节点**，再前序遍历左子树，再前序遍历右子树
**中序遍历**：先中序遍历左子树，**再访问根节点**，再中序遍历右子树
**后序遍历**：先后序遍历左子树，再后序遍历右子树，**再访问根节点**

注意点

- 以根访问顺序决定是什么遍历
- 左子树都是优先右子树
#### 树结构
```java
public class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode(int x) { val = x; }
}
```
#### 前序递归

```java
public class PreOrderRecursive {
    public void preOrder(TreeNode root) {
        if (root == null) {
            return;
        }
        System.out.println(root.val);
        preOrder(root.left);
        preOrder(root.right);
    }
}
```

#### 中序递归
```java
public class InOrderRecursive {
    public void inOrder(TreeNode root) {
        if (root == null) {
            return;
        }
        inOrder(root.left);
        // 在递归中间写操作
        System.out.println(root.val);
        inOrder(root.right);
    }
}
```
#### 后序递归
```java
public class InOrderRecursive {
    public void inOrder(TreeNode root) {
        if (root == null) {
            return;
        }
        inOrder(root.left);
        inOrder(root.right);
        // 在递归后面写操作
        System.out.println(root.val);
    }
}
```
#### 前序非递归
* 用Deque模拟栈，因为Stack类是遗留类，不推荐使用。所有需要使用栈的地方都用Deque来模拟。
```java
class Solution {
    public List<Integer> preOrderTraversal(TreeNode root) {
        if (root == null) {
            return new LinkedList<>();
        }
        List<Integer> res = new LinkedList<>();
        Deque<TreeNode> stack = new LinkedList<>();
        stack.addFirst(root);
        while(!stack.isEmpty()) {
            TreeNode node = stack.removeFirst();
            res.add(node.val);
            if (node.right != null) {
                stack.addFirst(node.right);
            }
            if (node.left != null) {
                stack.addFirst(node.left);
            }
        }
        return res;
    }
}
```

#### 中序非递归
中序非递归遍历是先遍历最左节点，然后层层向上回溯。
```java
class Solution {
    public List<Integer> inOrderTraversal(TreeNode root) {
        if (root == null) {
            return new LinkedList<>();
        }
        List<Integer> res = new LinkedList<>();
        Deque<TreeNode> stack = new LinkedList<>();
        TreeNode node = root;
        while(node != null || !stack.isEmpty()) {
            while (node != null) {
                stack.addLast(node);
                node = node.left;
            }
            node = stack.removeLast();
            res.add(node.val);
            node = node.right;
        }
        return res;
    }
}


```

#### 后序非递归
后序非递归遍历，跟前序非递归有些类似，不过后序是先访问跟节点，然后左子节点，再访问右子节点，依次压入栈；
从栈里取出时，是后序遍历的反序，需要翻转。这里利用Deque的性质，可每次插入到链头，相当于翻转。
```java
class Solution {
    public List<Integer> postrderTraversal(TreeNode root) {
        if (root == null) {
            return new LinkedList<>();
        }
        LinkedList<Integer> res = new LinkedList<>();
        Deque<TreeNode> stack = new LinkedList<>();
        stack.addFirst(root);
        while(!stack.isEmpty()) {
            TreeNode node = stack.removeFirst();
            res.addFirst(node.val);
            if (node.left != null) {
                stack.addFirst(node.left);
            }
            if (node.right != null) {
                stack.addFirst(node.right);
            }
        }
        return res;
    }
}
```

#### DFS 深度搜索-从上到下

```java
public class Solution {
    public List<Integer> dfsUpToDown(TreeNode root) {
        List<Integer> res = new LinkedList<>();
        dfs(root, res);
        return res;
    }
    
    public void dfs(TreeNode node, List<Integer> res) {
        if (node == null) {
            return;
        }
        res.add(node.val);
        dfs(node.left, res);
        dfs(node.right, res);
    }
}
```

#### DFS 深度搜索-从下向上（分治法）

```java
public class Solution {
    public List<Integer> prerderTraversal(TreeNode root) {
        return divideAndConquer(root);
    }

    public List<Integer> divideAndConquer(TreeNode node) {
        List<Integer> result = new LinkedList<>();
        if (node == null) {
            return null;
        }
        // 分治
        List<Integer> left = divideAndConquer(node.left);
        List<Integer> right = divideAndConquer(node.right);
        // 合并结果
        result.add(node.val);
      	if (left != null) {
            result.addAll(left);
        }
        if (right != null) {
            result.addAll(right);
        }
        return result;
    }
}
```

注意点：

> DFS 深度搜索（从上到下） 和分治法区别：前者一般将最终结果通过指针参数传入，后者一般递归返回结果最后合并

#### BFS 层次遍历

```java
public class Solution {
    public List<Integer> levelOrder(TreeNode root) {
        List<Integer> res = new LinkedList<>();
        Queue<TreeNode> queue = new LinkedList<>();
        queue.add(root);
        while(!queue.isEmpty()) {
            // size记录当前层有多少元素（遍历当前层，再添加下一层）
            int size = queue.size();
            for (int i = 0; i < size; ++i) {
                TreeNode node = queue.poll();
                res.add(node.val);
                if (node.left != null) {
                    queue.add(node.left);
                }
                if (node.right != null) {
                    queue.add(node.right);
                }
            }
        }
        return res;
    }
}
```

### 分治法应用

先分别处理局部，再合并结果

适用场景

- 快速排序
- 归并排序
- 二叉树相关问题

分治法模板

- 递归返回条件
- 分段处理
- 合并结果

```java
// 伪代码
public class Solution {
    public ResultType traversal(TreeNode root) {
        if (root == null) {
            // do something and return
        }

        // Divide
        ResultType left = traversal(root.left);
        ResultType right = traversal(root.right);

        // Conquer
        ResultType result = Merge from left and right

        return result;
    }
}
```

#### 典型示例

```java
// 通过分治法遍历二叉树
public class Solution {
    public List<Integer> prerderTraversal(TreeNode root) {
        return divideAndConquer(root);
    }

    public List<Integer> divideAndConquer(TreeNode node) {
        List<Integer> result = new LinkedList<>();
        if (node == null) {
            return null;
        }
        // 分治
        List<Integer> left = divideAndConquer(node.left);
        List<Integer> right = divideAndConquer(node.right);
        // 合并结果
        result.add(node.val);
        result.addAll(left);
        result.addAll(right);
        return result;
    }
}
```

#### 归并排序  

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

注意点

> 递归需要返回结果用于合并

#### 快速排序  

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

注意点：

> 快排由于是原地交换所以没有合并过程
> 传入的索引是存在的索引（如：0、length-1 等），越界可能导致崩溃

常见题目示例

#### maximum-depth-of-binary-tree

[maximum-depth-of-binary-tree](https://leetcode-cn.com/problems/maximum-depth-of-binary-tree/)

> 给定一个二叉树，找出其最大深度。

思路：分治法

```java
// 计算maxDepth(root.left)，maxDepth(root.right)就是分治，
// Math.max(maxDepth(root.left), maxDepth(root.right)) + 1就是合并的过程
class Solution {
    public int maxDepth(TreeNode root) {
        if (root == null) {
            return 0;
        }
        return Math.max(maxDepth(root.left), maxDepth(root.right)) + 1;
    }
}


```

#### balanced-binary-tree

[balanced-binary-tree](https://leetcode-cn.com/problems/balanced-binary-tree/)

> 给定一个二叉树，判断它是否是高度平衡的二叉树。

思路：分治法，左边平衡 && 右边平衡 && 左右两边高度 <= 1，
遍历一遍，如果有左右两边高度 > 1，则不是高度平衡的二叉树。

```java
class Solution {
    private boolean result = true;
    public boolean isBalanced(TreeNode root) {
        maxDepth(root);
        return result;
    }
    private int maxDepth(TreeNode root) {
        if (root == null) {
            return 0;
        }
        int leftDepth = maxDepth(root.left);
        int rightDepth = maxDepth(root.right);
        if (Math.abs(leftDepth - rightDepth) > 1) {
            result = false;
        }
        // 返回的相当于子树的高度
        return 1 + Math.max(leftDepth, rightDepth);
        
    }
}


```


#### binary-tree-maximum-path-sum

[binary-tree-maximum-path-sum](https://leetcode-cn.com/problems/binary-tree-maximum-path-sum/)

> 给定一个**非空**二叉树，返回其最大路径和。

思路：分治法，递归计算出左右子节点的最大贡献值，只有在最大贡献值大于 0 时，才会选取对应子节点；
节点的最大路径和取决于该节点的值与该节点的左右子节点的最大贡献值；每次递归返回该节点的最大贡献值。

```java
class Solution {
    private int maxSum = Integer.MIN_VALUE;
    
    public int maxPathSum(TreeNode root) {
        maxGain(root);
        return maxSum;
    }
    
    private int maxGain(TreeNode node) {
        if (node == null) {
            return 0;
        }
        // 递归计算左右子节点的最大贡献值
        // 只有在最大贡献值大于 0 时，才会选取对应子节点
        int leftGain = Math.max(maxGain(node.left), 0);
        int rightGain = Math.max(maxGain(node.right), 0);
        // 节点的最大路径和取决于该节点的值与该节点的左右子节点的最大贡献值
        int curMaxSum = node.val + leftGain + rightGain;
        // 更新最大路径和
        maxSum = Math.max(maxSum, curMaxSum);
        // 返回节点的最大贡献值
        return node.val + Math.max(leftGain, rightGain);
    }
}
```

#### lowest-common-ancestor-of-a-binary-tree

[lowest-common-ancestor-of-a-binary-tree](https://leetcode-cn.com/problems/lowest-common-ancestor-of-a-binary-tree/)

> 给定一个二叉树, 找到该树中两个指定节点的最近公共祖先。

思路：分治法，有左子树的公共祖先或者有右子树的公共祖先，就返回子树的祖先，否则返回根节点

```java
class Solution {
    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        if (root == null || root == p || root == q) {
            return root;
        }
        TreeNode left = lowestCommonAncestor(root.left, p, q);
        TreeNode right = lowestCommonAncestor(root.right, p, q);
        return left == null ? right : right == null ? left : root;
    }
}
```

### BFS 层次应用

#### binary-tree-level-order-traversal

[binary-tree-level-order-traversal](https://leetcode-cn.com/problems/binary-tree-level-order-traversal/)

> 给你一个二叉树，请你返回其按  **层序遍历**  得到的节点值。 （即逐层地，从左到右访问所有节点）

思路：用一个队列记录一层的元素，然后扫描这一层元素添加下一层元素到队列（一个数进去出来一次，所以复杂度 O(logN)）

```java
import java.util.Queue;
class Solution {
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> lists = new ArrayList<>();
        if (root == null) {
            return lists;
        }
        Queue<TreeNode> queue = new LinkedList<TreeNode>();
        queue.offer(root);
        while (!queue.isEmpty()) {
            int size = queue.size();
            List<Integer> list = new ArrayList<>();
            for (int i = 0; i < size; i++) {
                TreeNode node = queue.poll();
                list.add(node.val);
                if (node.left != null) {
                    queue.add(node.left);
                }
                if (node.right != null) {
                    queue.add(node.right);
                }
            }
            lists.add(list);
        }
        return lists;
    }
}
```

#### binary-tree-level-order-traversal-ii

[binary-tree-level-order-traversal-ii](https://leetcode-cn.com/problems/binary-tree-level-order-traversal-ii/)

> 给定一个二叉树，返回其节点值自底向上的层次遍历。 （即按从叶子节点所在层到根节点所在的层，逐层从左向右遍历）

思路：在层级遍历的基础上，翻转一下结果即可，这里利用LinkedList的性质，每次插入到首部，就相当于翻转了

```java
class Solution {
    public List<List<Integer>> levelOrderBottom(TreeNode root) {
        List<List<Integer>> lists = new LinkedList<>();
        if (root == null) {
            return lists;
        }
        Queue<TreeNode> queue = new LinkedList<TreeNode>();
        queue.offer(root);
        while (!queue.isEmpty()) {
            int size = queue.size();
            List<Integer> list = new ArrayList<>();
            for (int i = 0; i < size; i++) {
                TreeNode node = queue.poll();
                list.add(node.val);
                if (node.left != null) {
                    queue.add(node.left);
                }
                if (node.right != null) {
                    queue.add(node.right);
                }
            }
            // 每次插入到首部，就相当于翻转了
            lists.add(0, list);
        }
        return lists;
    }
}
```

#### binary-tree-zigzag-level-order-traversal

[binary-tree-zigzag-level-order-traversal](https://leetcode-cn.com/problems/binary-tree-zigzag-level-order-traversal/)

> 给定一个二叉树，返回其节点值的锯齿形层次遍历。Z 字形遍历

```java
class Solution {
    public List<List<Integer>> zigzagLevelOrder(TreeNode root) {
        List<List<Integer>> lists = new ArrayList<>();
        if (root == null) {
            return lists;
        }
        Queue<TreeNode> queue = new LinkedList<TreeNode>();
        queue.offer(root);
        boolean flag = true;
        while (!queue.isEmpty()) {
            int size = queue.size();
            List<Integer> list = new LinkedList<>();
            for (int i = 0; i < size; i++) {
                TreeNode node = queue.poll();
                if (!flag) {
                    // flag 为false, 需要从右往左遍历，这里直接插入首部，实现翻转的效果。也可以再插入完一层后，直接reverse()
                    list.add(0, node.val);
                } else {
                    list.add(node.val);
                }         
                if (node.left != null) {
                    queue.add(node.left);
                }
                if (node.right != null) {
                    queue.add(node.right);
                }
            }
            if (!flag) {
                flag = true;
            } else {
                flag = false;
            }
            lists.add(list);
        }
        return lists;
    }
}
```

### 二叉搜索树应用

#### validate-binary-search-tree

[validate-binary-search-tree](https://leetcode-cn.com/problems/validate-binary-search-tree/)

> 给定一个二叉树，判断其是否是一个有效的二叉搜索树。

思路 1：中序遍历，如果中序遍历得到的节点的值小于等于前一个 preVal，说明不是二叉搜索树

思路 2：递归法，判断左 MAX < 根 < 右 MIN
##### 中序遍历
```java
class Solution {
    public boolean isValidBST(TreeNode root) {
        Deque<TreeNode> stack = new LinkedList<>();
        double preVal = - Double.MAX_VALUE;
        while (!stack.isEmpty() || root != null) {
            while (root != null) {
                stack.offerFirst(root);
                root = root.left;
            }
            root = stack.pollFirst();
            // 如果中序遍历得到的节点的值小于等于前一个 preVal，说明不是二叉搜索树
            if (root.val <= preVal) {
                return false;
            }
            preVal = root.val;
            root = root.right;
        }
        return true;
    }
}
```

##### 递归

```java
// 递归
class Solution {
    private boolean helper (TreeNode node, Integer lower, Integer upper) {
        if (node == null) {
            return true;
        }
        int val = node.val;
        if ((lower != null && val <= lower) || (upper != null && val >= upper)) {
            return false;
        }
        return helper(node.right, val, upper) && helper(node.left, lower, val);
    }
    public boolean isValidBST(TreeNode root) {
        return helper(root, null, null);
    }
}
```

#### insert-into-a-binary-search-tree

[insert-into-a-binary-search-tree](https://leetcode-cn.com/problems/insert-into-a-binary-search-tree/)

> 给定二叉搜索树（BST）的根节点和要插入树中的值，将值插入二叉搜索树。 返回插入后二叉搜索树的根节点。

思路：找到最后一个叶子节点满足插入条件即可

```java
// DFS查找插入位置
class Solution {
    public TreeNode insertIntoBST(TreeNode root, int val) {
        if (root == null) {
            return new TreeNode(val);
        }
        if (root.val < val) {
            root.right = insertIntoBST(root.right, val);
        } else {
            root.left = insertIntoBST(root.left, val);
        }
        return root;
    }
}
```

## 总结

- 掌握二叉树递归与非递归遍历
- 理解 DFS 前序遍历与分治法
- 理解 BFS 层次遍历

## 练习

- [ ] [maximum-depth-of-binary-tree](https://leetcode-cn.com/problems/maximum-depth-of-binary-tree/)
- [ ] [balanced-binary-tree](https://leetcode-cn.com/problems/balanced-binary-tree/)
- [ ] [binary-tree-maximum-path-sum](https://leetcode-cn.com/problems/binary-tree-maximum-path-sum/)
- [ ] [lowest-common-ancestor-of-a-binary-tree](https://leetcode-cn.com/problems/lowest-common-ancestor-of-a-binary-tree/)
- [ ] [binary-tree-level-order-traversal](https://leetcode-cn.com/problems/binary-tree-level-order-traversal/)
- [ ] [binary-tree-level-order-traversal-ii](https://leetcode-cn.com/problems/binary-tree-level-order-traversal-ii/)
- [ ] [binary-tree-zigzag-level-order-traversal](https://leetcode-cn.com/problems/binary-tree-zigzag-level-order-traversal/)
- [ ] [validate-binary-search-tree](https://leetcode-cn.com/problems/validate-binary-search-tree/)
- [ ] [insert-into-a-binary-search-tree](https://leetcode-cn.com/problems/insert-into-a-binary-search-tree/)
