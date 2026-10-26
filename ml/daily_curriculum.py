# 30-Day Engineering Curriculum & Daily Course Roadmap

DAILY_COURSE_ROADMAP = [
    {
        'day': 1,
        'subject_code': 'CS3351',
        'subject_name': 'Data Structures',
        'title': 'Linear Lists & Abstract Data Types (ADT)',
        'description': 'Understand ADT definitions, dynamic memory allocation in C/Python, and memory models of Arrays vs Linked Lists.',
        'duration_mins': 45,
        'badge': 'Core Foundation'
    },
    {
        'day': 2,
        'subject_code': 'CS3351',
        'subject_name': 'Data Structures',
        'title': 'Singly & Doubly Linked Lists Implementations',
        'description': 'Implement insertion, deletion, reversal, and circular traversal algorithms with pointer manipulation.',
        'duration_mins': 50,
        'badge': 'Algorithms'
    },
    {
        'day': 3,
        'subject_code': 'CS3351',
        'subject_name': 'Data Structures',
        'title': 'Stack ADT & Expression Evaluation',
        'description': 'Master Infix to Postfix conversion using Shunting-Yard algorithm and stack-based postfix evaluation.',
        'duration_mins': 45,
        'badge': 'Exam High-Yield'
    },
    {
        'day': 4,
        'subject_code': 'CS3351',
        'subject_name': 'Data Structures',
        'title': 'Queue ADT & Circular Buffer Systems',
        'description': 'Circular queue front/rear modulo pointer math, double-ended queue (Deque), and Priority Queues.',
        'duration_mins': 40,
        'badge': 'Core Foundation'
    },
    {
        'day': 5,
        'subject_code': 'CS3351',
        'subject_name': 'Data Structures',
        'title': 'Binary Tree Traversals (Inorder, Preorder, Postorder)',
        'description': 'Master recursive and iterative DFS traversals, BFS level-order traversal, and expression tree construction.',
        'duration_mins': 55,
        'badge': 'Hands-on Code'
    },
    {
        'day': 6,
        'subject_code': 'CS3351',
        'subject_name': 'Data Structures',
        'title': 'Binary Search Trees (BST) Operations',
        'description': 'Implement BST search, insert, predecessor/successor lookup, and two-child deletion handling.',
        'duration_mins': 50,
        'badge': 'Algorithms'
    },
    {
        'day': 7,
        'subject_code': 'CS3351',
        'subject_name': 'Data Structures',
        'title': 'Self-Balancing AVL Trees & Rotations',
        'description': 'Master LL, RR, LR, RL single and double tree rotations and balance factor calculations.',
        'duration_mins': 60,
        'badge': 'Challenging'
    },
    {
        'day': 8,
        'subject_code': 'CS3451',
        'subject_name': 'Operating Systems',
        'title': 'OS Architecture, Kernel Modes & System Calls',
        'description': 'Dual-mode CPU hardware protection, context switches, interrupt vector tables, and fork() process creation.',
        'duration_mins': 45,
        'badge': 'System Concepts'
    },
    {
        'day': 9,
        'subject_code': 'CS3451',
        'subject_name': 'Operating Systems',
        'title': 'CPU Scheduling: FCFS, SJF & Round Robin',
        'description': 'Solve Gantt charts, calculate Turnaround Time, Waiting Time, and analyze Convoy effect and quantum tuning.',
        'duration_mins': 50,
        'badge': 'Exam High-Yield'
    },
    {
        'day': 10,
        'subject_code': 'CS3451',
        'subject_name': 'Operating Systems',
        'title': 'Concurrency, Race Conditions & Semaphores',
        'description': 'Critical section criteria, Peterson algorithm, Mutex locks, and Producer-Consumer synchronization.',
        'duration_mins': 55,
        'badge': 'Core Foundation'
    },
    {
        'day': 11,
        'subject_code': 'CS3451',
        'subject_name': 'Operating Systems',
        'title': 'Deadlocks & Dijkstra Banker Algorithm',
        'description': 'Coffman 4 conditions, Resource Allocation Graphs, and step-by-step Banker safety vector calculations.',
        'duration_mins': 50,
        'badge': 'Problem Solving'
    },
    {
        'day': 12,
        'subject_code': 'CS3451',
        'subject_name': 'Operating Systems',
        'title': 'Memory Virtualization & Paging Hardware',
        'description': 'Page tables, Frame translation, Translation Lookaside Buffer (TLB) hit ratios, and Effective Access Time (EAT).',
        'duration_mins': 45,
        'badge': 'Architecture'
    },
    {
        'day': 13,
        'subject_code': 'CS3451',
        'subject_name': 'Operating Systems',
        'title': 'Virtual Memory & Page Replacement (FIFO, LRU, OPT)',
        'description': 'Simulate Belady anomaly, analyze LRU stack algorithms, and calculate page fault frequencies.',
        'duration_mins': 50,
        'badge': 'Numerical Practice'
    },
    {
        'day': 14,
        'subject_code': 'CS3391',
        'subject_name': 'Database Systems',
        'title': 'Relational Algebra & Schema Design',
        'description': 'Selection, Projection, Cartesian Product, Natural Join, Theta Join, and relational tuple calculus.',
        'duration_mins': 45,
        'badge': 'Core Foundation'
    },
    {
        'day': 15,
        'subject_code': 'CS3391',
        'subject_name': 'Database Systems',
        'title': 'Complex SQL & Correlated Subqueries',
        'description': 'Master Nested queries, Group By with Having clauses, correlated subqueries, and window functions.',
        'duration_mins': 60,
        'badge': 'Practical Lab'
    },
    {
        'day': 16,
        'subject_code': 'CS3391',
        'subject_name': 'Database Systems',
        'title': 'Functional Dependencies & Normalization (1NF, 2NF, 3NF)',
        'description': 'Armstrong axioms, attribute closures, candidate key identification, and partial/transitive dependency elimination.',
        'duration_mins': 55,
        'badge': 'Exam High-Yield'
    },
    {
        'day': 17,
        'subject_code': 'CS3391',
        'subject_name': 'Database Systems',
        'title': 'Boyce-Codd Normal Form (BCNF) & Decompositions',
        'description': 'Lossless join decomposition verification and dependency preservation testing.',
        'duration_mins': 50,
        'badge': 'Advanced Theory'
    },
    {
        'day': 18,
        'subject_code': 'CS3391',
        'subject_name': 'Database Systems',
        'title': 'Transaction Management & ACID Properties',
        'description': 'Write-ahead logging (WAL), dirty reads, non-repeatable reads, and serializability testing.',
        'duration_mins': 45,
        'badge': 'System Concepts'
    },
    {
        'day': 19,
        'subject_code': 'CS3391',
        'subject_name': 'Database Systems',
        'title': 'Concurrency Control: Two-Phase Locking (2PL)',
        'description': 'Rigorous analysis of 2PL, Strict 2PL, cascading abort prevention, and deadlock detection graphs.',
        'duration_mins': 50,
        'badge': 'Theoretical'
    },
    {
        'day': 20,
        'subject_code': 'AD3491',
        'subject_name': 'AI & Machine Learning',
        'title': 'State Space Search & A* Heuristic Algorithm',
        'description': 'PEAS frameworks, admissibility/consistency proofs for heuristics, and path cost optimization.',
        'duration_mins': 50,
        'badge': 'AI Principles'
    },
    {
        'day': 21,
        'subject_code': 'AD3491',
        'subject_name': 'AI & Machine Learning',
        'title': 'Linear Regression & Gradient Descent Optimization',
        'description': 'Cost function math, vectorization in Python NumPy, learning rate tuning, and feature scaling.',
        'duration_mins': 55,
        'badge': 'Math & Code'
    },
    {
        'day': 22,
        'subject_code': 'AD3491',
        'subject_name': 'AI & Machine Learning',
        'title': 'Logistic Regression & Classification Metrics',
        'description': 'Sigmoid activation, binary cross-entropy loss, Confusion Matrix, Precision, Recall, and ROC-AUC curve.',
        'duration_mins': 50,
        'badge': 'Exam High-Yield'
    },
    {
        'day': 23,
        'subject_code': 'AD3491',
        'subject_name': 'AI & Machine Learning',
        'title': 'K-Means Clustering & PCA Dimensionality Reduction',
        'description': 'Mathematical centroid recalculation, Inertia elbow curve, Silhouette analysis, and Eigen-projection.',
        'duration_mins': 60,
        'badge': 'Core ML Model'
    },
    {
        'day': 24,
        'subject_code': 'AD3491',
        'subject_name': 'AI & Machine Learning',
        'title': 'Neural Networks & Backpropagation Calculus',
        'description': 'Forward pass, activation functions (ReLU, Sigmoid, Softmax), chain rule partial derivatives, and weight updates.',
        'duration_mins': 65,
        'badge': 'Deep Learning'
    },
    {
        'day': 25,
        'subject_code': 'CS3591',
        'subject_name': 'Computer Networks',
        'title': 'OSI vs TCP/IP Models & Packet Switching',
        'description': 'Packet framing, encapsulation, header overheads, and statistical multiplexing fundamentals.',
        'duration_mins': 45,
        'badge': 'Networking'
    },
    {
        'day': 26,
        'subject_code': 'CS3591',
        'subject_name': 'Computer Networks',
        'title': 'CRC Checksums & Sliding Window Protocols',
        'description': 'Modulo-2 polynomial division CRC calculation, Stop-and-Wait, Go-Back-N, and Selective Repeat.',
        'duration_mins': 50,
        'badge': 'Numerical Practice'
    },
    {
        'day': 27,
        'subject_code': 'CS3591',
        'subject_name': 'Computer Networks',
        'title': 'IPv4 Addressing, Subnet Masks & CIDR Calculations',
        'description': 'Subnetting classful and classless blocks, broadcast address calculation, and host capacity planning.',
        'duration_mins': 55,
        'badge': 'Exam High-Yield'
    },
    {
        'day': 28,
        'subject_code': 'CS3591',
        'subject_name': 'Computer Networks',
        'title': 'Routing Protocols: OSPF (Link State) vs RIP (Distance Vector)',
        'description': 'Dijkstra shortest path algorithm vs Bellman-Ford count-to-infinity problem and BGP autonomous peering.',
        'duration_mins': 50,
        'badge': 'Protocols'
    },
    {
        'day': 29,
        'subject_code': 'CS3591',
        'subject_name': 'Computer Networks',
        'title': 'TCP 3-Way Handshake & Congestion Control (AIMD)',
        'description': 'Slow Start, Congestion Avoidance, Fast Retransmit, and Fast Recovery Reno/Cubic state machines.',
        'duration_mins': 50,
        'badge': 'High Impact'
    },
    {
        'day': 30,
        'subject_code': 'MA3354',
        'subject_name': 'Discrete Math',
        'title': 'Graph Isomorphism, Euler Circuits & Final Synthesis',
        'description': 'Euler circuit degree criteria, Hamiltonian path complexity, mathematical induction, and semester recap.',
        'duration_mins': 60,
        'badge': 'Capstone Review'
    }
]
