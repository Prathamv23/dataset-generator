import random
import hashlib
from typing import Optional


# ─────────────────────────────────────────────
# ANSWER TEMPLATE BANKS
# Each domain has: correct_templates, partial_templates, incorrect_templates
# Multiple variants per type ensure output diversity.
# ─────────────────────────────────────────────

ANSWER_BANK: dict[str, dict[str, list[str]]] = {

    # ── OOP ──────────────────────────────────────────────────────────────────
    "OOP": {
        "correct": [
            "Polymorphism allows objects of different classes to be treated as objects of a common superclass. "
            "It enables a single interface to represent different underlying forms, such as method overriding in "
            "subclasses or method overloading. For example, a `Shape` class can have an `area()` method that "
            "is overridden differently by `Circle` and `Rectangle` subclasses.",

            "Encapsulation bundles data (attributes) and behavior (methods) into a single unit called a class "
            "and restricts direct access to some of an object's components. This is typically done using access "
            "modifiers like private or protected. It improves maintainability and protects object integrity.",

            "Inheritance allows a child class to acquire the properties and methods of a parent class, "
            "enabling code reuse. For example, a `Dog` class can inherit from `Animal`, reusing its `eat()` "
            "and `sleep()` methods while adding its own `bark()` method.",

            "A class is a blueprint that defines the structure and behavior of objects. An object is a "
            "concrete instance of that class. For example, `Car` is a class; `my_car = Car()` creates an object.",

            "Method overriding occurs when a subclass provides a specific implementation for a method already "
            "defined in its parent class. Method overloading means defining multiple methods with the same name "
            "but different parameters — Python handles this with default/variable arguments.",

            "SOLID stands for: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, "
            "and Dependency Inversion. These five principles guide writing maintainable, scalable OOP code. "
            "For example, Single Responsibility means a class should have only one reason to change.",

            "Abstract classes define a template with abstract methods that must be implemented by subclasses. "
            "Interfaces (in Python via ABCs) declare method signatures without implementation. The difference: "
            "abstract classes can have concrete methods; interfaces are purely contracts.",

            "Design patterns are reusable solutions to common software design problems. The Singleton pattern, "
            "for example, ensures a class has only one instance and provides a global access point to it. "
            "The Factory pattern creates objects without specifying the exact class to instantiate."
        ],
        "partial": [
            "Polymorphism is when different classes can use the same method name. It helps with flexibility "
            "but I'm not entirely sure about all the details like compile-time vs runtime polymorphism.",

            "Encapsulation is about keeping data inside a class. I know it uses private variables but I'm "
            "not fully clear on how access modifiers work across different languages.",

            "Inheritance lets one class use methods from another class. I know it helps with code reuse "
            "but I'm not sure about the differences between single and multiple inheritance.",

            "A class defines attributes and methods, and objects are created from it. I think objects are "
            "instances but I'm not confident about memory allocation details.",

            "Overriding is when a child class changes a parent method. Overloading I think is similar but "
            "I'm not sure of the exact distinction in Python specifically.",

            "SOLID has something to do with good OOP design principles. I remember Single Responsibility "
            "and Open/Closed but I can't recall all five principles clearly.",

            "Abstract classes can't be instantiated directly and have some unimplemented methods. "
            "I think interfaces are similar but I'm not sure exactly how Python implements them.",

            "Design patterns are templates for solving common problems. I've heard of Singleton and Factory "
            "but I haven't used them in practice so I only have a surface-level understanding."
        ],
        "incorrect": [
            "Polymorphism means an object can store multiple values at the same time, like a list. "
            "It's mainly used for data storage in OOP.",

            "Encapsulation means combining two classes together into one to save memory. "
            "It's a way to merge functionality across classes.",

            "Inheritance means a child class completely replaces the parent class. Once you inherit, "
            "the parent class is no longer used.",

            "A class and an object are the same thing in Python. You use the keywords interchangeably "
            "when writing code.",

            "Overriding and overloading are the same concept — both mean changing a method's behavior "
            "in a subclass.",

            "SOLID is a testing framework used to verify OOP code correctness. It stands for different "
            "types of unit test strategies.",

            "Abstract classes and interfaces are identical in Python. There is no practical difference "
            "between using one or the other.",

            "Design patterns are Python built-in libraries you import to solve specific problems, "
            "like `import singleton` or `import factory`."
        ]
    },

    # ── Python ────────────────────────────────────────────────────────────────
    "Python": {
        "correct": [
            "Lists are mutable ordered collections while tuples are immutable. Lists use square brackets "
            "`[1, 2, 3]` and support item assignment; tuples use parentheses `(1, 2, 3)` and cannot be "
            "changed after creation. Tuples are faster and can be used as dictionary keys.",

            "Decorators are functions that wrap another function to extend its behavior without modifying it. "
            "Using `@decorator_name` syntax, they intercept the function call. A common example is `@staticmethod` "
            "or a custom `@timer` decorator that measures execution time.",

            "The GIL (Global Interpreter Lock) is a mutex in CPython that allows only one thread to execute "
            "Python bytecode at a time. It prevents race conditions in memory management but limits true "
            "multi-threading parallelism. Solutions include multiprocessing or using C extensions.",

            "A generator is a function that yields values lazily using the `yield` keyword instead of "
            "returning all at once. It saves memory for large sequences. Example: `def count(): yield 1; yield 2`.",

            "List comprehension provides a concise way to create lists. Example: `[x**2 for x in range(10)]` "
            "creates a list of squares. It's faster than a for-loop and more Pythonic.",

            "Shallow copy creates a new object but references the same nested objects. Deep copy recursively "
            "copies all nested objects too. Use `copy.copy()` for shallow and `copy.deepcopy()` for deep copy.",

            "*args captures extra positional arguments as a tuple; **kwargs captures extra keyword arguments "
            "as a dictionary. Example: `def func(*args, **kwargs)` accepts any number of positional and "
            "keyword arguments."
        ],
        "partial": [
            "Lists can be changed but tuples can't. I know tuples use parentheses but I'm not sure "
            "about performance differences or when to prefer one over the other.",

            "Decorators modify a function's behavior. I've used `@staticmethod` before but writing "
            "custom decorators is something I haven't done much.",

            "The GIL is something to do with Python threads being limited. I know it affects performance "
            "in some way but I'm not clear on the technical mechanism.",

            "Generators yield values one at a time. I know they save memory but I haven't used them "
            "extensively in real projects.",

            "List comprehension is a shorter way to write a for-loop inside a list. Like `[x for x in range(5)]`. "
            "I use it often but don't know all the advanced forms like nested comprehensions.",

            "Shallow copy copies the object but deep copy also copies nested objects. I sometimes confuse "
            "which one to use in practice.",

            "*args is for variable positional arguments and **kwargs for keyword arguments. I use them "
            "occasionally but I'm not confident about combining them with regular parameters."
        ],
        "incorrect": [
            "Lists and tuples are identical in Python. The only difference is the brackets used — "
            "square brackets vs parentheses — but functionally they behave the same.",

            "Decorators are used to add comments to functions in Python. They don't change behavior, "
            "they just annotate the function for documentation purposes.",

            "The GIL is a Python library used for multi-processing. You import it when you need to "
            "run parallel computations.",

            "A generator is a class that generates random numbers. It's used primarily in data science "
            "for creating synthetic datasets.",

            "List comprehension is a built-in Python function called `listcomp()`. You pass it an "
            "iterable and it returns a new list.",

            "Deep copy and shallow copy refer to memory depth in arrays — shallow copies only the first "
            "dimension and deep copies all dimensions.",

            "*args means the function accepts no arguments at all. **kwargs means it accepts only "
            "keyword arguments defined in the function signature."
        ]
    },

    # ── Data Structures ───────────────────────────────────────────────────────
    "Data Structures": {
        "correct": [
            "A stack is a LIFO (Last In First Out) structure — think of stacking plates. A queue is FIFO "
            "(First In First Out) — like a line at a bank. Stacks use `push`/`pop`; queues use `enqueue`/`dequeue`.",

            "A hash map stores key-value pairs using a hash function to compute an index (bucket) for each key. "
            "This gives O(1) average-case lookup. Collisions are handled via chaining or open addressing.",

            "A BST is a binary tree where every left child is smaller than its parent and every right child "
            "is larger. This property enables O(log n) search, insert, and delete on average for balanced trees.",

            "BFS (Breadth-First Search) explores nodes level by level using a queue, good for shortest paths. "
            "DFS (Depth-First Search) explores as deep as possible before backtracking, using a stack or recursion.",

            "A linked list is a sequence of nodes where each node holds data and a pointer to the next node. "
            "It's preferred over arrays when frequent insertions/deletions at arbitrary positions are needed, "
            "since no shifting is required.",

            "A heap is a complete binary tree satisfying the heap property: in a max-heap, every parent is "
            "greater than its children. Heaps are used for priority queues and HeapSort. Operations like "
            "insert and extract-min/max are O(log n)."
        ],
        "partial": [
            "A stack is LIFO and a queue is FIFO. I know the difference conceptually but I'm not always "
            "sure which Python data structure to use to implement them efficiently.",

            "A hash map uses a hash function to store key-value pairs. I understand the basic concept "
            "but collision handling details like chaining vs probing are fuzzy for me.",

            "A BST organizes data so left is smaller and right is larger. I understand searching but "
            "I'm less confident about balancing operations like AVL or Red-Black trees.",

            "BFS uses a queue and DFS uses a stack or recursion. I know the difference but I sometimes "
            "confuse when to use which for specific problem types.",

            "A linked list stores elements as nodes connected by pointers. I understand the concept but "
            "I'm not confident implementing all operations like reversing it in-place.",

            "A heap is some kind of tree used for priority queues. I know the basic idea but heapify "
            "and the internal implementation details are not fully clear to me."
        ],
        "incorrect": [
            "A stack and a queue are the same thing. Both follow FIFO order and the only difference "
            "is that stacks are used in Python and queues are used in Java.",

            "A hash map stores data sorted alphabetically. The hash function just assigns the position "
            "based on the first letter of the key.",

            "A BST is a binary tree where each node has exactly two children. All nodes must be "
            "filled before the tree can be used for searching.",

            "BFS and DFS are sorting algorithms. BFS sorts from the root and DFS sorts from leaves "
            "of a tree structure.",

            "A linked list is just another name for a Python list. They are interchangeable and "
            "have the same performance characteristics.",

            "A heap is a type of database that stores data in chunks called heaps. It's mainly "
            "used for disk-based storage in database management systems."
        ]
    },

    # ── Algorithms ────────────────────────────────────────────────────────────
    "Algorithms": {
        "correct": [
            "QuickSort has an average-case time complexity of O(n log n) and a worst-case of O(n²) "
            "when the pivot selection is poor (e.g., always picking the smallest element on a sorted array). "
            "It's in-place and cache-friendly, making it fast in practice.",

            "Binary search works on a sorted array by repeatedly halving the search space. It compares "
            "the target with the middle element, then searches left or right half. Time complexity: O(log n).",

            "Dynamic programming solves complex problems by breaking them into overlapping subproblems and "
            "storing results (memoization/tabulation) to avoid redundant computation. Classic examples: "
            "Fibonacci, Longest Common Subsequence, Knapsack problem.",

            "Recursion is when a function calls itself with a smaller input until a base case is reached. "
            "Example: `def factorial(n): return 1 if n == 0 else n * factorial(n-1)`. It's elegant but "
            "can cause stack overflow for large inputs without optimization."
        ],
        "partial": [
            "QuickSort is O(n log n) on average. I know it's faster than BubbleSort but I'm not fully "
            "clear on how the pivot selection affects worst-case performance.",

            "Binary search divides the array in half each time. I know it requires a sorted array "
            "and is O(log n) but I sometimes struggle implementing it without off-by-one errors.",

            "Dynamic programming is about solving problems by breaking them into subproblems. I understand "
            "memoization conceptually but I find it hard to identify DP problems from scratch.",

            "Recursion is when a function calls itself. I understand it conceptually and have used it "
            "for simple cases like factorials but complex recursive algorithms are still challenging."
        ],
        "incorrect": [
            "QuickSort always has O(n log n) complexity in all cases. It's considered the best sorting "
            "algorithm with no downsides compared to MergeSort.",

            "Binary search works on any unsorted array. You just check elements one by one from both "
            "ends simultaneously to make it fast.",

            "Dynamic programming means your program adapts at runtime. It's a Python feature where "
            "variables automatically change type based on the context.",

            "Recursion means a program runs in a loop. It's the same as a while loop but uses "
            "different syntax."
        ]
    },

    # ── Databases ─────────────────────────────────────────────────────────────
    "Databases": {
        "correct": [
            "SQL databases are relational, use structured schemas with tables and enforce ACID properties. "
            "NoSQL databases (like MongoDB, Redis) are non-relational, schema-flexible, and scale horizontally. "
            "SQL is better for complex queries; NoSQL for unstructured, high-volume data.",

            "Normalization is the process of organizing a database to reduce redundancy and improve integrity. "
            "It involves decomposing tables into smaller ones and defining relationships. Normal forms (1NF, 2NF, 3NF) "
            "are guidelines for this process.",

            "A database index is a data structure (often a B-tree) that speeds up data retrieval by allowing "
            "the database engine to find rows without full table scans. The tradeoff is slower write operations "
            "and extra storage.",

            "A primary key uniquely identifies each row in a table and cannot be NULL. A foreign key is a "
            "column that references the primary key of another table, establishing a relationship between tables."
        ],
        "partial": [
            "SQL uses tables and is good for structured data. NoSQL is more flexible. I know the basic "
            "differences but I haven't worked with both in a production environment.",

            "Normalization removes duplicate data in a database. I know about 1NF and 2NF but I'm not "
            "fully confident explaining 3NF or BCNF.",

            "An index makes queries faster. I understand the benefit but I'm not sure exactly how the "
            "underlying data structure works or when NOT to add an index.",

            "A primary key uniquely identifies a row. A foreign key connects tables. I understand the "
            "concept but I sometimes confuse referential integrity rules."
        ],
        "incorrect": [
            "SQL and NoSQL are basically the same. NoSQL just uses a different query language syntax "
            "but stores data in tables just like SQL.",

            "Normalization means converting all text columns to normal casing (uppercase or lowercase). "
            "It's a formatting operation for consistency.",

            "An index is a backup copy of your table. Databases use it when the main table is locked "
            "or unavailable during high traffic.",

            "A primary key is the first column in any table by default. A foreign key is a key "
            "that comes from a foreign (external) database."
        ]
    },

    # ── Web Development ───────────────────────────────────────────────────────
    "Web Development": {
        "correct": [
            "A REST API is an architectural style for networked applications using HTTP methods (GET, POST, "
            "PUT, DELETE) to perform CRUD operations on resources identified by URLs. It is stateless — "
            "each request contains all information needed to process it.",

            "GET retrieves data from a server and should be idempotent and safe (no side effects). POST "
            "submits data to create a resource, is not idempotent, and the data is sent in the request body. "
            "GET parameters appear in the URL; POST data does not.",

            "CORS (Cross-Origin Resource Sharing) is a browser security mechanism that restricts web pages "
            "from making requests to a different domain than the one that served the page. It exists to "
            "prevent malicious sites from reading data from another site. Servers configure allowed origins "
            "via response headers."
        ],
        "partial": [
            "A REST API uses HTTP methods to interact with resources over the web. I've used GET and POST "
            "but I'm not fully clear on REST constraints like statelessness or HATEOAS.",

            "GET fetches data and POST sends data. I know POST is for forms and GET for retrieval but "
            "I'm not sure about idempotency differences.",

            "CORS is a browser security policy about cross-domain requests. I've encountered CORS errors "
            "before but I'm not always sure how to properly configure it on the server side."
        ],
        "incorrect": [
            "A REST API is a Python framework for building web applications, similar to Django or Flask. "
            "It's installed via `pip install rest`.",

            "GET and POST are identical in terms of security and function. The only difference is that "
            "GET is faster because it's older technology.",

            "CORS is a type of database encryption. It stands for Cryptographic Online Record Security "
            "and is used to protect stored data."
        ]
    },

    # ── Machine Learning ──────────────────────────────────────────────────────
    "Machine Learning": {
        "correct": [
            "Supervised learning uses labeled data — both input features and output labels are provided "
            "for training. Unsupervised learning uses unlabeled data to find hidden patterns or structure. "
            "Examples: classification (supervised), clustering (unsupervised).",

            "Overfitting occurs when a model learns the training data too well, including noise, leading "
            "to poor generalization on unseen data. It's prevented using regularization (L1/L2), dropout, "
            "early stopping, or cross-validation.",

            "Gradient descent is an optimization algorithm that minimizes a loss function by iteratively "
            "moving in the direction of the steepest descent (negative gradient). The learning rate controls "
            "step size. Variants include SGD, Mini-batch GD, and Adam optimizer.",

            "Cross-validation (especially k-fold) splits data into k subsets, trains the model k times "
            "each time using a different subset as validation. It gives a more reliable estimate of model "
            "generalization than a single train/test split."
        ],
        "partial": [
            "Supervised learning has labeled data and unsupervised doesn't. I know examples like regression "
            "and clustering but I'm fuzzy on semi-supervised or reinforcement learning.",

            "Overfitting means the model performs well on training data but badly on test data. I know "
            "regularization helps but I can't always explain the math behind L1 vs L2.",

            "Gradient descent updates model weights to minimize loss. I understand the concept but "
            "I'm not confident explaining adaptive optimizers like Adam.",

            "Cross-validation splits data to test model performance more reliably. I understand k-fold "
            "but I'm unsure about stratified k-fold or leave-one-out CV."
        ],
        "incorrect": [
            "Supervised and unsupervised learning refer to whether a human is watching the training "
            "process. Supervised means a developer monitors the training in real-time.",

            "Overfitting means the model didn't train long enough. You fix it by running more epochs "
            "and using a larger learning rate.",

            "Gradient descent is a graph visualization technique used to plot the loss curve during "
            "training. It doesn't affect the model weights.",

            "Cross-validation means running the model multiple times on the same training data "
            "with different random seeds to improve accuracy."
        ]
    }
}

