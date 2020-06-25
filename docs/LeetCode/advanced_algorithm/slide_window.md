# 滑动窗口

## 模板

```java
/* 滑动窗口算法框架 */
class Solution {
    void slidingWindow(string s, string t) {
        HashMap<Character, Integer> need, window;
        for (char c : t) {
            need.put(c, need.getOrDefault(c, 0) + 1);
        }
        int left = 0, right = 0;
        int valid = 0;
        while (right < s.size()) {
            // c 是将移入窗口的字符
            char c = s.charAt(right);
            // 右移窗口
            right++;
            // 进行窗口内数据的一系列更新
            ...
    
            /*** debug 输出的位置 ***/
            System.out.print("window: [%d, %d)\n", left, right);
            /********************/
    
            // 判断左侧窗口是否要收缩
            while (window needs shrink) {
                // d 是将移出窗口的字符
                char d = s.charAt(left);
                // 左移窗口
                left++;
                // 进行窗口内数据的一系列更新
                ...
            }
        }
    }
}
```

需要变化的地方

- 1、右指针右移之后窗口数据更新
- 2、判断窗口是否要收缩
- 3、左指针右移之后窗口数据更新
- 4、根据题意计算结果

## 示例

[minimum-window-substring](https://leetcode-cn.com/problems/minimum-window-substring/)

> 给你一个字符串 S、一个字符串 T，请在字符串 S 里面找出：包含 T 所有字母的最小子串

```java
class Solution {
    public String minWindow(String s, String t) {
        int start = 0, minLen = Integer.MAX_VALUE;
        int left = 0, right = 0, match = 0;
        // needs存储t的<字符,出现次数>,windows存储<s中与t中字符相同的字符,出现次数>
        HashMap<Character, Integer> needs = new HashMap<>();
        HashMap<Character, Integer> windows = new HashMap<>();
        int sLength = s.length();
        // 初始化needs
        for (char c : t.toCharArray()) {
            needs.put(c, needs.getOrDefault(c, 0) + 1);
        }
        while (right < sLength) {
            // 获取字符
            char temp = s.charAt(right);
            // 如果是t中字符，在windows里添加，累计出现次数
            if (needs.containsKey(temp)) {
                windows.put(temp, windows.getOrDefault(temp,0) + 1);
                // 注意：Integer不能用==比较，要用compareTo
                if (windows.get(temp).compareTo(needs.get(temp)) == 0 ) {
                    // 字符temp出现次数符合要求，match代表符合要求的字符个数
                    match++;
                }
            }
            // 优化到不满足情况，right继续前进找可行解
            right++;
            // 符合要求的字符个数正好是t中所有字符，获得一个可行解
            while (match == needs.size()) {
                // 更新结果
                if (right - left < minLen) {
                    start = left;
                    minLen = right - left;
                }
                // 开始进行优化，即缩小区间，删除s[left],
                char c = s.charAt(left);
                // 当前删除的字符包含于t,更新Windows中对应出现的次数，如果更新后的次数<t中出现的次数，符合要求的字符数减1，下次判断match==needs.size()时不满足情况，
                if (needs.containsKey(c)) {
                    windows.put(c, windows.getOrDefault(c, 1) - 1);
                    if (windows.get(c) < needs.get(c)){
                        match--;
                    }
                }
                left++;
            }
        }
        // 返回覆盖的最小串
        return minLen == Integer.MAX_VALUE ? "" : s.substring(start, minLen + start);
    }
}
```
更快的版本
```java
class Solution {
    public String minWindow(String s, String t) {
        if (s == null || t == null || s.length() == 0 || t.length() == 0) return "";
        // 定义一个数字，用来记录字符串 t 中出现字符的频率，也就是窗口内需要匹配的字符和相应的频率
        int[] map = new int[128];
        for (char c : t.toCharArray()) {
            map[c]++;
        }
        int left = 0, right = 0;
        int match = 0;  // 匹配字符的个数
        int minLen = s.length() + 1;   // 最大的子串的长度
        // 子串的起始位置 子串结束的位置(如果不存在这样的子串的话，start，end 都是 0，s.substring 截取就是 “”
        int start = 0, end = 0;
        int slength = s.length();
        int tlength = t.length();
        while (right < slength){
            char charRight = s.charAt(right); // 右边界的那个字符
            map[charRight]--;   // 可以理解为需要匹配的字符 charRight 减少了一个
            // 如果字符 charRight 在 t 中存在，那么经过这一次操作，只要个数大于等于 0，说明匹配了一个
            // 若字符 charRight 不在 t 中，那么 map[charRight] < 0, 不进行任何操作
            if (map[charRight] >= 0) match++;
            right++;  // 右边界右移，这样下面就变成了 [)，方便计算窗口大小

            // 只要窗口内匹配的字符达到了要求，右边界固定，左边界收缩
            while (match == tlength){
                int size = right - left;
                if (size < minLen){
                    minLen = size;
                    start = left;
                    end = right;
                }
                char charLeft = s.charAt(left);  // 左边的那个字符
                map[charLeft]++;  // 左边的字符要移出窗口
                // 不在 t 中出现的字符，移出窗口，最终能够达到的最大值 map[charLeft] = 0
                // 如果恰好移出了需要匹配的一个字符，那么这里 map[charLeft] > 0, 也就是还要匹配字符 charLeft，此时 match--
                if (map[charLeft] > 0) match--;
                left++;  // 左边界收缩
            }
        }
        return s.substring(start, end);
    }
}
```
[permutation-in-string](https://leetcode-cn.com/problems/permutation-in-string/)

> 给定两个字符串  **s1**  和  **s2**，写一个函数来判断  **s2**  是否包含  **s1 **的排列。



```java
public class Solution {
    public boolean checkInclusion(String s1, String s2) {
        if (s1.length() > s2.length())
            return false;
        int[] s1map = new int[26];
        int[] s2map = new int[26];
        for (int i = 0; i < s1.length(); i++) {
            s1map[s1.charAt(i) - 'a']++;
            s2map[s2.charAt(i) - 'a']++;
        }
        int count = 0;
        for (int i = 0; i < 26; i++)
            if (s1map[i] == s2map[i])
                count++;
        for (int i = 0; i < s2.length() - s1.length(); i++) {
            int r = s2.charAt(i + s1.length()) - 'a', l = s2.charAt(i) - 'a';
            if (count == 26)
                return true;
            s2map[r]++;
            if (s2map[r] == s1map[r])
                count++;
            else if (s2map[r] == s1map[r] + 1)
                count--;
            s2map[l]--;
            if (s2map[l] == s1map[l])
                count++;
            else if (s2map[l] == s1map[l] - 1)
                count--;
        }
        return count == 26;
    }
}
```

[find-all-anagrams-in-a-string](https://leetcode-cn.com/problems/find-all-anagrams-in-a-string/)

> 给定一个字符串  **s **和一个非空字符串  **p**，找到  **s **中所有是  **p **的字母异位词的子串，返回这些子串的起始索引。

```java
class Solution {
    public List<Integer> findAnagrams(String s, String p) {
        char[] arrS = s.toCharArray();
        char[] arrP = p.toCharArray();
        
        // 接收最后返回的结果
        List<Integer> ans = new ArrayList<>();
        
        // 定义一个 needs 数组来看 arrP 中包含元素的个数
        int[] needs = new int[26];
        // 定义一个 window 数组来看滑动窗口中是否有 arrP 中的元素，并记录出现的个数
        int[] window = new int[26]; 
        
        // 先将 arrP 中的元素保存到 needs 数组中
        for (int i = 0; i < arrP.length; i++) {
            needs[arrP[i] - 'a'] += 1;
        }
        
        // 定义滑动窗口的两端
        int left = 0;
        int right = 0;
        
        // 右窗口开始不断向右移动
        while (right < arrS.length) {
            int curR = arrS[right] - 'a';
            right++;
            // 将右窗口当前访问到的元素 curR 个数加 1 
            window[curR] += 1;
            
            // 当 window 数组中 curR 比 needs 数组中对应元素的个数要多的时候就该移动左窗口指针 
            while (window[curR] > needs[curR]) {
                int curL = arrS[left] - 'a';
                left++;
                // 将左窗口当前访问到的元素 curL 个数减 1 
                window[curL] -= 1;            
            }
            
            // 这里将所有符合要求的左窗口索引放入到了接收结果的 List 中
            if (right - left == arrP.length) {
                ans.add(left);
            }
        }
        return ans;
    }
}
```

[longest-substring-without-repeating-characters](https://leetcode-cn.com/problems/longest-substring-without-repeating-characters/)

> 给定一个字符串，请你找出其中不含有重复字符的   最长子串   的长度。
> 示例  1:
>
> 输入: "abcabcbb"
> 输出: 3
> 解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。

```java
class Solution {
    public int lengthOfLongestSubstring(String s) {
        // 哈希集合，记录每个字符是否出现过
        Set<Character> occ = new HashSet<Character>();
        int n = s.length();
        // 右指针，初始值为 -1，相当于我们在字符串的左边界的左侧，还没有开始移动
        int rk = -1, ans = 0;
        for (int i = 0; i < n; ++i) {
            if (i != 0) {
                // 左指针向右移动一格，移除一个字符
                occ.remove(s.charAt(i - 1));
            }
            while (rk + 1 < n && !occ.contains(s.charAt(rk + 1))) {
                // 不断地移动右指针
                occ.add(s.charAt(rk + 1));
                ++rk;
            }
            // 第 i 到 rk 个字符是一个极长的无重复字符子串
            ans = Math.max(ans, rk - i + 1);
        }
        return ans;
    }
}
```

## 总结

- 和双指针题目类似，更像双指针的升级版，滑动窗口核心点是维护一个窗口集，根据窗口集来进行处理
- 核心步骤
  - right 右移
  - 收缩
  - left 右移
  - 求结果

## 练习

- [ ] [minimum-window-substring](https://leetcode-cn.com/problems/minimum-window-substring/)
- [ ] [permutation-in-string](https://leetcode-cn.com/problems/permutation-in-string/)
- [ ] [find-all-anagrams-in-a-string](https://leetcode-cn.com/problems/find-all-anagrams-in-a-string/)
- [ ] [longest-substring-without-repeating-characters](https://leetcode-cn.com/problems/longest-substring-without-repeating-characters/)
