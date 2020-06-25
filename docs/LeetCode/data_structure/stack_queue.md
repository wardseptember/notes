# 栈和队列

## 简介

栈的特点是后入先出

![image.png](https://img.fuiboom.com/img/stack.png)

根据这个特点可以临时保存一些数据，之后用到依次再弹出来，常用于 DFS 深度搜索

队列一般常用于 BFS 广度搜索，类似一层一层的搜索

## Stack 栈

[min-stack](https://leetcode-cn.com/problems/min-stack/)

> 设计一个支持 push，pop，top 操作，并能在常数时间内检索到最小元素的栈。

思路：用两个栈实现，一个最小栈始终保证最小值在顶部

```java
class MinStack {
    
    private Deque<Integer> stack;
    private Deque<Integer> minStack;
    private int min;

    /** initialize your data structure here. */
    public MinStack() {
        stack = new LinkedList<>();
        minStack = new LinkedList<>();
        min = Integer.MAX_VALUE;
    }
        
    public void push(int x) {
        stack.offerFirst(x);
        min = Math.min(min, x);
        minStack.offerFirst(min);
    }
    
    public void pop() {
        stack.pollFirst();
        minStack.pollFirst();
        min = minStack.isEmpty() ? Integer.MAX_VALUE : minStack.peekFirst();
    }
    
    public int top() {
        return stack.peekFirst();
    }
    
    public int getMin() {
        return minStack.peekFirst();
    }
}

/**
 * Your MinStack object will be instantiated and called as such:
 * MinStack obj = new MinStack();
 * obj.push(x);
 * obj.pop();
 * int param_3 = obj.top();
 * int param_4 = obj.getMin();
 */
```

[evaluate-reverse-polish-notation](https://leetcode-cn.com/problems/evaluate-reverse-polish-notation/)

> **波兰表达式计算** > **输入:** ["2", "1", "+", "3", "*"] > **输出:** 9
> **解释:** ((2 + 1) \* 3) = 9

思路：用数组保存原来的元素，遇到+-*/取出运算，再存入结果，重复这个过程

```java
class Solution {
    public int evalRPN(String[] tokens) {
        int[] nums = new int[tokens.length / 2 + 1];
        int index = 0;
        for (String s : tokens) {
            switch (s) {
                case "+": 
                    nums[index - 2] += nums[--index];
                    break;
                case "-": 
                    nums[index - 2] -= nums[--index];
                    break;
                case "*": 
                    nums[index - 2] *= nums[--index];
                    break;
                case "/": 
                    nums[index - 2] /= nums[--index];
                    break;
                default:
                    nums[index++] = Integer.parseInt(s);
                    break; 
            }
        }
        return nums[0];
    }
}
```

[decode-string](https://leetcode-cn.com/problems/decode-string/)

> 给定一个经过编码的字符串，返回它解码后的字符串。
> s = "3[a]2[bc]", 返回 "aaabcbc".
> s = "3[a2[c]]", 返回 "accaccacc".
> s = "2[abc]3[cd]ef", 返回 "abcabccdcdcdef".

思路：数字一个栈，字母一个栈，取出来计算就可以了。

```java
class Solution {
    public String decodeString(String s) {
        StringBuilder res = new StringBuilder();
        int multi = 0;
        LinkedList<Integer> stackMulti = new LinkedList<>();
        LinkedList<StringBuilder> stackRes = new LinkedList<>();
        for (char c : s.toCharArray()) {
            if (c == '[') {
                stackMulti.addLast(multi);
                stackRes.addLast(res);
                multi = 0;
                res = new StringBuilder();
            } else if (c == ']') {
                StringBuilder tmp = stackRes.removeLast();
                int curMulti = stackMulti.removeLast();
                for (int i = 0; i < curMulti; ++i) {
                    tmp.append(res);
                }
                res = tmp;
            } else if (c >= '0' && c <= '9') {
                multi = multi * 10 + Integer.parseInt(c + "");
            } else {
                res.append(c);
            }
        }
        return res.toString();
    }
}
```

利用栈进行 BFS 非递归搜索模板

```
// 伪代码
public class Solution 
    boolean BFS(Node root, int target) {
        Set<Node> visited;
        Stack<Node> s;
        add root to s;
        while (s is not empty) {
            Node cur = the top element in s;
            return true if cur is target;
            for (Node next : the neighbors of cur) {
                if (next is not in visited) {
                    add next to s;
                    add next to visited;
                }
            }
            remove cur from s;
        }
        return false;
    }
}
```

[binary-tree-inorder-traversal](https://leetcode-cn.com/problems/binary-tree-inorder-traversal/)

> 给定一个二叉树，返回它的*中序*遍历。

```java
// 思路：通过stack 保存已经访问的元素，用于原路返回
class Solution {
    public List<Integer> inorderTraversal(TreeNode root) {
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

[clone-graph](https://leetcode-cn.com/problems/clone-graph/)

> 给你无向连通图中一个节点的引用，请你返回该图的深拷贝（克隆）。

```java
/*
// Definition for a Node.
class Node {
    public int val;
    public List<Node> neighbors;
    
    public Node() {
        val = 0;
        neighbors = new ArrayList<Node>();
    }
    
    public Node(int _val) {
        val = _val;
        neighbors = new ArrayList<Node>();
    }
    
    public Node(int _val, ArrayList<Node> _neighbors) {
        val = _val;
        neighbors = _neighbors;
    }
}
*/

class Solution {
    HashMap<Node, Node> visited = new HashMap<>();
    public Node cloneGraph(Node node) {
        if (node == null) {
            return node;
        }
        // 如果visited存在node的克隆结点则返回克隆结点
        if (visited.containsKey(node)) {
            return visited.get(node);
        }
        Node cloneNode = new Node(node.val, new ArrayList());
        visited.put(node, cloneNode);
        // 设置好cloneNode结点的克隆结点
        for (Node neighbor : node.neighbors) {
            // 递归node邻居结点的克隆结点
            cloneNode.neighbors.add(cloneGraph(neighbor));
        }
        return cloneNode;
    }
}
```

[number-of-islands](https://leetcode-cn.com/problems/number-of-islands/)

> 给定一个由  '1'（陆地）和 '0'（水）组成的的二维网格，计算岛屿的数量。一个岛被水包围，并且它是通过水平方向或垂直方向上相邻的陆地连接而成的。你可以假设网格的四个边均被水包围。

思路：通过深度搜索遍历可能性（注意标记已访问元素）

```java
class Solution {
    int[][] move = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
    private int dfs(char[][] grid, boolean[][] visited, int x, int y, int count){
        if(x < 0 || x >= grid.length || y < 0 || y >= grid[0].length || grid[x][y] != '1' || visited[x][y])
            return count;
        visited[x][y] = true;
        for(int i = 0; i < move.length; ++i){
            count = dfs(grid, visited, x + move[i][0], y + move[i][1], count);
        }
        return count+1;
    }
    public int numIslands(char[][] grid) {
        if(grid.length == 0)
            return 0;
        int total = 0, row = grid.length, col = grid[0].length;
        boolean[][] visited = new boolean[row][col];
        int count = 0;
        for(int i = 0; i < row; ++i){
            for(int j = 0; j < col; ++j){
                if(grid[i][j] == '1'){
                    count = dfs(grid, visited, i, j, 0);
                    if(count >= 1){
                        total++;
                    }
                }
            }
        }
        return total;
    }
}
```

[largest-rectangle-in-histogram](https://leetcode-cn.com/problems/largest-rectangle-in-histogram/)

> 给定 _n_ 个非负整数，用来表示柱状图中各个柱子的高度。每个柱子彼此相邻，且宽度为 1 。
> 求在该柱状图中，能够勾勒出来的矩形的最大面积。

详解见[https://leetcode-cn.com/problems/largest-rectangle-in-histogram/solution/zhu-zhuang-tu-zhong-zui-da-de-ju-xing-by-leetcode-/](https://leetcode-cn.com/problems/largest-rectangle-in-histogram/solution/zhu-zhuang-tu-zhong-zui-da-de-ju-xing-by-leetcode-/)

```java
class Solution {
    public int largestRectangleArea(int[] heights) {
        int len = heights.length;
        if (len == 0) {
            return 0;
        }
        if (len == 1) {
            return heights[0];
        }
        int[] newHeights = new int[len + 2];
        for (int i = 0; i < len; ++i) {
            newHeights[i + 1] = heights[i];
        }
        int maxArea = 0;
        len += 2;
        heights = newHeights;
        Deque<Integer> stack = new LinkedList<>();
        stack.addFirst(0);
        for (int i = 1; i < len; ++i) {
            while (heights[stack.peekFirst()] > heights[i]) {
                int height = heights[stack.removeFirst()];
                int width = i - stack.peekFirst() - 1;
                maxArea = Math.max(maxArea, height * width);
            }
            stack.addFirst(i);
        }
        return maxArea;
    }
}
```

## Queue 队列

常用于 BFS 宽度优先搜索

[implement-queue-using-stacks](https://leetcode-cn.com/problems/implement-queue-using-stacks/)

> 使用栈实现队列

```java
class MyQueue {

    /** Initialize your data structure here. */
    public MyQueue() {
        
    }
    
    private Deque<Integer> in = new LinkedList<>();
    private Deque<Integer> out = new LinkedList<>();
    
    /** Push element x to the back of queue. */
    public void push(int x) {
        in.addFirst(x);
    }
    
    /** Removes the element from in front of queue and returns that element. */
    public int pop() {
        in2out();
        return out.removeFirst();
    }
    
    /** Get the front element. */
    public int peek() {
        in2out();
        return out.peekFirst();
    }
    
    /** Returns whether the queue is empty. */
    public boolean empty() {
        return out.isEmpty() && in.isEmpty();
    }
    
    private void in2out() {
        if (out.isEmpty()) {
            while(!in.isEmpty()) {
                out.addFirst(in.removeFirst());
            }
        }
    }
}

/**
 * Your MyQueue object will be instantiated and called as such:
 * MyQueue obj = new MyQueue();
 * obj.push(x);
 * int param_2 = obj.pop();
 * int param_3 = obj.peek();
 * boolean param_4 = obj.empty();
 */
```

[二叉树层次遍历](https://leetcode-cn.com/problems/binary-tree-level-order-traversal/)


```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */
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
            // 将这一层的节点存起来
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

[01-matrix](https://leetcode-cn.com/problems/01-matrix/)

> 给定一个由 0 和 1 组成的矩阵，找出每个元素到最近的 0 的距离。
> 两个相邻元素间的距离为 1


```java
class Solution {
    public int[][] updateMatrix(int[][] matrix) {
        int row = matrix.length, col = matrix[0].length;
        int[][] dist = new int[row][col];
        int MAX_TEMP = Integer.MAX_VALUE / 2;
        // 如果 (i, j) 的元素为 0，那么距离为 0，否则设置成一个很大的数
        for (int i = 0; i < row; ++i) {
            for (int j = 0; j < col; ++j) {
                if (matrix[i][j] == 0) {
                    dist[i][j] = 0;
                } else {
                    dist[i][j] = MAX_TEMP;
                }
            }
        }
        // 水平向左移动 和 竖直向上移动
        for (int i = 0; i < row; ++i) {
            for (int j = 0; j < col; ++j) {
                if (i - 1 >= 0) {
                    dist[i][j] = Math.min(dist[i][j], dist[i - 1][j] + 1);
                }
                if (j - 1 >= 0) {
                    dist[i][j] = Math.min(dist[i][j], dist[i][j - 1] + 1);
                }
            }
        }
        // 水平向右移动 和 竖直向下移动
        for (int i = row - 1; i >= 0; --i) {
            for (int j = col - 1; j >= 0; --j) {
                if (i + 1 < row) {
                    dist[i][j] = Math.min(dist[i][j], dist[i + 1][j] + 1);
                }
                if (j + 1 < col) {
                    dist[i][j] = Math.min(dist[i][j], dist[i][j + 1] + 1);
                }
            }
        }
        return dist;
    }
}
```

## 总结

- 熟悉栈的使用场景
  - 后出先出，保存临时值
  - 利用栈 DFS 深度搜索
- 熟悉队列的使用场景
  - 利用队列 BFS 广度搜索

## 练习

- [ ] [min-stack](https://leetcode-cn.com/problems/min-stack/)
- [ ] [evaluate-reverse-polish-notation](https://leetcode-cn.com/problems/evaluate-reverse-polish-notation/)
- [ ] [decode-string](https://leetcode-cn.com/problems/decode-string/)
- [ ] [binary-tree-inorder-traversal](https://leetcode-cn.com/problems/binary-tree-inorder-traversal/)
- [ ] [clone-graph](https://leetcode-cn.com/problems/clone-graph/)
- [ ] [number-of-islands](https://leetcode-cn.com/problems/number-of-islands/)
- [ ] [largest-rectangle-in-histogram](https://leetcode-cn.com/problems/largest-rectangle-in-histogram/)
- [ ] [implement-queue-using-stacks](https://leetcode-cn.com/problems/implement-queue-using-stacks/)
- [ ] [01-matrix](https://leetcode-cn.com/problems/01-matrix/)
