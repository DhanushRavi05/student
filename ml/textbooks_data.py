# Comprehensive Academic Textbooks Repository (Autonomous University Curriculum)
import json

TEXTBOOKS_SEED = [
    {
        'subject_code': 'CS3351',
        'subject_name': 'Data Structures and Algorithms',
        'department': 'CSE',
        'semester': 3,
        'title': 'Data Structures and Algorithmic Analysis in C & Python: Complete University Coursebook',
        'author': 'Prof. A. Nithya & Dr. K. Senthil Kumar (Department of Computer Science)',
        'edition': 'Autonomous 2025 Revised Comprehensive Edition',
        'pages': 365,
        'summary': 'The definitive textbook for engineering students covering Linear Data Structures (Stacks, Queues, Linked Lists), Non-Linear Structures (Trees, AVL, B-Trees, Heaps), Graph Algorithms (Shortest Path, Spanning Trees), Sorting & Hashing, and Algorithm Design Techniques.',
        'units_json': json.dumps([
            {
                'unit_number': 1,
                'unit_title': 'Unit I: Linear Data Structures - Arrays, Linked Lists, Stacks & Queues',
                'summary': 'Abstract Data Types (ADTs), Singly & Doubly Linked Lists, Stack applications (Infix to Postfix, Evaluator), Circular Queues & Priority Queues.',
                'content': """1.1 CONCEPT OF ABSTRACT DATA TYPES (ADT)
An Abstract Data Type (ADT) is a mathematical model for data types where a data type is defined by its behavior (semantics) from the point of view of a user of the data, specifically in terms of possible values, possible operations on data of this type, and the behavior of these operations.
Mathematically, an ADT is a pair: ADT = (D, F) where D is a set of data objects, and F is a set of operations that can be performed on those objects.

1.2 SINGLY LINKED LIST IMPLEMENTATION
A singly linked list is a linear data structure in which each element is a separate object known as a node. Each node contains two items:
1. Data field: stores the value.
2. Next pointer field: stores the memory address of the succeeding node.

C Structure Definition:
struct Node {
    int data;
    struct Node* next;
};

Key Operations & Time Complexities:
- Insertion at Head: O(1)
- Insertion at Tail (without tail pointer): O(n); with tail pointer: O(1)
- Deletion at Head: O(1)
- Deletion at arbitrary position: O(n)
- Search: O(n)

1.3 DOUBLY LINKED LIST & CIRCULAR LINKED LIST
A Doubly Linked List has two pointers: `prev` and `next`, enabling bidirectional traversal. This allows O(1) deletion given a node reference, but introduces 1 pointer overhead per node (8 bytes on 64-bit systems).

1.4 STACK ADT & APPLICATIONS
A Stack is a Last-In-First-Out (LIFO) data structure.
Fundamental operations:
- push(x): Adds item x to the top. Time complexity: O(1).
- pop(): Removes and returns the top element. Time complexity: O(1).
- peek(): Returns top without removal. Time complexity: O(1).

Application: Infix to Postfix Conversion (Shunting-Yard Algorithm)
Algorithm Steps:
1. Scan the infix expression from left to right.
2. If the scanned character is an operand, output it to postfix string.
3. If '(', push it onto the stack.
4. If ')', pop from stack to output until '(' is encountered, then discard '('.
5. If operator op1:
   While stack is non-empty and precedence(stack.top()) >= precedence(op1), pop stack to output.
   Push op1 onto stack.
6. Pop remaining operators from stack.

1.5 QUEUE ADT & CIRCULAR BUFFER
A Queue is a First-In-First-Out (FIFO) linear structure.
Circular Queue overcomes the limitation of linear array queue where front cannot wrap around:
- Enqueue condition: (rear + 1) % capacity == front (Queue Full).
- Dequeue condition: front == -1 (Queue Empty)."""
            },
            {
                'unit_number': 2,
                'unit_title': 'Unit II: Non-Linear Structures - Trees, Binary Search Trees & Balanced Trees',
                'summary': 'Tree Terminologies, Binary Tree Traversals, BST Operations, AVL Trees (Rotations LL, RR, LR, RL), Red-Black Trees, and B-Trees.',
                'content': """2.1 BINARY TREE TERMINOLOGY & PROPERTIES
A Binary Tree is a hierarchical structure where each node has at most two children, referred to as left child and right child.
Properties:
1. Maximum number of nodes at level i of a binary tree is 2^i (level 0 is root).
2. Maximum number of nodes in a binary tree of height h is 2^(h+1) - 1.
3. In any non-empty binary tree, if n0 is number of leaf nodes and n2 is number of nodes with 2 children: n0 = n2 + 1.

2.2 TREE TRAVERSALS (RECURSIVE & ITERATIVE)
Traversals systematically visit each node exactly once:
- Preorder Traversal (Root, Left, Right): Used for prefix expression trees and cloning.
- Inorder Traversal (Left, Root, Right): Produces sorted sequence in a Binary Search Tree (BST).
- Postorder Traversal (Left, Right, Root): Used in bottom-up deletion and postfix calculation.
- Level Order Traversal (BFS): Uses a FIFO queue to visit level by level.

2.3 BINARY SEARCH TREE (BST)
Definition: For every node X:
- All keys in left subtree of X are strictly smaller than X.key.
- All keys in right subtree of X are strictly greater than X.key.
Average time complexity: O(log n) for search, insert, and delete.
Worst case (skewed tree): O(n).

2.4 SELF-BALANCING AVL TREES
An AVL Tree is a self-balancing BST where the difference between heights of left and right subtrees for ANY node (Balance Factor) is at most 1:
Balance Factor BF(X) = height(LeftSubtree) - height(RightSubtree) in {-1, 0, +1}.

Four Types of Rotations:
1. Left-Left (LL) Heavy: Fixed with a Single Right Rotation.
2. Right-Right (RR) Heavy: Fixed with a Single Left Rotation.
3. Left-Right (LR) Heavy: Fixed with Double Rotation (Left on left child, then Right on node).
4. Right-Left (RL) Heavy: Fixed with Double Rotation (Right on right child, then Left on node).
Guaranteed Search/Insert/Delete Complexity: O(log n) worst case."""
            },
            {
                'unit_number': 3,
                'unit_title': 'Unit III: Graph Algorithms - Traversal, Minimum Spanning Trees & Shortest Paths',
                'summary': 'Graph Representations (Matrix vs Adjacency List), BFS, DFS, Topological Sorting, Prim and Kruskal MST, Dijkstra and Bellman-Ford Shortest Paths.',
                'content': """3.1 GRAPH REPRESENTATIONS
A Graph G = (V, E) consists of a set of vertices V and edges E.
- Adjacency Matrix: Space complexity O(|V|^2). Fast edge query O(1), but expensive for sparse graphs.
- Adjacency List: Space complexity O(|V| + |E|). Ideal for sparse graphs; iterates over neighbors in O(deg(v)).

3.2 BREADTH FIRST SEARCH (BFS) & DEPTH FIRST SEARCH (DFS)
- BFS uses a FIFO queue. Finds shortest path in unweighted graphs. Time: O(|V| + |E|).
- DFS uses recursion or an explicit LIFO stack. Used for cycle detection, topological sorting, and strongly connected components (Kosaraju algorithm). Time: O(|V| + |E|).

3.3 MINIMUM SPANNING TREE (MST)
A Minimum Spanning Tree of a connected, undirected, weighted graph is a subgraph that connects all vertices without cycles and with minimum total edge weight. Total edges in MST = |V| - 1.

1. Kruskal's Algorithm (Greedy, Edge-centric):
   - Sort all edges in non-decreasing order of weights.
   - Using Disjoint-Set Union-Find (DSU) with path compression, pick the smallest edge that does not form a cycle.
   - Time Complexity: O(E log E) or O(E log V).

2. Prim's Algorithm (Greedy, Vertex-centric):
   - Start from an arbitrary root vertex. Grow a single tree by repeatedly adding the cheapest edge connecting a tree vertex to a non-tree vertex.
   - Using Min-Heap: Time Complexity O((V + E) log V).

3.4 SINGLE SOURCE SHORTEST PATH: DIJKSTRA'S ALGORITHM
Computes shortest paths from source vertex s to all other vertices in graphs with non-negative edge weights.
Algorithm:
- Initialize distance array: dist[s] = 0, dist[v] = infinity for all v != s.
- Min-priority queue Q contains pairs (dist[u], u).
- Repeatedly extract vertex u with minimum dist, and relax all outgoing edges (u, v):
  if dist[u] + weight(u, v) < dist[v]:
      dist[v] = dist[u] + weight(u, v)
      decrease_key(Q, v)
Time Complexity: O((V + E) log V) with binary heap."""
            },
            {
                'unit_number': 4,
                'unit_title': 'Unit IV: Sorting Techniques & Advanced Hashing Strategies',
                'summary': 'Comparison Sorts (QuickSort, MergeSort, HeapSort), Non-comparison Sorts (Radix, Counting), Hashing Functions, Collision Resolution (Open Addressing vs Chaining).',
                'content': """4.1 MERGESORT & QUICKSORT ANALYSIS
- MergeSort: Divide and Conquer paradigm. Divides array into two halves, recursively sorts, and merges in O(n).
  Recurrence: T(n) = 2T(n/2) + O(n) => T(n) = O(n log n) in all cases (Best, Average, Worst). Stable sorting. Space O(n).
- QuickSort: Selects a pivot element (Lomuto or Hoare partition). Partitions elements into smaller and larger.
  Average Time: O(n log n). Worst Case (already sorted with first element pivot): O(n^2). In-place, unstable.

4.2 HEAPSORT
Constructs a Max-Heap from the array in O(n) using bottom-up heapify.
Repeatedly extracts root (maximum element), swaps with last element, and restores heap property in O(log n).
Total Time: O(n log n) guaranteed worst case. In-place O(1) auxiliary space.

4.3 HASHING & COLLISION RESOLUTION
A Hash Table maps keys to bucket indices using a hash function h(k).
Collision occurs when h(k1) == h(k2) for k1 != k2.

Resolution Techniques:
1. Separate Chaining (Open Hashing): Each bucket contains a linked list of entries that hash to the same slot.
   Load factor alpha = n / m. Average search time: O(1 + alpha).
2. Open Addressing (Closed Hashing): All elements stored in the hash table itself.
   - Linear Probing: h(k, i) = (h'(k) + i) % m. Prone to Primary Clustering.
   - Quadratic Probing: h(k, i) = (h'(k) + c1*i + c2*i^2) % m. Eliminates primary clustering.
   - Double Hashing: h(k, i) = (h1(k) + i * h2(k)) % m. Best open addressing method."""
            },
            {
                'unit_number': 5,
                'unit_title': 'Unit V: Algorithm Design Techniques & Complexity Classes',
                'summary': 'Divide and Conquer, Dynamic Programming (0/1 Knapsack, LCS), Greedy Method, Backtracking (N-Queens), P vs NP and NP-Completeness.',
                'content': """5.1 DYNAMIC PROGRAMMING (DP)
Dynamic Programming solves problems with Overlapping Subproblems and Optimal Substructure by storing intermediate results (Memoization or Tabulation).

Classic Example 1: 0/1 Knapsack Problem
Given n items with weights w[i] and values v[i], and maximum capacity W:
Recurrence Relation:
dp[i][w] = dp[i-1][w]                           if w[i] > w
dp[i][w] = max(dp[i-1][w], v[i] + dp[i-1][w - w[i]]) if w[i] <= w
Time Complexity: O(n * W) (Pseudo-polynomial). Space Complexity: O(W) with state compression.

Classic Example 2: Longest Common Subsequence (LCS)
Given strings X[1..m] and Y[1..n]:
dp[i][j] = 1 + dp[i-1][j-1]            if X[i] == Y[j]
dp[i][j] = max(dp[i-1][j], dp[i][j-1]) if X[i] != Y[j]
Time & Space: O(m * n).

5.2 BACKTRACKING ALGORITHMS
Systematically searches for a solution by trying partial candidates and abandoning (backtracking) as soon as it determines the candidate cannot lead to a valid solution.
Example: 8-Queens Problem
Places 8 non-attacking queens on an 8x8 chessboard.
Uses bounding function to prune invalid branches: no two queens share the same row, column, or diagonal.

5.3 COMPUTATIONAL COMPLEXITY CLASSES
- P: Class of decision problems solvable by a deterministic Turing machine in polynomial time O(n^k).
- NP: Class of decision problems verifiable by a deterministic machine in polynomial time.
- NP-Complete: A problem X is NP-Complete if X is in NP and every problem in NP is polynomial-time reducible to X (e.g., Boolean SAT, Traveling Salesperson Decision, Clique, Subset Sum)."""
            }
        ])
    },
    {
        'subject_code': 'CS3451',
        'subject_name': 'Operating Systems',
        'department': 'CSE',
        'semester': 4,
        'title': 'Operating Systems: Architecture, Kernels & Concurrency Mastery',
        'author': 'Dr. R. Vijay Anand (Associate Professor / Computing)',
        'edition': 'Autonomous 2025 Edition',
        'pages': 348,
        'summary': 'Comprehensive academic textbook covering OS structures, Process Management, CPU Scheduling Algorithms, Synchronization & Semaphores, Deadlocks (Banker Algorithm), Memory Virtualization & Paging, and File System Design.',
        'units_json': json.dumps([
            {
                'unit_number': 1,
                'unit_title': 'Unit I: Operating System Architecture & System Calls',
                'summary': 'Kernel structures (Monolithic vs Microkernel), Dual-mode operation (User vs Kernel Mode), System call interfaces (fork, exec, wait), Interrupt handling.',
                'content': """1.1 OPERATING SYSTEM SERVICES & SYSTEM ARCHITECTURE
An Operating System is a control program that manages computer hardware, allocates resources to user programs, and prevents improper use.
Dual-Mode Operation:
Hardware provides a Mode Bit (0 for Kernel Mode, 1 for User Mode) to protect privileged instructions (I/O execution, disabling interrupts, modifying timer).
Transitions:
User mode -> System Call (trap / software interrupt) -> Kernel mode execution -> Return from trap -> User mode.

1.2 MONOLITHIC VS MICROKERNEL ARCHITECTURES
- Monolithic Kernels (Linux, traditional UNIX): All OS services (scheduler, file system, memory manager, device drivers) execute in kernel space within a single address space. High performance, but a bug in any driver can crash the whole OS.
- Microkernels (Mach, QNX): Minimizes kernel functionality down to IPC, basic memory paging, and low-level scheduling. File systems and network stacks run as user space daemons. High security and fault isolation at the cost of IPC message passing overhead.

1.3 PROCESS CREATION & THE FORK() SYSTEM CALL
In POSIX systems:
- pid = fork(): Clones current process. Returns 0 to the child process, positive PID of child to the parent process, and -1 on error.
- execvp(): Replaces child address space with a new executable.
- wait(): Parent blocks until child terminates, collecting termination status to prevent Zombie processes."""
            },
            {
                'unit_number': 2,
                'unit_title': 'Unit II: CPU Scheduling, Concurrency & Synchronization',
                'summary': 'Preemptive vs Non-preemptive Scheduling (FCFS, SJF, Round Robin, Multilevel Feedback Queues), Race Conditions, Semaphores, Mutexes, and Monitors.',
                'content': """2.1 CPU SCHEDULING CRITERIA & ALGORITHMS
Criteria:
- CPU Utilization: Percentage of time CPU is busy.
- Throughput: Number of processes completed per unit time.
- Turnaround Time: Time from submission to completion (Completion Time - Arrival Time).
- Waiting Time: Total time spent in ready queue (Turnaround Time - Burst Time).
- Response Time: Time from submission to first response.

Algorithms:
1. First-Come, First-Served (FCFS): Non-preemptive. Subject to Convoy Effect where short processes wait behind long CPU-bound process.
2. Shortest Job First (SJF) & Shortest Remaining Time First (SRTF): Provably optimal average waiting time. Difficult to know future CPU burst.
3. Round Robin (RR): Preemptive with time quantum q. Ensures fairness. If q is too large, degenerates to FCFS; if q is too small, context switch overhead dominates.
4. Multilevel Feedback Queue (MLFQ): Multiple priority queues with dynamic aging to prevent starvation.

2.2 PROCESS SYNCHRONIZATION & CRITICAL SECTION PROBLEM
The Critical Section is a segment of code where shared resources are accessed.
Requirements for Solution:
1. Mutual Exclusion: At most one process in critical section.
2. Progress: Selection of next process cannot be postponed indefinitely.
3. Bounded Waiting: Bound on number of times other processes enter critical section before a request is granted.

2.3 SEMAPHORES & CLASSICAL PROBLEMS
A Semaphore S is an integer variable accessed only through atomic operations:
- wait(S) / P(S): while (S <= 0); S--;
- signal(S) / V(S): S++;
Binary Semaphore (Mutex) has value 0 or 1; Counting Semaphore manages multiple resource instances.
Classic Problems:
- Producer-Consumer with bounded buffer.
- Readers-Writers problem.
- Dining Philosophers problem."""
            },
            {
                'unit_number': 3,
                'unit_title': 'Unit III: Deadlocks - Prevention, Avoidance & Recovery',
                'summary': 'Deadlock Characterization (Coffman Conditions), Resource Allocation Graphs, Deadlock Prevention, Banker Algorithm for Safe State Detection.',
                'content': """3.1 COFFMAN FOUR CONDITIONS FOR DEADLOCK
A deadlock state occurs if and only if all four conditions hold simultaneously:
1. Mutual Exclusion: At least one resource held in non-shareable mode.
2. Hold and Wait: A process holds at least one resource and is waiting to acquire others.
3. No Preemption: Resources cannot be forcibly taken from a process.
4. Circular Wait: A closed loop of processes {P0, P1, ..., Pn} exists where Pi waits for Pi+1.

3.2 DEADLOCK AVOIDANCE: BANKER'S ALGORITHM
Proposed by Edsger Dijkstra. Requires prior declaration of maximum resources by each process.
Data Structures:
- Available[m]: Available instances of resource type j.
- Max[n][m]: Maximum demand of process i.
- Allocation[n][m]: Currently allocated instances.
- Need[n][m] = Max[i][j] - Allocation[i][j].

Safety Algorithm:
1. Work = Available, Finish[i] = False for all i.
2. Find index i such that: Finish[i] == False and Need[i] <= Work.
   If no such i exists, goto step 4.
3. Work = Work + Allocation[i], Finish[i] = True, goto step 2.
4. If Finish[i] == True for all i, system is in a SAFE state; otherwise, UNSAFE."""
            },
            {
                'unit_number': 4,
                'unit_title': 'Unit IV: Memory Management & Virtual Memory Architecture',
                'summary': 'Logical vs Physical Addresses, Paging, Translation Lookaside Buffer (TLB), Page Fault Handling, Page Replacement Algorithms (FIFO, LRU, Optimal).',
                'content': """4.1 PAGING HARDWARE & ADDRESS TRANSLATION
Paging divides physical memory into fixed-sized frames and logical memory into pages of identical size (typically 4 KB).
Address generated by CPU consists of:
- Page Number (p): Index into the Page Table.
- Page Offset (d): Displacement within the page.
Physical Address = (Frame Number * Page Size) + Offset.

4.2 TRANSLATION LOOKASIDE BUFFER (TLB)
A high-speed associative hardware cache holding recent page-to-frame translations.
Effective Memory Access Time (EAT):
EAT = (Hit Ratio * (TLB Access Time + Memory Access Time)) + ((1 - Hit Ratio) * (TLB Access Time + 2 * Memory Access Time)).

4.3 VIRTUAL MEMORY & PAGE REPLACEMENT ALGORITHMS
Demand Paging loads pages into physical frames only when referenced. A reference to an unmapped page triggers a Page Fault interrupt.
Replacement Algorithms:
1. FIFO: Replaces oldest loaded page. Suffers from Belady's Anomaly (more frames can yield more page faults).
2. Optimal Page Replacement (OPT): Replaces the page that will not be used for the longest period in future. Theoretical benchmark.
3. Least Recently Used (LRU): Replaces the page that has not been referenced for the longest time in the past. Standard practical algorithm."""
            },
            {
                'unit_number': 5,
                'unit_title': 'Unit V: Storage Systems, File Management & Disk Scheduling',
                'summary': 'File System Structures, Inode Concepts, Directory Implementation, Disk Scheduling (FCFS, SSTF, SCAN, C-LOOK), RAID Levels.',
                'content': """5.1 UNIX FILE SYSTEM & INODE ARCHITECTURE
In UNIX-like operating systems, files are represented by an Inode (Index Node) containing:
- File metadata: permissions, owner, size, timestamps.
- Pointers: Direct blocks (0-11), Single Indirect block, Double Indirect block, Triple Indirect block.
Allows fast access to small files while supporting multi-terabyte large files.

5.2 DISK SCHEDULING ALGORITHMS
Magnetic hard disks have mechanical seek time. Disk scheduling minimizes head movement:
- Shortest Seek Time First (SSTF): Serves closest request. Can lead to starvation of distant requests.
- SCAN (Elevator Algorithm): Head sweeps back and forth across platters, servicing requests in current direction.
- C-SCAN / C-LOOK: Sweeps in one direction only, then immediately jumps back to the beginning without servicing on return trip, providing uniform waiting time.

5.3 RAID STORAGE ARCHITECTURES
- RAID 0: Block striping without redundancy. High throughput, zero fault tolerance.
- RAID 1: Disk mirroring. 100% redundancy overhead. High read throughput.
- RAID 5: Block striping with distributed parity. Can tolerate single disk failure with N-1 capacity efficiency."""
            }
        ])
    },
    {
        'subject_code': 'AD3491',
        'subject_name': 'Artificial Intelligence and Machine Learning',
        'department': 'AI&DS',
        'semester': 4,
        'title': 'Artificial Intelligence & Machine Learning: Mathematical Foundations to PyTorch Labs',
        'author': 'Dr. M. Revathi (Chairperson / AI & Data Science)',
        'edition': 'Autonomous 2025 Edition',
        'pages': 390,
        'summary': 'Complete textbook covering Informed & Uninformed Search, Adversarial Games, Supervised Learning (Linear/Logistic Regression, SVM, Decision Trees), Unsupervised Learning (K-Means, PCA, Hierarchical), and Deep Neural Networks with Backpropagation.',
        'units_json': json.dumps([
            {
                'unit_number': 1,
                'unit_title': 'Unit I: Intelligent Agents & Heuristic Search Strategies',
                'summary': 'PEAS Agent descriptions, State Space Search, Uniform Cost Search, A* Algorithm, Admissibility and Consistency of Heuristics, Alpha-Beta Game Trees.',
                'content': """1.1 AGENT ARCHITECTURES & THE PEAS FORMULATION
An Intelligent Agent perceives its environment through sensors and acts upon it through actuators.
PEAS Framework:
- Performance Measure: Success metric.
- Environment: Fully vs Partially observable, Deterministic vs Stochastic, Static vs Dynamic.
- Actuators: Mechanisms of action.
- Sensors: Input capture devices.

1.2 HEURISTIC SEARCH: THE A* ALGORITHM
A* search combines path cost g(n) and heuristic estimate h(n) to goal:
f(n) = g(n) + h(n).
Properties:
- Admissibility: An heuristic h(n) is admissible if it never overestimates the true cost to reach goal: 0 <= h(n) <= h*(n).
- Consistency (Monotonicity): For every node n and successor n' generated by action a: h(n) <= c(n, a, n') + h(n').
Theorem: If h(n) is admissible, A* using Tree-Search is optimal; if h(n) is consistent, A* using Graph-Search is optimal."""
            },
            {
                'unit_number': 2,
                'unit_title': 'Unit II: Supervised Learning - Regression & Classification',
                'summary': 'Cost Functions, Gradient Descent Optimization, Linear Regression, Logistic Regression, Support Vector Machines (Kernel Trick), Decision Trees & Ensembles.',
                'content': """2.1 LINEAR REGRESSION & GRADIENT DESCENT
Hypothesis function: h_theta(x) = theta_0 + theta_1 * x_1 + ... + theta_n * x_n = theta^T * x.
Mean Squared Error (MSE) Cost Function:
J(theta) = (1 / 2m) * sum_{i=1}^m (h_theta(x^(i)) - y^(i))^2.
Gradient Update Rule:
theta_j := theta_j - alpha * (1/m) * sum_{i=1}^m (h_theta(x^(i)) - y^(i)) * x_j^(i).

2.2 SUPPORT VECTOR MACHINES (SVM)
Finds the maximum margin hyperplane separating classes:
Optimization: min (1/2) * ||w||^2 subject to y_i * (w^T * x_i + b) >= 1.
Kernel Trick: Computes inner products in higher-dimensional feature space without explicit transformation:
- Polynomial Kernel: K(x, z) = (x^T * z + c)^d.
- Radial Basis Function (RBF / Gaussian): K(x, z) = exp(-gamma * ||x - z||^2)."""
            },
            {
                'unit_number': 3,
                'unit_title': 'Unit III: Unsupervised Learning - Clustering & Dimensionality Reduction',
                'summary': 'K-Means Algorithm, Centroid Recalculation, Elbow Method, Silhouette Score, Principal Component Analysis (PCA) Eigen-decomposition.',
                'content': """3.1 K-MEANS CLUSTERING MATHEMATICAL FOUNDATIONS
Given dataset X = {x_1, ..., x_n}, partition into k clusters S = {S_1, ..., S_k} minimizing within-cluster sum of squares (WCSS / Inertia):
min sum_{i=1}^k sum_{x in S_i} ||x - mu_i||^2, where mu_i is the mean centroid of cluster S_i.

Algorithm Steps:
1. Initialize k cluster centroids randomly or using k-means++ (probabilistic distance seeding).
2. Assignment Step: Assign each sample x_j to the nearest centroid:
   c^(j) = argmin_i ||x_j - mu_i||^2.
3. Update Step: Recalculate centroids as the arithmetic mean of all assigned points:
   mu_i = (1 / |S_i|) * sum_{x in S_i} x.
4. Repeat steps 2 and 3 until convergence (no centroid movement).

Validation Metrics:
- Silhouette Coefficient s(i) = (b(i) - a(i)) / max(a(i), b(i)), where a(i) is mean intra-cluster distance and b(i) is mean nearest-cluster distance. Ranges from -1 to +1."""
            },
            {
                'unit_number': 4,
                'unit_title': 'Unit IV: Artificial Neural Networks & Deep Learning',
                'summary': 'Perceptron Model, Multi-layer Perceptron (MLP), Activation Functions (ReLU, Sigmoid, Softmax), Backpropagation Algorithm, Optimization (Adam, SGD).',
                'content': """4.1 MULTILAYER PERCEPTRON & ACTIVATIONS
Forward Propagation:
z^[l] = W^[l] * a^[l-1] + b^[l]
a^[l] = g^[l](z^[l])
Activation Functions:
- Sigmoid: sigma(z) = 1 / (1 + exp(-z)). Vanishing gradient for large |z|.
- ReLU (Rectified Linear Unit): f(z) = max(0, z). Fast computation, prevents saturation in positive domain.
- Softmax (Multi-class output): p_i = exp(z_i) / sum_j exp(z_j).

4.2 BACKPROPAGATION & CHAIN RULE
Computes the gradient of cost function J with respect to every weight matrix W^[l]:
delta^[L] = partial J / partial z^[L] = a^[L] - y (for cross-entropy loss with softmax).
For hidden layers l:
delta^[l] = (W^[l+1]^T * delta^[l+1]) * g'^[l](z^[l]).
Weight gradients:
partial J / partial W^[l] = delta^[l] * (a^[l-1])^T."""
            },
            {
                'unit_number': 5,
                'unit_title': 'Unit V: Model Evaluation & Practical Machine Learning Engineering',
                'summary': 'Confusion Matrix, Precision, Recall, F1-Score, ROC-AUC Curve, Cross-Validation, Bias-Variance Tradeoff, Regularization (L1 Lasso, L2 Ridge).',
                'content': """5.1 CONFUSION MATRIX & METRICS
- Accuracy = (TP + TN) / (TP + TN + FP + FN)
- Precision = TP / (TP + FP) (Quality of positive predictions)
- Recall (Sensitivity) = TP / (TP + FN) (Completeness of positive capture)
- F1-Score = 2 * (Precision * Recall) / (Precision + Recall) (Harmonic mean)

5.2 BIAS-VARIANCE TRADEOFF & REGULARIZATION
- High Bias (Underfitting): Model too simplistic. Training error high. Fix: Increase model capacity, add polynomial features.
- High Variance (Overfitting): Model memorizes noise. Test error substantially higher than training error. Fix: Add training data, L2 weight decay (Ridge penalty lambda * ||w||^2), Dropout."""
            }
        ])
    },
    {
        'subject_code': 'CS3391',
        'subject_name': 'Database Management Systems',
        'department': 'IT',
        'semester': 3,
        'title': 'Database Management Systems: Relational Theory, SQL & Transaction Architecture',
        'author': 'Dr. S. Kavitha & Prof. M. Bhuvanesh (Database Systems Group)',
        'edition': 'Autonomous 2025 Edition',
        'pages': 335,
        'summary': 'Comprehensive textbook covering ER modeling, Relational Algebra, SQL DDL/DML/DCL, Functional Dependencies & Normalization (1NF to BCNF), Transaction ACID Properties, Concurrency Control (2PL, Timestamps), and B+ Tree Indexing.',
        'units_json': json.dumps([
            {
                'unit_number': 1,
                'unit_title': 'Unit I: Relational Model & Database Architecture',
                'summary': 'Three-schema architecture, Data Independence, Relational Data Model, Integrity Constraints, Relational Algebra operations.',
                'content': """1.1 THREE-SCHEMA ARCHITECTURE & DATA INDEPENDENCE
The ANSI/SPARC 3-level architecture:
1. External Schema: Individual user and application views.
2. Conceptual Schema: Global logical structure of entire database (entities, relationships, data types).
3. Internal Schema: Physical storage structure, file organizations, and index access paths.
Physical Data Independence allows altering physical storage without rewriting conceptual schema; Logical Data Independence protects external applications when conceptual schema evolves.

1.2 RELATIONAL ALGEBRA FUNDAMENTAL OPERATORS
- Selection (sigma_P(R)): Selects rows satisfying predicate P.
- Projection (pi_{A1..An}(R)): Extracts designated columns, eliminating duplicate tuples.
- Cartesian Product (R x S): Combines each tuple of R with each tuple of S.
- Union (R cup S): Set union; requires union-compatible schemas.
- Set Difference (R - S): Tuples in R not in S.
- Rename (rho_S(R)): Renames relation or attributes.
Join Operators: Natural Join (bowtie), Theta Join, Left/Right/Full Outer Joins."""
            },
            {
                'unit_number': 2,
                'unit_title': 'Unit II: SQL Declarative Language, Joins & Subqueries',
                'summary': 'SQL DDL, DML, Nested subqueries, Group By / Having aggregations, Views, Triggers, and Stored Procedures.',
                'content': """2.1 ADVANCED SQL QUERY PATTERNS
Correlated Subquery Example:
SELECT e.name, e.salary, e.dept_id
FROM Employees e
WHERE e.salary > (
    SELECT AVG(e2.salary)
    FROM Employees e2
    WHERE e2.dept_id = e.dept_id
);
The inner query executes once for each candidate row of outer query.

2.2 GROUP BY & HAVING FILTERING
HAVING filters aggregated groups, while WHERE filters individual tuples prior to aggregation.
Execution order:
FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY."""
            },
            {
                'unit_number': 3,
                'unit_title': 'Unit III: Functional Dependencies & Database Normalization',
                'summary': 'Inference Rules (Armstrong Axioms), 1NF, 2NF, 3NF, Boyce-Codd Normal Form (BCNF), Lossless Join & Dependency Preservation.',
                'content': """3.1 ARMSTRONG'S AXIOMS FOR FUNCTIONAL DEPENDENCIES
Given schema R and set of FDs F:
1. Reflexivity: If Y subset of X, then X -> Y.
2. Augmentation: If X -> Y, then XZ -> YZ.
3. Transitivity: If X -> Y and Y -> Z, then X -> Z.
Derived Rules: Union (X -> Y and X -> Z implies X -> YZ), Decomposition, Pseudo-transitivity.

3.2 NORMAL FORMS DEFINITIONS
- First Normal Form (1NF): All attribute domains contain only atomic (indivisible) values. No repeating groups.
- Second Normal Form (2NF): In 1NF and every non-prime attribute is fully functionally dependent on every candidate key (no partial dependencies).
- Third Normal Form (3NF): In 2NF and for every non-trivial FD X -> Y, either X is a superkey or Y is a prime attribute (no transitive dependencies).
- Boyce-Codd Normal Form (BCNF): For EVERY non-trivial FD X -> Y, X MUST be a superkey."""
            },
            {
                'unit_number': 4,
                'unit_title': 'Unit IV: Transaction Management & Concurrency Control',
                'summary': 'ACID Properties, Serializability, Two-Phase Locking (2PL), Strict 2PL, Deadlock Prevention (Wait-Die, Wound-Wait), Timestamp Ordering.',
                'content': """4.1 THE ACID PROPERTIES
- Atomicity: All operations in transaction succeed, or all are rolled back. Maintained by Write-Ahead Logging (WAL).
- Consistency: Execution of transaction in isolation preserves database integrity constraints.
- Isolation: Concurrent transactions cannot observe each other's uncommitted intermediate updates.
- Durability: Once committed, updates persist even across system crashes.

4.2 TWO-PHASE LOCKING (2PL)
A transaction obtains locks in two phases:
1. Growing Phase: Locks acquired, none released.
2. Shrinking Phase: Locks released, none acquired.
Theorem: Any schedule generated by 2PL is Conflict-Serializable.
Strict 2PL: Holds all exclusive (write) locks until the transaction commits, preventing Cascading Aborts."""
            },
            {
                'unit_number': 5,
                'unit_title': 'Unit V: Physical Storage, Indexing & Query Optimization',
                'summary': 'File Organization, Dense vs Sparse Indexing, B+ Trees Search/Insert/Delete, Query Tree Cost Estimation.',
                'content': """5.1 B+ TREE INDEX ARCHITECTURE
A balanced multi-way search tree of order m:
- All data records (or record pointers) reside exclusively in leaf nodes.
- Leaf nodes are linked together via pointers to support efficient range scans.
- Internal nodes contain only routing keys and child pointers.
Search, insertion, and deletion complexity: O(log_m N) where N is number of data entries. Typical disk block can store hundreds of keys per node, keeping tree depth <= 3 or 4."""
            }
        ])
    },
    {
        'subject_code': 'CS3591',
        'subject_name': 'Computer Networks',
        'department': 'CSE',
        'semester': 5,
        'title': 'Computer Networks: Protocols, Routing & Systems Engineering',
        'author': 'Dr. R. Vijay Anand & Department Network Systems Faculty',
        'edition': 'Autonomous 2025 Edition',
        'pages': 355,
        'summary': 'Comprehensive textbook covering OSI/TCP-IP 5-layer architecture, Error Detection (CRC), MAC protocols, IPv4/IPv6 Subnetting, Routing Algorithms (OSPF, RIP, BGP), TCP Congestion Control, and Network Security.',
        'units_json': json.dumps([
            {
                'unit_number': 1,
                'unit_title': 'Unit I: Layered Architecture & Physical Media',
                'summary': 'OSI 7-Layer model vs TCP/IP 5-layer model, Transmission media, Bandwidth-delay product, Packet switching vs Circuit switching.',
                'content': """1.1 PACKET SWITCHING VS CIRCUIT SWITCHING
Circuit Switching reserves dedicated physical transmission path for entire connection duration (e.g. legacy telephone network). Guarantees bandwidth, but wastes idle capacity.
Packet Switching divides messages into packets forwarded hop-by-hop. Maximizes link utilization through Statistical Multiplexing, but introduces Queuing Delay and Packet Loss during congestion."""
            },
            {
                'unit_number': 2,
                'unit_title': 'Unit II: Data Link Layer & Medium Access Control',
                'summary': 'Framing, Error Detection (Cyclic Redundancy Check - CRC), Sliding Window Protocols (Stop-and-Wait, Go-Back-N, Selective Repeat), CSMA/CD.',
                'content': """2.1 CYCLIC REDUNDANCY CHECK (CRC)
Binary polynomial division.
Let D be the k-bit data word and G be the (r+1)-bit generator polynomial.
1. Append r zeros to D, forming D * 2^r.
2. Divide D * 2^r by G using modulo-2 arithmetic (XOR).
3. The remainder R is the CRC checksum.
4. Transmitted codeword = D * 2^r + R. Receiver divides codeword by G; remainder is 0 if no transmission error."""
            },
            {
                'unit_number': 3,
                'unit_title': 'Unit III: Network Layer - IP Addressing & Routing Protocols',
                'summary': 'IPv4 Addressing, Subnet Masks, CIDR Notation, IPv6 Transition, Distance Vector Routing (Bellman-Ford), Link State Routing (Dijkstra/OSPF).',
                'content': """3.1 CLASSLESS INTER-DOMAIN ROUTING (CIDR) & SUBNETTING
An IPv4 address is 32 bits divided into Network ID and Host ID by a subnet mask.
CIDR Notation /24 means 24 network bits, leaving 8 host bits (256 addresses - 2 reserved = 254 usable hosts).

3.2 ROUTING ALGORITHMS
- Distance Vector Routing: Each router maintains a vector of distances to all nodes, sharing periodically with neighbors. Prone to Count-to-Infinity problem (solved by Split Horizon and Poison Reverse).
- Link State Routing (OSPF): Each router floods its local link states to all routers in autonomous system using Link State Advertisements (LSAs), builds identical topology database, and runs Dijkstra's algorithm."""
            },
            {
                'unit_number': 4,
                'unit_title': 'Unit IV: Transport Layer - TCP & Congestion Control',
                'summary': 'UDP Sockets, TCP 3-Way Handshake, Flow Control (Sliding Window), Congestion Control (Slow Start, Congestion Avoidance, Fast Retransmit, Fast Recovery).',
                'content': """4.1 TCP THREE-WAY HANDSHAKE & CONNECTION TERMINATION
Handshake:
1. Client sends SYN (seq = x).
2. Server responds SYN-ACK (seq = y, ack = x + 1).
3. Client sends ACK (ack = y + 1).

4.2 TCP CONGESTION CONTROL (AIMD)
Additive Increase, Multiplicative Decrease:
- Slow Start: Congestion Window (cwnd) doubles every RTT (exponential growth) until Slow Start Threshold (ssthresh).
- Congestion Avoidance: cwnd increases by 1 MSS per RTT (linear growth).
- Loss Event (Triple Duplicate ACK): Fast Retransmit missing segment, cut ssthresh = cwnd / 2, enter Fast Recovery."""
            },
            {
                'unit_number': 5,
                'unit_title': 'Unit V: Application Layer & Network Security',
                'summary': 'DNS Resolution, HTTP/1.1 vs HTTP/2 vs HTTP/3 (QUIC), TLS/SSL Cryptographic Handshake, Public-Key Cryptography (RSA).',
                'content': """5.1 DNS HIERARCHICAL ARCHITECTURE
Root DNS Servers -> Top-Level Domain (TLD) Servers (.edu, .com) -> Authoritative DNS Servers.
Recursive queries resolution: Client asks local resolver; resolver traverses hierarchy iteratively.

5.2 TRANSPORT LAYER SECURITY (TLS 1.3)
Protects communications with confidentiality, integrity, and authenticity.
Uses asymmetric Diffie-Hellman / RSA for session key exchange and symmetric AES-GCM for fast bulk data encryption."""
            }
        ])
    },
    {
        'subject_code': 'MA3354',
        'subject_name': 'Discrete Mathematics',
        'department': 'CSE',
        'semester': 3,
        'title': 'Discrete Mathematics: Mathematical Structures for Computing',
        'author': 'Department of Mathematics & Theoretical Computing',
        'edition': 'Autonomous 2025 Edition',
        'pages': 310,
        'summary': 'Comprehensive textbook covering Propositional & Predicate Logic, Proof Techniques, Set Theory & Relations, Permutations & Combinations, Pigeonhole Principle, Recurrence Relations, Graph Theory, and Algebraic Structures (Groups, Rings).',
        'units_json': json.dumps([
            {
                'unit_number': 1,
                'unit_title': 'Unit I: Propositional & Predicate Logic',
                'summary': 'Truth Tables, Tautologies, Normal Forms (CNF/DNF), Rules of Inference, Quantifiers (Universal and Existential), Mathematical Induction.',
                'content': """1.1 PROPOSITIONAL LOGIC & EQUIVALENCES
A proposition is a declarative statement that is either True or False.
Logical Connectives:
- Negation (~p), Conjunction (p and q), Disjunction (p or q), Conditional (p -> q), Biconditional (p <-> q).
Tautology: Formula that evaluates to True under all truth value assignments.
De Morgan's Laws:
~(p and q) equiv ~p or ~q
~(p or q) equiv ~p and ~q

1.2 MATHEMATICAL INDUCTION
Principle of Mathematical Induction to prove P(n) holds for all positive integers n:
1. Base Step: Verify P(1) is true.
2. Inductive Hypothesis: Assume P(k) is true for arbitrary integer k >= 1.
3. Inductive Step: Prove that P(k) implies P(k+1) is true.
Conclusion: P(n) holds for all n in Z+."""
            },
            {
                'unit_number': 2,
                'unit_title': 'Unit II: Combinatorics & Recurrence Relations',
                'summary': 'Permutations, Combinations, Generalized Pigeonhole Principle, Solving Linear Homogeneous Recurrence Relations with Constant Coefficients.',
                'content': """2.1 PIGEONHOLE PRINCIPLE
If k + 1 or more objects are placed into k boxes, then at least one box must contain two or more objects.
Generalized Principle: If N objects are placed into k boxes, then at least one box contains at least ceil(N / k) objects.

2.2 RECURRENCE RELATIONS
Linear Homogeneous Recurrence of degree 2:
a_n = c_1 * a_{n-1} + c_2 * a_{n-2}.
Characteristic Equation: r^2 - c_1 * r - c_2 = 0.
Roots r_1, r_2:
- Distinct Real Roots: a_n = A * (r_1)^n + B * (r_2)^n.
- Equal Roots (r_1 = r_2 = r): a_n = (A + B * n) * r^n."""
            },
            {
                'unit_number': 3,
                'unit_title': 'Unit III: Relations & Boolean Algebra',
                'summary': 'Binary Relations, Equivalence Relations, Partial Ordering Relations (Posets), Hasse Diagrams, Lattices and Boolean Algebras.',
                'content': """3.1 EQUIVALENCE RELATIONS
A relation R on set A is an Equivalence Relation if and only if it is:
1. Reflexive: (a, a) in R for all a in A.
2. Symmetric: (a, b) in R implies (b, a) in R.
3. Transitive: (a, b) in R and (b, c) in R implies (a, c) in R.
Equivalence classes partition set A into disjoint subsets."""
            },
            {
                'unit_number': 4,
                'unit_title': 'Unit IV: Graph Theory & Trees',
                'summary': 'Graph Isomorphism, Euler Paths and Circuits, Hamiltonian Cycles, Planar Graphs (Euler Formula V - E + R = 2), Chromatic Number.',
                'content': """4.1 EULERIAN & HAMILTONIAN GRAPHS
- An Eulerian trail visits every EDGE exactly once. A connected graph has an Euler circuit if and only if every vertex has an EVEN degree.
- A Hamiltonian cycle visits every VERTEX exactly once. (NP-Complete decision problem in general graphs).
- Euler's Planar Formula: For any connected planar graph: V - E + F = 2."""
            },
            {
                'unit_number': 5,
                'unit_title': 'Unit V: Algebraic Structures & Group Theory',
                'summary': 'Semigroups, Monoids, Groups, Abelian Groups, Subgroups, Cosets, Lagrange Theorem, Homomorphisms and Rings.',
                'content': """5.1 DEFINITION OF A GROUP
An algebraic structure (G, *) is a Group if:
1. Closure: a * b in G for all a, b in G.
2. Associativity: (a * b) * c = a * (b * c).
3. Identity Element: Exists e in G such that a * e = e * a = a.
4. Inverse Element: For each a in G, exists a^(-1) in G such that a * a^(-1) = a^(-1) * a = e.
If commutative (a * b = b * a), it is an Abelian Group.
Lagrange's Theorem: The order of every subgroup H divides the order of finite group G: |G| = |H| * [G : H]."""
            }
        ])
    }
]
