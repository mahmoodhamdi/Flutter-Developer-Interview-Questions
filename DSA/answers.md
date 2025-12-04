# DSA (Data Structures & Algorithms): Answers

## Arrays and Lists

**1. What is the difference between List and Array in Dart? How do you create a fixed-length list?**

In Dart, there's no separate Array type - `List` is the primary collection for ordered elements. Lists can be growable (default) or fixed-length.

```dart
// Growable list (default)
var growable = <int>[];
growable.add(1); // Works

// Fixed-length list
var fixed = List<int>.filled(5, 0); // Creates [0, 0, 0, 0, 0]
// fixed.add(1); // Error: Cannot add to a fixed-length list

// Fixed-length from existing list
var fixedCopy = List<int>.of([1, 2, 3], growable: false);
```

**Time Complexity**: Access O(1), Fixed-length creation O(n)

---

**2. How do you reverse a list in-place in Dart without using built-in methods?**

```dart
void reverseInPlace<T>(List<T> list) {
  int left = 0;
  int right = list.length - 1;

  while (left < right) {
    // Swap elements
    T temp = list[left];
    list[left] = list[right];
    list[right] = temp;

    left++;
    right--;
  }
}

// Usage
var numbers = [1, 2, 3, 4, 5];
reverseInPlace(numbers);
print(numbers); // [5, 4, 3, 2, 1]
```

**Time Complexity**: O(n/2) = O(n)
**Space Complexity**: O(1)

---

**3. What is the time complexity of adding an element to the end of a Dart List? What about inserting at the beginning?**

- **Adding to end (`add()`)**: O(1) amortized - Dart uses a dynamic array that doubles capacity when needed
- **Inserting at beginning (`insert(0, element)`)**: O(n) - all elements must shift right

```dart
var list = [1, 2, 3];

// O(1) amortized
list.add(4);

// O(n) - shifts all elements
list.insert(0, 0); // [0, 1, 2, 3, 4]
```

---

