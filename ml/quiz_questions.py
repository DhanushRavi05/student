# Online Assessment & Timed Examination Question Bank

QUIZ_SUBJECTS = {
    'CS3351': 'Data Structures & Algorithms',
    'CS3451': 'Operating Systems',
    'CS3391': 'Database Management Systems',
    'AD3491': 'Artificial Intelligence & Machine Learning',
    'CS3591': 'Computer Networks'
}

QUIZ_QUESTIONS = [
    # Data Structures
    {
        'id': 1,
        'subject_code': 'CS3351',
        'question': 'What is the worst-case time complexity of searching an element in a balanced AVL tree with n nodes?',
        'options': ['O(1)', 'O(log n)', 'O(n)', 'O(n log n)'],
        'correct_idx': 1,
        'explanation': 'Because an AVL tree maintains a balance factor in {-1, 0, 1} for all nodes, its height is strictly bounded by approximately 1.44 log2(n). Thus, search, insertion, and deletion are guaranteed O(log n) worst-case.'
    },
    {
        'id': 2,
        'subject_code': 'CS3351',
        'question': 'Which data structure is fundamentally utilized by the Dijkstra single-source shortest path algorithm to achieve O((V + E) log V) time complexity?',
        'options': ['LIFO Stack', 'FIFO Circular Queue', 'Binary Min-Heap / Priority Queue', 'Hash Table with Open Addressing'],
        'correct_idx': 2,
        'explanation': 'A binary min-heap allows extracting the minimum distance vertex in O(log V) time and relaxing edges with decrease-key in O(log V), yielding total complexity O((V + E) log V).'
    },
    {
        'id': 3,
        'subject_code': 'CS3351',
        'question': 'In a binary search tree (BST), which traversal produces the keys in strictly monotonically ascending sorted order?',
        'options': ['Preorder Traversal', 'Inorder Traversal', 'Postorder Traversal', 'Level Order (BFS) Traversal'],
        'correct_idx': 1,
        'explanation': 'Inorder traversal visits (Left Subtree, Root, Right Subtree). By BST definition, all keys in the left subtree are smaller than root, and all in the right subtree are larger, producing sorted order.'
    },
    # Operating Systems
    {
        'id': 4,
        'subject_code': 'CS3451',
        'question': 'Which of the following is NOT one of the Coffman conditions required for a deadlock to occur?',
        'options': ['Mutual Exclusion', 'Preemptive Resource Allocation', 'Hold and Wait', 'Circular Wait'],
        'correct_idx': 1,
        'explanation': 'The Coffman condition is "No Preemption" (resources cannot be forcibly taken). If preemptive resource allocation is supported, deadlock cannot occur.'
    },
    {
        'id': 5,
        'subject_code': 'CS3451',
        'question': 'Belady\'s Anomaly refers to the counter-intuitive phenomenon where increasing physical page frames leads to more page faults. Which page replacement algorithm suffers from Belady\'s Anomaly?',
        'options': ['Least Recently Used (LRU)', 'Optimal Page Replacement (OPT)', 'First-In, First-Out (FIFO)', 'Most Recently Used (MRU) Stack Algorithm'],
        'correct_idx': 2,
        'explanation': 'FIFO is not a stack algorithm and can exhibit Belady\'s anomaly. Stack algorithms like LRU and OPT are mathematically proven to be immune.'
    },
    {
        'id': 6,
        'subject_code': 'CS3451',
        'question': 'In Unix/Linux systems, what is the exact return value of the fork() system call in the newly created child process?',
        'options': ['-1', '0', 'The PID of the parent process', 'A random positive integer above 1000'],
        'correct_idx': 1,
        'explanation': 'fork() returns 0 to the child process, the child\'s PID to the parent process, and -1 on system failure.'
    },
    # Database Systems
    {
        'id': 7,
        'subject_code': 'CS3391',
        'question': 'A relation R is in Boyce-Codd Normal Form (BCNF) if and only if for every non-trivial functional dependency X -> Y:',
        'options': ['Y is a prime attribute', 'X is a candidate key / superkey', 'X and Y have the same cardinality', 'Y is functionally dependent on the primary key'],
        'correct_idx': 1,
        'explanation': 'BCNF requires that for EVERY non-trivial FD X -> Y, X MUST be a superkey. Unlike 3NF, BCNF does not allow exceptions where Y is prime.'
    },
    {
        'id': 8,
        'subject_code': 'CS3391',
        'question': 'Which ACID property guarantees that once a database transaction commits, its modifications are permanently recorded even in the event of an immediate power outage?',
        'options': ['Atomicity', 'Consistency', 'Isolation', 'Durability'],
        'correct_idx': 3,
        'explanation': 'Durability ensures committed data survives subsequent system crashes, typically implemented via non-volatile Write-Ahead Logging (WAL) and checkpointing.'
    },
    {
        'id': 9,
        'subject_code': 'CS3391',
        'question': 'What is the primary architectural difference between B-Trees and B+ Trees in database storage engines?',
        'options': ['B+ Trees have no root node', 'In B+ Trees, all actual data pointers/records reside exclusively in the leaf nodes', 'B-Trees cannot balance dynamically', 'B+ Trees do not support range queries'],
        'correct_idx': 1,
        'explanation': 'In B+ Trees, internal nodes only store routing keys, and all data records/pointers reside in leaf nodes, which are linked together in a doubly-linked list for fast range scanning.'
    },
    # AI & Machine Learning
    {
        'id': 10,
        'subject_code': 'AD3491',
        'question': 'In the K-Means clustering algorithm, how are new cluster centroids updated during each iteration?',
        'options': ['By selecting the median point along the principal axis', 'By computing the arithmetic mean of all data points currently assigned to that cluster', 'By running PCA on each cluster partition', 'By taking the outer boundary convex hull'],
        'correct_idx': 1,
        'explanation': 'Centroids are recalculated as mu_i = (1 / |S_i|) * sum_{x in S_i} x, which is the arithmetic mean of all vectors assigned to cluster S_i.'
    },
    {
        'id': 11,
        'subject_code': 'AD3491',
        'question': 'Which metric is defined as the harmonic mean of Precision and Recall?',
        'options': ['ROC-AUC Score', 'Silhouette Coefficient', 'F1-Score', 'Mean Absolute Error (MAE)'],
        'correct_idx': 2,
        'explanation': 'F1-Score = 2 * (Precision * Recall) / (Precision + Recall). It balances false positives and false negatives, especially in imbalanced datasets.'
    },
    {
        'id': 12,
        'subject_code': 'AD3491',
        'question': 'A heuristic function h(n) in A* search is said to be admissible if:',
        'options': ['It always overestimates the cost to goal by at least 1', 'It never overestimates the actual minimal cost to reach the goal state', 'It equals the path cost g(n) at all nodes', 'It is non-differentiable'],
        'correct_idx': 1,
        'explanation': 'Admissibility means 0 <= h(n) <= h*(n) for all nodes n, where h*(n) is the true cost to reach goal. An admissible heuristic guarantees A* optimality in tree search.'
    },
    # Computer Networks
    {
        'id': 13,
        'subject_code': 'CS3591',
        'question': 'In Classless Inter-Domain Routing (CIDR), how many total usable host IP addresses are available in a /26 subnet block?',
        'options': ['64', '62', '128', '126'],
        'correct_idx': 1,
        'explanation': 'A /26 subnet leaves 32 - 26 = 6 host bits. 2^6 = 64 total addresses. Subtracting 2 reserved addresses (1 network ID + 1 broadcast address) yields 62 usable hosts.'
    },
    {
        'id': 14,
        'subject_code': 'CS3591',
        'question': 'What are the three flags exchanged in the correct sequence during a standard TCP Three-Way Connection Handshake?',
        'options': ['ACK -> SYN -> FIN', 'SYN -> SYN-ACK -> ACK', 'FIN -> ACK -> FIN-ACK', 'RST -> SYN -> ACK'],
        'correct_idx': 1,
        'explanation': 'Client sends SYN, server responds with SYN-ACK, and client completes handshake with ACK.'
    },
    {
        'id': 15,
        'subject_code': 'CS3591',
        'question': 'Which routing protocol utilizes the Dijkstra shortest path algorithm over an identical link-state database flooded across an Autonomous System?',
        'options': ['Routing Information Protocol (RIP)', 'Border Gateway Protocol (BGP)', 'Open Shortest Path First (OSPF)', 'Address Resolution Protocol (ARP)'],
        'correct_idx': 2,
        'explanation': 'OSPF is a Link-State routing protocol. Routers exchange Link State Advertisements (LSAs) and run Dijkstra\'s algorithm locally to compute the shortest-path tree.'
    }
]