# ─────────────────────────────────────────────
# FALLBACK TEMPLATES  (for unknown domains)
# ─────────────────────────────────────────────
FALLBACK_BANK: dict[str, list[str]] = {
    "correct": [
        "This concept involves a well-defined set of principles that ensure reliability and correctness. "
        "It is widely used in industry because it provides clear, testable guarantees. For example, applying "
        "this approach reduces bugs and improves maintainability.",

        "The correct way to approach this is by understanding the underlying theory first, then applying it "
        "systematically. It follows established best practices and is validated through real-world usage."
    ],
    "partial": [
        "I have a general understanding of this topic. I know the basic idea and have encountered it in "
        "coursework, but some of the advanced details or edge cases are not fully clear to me yet.",

        "I'm somewhat familiar with this concept. I understand the high-level purpose but I'd need to "
        "review the specifics before applying it confidently in a production environment."
    ],
    "incorrect": [
        "I believe this works by directly modifying the system memory at runtime, which allows it to "
        "bypass normal execution flow and improve performance.",

        "This is a built-in operating system feature that Python automatically uses in the background. "
        "Developers don't need to interact with it directly."
    ]
}


class AnswerGenerator:
    """
    Generates synthetic interview answers for a given question.

    Each call to `generate_answers()` returns a list of 3 answer dicts:
    one for each label (correct, partial, incorrect).

    EXTENSIBILITY:
    - To plug in an LLM API: override `_generate_correct_answer()` etc.
    - The rest of the pipeline (validator, exporter) does not need changes.
    """

    def __init__(self, seed: Optional[int] = None):
        """
        Args:
            seed: Optional random seed for reproducibility during testing.
        """
        if seed is not None:
            random.seed(seed)
        # Track used answers per (domain, label) to reduce repetition
        self._used: dict[str, set[str]] = {}

    # ──────────────────────────────────────────
    # PUBLIC API
    # ──────────────────────────────────────────

    def generate_answers(self, question_obj: dict) -> list[dict]:
        """
        Main entry point. Given one question dict, returns 3 labeled answer dicts.

        Args:
            question_obj: {"question": str, "domain": str, "difficulty": str}

        Returns:
            List of 3 dicts each matching the output schema.
        """
        question = question_obj["question"]
        domain   = question_obj.get("domain", "General")
        difficulty = question_obj.get("difficulty", "medium")

        results = []
        for label in ["correct", "partial", "incorrect"]:
            answer_text = self._pick_answer(domain, label)
            results.append({
                "question":   question,
                "answer":     answer_text,
                "label":      label,          # ← deterministic, never guessed
                "domain":     domain,
                "difficulty": difficulty
            })

        return results

    # ──────────────────────────────────────────
    # PRIVATE HELPERS
    # ──────────────────────────────────────────

    def _pick_answer(self, domain: str, label: str) -> str:
        """
        Picks a random answer from the domain bank, avoiding recent repeats.
        Falls back to the generic bank if the domain is unknown.

        Label assignment: labels are set BEFORE this call in `generate_answers`.
        This function only retrieves text — it never decides the label.
        """
        # Determine which pool to use
        bank = ANSWER_BANK.get(domain, FALLBACK_BANK)
        pool: list[str] = bank.get(label, FALLBACK_BANK[label])

        # Track used per (domain, label) key
        cache_key = f"{domain}::{label}"
        if cache_key not in self._used:
            self._used[cache_key] = set()

        used_set = self._used[cache_key]

        # Build list of unused answers; if all used, reset (cycle through)
        unused = [a for a in pool if self._fingerprint(a) not in used_set]
        if not unused:
            self._used[cache_key] = set()  # reset cycle
            unused = pool

        chosen = random.choice(unused)
        self._used[cache_key].add(self._fingerprint(chosen))
        return chosen

    @staticmethod
    def _fingerprint(text: str) -> str:
        """Returns a short hash of the answer text for dedup tracking."""
        return hashlib.md5(text.encode()).hexdigest()[:8]