**4. How would you find the maximum subarray sum (Kadane's Algorithm) in Dart?**

Kadane's Algorithm finds the contiguous subarray with the maximum sum in O(n) time.

```dart
int maxSubarraySum(List<int> nums) {
  if (nums.isEmpty) return 0;

  int maxSoFar = nums[0];
  int maxEndingHere = nums[0];

  for (int i = 1; i < nums.length; i++) {
    // Either extend the previous subarray or start new
    maxEndingHere = max(nums[i], maxEndingHere + nums[i]);
    maxSoFar = max(maxSoFar, maxEndingHere);
  }

  return maxSoFar;
}

int max(int a, int b) => a > b ? a : b;

// Usage
print(maxSubarraySum([-2, 1, -3, 4, -1, 2, 1, -5, 4])); // 6 (subarray [4, -1, 2, 1])
```

**Time Complexity**: O(n)
**Space Complexity**: O(1)

---

**5. Implement a function to rotate an array by k positions to the right.**

```dart
void rotateRight(List<int> nums, int k) {
  if (nums.isEmpty) return;

  k = k % nums.length; // Handle k > length
  if (k == 0) return;

  // Reverse entire array, then reverse first k, then reverse rest
  reverse(nums, 0, nums.length - 1);
  reverse(nums, 0, k - 1);
  reverse(nums, k, nums.length - 1);
}

void reverse(List<int> nums, int start, int end) {
  while (start < end) {
    int temp = nums[start];
    nums[start] = nums[end];
    nums[end] = temp;
    start++;
    end--;
  }
}

// Usage
var arr = [1, 2, 3, 4, 5, 6, 7];
rotateRight(arr, 3);
print(arr); // [5, 6, 7, 1, 2, 3, 4]
```

**Time Complexity**: O(n)
**Space Complexity**: O(1)

---

**6. How do you remove duplicates from a sorted list in O(n) time?**

```dart
int removeDuplicates(List<int> nums) {
  if (nums.isEmpty) return 0;

  int writeIndex = 1;

  for (int i = 1; i < nums.length; i++) {
    if (nums[i] != nums[i - 1]) {
      nums[writeIndex] = nums[i];
      writeIndex++;
    }
  }

  return writeIndex; // New length
}

// Usage
var sorted = [1, 1, 2, 2, 2, 3, 4, 4, 5];
int newLength = removeDuplicates(sorted);
print(sorted.sublist(0, newLength)); // [1, 2, 3, 4, 5]
```

**Time Complexity**: O(n)
**Space Complexity**: O(1)

---

**7. Explain how to find two numbers in a list that sum to a target value (Two Sum problem).**

```dart
// Using HashMap - O(n) time, O(n) space
List<int> twoSum(List<int> nums, int target) {
  Map<int, int> seen = {};

  for (int i = 0; i < nums.length; i++) {
    int complement = target - nums[i];

    if (seen.containsKey(complement)) {
      return [seen[complement]!, i];
    }

    seen[nums[i]] = i;
  }

  return []; // No solution found
}

// Usage
print(twoSum([2, 7, 11, 15], 9)); // [0, 1] (2 + 7 = 9)
```

**Time Complexity**: O(n)
**Space Complexity**: O(n)

---

**8. How would you merge two sorted lists into one sorted list?**

```dart
List<int> mergeSorted(List<int> list1, List<int> list2) {
  List<int> result = [];
  int i = 0, j = 0;

  while (i < list1.length && j < list2.length) {
    if (list1[i] <= list2[j]) {
      result.add(list1[i]);
      i++;
    } else {
      result.add(list2[j]);
      j++;
    }
  }

  // Add remaining elements
  while (i < list1.length) {
    result.add(list1[i]);
    i++;
  }
  while (j < list2.length) {
    result.add(list2[j]);
    j++;
  }

  return result;
}

// Usage
print(mergeSorted([1, 3, 5], [2, 4, 6])); // [1, 2, 3, 4, 5, 6]
```

**Time Complexity**: O(n + m)
**Space Complexity**: O(n + m)

---

## Linked Lists

**9. Implement a singly linked list in Dart with insert, delete, and search operations.**

```dart
class Node<T> {
  T data;
  Node<T>? next;

  Node(this.data);
}

class LinkedList<T> {
  Node<T>? head;
  int _length = 0;

  int get length => _length;
  bool get isEmpty => head == null;

  // Insert at end - O(n)
  void append(T data) {
    final newNode = Node(data);
    if (head == null) {
      head = newNode;
    } else {
      var current = head;
      while (current!.next != null) {
        current = current.next;
      }
      current.next = newNode;
    }
    _length++;
  }

  // Insert at beginning - O(1)
  void prepend(T data) {
    final newNode = Node(data);
    newNode.next = head;
    head = newNode;
    _length++;
  }

  // Delete by value - O(n)
  bool delete(T data) {
    if (head == null) return false;

    if (head!.data == data) {
      head = head!.next;
      _length--;
      return true;
    }

    var current = head;
    while (current!.next != null) {
      if (current.next!.data == data) {
        current.next = current.next!.next;
        _length--;
        return true;
      }
      current = current.next;
    }
    return false;
  }

  // Search - O(n)
  bool contains(T data) {
    var current = head;
    while (current != null) {
      if (current.data == data) return true;
      current = current.next;
    }
    return false;
  }

  @override
  String toString() {
    var result = <T>[];
    var current = head;
    while (current != null) {
      result.add(current.data);
      current = current.next;
    }
    return result.toString();
  }
}

// Usage
var list = LinkedList<int>();
list.append(1);
list.append(2);
list.prepend(0);
print(list); // [0, 1, 2]
print(list.contains(1)); // true
list.delete(1);
print(list); // [0, 2]
```

---

**10. How do you detect a cycle in a linked list using Floyd's algorithm?**

Floyd's Cycle Detection (Tortoise and Hare) uses two pointers moving at different speeds.

```dart
bool hasCycle<T>(Node<T>? head) {
  if (head == null) return false;

  Node<T>? slow = head;
  Node<T>? fast = head;

  while (fast != null && fast.next != null) {
    slow = slow!.next;        // Move 1 step
    fast = fast.next!.next;   // Move 2 steps

    if (slow == fast) {
      return true; // Cycle detected
    }
  }

  return false; // No cycle
}
```

**Time Complexity**: O(n)
**Space Complexity**: O(1)

---

**11. Write a function to reverse a singly linked list both iteratively and recursively.**

```dart
// Iterative - O(n) time, O(1) space
Node<T>? reverseIterative<T>(Node<T>? head) {
  Node<T>? prev = null;
  Node<T>? current = head;

  while (current != null) {
    Node<T>? next = current.next;
    current.next = prev;
    prev = current;
    current = next;
  }

  return prev;
}

// Recursive - O(n) time, O(n) space (call stack)
Node<T>? reverseRecursive<T>(Node<T>? head) {
  if (head == null || head.next == null) {
    return head;
  }

  Node<T>? newHead = reverseRecursive(head.next);
  head.next!.next = head;
  head.next = null;

  return newHead;
}
```

---

**12. How do you find the middle element of a linked list in one pass?**

Use the slow/fast pointer technique:

```dart
Node<T>? findMiddle<T>(Node<T>? head) {
  if (head == null) return null;

  Node<T>? slow = head;
  Node<T>? fast = head;

  while (fast != null && fast.next != null) {
    slow = slow!.next;        // Move 1 step
    fast = fast.next!.next;   // Move 2 steps
  }

  return slow; // Middle element
}
```

**Time Complexity**: O(n)
**Space Complexity**: O(1)

---

**13. Implement a function to merge two sorted linked lists.**

```dart
Node<int>? mergeSortedLists(Node<int>? l1, Node<int>? l2) {
  // Dummy head to simplify logic
  Node<int> dummy = Node(0);
  Node<int> current = dummy;

  while (l1 != null && l2 != null) {
    if (l1.data <= l2.data) {
      current.next = l1;
      l1 = l1.next;
    } else {
      current.next = l2;
      l2 = l2.next;
    }
    current = current.next!;
  }

  // Attach remaining nodes
  current.next = l1 ?? l2;

  return dummy.next;
}
```

**Time Complexity**: O(n + m)
**Space Complexity**: O(1)

---

## Stacks and Queues

**14. Implement a Stack using a Dart List with push, pop, peek, and isEmpty operations.**

```dart
class Stack<T> {
  final List<T> _items = [];

  bool get isEmpty => _items.isEmpty;
  int get length => _items.length;

  // Push - O(1) amortized
  void push(T item) {
    _items.add(item);
  }

  // Pop - O(1)
  T pop() {
    if (isEmpty) throw StateError('Stack is empty');
    return _items.removeLast();
  }

  // Peek - O(1)
  T peek() {
    if (isEmpty) throw StateError('Stack is empty');
    return _items.last;
  }

  @override
  String toString() => _items.toString();
}

// Usage
var stack = Stack<int>();
stack.push(1);
stack.push(2);
stack.push(3);
print(stack.peek()); // 3
print(stack.pop());  // 3
print(stack);        // [1, 2]
```

---

**15. Implement a Queue using Dart collections. What are the time complexities?**

```dart
import 'dart:collection';

class Queue<T> {
  final _queue = ListQueue<T>();

  bool get isEmpty => _queue.isEmpty;
  int get length => _queue.length;

  // Enqueue - O(1)
  void enqueue(T item) {
    _queue.addLast(item);
  }

  // Dequeue - O(1)
  T dequeue() {
    if (isEmpty) throw StateError('Queue is empty');
    return _queue.removeFirst();
  }

  // Peek front - O(1)
  T peek() {
    if (isEmpty) throw StateError('Queue is empty');
    return _queue.first;
  }

  @override
  String toString() => _queue.toString();
}

// Usage
var queue = Queue<int>();
queue.enqueue(1);
queue.enqueue(2);
queue.enqueue(3);
print(queue.dequeue()); // 1
print(queue);           // (2, 3)
```

**Note**: Using `ListQueue` gives O(1) for both ends. Using `List` would give O(n) for `removeAt(0)`.

---

**16. How would you implement a Stack that supports getMin() in O(1) time?**

Use an auxiliary stack to track minimums:

```dart
class MinStack {
  final List<int> _stack = [];
  final List<int> _minStack = [];

  void push(int val) {
    _stack.add(val);
    if (_minStack.isEmpty || val <= _minStack.last) {
      _minStack.add(val);
    }
  }

  int pop() {
    int val = _stack.removeLast();
    if (val == _minStack.last) {
      _minStack.removeLast();
    }
    return val;
  }

  int top() => _stack.last;

  int getMin() => _minStack.last; // O(1)
}

// Usage
var minStack = MinStack();
minStack.push(3);
minStack.push(5);
minStack.push(2);
print(minStack.getMin()); // 2
minStack.pop();
print(minStack.getMin()); // 3
```

**Time Complexity**: All operations O(1)
**Space Complexity**: O(n)

---

**17. Explain how to check if parentheses are balanced using a stack.**

```dart
bool isBalanced(String s) {
  final stack = <String>[];
  final pairs = {')': '(', '}': '{', ']': '['};

  for (var char in s.split('')) {
    if ('({['.contains(char)) {
      stack.add(char);
    } else if (')}]'.contains(char)) {
      if (stack.isEmpty || stack.last != pairs[char]) {
        return false;
      }
      stack.removeLast();
    }
  }

  return stack.isEmpty;
}

// Usage
print(isBalanced('({[]})')); // true
print(isBalanced('({[}])'));  // false
print(isBalanced('((())'));   // false
```

**Time Complexity**: O(n)
**Space Complexity**: O(n)

---

**18. How do you implement a queue using two stacks?**

```dart
class QueueUsingStacks<T> {
  final List<T> _inbox = [];   // For enqueue
  final List<T> _outbox = [];  // For dequeue

  // Enqueue - O(1)
  void enqueue(T item) {
    _inbox.add(item);
  }

  // Dequeue - O(1) amortized
  T dequeue() {
    if (_outbox.isEmpty) {
      // Transfer all from inbox to outbox
      while (_inbox.isNotEmpty) {
        _outbox.add(_inbox.removeLast());
      }
    }
    if (_outbox.isEmpty) throw StateError('Queue is empty');
    return _outbox.removeLast();
  }

  bool get isEmpty => _inbox.isEmpty && _outbox.isEmpty;
}

// Usage
var queue = QueueUsingStacks<int>();
queue.enqueue(1);
queue.enqueue(2);
queue.enqueue(3);
print(queue.dequeue()); // 1
print(queue.dequeue()); // 2
```

**Time Complexity**: Enqueue O(1), Dequeue O(1) amortized

---

## Trees

**19. Implement a Binary Search Tree (BST) in Dart with insert and search operations.**

```dart
class TreeNode<T extends Comparable> {
  T value;
  TreeNode<T>? left;
  TreeNode<T>? right;

  TreeNode(this.value);
}

class BinarySearchTree<T extends Comparable> {
  TreeNode<T>? root;

  // Insert - O(log n) average, O(n) worst
  void insert(T value) {
    root = _insertRecursive(root, value);
  }

  TreeNode<T> _insertRecursive(TreeNode<T>? node, T value) {
    if (node == null) return TreeNode(value);

    if (value.compareTo(node.value) < 0) {
      node.left = _insertRecursive(node.left, value);
    } else if (value.compareTo(node.value) > 0) {
      node.right = _insertRecursive(node.right, value);
    }

    return node;
  }

  // Search - O(log n) average, O(n) worst
  bool contains(T value) {
    return _searchRecursive(root, value);
  }

  bool _searchRecursive(TreeNode<T>? node, T value) {
    if (node == null) return false;

    int cmp = value.compareTo(node.value);
    if (cmp == 0) return true;
    if (cmp < 0) return _searchRecursive(node.left, value);
    return _searchRecursive(node.right, value);
  }
}

// Usage
var bst = BinarySearchTree<int>();
bst.insert(5);
bst.insert(3);
bst.insert(7);
bst.insert(1);
print(bst.contains(3)); // true
print(bst.contains(4)); // false
```

---

**20. Write functions to perform in-order, pre-order, and post-order tree traversals.**

```dart
class TreeTraversals {
  // In-order: Left -> Root -> Right (sorted order for BST)
  static List<T> inOrder<T>(TreeNode<T>? node) {
    if (node == null) return [];
    return [
      ...inOrder(node.left),
      node.value,
      ...inOrder(node.right),
    ];
  }

  // Pre-order: Root -> Left -> Right (useful for copying tree)
  static List<T> preOrder<T>(TreeNode<T>? node) {
    if (node == null) return [];
    return [
      node.value,
      ...preOrder(node.left),
      ...preOrder(node.right),
    ];
  }

  // Post-order: Left -> Right -> Root (useful for deletion)
  static List<T> postOrder<T>(TreeNode<T>? node) {
    if (node == null) return [];
    return [
      ...postOrder(node.left),
      ...postOrder(node.right),
      node.value,
    ];
  }
}

// For tree:      5
//              /   \
//             3     7
//            / \
//           1   4

// In-order:   [1, 3, 4, 5, 7]
// Pre-order:  [5, 3, 1, 4, 7]
// Post-order: [1, 4, 3, 7, 5]
```

**Time Complexity**: O(n) for all traversals
**Space Complexity**: O(h) where h is height (O(log n) balanced, O(n) worst)

---

**21. How do you find the height of a binary tree?**

```dart
int height<T>(TreeNode<T>? node) {
  if (node == null) return 0;

  int leftHeight = height(node.left);
  int rightHeight = height(node.right);

  return 1 + (leftHeight > rightHeight ? leftHeight : rightHeight);
}

// Alternative: return -1 for null to get height as edges count
int heightAsEdges<T>(TreeNode<T>? node) {
  if (node == null) return -1;
  return 1 + max(heightAsEdges(node.left), heightAsEdges(node.right));
}
```

**Time Complexity**: O(n)
**Space Complexity**: O(h)

---

**22. Implement a function to check if a binary tree is balanced.**

A balanced tree has height difference of at most 1 for all subtrees.

```dart
bool isBalanced<T>(TreeNode<T>? node) {
  return checkHeight(node) != -1;
}

int checkHeight<T>(TreeNode<T>? node) {
  if (node == null) return 0;

  int leftHeight = checkHeight(node.left);
  if (leftHeight == -1) return -1; // Left subtree unbalanced

  int rightHeight = checkHeight(node.right);
  if (rightHeight == -1) return -1; // Right subtree unbalanced

  if ((leftHeight - rightHeight).abs() > 1) {
    return -1; // Current node unbalanced
  }

  return 1 + (leftHeight > rightHeight ? leftHeight : rightHeight);
}
```

**Time Complexity**: O(n)
**Space Complexity**: O(h)

---

**23. How do you find the lowest common ancestor (LCA) of two nodes in a BST?**

```dart
TreeNode<int>? lowestCommonAncestor(
  TreeNode<int>? root,
  int p,
  int q
) {
  if (root == null) return null;

  // If both p and q are smaller, LCA is in left subtree
  if (p < root.value && q < root.value) {
    return lowestCommonAncestor(root.left, p, q);
  }

  // If both p and q are larger, LCA is in right subtree
  if (p > root.value && q > root.value) {
    return lowestCommonAncestor(root.right, p, q);
  }

  // Otherwise, current node is the LCA
  return root;
}

// Iterative version
TreeNode<int>? lcaIterative(TreeNode<int>? root, int p, int q) {
  while (root != null) {
    if (p < root.value && q < root.value) {
      root = root.left;
    } else if (p > root.value && q > root.value) {
      root = root.right;
    } else {
      return root;
    }
  }
  return null;
}
```

**Time Complexity**: O(h)
**Space Complexity**: O(h) recursive, O(1) iterative

---

**24. Write a function to perform level-order traversal (BFS) of a binary tree.**

```dart
import 'dart:collection';

List<List<T>> levelOrder<T>(TreeNode<T>? root) {
  if (root == null) return [];

  List<List<T>> result = [];
  Queue<TreeNode<T>> queue = Queue();
  queue.add(root);

  while (queue.isNotEmpty) {
    int levelSize = queue.length;
    List<T> currentLevel = [];

    for (int i = 0; i < levelSize; i++) {
      TreeNode<T> node = queue.removeFirst();
      currentLevel.add(node.value);

      if (node.left != null) queue.add(node.left!);
      if (node.right != null) queue.add(node.right!);
    }

    result.add(currentLevel);
  }

  return result;
}

// For tree:      5
//              /   \
//             3     7
//            / \
//           1   4
// Result: [[5], [3, 7], [1, 4]]
```

**Time Complexity**: O(n)
**Space Complexity**: O(w) where w is maximum width

---

**25. How do you validate if a binary tree is a valid Binary Search Tree?**

```dart
bool isValidBST(TreeNode<int>? root) {
  return _validate(root, null, null);
}

bool _validate(TreeNode<int>? node, int? min, int? max) {
  if (node == null) return true;

  // Check current node value against bounds
  if (min != null && node.value <= min) return false;
  if (max != null && node.value >= max) return false;

  // Left subtree must be < current, right must be > current
  return _validate(node.left, min, node.value) &&
         _validate(node.right, node.value, max);
}

// Alternative using in-order traversal
bool isValidBSTInOrder(TreeNode<int>? root) {
  List<int> values = [];
  inOrderCollect(root, values);

  for (int i = 1; i < values.length; i++) {
    if (values[i] <= values[i - 1]) return false;
  }
  return true;
}

void inOrderCollect(TreeNode<int>? node, List<int> values) {
  if (node == null) return;
  inOrderCollect(node.left, values);
  values.add(node.value);
  inOrderCollect(node.right, values);
}
```

**Time Complexity**: O(n)
**Space Complexity**: O(h)

---

**26. Implement a function to find the maximum depth of a binary tree.**

```dart
int maxDepth<T>(TreeNode<T>? root) {
  if (root == null) return 0;

  return 1 + max(maxDepth(root.left), maxDepth(root.right));
}

int max(int a, int b) => a > b ? a : b;

// Iterative BFS approach
int maxDepthBFS<T>(TreeNode<T>? root) {
  if (root == null) return 0;

  Queue<TreeNode<T>> queue = Queue();
  queue.add(root);
  int depth = 0;

  while (queue.isNotEmpty) {
    int levelSize = queue.length;
    depth++;

    for (int i = 0; i < levelSize; i++) {
      TreeNode<T> node = queue.removeFirst();
      if (node.left != null) queue.add(node.left!);
      if (node.right != null) queue.add(node.right!);
    }
  }

  return depth;
}
```

---

## Graphs

**27. How do you represent a graph in Dart? Explain adjacency list and adjacency matrix.**

```dart
// Adjacency List - Space efficient for sparse graphs O(V + E)
class GraphAdjList {
  Map<int, List<int>> adjList = {};

  void addVertex(int v) {
    adjList.putIfAbsent(v, () => []);
  }

  void addEdge(int from, int to, {bool directed = false}) {
    adjList.putIfAbsent(from, () => []);
    adjList.putIfAbsent(to, () => []);
    adjList[from]!.add(to);
    if (!directed) {
      adjList[to]!.add(from);
    }
  }

  List<int> neighbors(int v) => adjList[v] ?? [];
}

// Adjacency Matrix - Space O(V²), good for dense graphs
class GraphAdjMatrix {
  late List<List<int>> matrix;
  int vertices;

  GraphAdjMatrix(this.vertices) {
    matrix = List.generate(vertices, (_) => List.filled(vertices, 0));
  }

  void addEdge(int from, int to, {bool directed = false, int weight = 1}) {
    matrix[from][to] = weight;
    if (!directed) {
      matrix[to][from] = weight;
    }
  }

  bool hasEdge(int from, int to) => matrix[from][to] != 0;
}

// Usage
var graph = GraphAdjList();
graph.addEdge(0, 1);
graph.addEdge(0, 2);
graph.addEdge(1, 2);
print(graph.neighbors(0)); // [1, 2]
```

---

**28. Implement Depth-First Search (DFS) for a graph using recursion.**

```dart
class DFS {
  static List<int> dfs(Map<int, List<int>> graph, int start) {
    List<int> result = [];
    Set<int> visited = {};

    void dfsRecursive(int node) {
      if (visited.contains(node)) return;

      visited.add(node);
      result.add(node);

      for (int neighbor in graph[node] ?? []) {
        dfsRecursive(neighbor);
      }
    }

    dfsRecursive(start);
    return result;
  }

  // Iterative using stack
  static List<int> dfsIterative(Map<int, List<int>> graph, int start) {
    List<int> result = [];
    Set<int> visited = {};
    List<int> stack = [start];

    while (stack.isNotEmpty) {
      int node = stack.removeLast();

      if (visited.contains(node)) continue;
      visited.add(node);
      result.add(node);

      // Add neighbors in reverse order for consistent traversal
      for (int neighbor in (graph[node] ?? []).reversed) {
        if (!visited.contains(neighbor)) {
          stack.add(neighbor);
        }
      }
    }

    return result;
  }
}

// Usage
var graph = {
  0: [1, 2],
  1: [0, 3],
  2: [0, 3],
  3: [1, 2],
};
print(DFS.dfs(graph, 0)); // [0, 1, 3, 2]
```

**Time Complexity**: O(V + E)
**Space Complexity**: O(V)

---

**29. Implement Breadth-First Search (BFS) for a graph using a queue.**

```dart
import 'dart:collection';

List<int> bfs(Map<int, List<int>> graph, int start) {
  List<int> result = [];
  Set<int> visited = {};
  Queue<int> queue = Queue();

  queue.add(start);
  visited.add(start);

  while (queue.isNotEmpty) {
    int node = queue.removeFirst();
    result.add(node);

    for (int neighbor in graph[node] ?? []) {
      if (!visited.contains(neighbor)) {
        visited.add(neighbor);
        queue.add(neighbor);
      }
    }
  }

  return result;
}

// Usage
var graph = {
  0: [1, 2],
  1: [0, 3],
  2: [0, 3],
  3: [1, 2],
};
print(bfs(graph, 0)); // [0, 1, 2, 3]
```

**Time Complexity**: O(V + E)
**Space Complexity**: O(V)

---

**30. How do you detect a cycle in a directed graph?**

```dart
bool hasCycle(Map<int, List<int>> graph) {
  Set<int> visited = {};
  Set<int> recursionStack = {};

  bool dfs(int node) {
    visited.add(node);
    recursionStack.add(node);

    for (int neighbor in graph[node] ?? []) {
      // If neighbor is in current recursion stack, cycle found
      if (recursionStack.contains(neighbor)) {
        return true;
      }
      // If not visited, explore it
      if (!visited.contains(neighbor) && dfs(neighbor)) {
        return true;
      }
    }

    recursionStack.remove(node);
    return false;
  }

  // Check all vertices (for disconnected graphs)
  for (int vertex in graph.keys) {
    if (!visited.contains(vertex)) {
      if (dfs(vertex)) return true;
    }
  }

  return false;
}

// Usage
var graphWithCycle = {
  0: [1],
  1: [2],
  2: [0], // Creates cycle
};
print(hasCycle(graphWithCycle)); // true

var graphNoCycle = {
  0: [1],
  1: [2],
  2: <int>[],
};
print(hasCycle(graphNoCycle)); // false
```

**Time Complexity**: O(V + E)
**Space Complexity**: O(V)

---

**31. Explain how to find the shortest path in an unweighted graph.**

Use BFS - it naturally finds shortest path in unweighted graphs:

```dart
import 'dart:collection';

List<int>? shortestPath(Map<int, List<int>> graph, int start, int end) {
  if (start == end) return [start];

  Queue<int> queue = Queue();
  Map<int, int> parent = {};
  Set<int> visited = {};

  queue.add(start);
  visited.add(start);
  parent[start] = -1;

  while (queue.isNotEmpty) {
    int node = queue.removeFirst();

    for (int neighbor in graph[node] ?? []) {
      if (!visited.contains(neighbor)) {
        visited.add(neighbor);
        parent[neighbor] = node;

        if (neighbor == end) {
          // Reconstruct path
          List<int> path = [];
          int? current = end;
          while (current != -1 && current != null) {
            path.add(current);
            current = parent[current];
          }
          return path.reversed.toList();
        }

        queue.add(neighbor);
      }
    }
  }

  return null; // No path found
}

// Usage
var graph = {
  0: [1, 2],
  1: [0, 3, 4],
  2: [0, 4],
  3: [1, 5],
  4: [1, 2, 5],
  5: [3, 4],
};
print(shortestPath(graph, 0, 5)); // [0, 1, 3, 5] or [0, 2, 4, 5]
```

**Time Complexity**: O(V + E)
**Space Complexity**: O(V)

---

## Hash Maps and Sets

**32. What is the time complexity of HashMap operations in Dart? When would you use a HashMap over a List?**

**Time Complexities (average case):**
- Insert: O(1)
- Lookup: O(1)
- Delete: O(1)
- Iteration: O(n)

**Use HashMap when:**
- Need fast key-based lookups
- Need to check existence frequently
- Keys are not sequential integers
- Need to associate values with keys

```dart
// HashMap example
var scores = <String, int>{};
scores['Alice'] = 100;  // O(1) insert
scores['Bob'] = 85;
print(scores['Alice']); // O(1) lookup
scores.containsKey('Alice'); // O(1) check

// Vs List - O(n) for search
var list = ['Alice', 'Bob'];
list.contains('Alice'); // O(n) search
```

---

**33. How do you find the first non-repeating character in a string using a HashMap?**

```dart
String? firstNonRepeating(String s) {
  Map<String, int> count = {};

  // Count occurrences - O(n)
  for (var char in s.split('')) {
    count[char] = (count[char] ?? 0) + 1;
  }

  // Find first with count 1 - O(n)
  for (var char in s.split('')) {
    if (count[char] == 1) {
      return char;
    }
  }

  return null;
}

// Usage
print(firstNonRepeating('leetcode')); // 'l'
print(firstNonRepeating('aabb'));     // null
```

**Time Complexity**: O(n)
**Space Complexity**: O(k) where k is unique characters

---

**34. Implement a function to check if two strings are anagrams using Dart collections.**

```dart
bool areAnagrams(String s1, String s2) {
  if (s1.length != s2.length) return false;

  Map<String, int> count = {};

  // Count characters in s1
  for (var char in s1.split('')) {
    count[char] = (count[char] ?? 0) + 1;
  }

  // Subtract counts using s2
  for (var char in s2.split('')) {
    if (!count.containsKey(char)) return false;
    count[char] = count[char]! - 1;
    if (count[char] == 0) count.remove(char);
  }

  return count.isEmpty;
}

// Alternative using sorted comparison
bool areAnagramsSorted(String s1, String s2) {
  if (s1.length != s2.length) return false;

  var chars1 = s1.split('')..sort();
  var chars2 = s2.split('')..sort();

  return chars1.join() == chars2.join();
}

// Usage
print(areAnagrams('listen', 'silent')); // true
print(areAnagrams('hello', 'world'));   // false
```

**Time Complexity**: O(n) for HashMap, O(n log n) for sorting

---

**35. How would you implement a simple LRU (Least Recently Used) cache in Dart?**

```dart
class LRUCache<K, V> {
  final int capacity;
  final Map<K, V> _cache = {};
  final List<K> _order = []; // Most recent at end

  LRUCache(this.capacity);

  V? get(K key) {
    if (!_cache.containsKey(key)) return null;

    // Move to end (most recently used)
    _order.remove(key);
    _order.add(key);

    return _cache[key];
  }

  void put(K key, V value) {
    if (_cache.containsKey(key)) {
      // Update and move to end
      _order.remove(key);
    } else if (_cache.length >= capacity) {
      // Evict least recently used (first in order)
      K lru = _order.removeAt(0);
      _cache.remove(lru);
    }

    _cache[key] = value;
    _order.add(key);
  }

  @override
  String toString() => 'Cache: $_cache, Order: $_order';
}

// Usage
var cache = LRUCache<int, String>(3);
cache.put(1, 'one');
cache.put(2, 'two');
cache.put(3, 'three');
print(cache.get(1));    // 'one' - moves 1 to end
cache.put(4, 'four');   // Evicts 2 (least recently used)
print(cache.get(2));    // null - was evicted
```

**Note**: This implementation has O(n) for `get` due to `_order.remove()`. For O(1) operations, use a LinkedHashMap or implement a doubly linked list.

---

## Sorting Algorithms

**36. Implement Quick Sort in Dart and explain its time complexity.**

```dart
void quickSort(List<int> arr, int low, int high) {
  if (low < high) {
    int pivotIndex = partition(arr, low, high);
    quickSort(arr, low, pivotIndex - 1);
    quickSort(arr, pivotIndex + 1, high);
  }
}

int partition(List<int> arr, int low, int high) {
  int pivot = arr[high];
  int i = low - 1;

  for (int j = low; j < high; j++) {
    if (arr[j] < pivot) {
      i++;
      // Swap arr[i] and arr[j]
      int temp = arr[i];
      arr[i] = arr[j];
      arr[j] = temp;
    }
  }

  // Place pivot in correct position
  int temp = arr[i + 1];
  arr[i + 1] = arr[high];
  arr[high] = temp;

  return i + 1;
}

// Usage
var arr = [64, 34, 25, 12, 22, 11, 90];
quickSort(arr, 0, arr.length - 1);
print(arr); // [11, 12, 22, 25, 34, 64, 90]
```

**Time Complexity:**
- Average: O(n log n)
- Worst (already sorted): O(n²)
- Best: O(n log n)

**Space Complexity**: O(log n) average for recursion stack

---

**37. Implement Merge Sort in Dart. What is its space complexity?**

```dart
List<int> mergeSort(List<int> arr) {
  if (arr.length <= 1) return arr;

  int mid = arr.length ~/ 2;
  List<int> left = mergeSort(arr.sublist(0, mid));
  List<int> right = mergeSort(arr.sublist(mid));

  return merge(left, right);
}

List<int> merge(List<int> left, List<int> right) {
  List<int> result = [];
  int i = 0, j = 0;

  while (i < left.length && j < right.length) {
    if (left[i] <= right[j]) {
      result.add(left[i]);
      i++;
    } else {
      result.add(right[j]);
      j++;
    }
  }

  // Add remaining elements
  result.addAll(left.sublist(i));
  result.addAll(right.sublist(j));

  return result;
}

// Usage
var arr = [64, 34, 25, 12, 22, 11, 90];
print(mergeSort(arr)); // [11, 12, 22, 25, 34, 64, 90]
```

**Time Complexity**: O(n log n) always
**Space Complexity**: O(n) for the merged arrays

---

**38. Write a Bubble Sort implementation and explain when it might be useful.**

```dart
void bubbleSort(List<int> arr) {
  int n = arr.length;
  bool swapped;

  for (int i = 0; i < n - 1; i++) {
    swapped = false;

    for (int j = 0; j < n - i - 1; j++) {
      if (arr[j] > arr[j + 1]) {
        // Swap
        int temp = arr[j];
        arr[j] = arr[j + 1];
        arr[j + 1] = temp;
        swapped = true;
      }
    }

    // If no swaps, array is sorted
    if (!swapped) break;
  }
}

// Usage
var arr = [64, 34, 25, 12, 22, 11, 90];
bubbleSort(arr);
print(arr); // [11, 12, 22, 25, 34, 64, 90]
```

**Time Complexity:**
- Worst/Average: O(n²)
- Best (already sorted): O(n)

**When useful:**
- Educational purposes (easy to understand)
- Nearly sorted data (O(n) with early termination)
- Small datasets where simplicity matters more than performance
- When memory is very limited (in-place, O(1) space)

---

**39. How does Dart's built-in sort() method work? What algorithm does it use?**

Dart uses a **dual-pivot Quicksort** algorithm for its built-in `sort()` method, with **insertion sort** for small arrays (typically < 32 elements).

```dart
var list = [5, 2, 8, 1, 9];
list.sort(); // Uses dual-pivot Quicksort
print(list); // [1, 2, 5, 8, 9]

// Custom comparator
var words = ['banana', 'apple', 'cherry'];
words.sort((a, b) => a.compareTo(b));
print(words); // [apple, banana, cherry]

// Descending order
list.sort((a, b) => b.compareTo(a));
print(list); // [9, 8, 5, 2, 1]
```

**Characteristics:**
- Average: O(n log n)
- Worst: O(n²) but rare due to dual-pivot
- In-place: Yes (modifies original list)
- Stable: No (equal elements may change relative order)

---

**40. Implement Insertion Sort and explain its best and worst-case scenarios.**

```dart
void insertionSort(List<int> arr) {
  for (int i = 1; i < arr.length; i++) {
    int key = arr[i];
    int j = i - 1;

    // Move elements greater than key one position ahead
    while (j >= 0 && arr[j] > key) {
      arr[j + 1] = arr[j];
      j--;
    }

    arr[j + 1] = key;
  }
}

// Usage
var arr = [64, 34, 25, 12, 22, 11, 90];
insertionSort(arr);
print(arr); // [11, 12, 22, 25, 34, 64, 90]
```

**Time Complexity:**
- Best (already sorted): O(n) - only compares, no moves
- Worst (reverse sorted): O(n²) - every element needs to move
- Average: O(n²)

**Space Complexity**: O(1)

**When useful:**
- Small datasets
- Nearly sorted data
- Online algorithm (can sort as data arrives)
- Stable sort required

---

## Searching Algorithms

**41. Implement Binary Search in Dart both iteratively and recursively.**

```dart
// Iterative - O(log n) time, O(1) space
int binarySearchIterative(List<int> arr, int target) {
  int left = 0;
  int right = arr.length - 1;

  while (left <= right) {
    int mid = left + (right - left) ~/ 2; // Avoid overflow

    if (arr[mid] == target) {
      return mid;
    } else if (arr[mid] < target) {
      left = mid + 1;
    } else {
      right = mid - 1;
    }
  }

  return -1; // Not found
}

// Recursive - O(log n) time, O(log n) space
int binarySearchRecursive(List<int> arr, int target, int left, int right) {
  if (left > right) return -1;

  int mid = left + (right - left) ~/ 2;

  if (arr[mid] == target) {
    return mid;
  } else if (arr[mid] < target) {
    return binarySearchRecursive(arr, target, mid + 1, right);
  } else {
    return binarySearchRecursive(arr, target, left, mid - 1);
  }
}

// Usage
var sorted = [1, 3, 5, 7, 9, 11, 13];
print(binarySearchIterative(sorted, 7));  // 3
print(binarySearchRecursive(sorted, 7, 0, sorted.length - 1)); // 3
```

---

**42. What is the time complexity of searching in a Dart List? How can you optimize it?**

**Default List search:**
- `list.contains(element)`: O(n) - linear search
- `list.indexOf(element)`: O(n) - linear search

**Optimization strategies:**

```dart
// 1. Binary search for sorted lists - O(log n)
var sorted = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
int index = binarySearchIterative(sorted, 7);

// 2. Use Set for O(1) lookups
var set = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
bool exists = set.contains(7); // O(1)

// 3. Use Map for O(1) key lookups
var map = {'a': 1, 'b': 2, 'c': 3};
bool hasKey = map.containsKey('b'); // O(1)

// 4. Keep list sorted and use binarySearch from collection package
import 'package:collection/collection.dart';
var idx = lowerBound(sorted, 7);
```

---

**43. How do you find the first and last position of an element in a sorted array?**

```dart
List<int> searchRange(List<int> nums, int target) {
  return [findFirst(nums, target), findLast(nums, target)];
}

int findFirst(List<int> nums, int target) {
  int left = 0, right = nums.length - 1;
  int result = -1;

  while (left <= right) {
    int mid = left + (right - left) ~/ 2;

    if (nums[mid] == target) {
      result = mid;
      right = mid - 1; // Continue searching left
    } else if (nums[mid] < target) {
      left = mid + 1;
    } else {
      right = mid - 1;
    }
  }

  return result;
}

int findLast(List<int> nums, int target) {
  int left = 0, right = nums.length - 1;
  int result = -1;

  while (left <= right) {
    int mid = left + (right - left) ~/ 2;

    if (nums[mid] == target) {
      result = mid;
      left = mid + 1; // Continue searching right
    } else if (nums[mid] < target) {
      left = mid + 1;
    } else {
      right = mid - 1;
    }
  }

  return result;
}

// Usage
print(searchRange([5, 7, 7, 8, 8, 10], 8)); // [3, 4]
print(searchRange([5, 7, 7, 8, 8, 10], 6)); // [-1, -1]
```

**Time Complexity**: O(log n)
**Space Complexity**: O(1)

---

## Recursion

**44. Explain recursion and write a recursive function to calculate factorial in Dart.**

Recursion is when a function calls itself to solve smaller subproblems. Every recursive function needs:
1. **Base case**: Condition to stop recursion
2. **Recursive case**: Function calls itself with smaller input

```dart
// Recursive factorial
int factorial(int n) {
  // Base case
  if (n <= 1) return 1;

  // Recursive case
  return n * factorial(n - 1);
}

// With tail recursion optimization
int factorialTail(int n, [int accumulator = 1]) {
  if (n <= 1) return accumulator;
  return factorialTail(n - 1, n * accumulator);
}

// Iterative (for comparison)
int factorialIterative(int n) {
  int result = 1;
  for (int i = 2; i <= n; i++) {
    result *= i;
  }
  return result;
}

// Usage
print(factorial(5));     // 120
print(factorialTail(5)); // 120
```

**Time Complexity**: O(n)
**Space Complexity**: O(n) for recursion stack, O(1) for iterative

---

**45. Implement the Fibonacci sequence using recursion and then optimize it with memoization.**

```dart
// Naive recursion - O(2^n) time
int fibNaive(int n) {
  if (n <= 1) return n;
  return fibNaive(n - 1) + fibNaive(n - 2);
}

// With memoization - O(n) time, O(n) space
int fibMemo(int n, [Map<int, int>? memo]) {
  memo ??= {};

  if (n <= 1) return n;
  if (memo.containsKey(n)) return memo[n]!;

  memo[n] = fibMemo(n - 1, memo) + fibMemo(n - 2, memo);
  return memo[n]!;
}

// Iterative DP - O(n) time, O(1) space
int fibIterative(int n) {
  if (n <= 1) return n;

  int prev2 = 0, prev1 = 1;

  for (int i = 2; i <= n; i++) {
    int current = prev1 + prev2;
    prev2 = prev1;
    prev1 = current;
  }

  return prev1;
}

// Usage
print(fibNaive(10));     // 55 (slow for large n)
print(fibMemo(50));      // 12586269025 (fast)
print(fibIterative(50)); // 12586269025 (fastest)
```

---

**46. How do you solve the Tower of Hanoi problem using recursion in Dart?**

```dart
void towerOfHanoi(int n, String source, String auxiliary, String destination) {
  if (n == 1) {
    print('Move disk 1 from $source to $destination');
    return;
  }

  // Move n-1 disks from source to auxiliary
  towerOfHanoi(n - 1, source, destination, auxiliary);

  // Move the largest disk to destination
  print('Move disk $n from $source to $destination');

  // Move n-1 disks from auxiliary to destination
  towerOfHanoi(n - 1, auxiliary, source, destination);
}

// Usage
towerOfHanoi(3, 'A', 'B', 'C');
// Output:
// Move disk 1 from A to C
// Move disk 2 from A to B
// Move disk 1 from C to B
// Move disk 3 from A to C
// Move disk 1 from B to A
// Move disk 2 from B to C
// Move disk 1 from A to C
```

**Time Complexity**: O(2^n)
**Space Complexity**: O(n) for recursion stack

---

**47. Write a recursive function to generate all permutations of a string.**

```dart
List<String> permutations(String s) {
  List<String> result = [];
  _permute(s.split(''), 0, result);
  return result;
}

void _permute(List<String> chars, int start, List<String> result) {
  if (start == chars.length - 1) {
    result.add(chars.join());
    return;
  }

  for (int i = start; i < chars.length; i++) {
    // Swap
    var temp = chars[start];
    chars[start] = chars[i];
    chars[i] = temp;

    // Recurse
    _permute(chars, start + 1, result);

    // Backtrack (swap back)
    temp = chars[start];
    chars[start] = chars[i];
    chars[i] = temp;
  }
}

// Usage
print(permutations('abc'));
// [abc, acb, bac, bca, cba, cab]
```

**Time Complexity**: O(n!)
**Space Complexity**: O(n) for recursion stack

---

## Dynamic Programming

**48. What is Dynamic Programming? Explain the difference between memoization and tabulation.**

**Dynamic Programming** breaks complex problems into overlapping subproblems, solving each once and storing results.

**Memoization (Top-Down):**
- Start with the main problem, recursively solve subproblems
- Cache results as you go
- Lazy evaluation - only computes what's needed

**Tabulation (Bottom-Up):**
- Start with smallest subproblems, build up to main problem
- Iteratively fill a table
- Computes all subproblems

```dart
// Memoization (Top-Down)
int fibMemo(int n, Map<int, int> cache) {
  if (n <= 1) return n;
  if (cache.containsKey(n)) return cache[n]!;

  cache[n] = fibMemo(n - 1, cache) + fibMemo(n - 2, cache);
  return cache[n]!;
}

// Tabulation (Bottom-Up)
int fibTabulation(int n) {
  if (n <= 1) return n;

  List<int> dp = List.filled(n + 1, 0);
  dp[1] = 1;

  for (int i = 2; i <= n; i++) {
    dp[i] = dp[i - 1] + dp[i - 2];
  }

  return dp[n];
}
```

---

**49. Implement the Fibonacci sequence using dynamic programming (both top-down and bottom-up).**

```dart
// Top-Down with Memoization
class FibMemo {
  final Map<int, int> _cache = {};

  int fib(int n) {
    if (n <= 1) return n;

    if (!_cache.containsKey(n)) {
      _cache[n] = fib(n - 1) + fib(n - 2);
    }

    return _cache[n]!;
  }
}

// Bottom-Up with Tabulation
int fibBottomUp(int n) {
  if (n <= 1) return n;

  List<int> dp = List.filled(n + 1, 0);
  dp[1] = 1;

  for (int i = 2; i <= n; i++) {
    dp[i] = dp[i - 1] + dp[i - 2];
  }

  return dp[n];
}

// Space-Optimized Bottom-Up
int fibOptimized(int n) {
  if (n <= 1) return n;

  int prev2 = 0, prev1 = 1;

  for (int i = 2; i <= n; i++) {
    int current = prev1 + prev2;
    prev2 = prev1;
    prev1 = current;
  }

  return prev1;
}

// Usage
print(FibMemo().fib(50));  // 12586269025
print(fibBottomUp(50));     // 12586269025
print(fibOptimized(50));    // 12586269025
```

**Time Complexity**: O(n) for all
**Space Complexity**: O(n) for memo/tabulation, O(1) for optimized

---

**50. How do you solve the Coin Change problem using dynamic programming in Dart?**

Find minimum coins needed to make a target amount:

```dart
int coinChange(List<int> coins, int amount) {
  // dp[i] = minimum coins needed for amount i
  List<int> dp = List.filled(amount + 1, amount + 1);
  dp[0] = 0;

  for (int i = 1; i <= amount; i++) {
    for (int coin in coins) {
      if (coin <= i) {
        dp[i] = min(dp[i], dp[i - coin] + 1);
      }
    }
  }

  return dp[amount] > amount ? -1 : dp[amount];
}

int min(int a, int b) => a < b ? a : b;

// Count number of ways to make change
int coinChangeWays(List<int> coins, int amount) {
  List<int> dp = List.filled(amount + 1, 0);
  dp[0] = 1; // One way to make 0: use no coins

  for (int coin in coins) {
    for (int i = coin; i <= amount; i++) {
      dp[i] += dp[i - coin];
    }
  }

  return dp[amount];
}

// Usage
print(coinChange([1, 2, 5], 11));     // 3 (5+5+1)
print(coinChange([2], 3));            // -1 (impossible)
print(coinChangeWays([1, 2, 5], 5));  // 4 ways
```

**Time Complexity**: O(amount * coins.length)
**Space Complexity**: O(amount)

---

**51. Implement the Longest Common Subsequence (LCS) problem using DP.**

```dart
int longestCommonSubsequence(String text1, String text2) {
  int m = text1.length;
  int n = text2.length;

  // dp[i][j] = LCS length for text1[0..i-1] and text2[0..j-1]
  List<List<int>> dp = List.generate(
    m + 1,
    (_) => List.filled(n + 1, 0),
  );

  for (int i = 1; i <= m; i++) {
    for (int j = 1; j <= n; j++) {
      if (text1[i - 1] == text2[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
      } else {
        dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }

  return dp[m][n];
}

// Get the actual LCS string
String getLCS(String text1, String text2) {
  int m = text1.length;
  int n = text2.length;

  List<List<int>> dp = List.generate(
    m + 1,
    (_) => List.filled(n + 1, 0),
  );

  for (int i = 1; i <= m; i++) {
    for (int j = 1; j <= n; j++) {
      if (text1[i - 1] == text2[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
      } else {
        dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }

  // Backtrack to find the sequence
  StringBuffer lcs = StringBuffer();
  int i = m, j = n;

  while (i > 0 && j > 0) {
    if (text1[i - 1] == text2[j - 1]) {
      lcs.write(text1[i - 1]);
      i--;
      j--;
    } else if (dp[i - 1][j] > dp[i][j - 1]) {
      i--;
    } else {
      j--;
    }
  }

  return lcs.toString().split('').reversed.join();
}

int max(int a, int b) => a > b ? a : b;

// Usage
print(longestCommonSubsequence('abcde', 'ace')); // 3
print(getLCS('abcde', 'ace')); // 'ace'
```

**Time Complexity**: O(m * n)
**Space Complexity**: O(m * n)

---

## Big O Notation and Complexity

**52. Explain Big O notation. What are the common time complexities (O(1), O(n), O(log n), O(n²))?**

Big O describes the **upper bound** of algorithm growth rate as input size increases.

| Notation | Name | Example |
|----------|------|---------|
| O(1) | Constant | Array access, HashMap lookup |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | Linear search, single loop |
| O(n log n) | Linearithmic | Merge sort, Quick sort (avg) |
| O(n²) | Quadratic | Nested loops, Bubble sort |
| O(2^n) | Exponential | Recursive Fibonacci (naive) |
| O(n!) | Factorial | Permutations |

```dart
// O(1) - Constant
int getFirst(List<int> arr) => arr[0];

// O(log n) - Logarithmic
int binarySearch(List<int> arr, int target) {
  int left = 0, right = arr.length - 1;
  while (left <= right) {
    int mid = (left + right) ~/ 2;
    if (arr[mid] == target) return mid;
    if (arr[mid] < target) left = mid + 1;
    else right = mid - 1;
  }
  return -1;
}

// O(n) - Linear
int sum(List<int> arr) => arr.fold(0, (a, b) => a + b);

// O(n²) - Quadratic
void bubbleSort(List<int> arr) {
  for (int i = 0; i < arr.length; i++) {
    for (int j = 0; j < arr.length - 1; j++) {
      if (arr[j] > arr[j + 1]) {
        var temp = arr[j];
        arr[j] = arr[j + 1];
        arr[j + 1] = temp;
      }
    }
  }
}
```

---

**53. What is the difference between time complexity and space complexity?**

**Time Complexity**: How runtime grows with input size
**Space Complexity**: How memory usage grows with input size

```dart
// O(n) time, O(n) space
List<int> doubleElements(List<int> arr) {
  List<int> result = []; // New list uses O(n) space
  for (var x in arr) {   // O(n) iterations
    result.add(x * 2);
  }
  return result;
}

// O(n) time, O(1) space (in-place)
void doubleInPlace(List<int> arr) {
  for (int i = 0; i < arr.length; i++) {
    arr[i] *= 2; // Modifies existing list
  }
}

// Trade-off example: Memoization
// Trades O(n) extra space for O(n) time vs O(2^n) time
```

---

**54. How do you analyze the time complexity of nested loops?**

```dart
// O(n) - Single loop
for (int i = 0; i < n; i++) { } // n iterations

// O(n²) - Nested loops (same range)
for (int i = 0; i < n; i++) {
  for (int j = 0; j < n; j++) { } // n * n = n²
}

// O(n * m) - Nested loops (different ranges)
for (int i = 0; i < n; i++) {
  for (int j = 0; j < m; j++) { } // n * m
}

// O(n²/2) = O(n²) - Triangular pattern
for (int i = 0; i < n; i++) {
  for (int j = i; j < n; j++) { } // Still O(n²)
}

// O(n log n) - Loop with halving
for (int i = 0; i < n; i++) {
  for (int j = n; j > 0; j ~/= 2) { } // n * log(n)
}
```

**Key rules:**
1. Drop constants: O(2n) → O(n)
2. Drop lower terms: O(n² + n) → O(n²)
3. Multiply nested loops
4. Add sequential operations: O(n) + O(m) = O(n + m)

---

**55. What is amortized time complexity? Give an example with Dart List operations.**

**Amortized analysis** averages time over a sequence of operations, even if individual operations vary.

```dart
// Dart List.add() - O(1) amortized
var list = <int>[];

// Most adds are O(1), but occasionally O(n) when resizing
for (int i = 0; i < 1000; i++) {
  list.add(i); // Usually O(1)
}

// How it works:
// - List starts with capacity (e.g., 8)
// - When full, doubles capacity and copies elements O(n)
// - But this only happens log(n) times
// - Average: (n + 1 + 2 + 4 + ... + n) / n ≈ O(1)

// Worst case vs Amortized:
// list.add()     - Worst: O(n), Amortized: O(1)
// list.insert(0) - Always O(n)
```

**Other examples:**
- HashMap insert: Worst O(n), Amortized O(1)
- Stack push (dynamic array): Worst O(n), Amortized O(1)

---

## Dart/Flutter Specific

**56. What are the differences between List, Set, and Map in Dart? When would you use each?**

| Feature | List | Set | Map |
|---------|------|-----|-----|
| Ordered | Yes | No (LinkedHashSet: Yes) | No (LinkedHashMap: Yes) |
| Duplicates | Allowed | Not allowed | Keys unique |
| Access | By index O(1) | By value O(1) | By key O(1) |
| Use case | Sequences | Unique items | Key-value pairs |

```dart
// List - Ordered, duplicates allowed
List<int> scores = [100, 85, 100, 90];
scores[0]; // Access by index
scores.add(95);

// Set - Unique items, fast lookup
Set<String> tags = {'flutter', 'dart', 'mobile'};
tags.contains('flutter'); // O(1) lookup
tags.add('flutter'); // No duplicate added

// Map - Key-value pairs
Map<String, int> ages = {'Alice': 30, 'Bob': 25};
ages['Alice']; // Access by key
ages.containsKey('Alice'); // O(1) lookup
```

**When to use:**
- **List**: Need order, allow duplicates, access by index
- **Set**: Need uniqueness, fast membership check
- **Map**: Need key-value association, fast key lookup

---

**57. Explain Dart's growable lists. How do they differ from fixed-length lists in terms of performance?**

```dart
// Growable list (default) - Can change size
var growable = <int>[];
growable.add(1);      // OK - O(1) amortized
growable.addAll([2, 3]); // OK
growable.length = 10; // OK - extends with null/default

// Fixed-length list - Size is immutable
var fixed = List<int>.filled(5, 0);
// fixed.add(1);      // Error!
// fixed.length = 10; // Error!
fixed[0] = 1;         // OK - can modify elements
```

**Performance differences:**

| Operation | Growable | Fixed-length |
|-----------|----------|--------------|
| add() | O(1) amortized | Not supported |
| Access | O(1) | O(1) |
| Memory | May over-allocate | Exact size |
| Resize | Automatic | Not allowed |

**Use fixed-length when:**
- Size is known and constant
- Memory efficiency is critical
- Prevent accidental modifications

---

**58. How does Dart's garbage collection affect algorithm performance in Flutter apps?**

Dart uses a **generational garbage collector**:
- **Young generation**: Short-lived objects (collected frequently)
- **Old generation**: Long-lived objects (collected less often)

**Performance considerations:**

```dart
// Bad: Creates many temporary objects (GC pressure)
String processData(List<String> items) {
  String result = '';
  for (var item in items) {
    result += item; // Creates new String each iteration!
  }
  return result;
}

// Good: Use StringBuffer to minimize allocations
String processDataOptimized(List<String> items) {
  final buffer = StringBuffer();
  for (var item in items) {
    buffer.write(item);
  }
  return buffer.toString();
}

// Bad: Creating lists in build methods
Widget build(BuildContext context) {
  var items = [1, 2, 3, 4, 5]; // Recreated every build!
  return ListView.builder(...);
}

// Good: Cache or use const
final _items = [1, 2, 3, 4, 5]; // Created once
Widget build(BuildContext context) {
  return ListView.builder(...);
}
```

**Tips for Flutter:**
1. Avoid creating objects in `build()` methods
2. Use `const` constructors where possible
3. Reuse objects instead of creating new ones
4. Use object pools for frequently created/destroyed objects

---

**59. What are Iterables in Dart? How do they differ from Lists in terms of memory and performance?**

**Iterable** is a lazy collection that generates values on demand.

```dart
// List - Eager, stored in memory
List<int> list = [1, 2, 3, 4, 5];
// All 5 integers are in memory immediately

// Iterable - Lazy, computed on demand
Iterable<int> iterable = [1, 2, 3, 4, 5].map((x) => x * 2);
// Multiplication happens when you iterate, not when created

// Generator function - Truly lazy
Iterable<int> range(int start, int end) sync* {
  for (int i = start; i < end; i++) {
    yield i;
  }
}

// Generates values one at a time
for (var n in range(0, 1000000)) {
  if (n > 10) break; // Only generated 11 values!
}
```

**Differences:**

| Aspect | List | Iterable |
|--------|------|----------|
| Memory | All elements stored | Values computed on demand |
| Random access | O(1) | Not supported |
| Length | O(1) | O(n) - must iterate |
| Multiple iteration | Efficient | May recompute |

**Use Iterable when:**
- Processing large data streams
- Only need to iterate once
- Want lazy evaluation
- Memory is constrained

---

**60. Explain how to use Dart's collection methods (map, where, reduce, fold) for efficient data manipulation.**

```dart
var numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// map - Transform each element (lazy)
var doubled = numbers.map((n) => n * 2);
print(doubled.toList()); // [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

// where - Filter elements (lazy)
var evens = numbers.where((n) => n.isEven);
print(evens.toList()); // [2, 4, 6, 8, 10]

// reduce - Combine to single value (left to right)
int sum = numbers.reduce((a, b) => a + b);
print(sum); // 55

// fold - Like reduce, but with initial value
int sumPlusTen = numbers.fold(10, (a, b) => a + b);
print(sumPlusTen); // 65

// Chaining (efficient - lazy evaluation)
var result = numbers
    .where((n) => n.isEven)
    .map((n) => n * 2)
    .toList();
print(result); // [4, 8, 12, 16, 20]

// any - Check if any element matches
bool hasLarge = numbers.any((n) => n > 5); // true

// every - Check if all elements match
bool allPositive = numbers.every((n) => n > 0); // true

// firstWhere - Find first matching element
int firstEven = numbers.firstWhere((n) => n.isEven); // 2

// expand - Flatten nested iterables
var nested = [[1, 2], [3, 4]];
var flat = nested.expand((list) => list).toList(); // [1, 2, 3, 4]
```

**Performance tips:**
1. Chain operations before `.toList()` for lazy evaluation
2. Use `firstWhere` with `orElse` to avoid exceptions
3. Prefer `fold` over `reduce` when list might be empty
4. Use `take(n)` to limit iterations
