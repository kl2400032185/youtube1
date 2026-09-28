from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=1,
    slug="arrays-basics-largest-second-largest-remove-duplicates",
    title="Arrays Intro · Largest Element · Second Largest · Remove Duplicates",
    meta="Striver A2Z · Arrays Playlist #1 · 43:26 · youtube.com/watch?v=37E9ckMDdTk",
    tag="ARRAYS · PART 1",
    topic="Arrays basics + largest / 2nd largest + remove duplicates",
)


def build(P):
    P.h2("0 · Array basics (the 5 minutes that save you later)", color=TEAL)
    P.bullets([
        "An array is a **contiguous** block of memory holding elements of the **same type**.",
        "`arr[i]` is not magic — it is just `base_address + i * sizeof(type)`.",
        "Because of that, `arr[i] == *(arr + i)` and even `i[arr]` compiles in C/C++ (joke, but true).",
        "Size is **fixed at compile time** in C/C++ (`int a[5]`), dynamic in Java/Python (`new int[n]` / `list`).",
        "Index always starts at **0**, last valid index is `n-1`. Going outside = **undefined behaviour**, no error thrown.",
    ])
    P.code("cpp", """
int arr[5] = {1, 2, 3, 4, 5};      // static, size fixed = 5
int n; cin >> n;
int b[n];                          // VLA - works in g++, NOT standard C++
vector<int> v(n);                  // the safe / STL way, can push_back
for (int i = 0; i < 5; i++) cout << arr[i] << " ";
int sz = sizeof(arr) / sizeof(arr[0]);   // number of elements = 5
""", caption="declaration, traversal, size", note="2-D: int mat[3][4] -> 3 rows x 4 cols, row-major in memory")
    P.callout("gotcha", "size inside a function",
              "Passing `int arr[]` to a function **decays to a pointer**, so `sizeof(arr)/sizeof(arr[0])` "
              "gives garbage. Always pass `n` along with the array.")

    P.h2("1 · Largest element in the array", color=RED)
    P.p("Problem: given `arr[]` of size n, return the largest element. "
        "This is the warm-up that introduces the idea of **carrying an answer while you walk**.")
    P.flow(["start with arr[0] as max", "walk i = 1 .. n-1", "if arr[i] > max -> max = arr[i]", "return max"])
    P.code("cpp", """
int largest(vector<int> &arr) {
    int maxi = arr[0];                    // seed with the first element
    for (int i = 1; i < arr.size(); i++) {
        if (arr[i] > maxi) maxi = arr[i];
    }
    return maxi;
}
""", caption="optimal")
    P.chips(["TC  O(n)", "SC  O(1)", "1 pass", "no sorting needed"])
    P.callout("note", "why not INT_MIN?",
              "Seeding with `arr[0]` is safer than `INT_MIN`: it works even when every element "
              "is negative, and it never breaks if the array holds `long long` / doubles.")

    P.h2("2 · Second LARGEST element (the main problem)", color=RED)
    P.p("Return the **second largest distinct** element. If it does not exist return `-1`. "
        "Example: `{1, 2, 4, 7, 7, 5}` -> `5` (7 repeats, so the 2nd largest is 5, not 7).")

    P.h3("Brute — sort and walk from the back")
    P.bullets([
        "Sort the array, take `arr[n-1]` as largest, then walk backwards until you find an element "
        "`< largest`. That is the second largest.",
        "Handles duplicates naturally because you **skip equal values**.",
    ])
    P.code("cpp", """
sort(arr.begin(), arr.end());
int largest = arr[n - 1];
int slargest = -1;
for (int i = n - 2; i >= 0; i--) {
    if (arr[i] != largest) { slargest = arr[i]; break; }
}
return slargest;
""", caption="O(n log n) time, O(1) space")

    P.h3("Better — two full passes")
    P.bullets([
        "Pass 1: find the largest. Pass 2: find the maximum among all elements `!= largest`.",
        "`2n` comparisons, still **O(n)**, but you traverse the array twice.",
    ])

    P.h3("Optimal — ONE pass, two variables")
    P.p("Keep `largest` and `slargest` side by side. This is the answer interviewers expect.")
    P.code("cpp", """
int secondLargest(vector<int> &arr) {
    int largest  = arr[0];
    int slargest = -1;                       // nothing found yet
    for (int i = 1; i < arr.size(); i++) {
        if (arr[i] > largest) {              // new champion -> demote the old one
            slargest = largest;
            largest  = arr[i];
        }
        else if (arr[i] < largest) {         // cannot be > largest, but may beat slargest
            if (arr[i] > slargest) slargest = arr[i];
        }
        // arr[i] == largest -> duplicate of champion, ignore it completely
    }
    return slargest;
}
""", caption="optimal · one traversal")
    P.chips(["TC  O(n)", "SC  O(1)", "1 traversal", "handles duplicates"])
    P.callout("trick", "the 3 cases you must memorise",
              "For every element: **(1)** bigger than largest -> push largest down into slargest; "
              "**(2)** smaller than largest -> maybe update slargest; "
              "**(3)** equal to largest -> do nothing (duplicates!). "
              "Forgetting case (3) is THE classic bug.")
    P.dryrun("Dry run on {1, 2, 4, 7, 7, 5}",
             ["i", "arr[i]", "largest", "slargest", "what happened"],
             [["init", "1", "1", "-1", "seed with arr[0]"],
              ["1", "2", "2", "1", "2 > 1 -> demote 1"],
              ["2", "4", "4", "2", "4 > 2 -> demote 2"],
              ["3", "7", "7", "4", "7 > 4 -> demote 4"],
              ["4", "7", "7", "4", "== largest -> skip"],
              ["5", "5", "7", "5", "5 < 7 and 5 > 4 -> update"]],
             "Answer = 5.  Note row i=4: the duplicate 7 never touched slargest.")
    P.arr([1, 2, 4, 7, 7, 5], marks={3: RED, 5: GREEN},
          captions={3: "largest", 5: "slargest"}, label="arr[]")
    P.h3("Mirror question: second SMALLEST")
    P.code("cpp", """
int smallest = arr[0], ssmallest = INT_MAX;
for (int i = 1; i < n; i++) {
    if (arr[i] < smallest)      { ssmallest = smallest; smallest = arr[i]; }
    else if (arr[i] > smallest) { if (arr[i] < ssmallest) ssmallest = arr[i]; }
}
""", caption="same logic, arrows flipped")
    P.callout("gotcha", "edge cases to say out loud",
              "`n < 2` -> no second largest, return -1.  All elements equal `{4,4,4}` -> return -1.  "
              "Negative numbers `{-1,-5,-2}` -> answer is -2 (seed with arr[0], not with 0).")

    P.divider()
    P.h2("3 · Remove duplicates from a SORTED array", color=RED)
    P.p("Duplicates sit **next to each other** because the array is sorted — that is the whole trick. "
        "Do it **in place** and return the new size (LeetCode 26 style).")
    P.h3("Brute — use a set")
    P.bullets([
        "Put everything in a `set` (it keeps unique values, already sorted), copy back into `arr`.",
        "`O(n log n)` time, **O(n) extra space** — fine to mention, then improve it.",
    ])
    P.h3("Optimal — two pointers (slow `i`, fast `j`)", color=GREEN)
    P.bullets([
        "`i` marks the **end of the clean part** of the array. `j` scans everything.",
        "Whenever `arr[j] != arr[i]`, we found a new value: `i++`, then `arr[i] = arr[j]`.",
        "Unique elements end up in `arr[0..i]`, answer length = `i + 1`.",
    ])
    P.code("cpp", """
int removeDuplicates(vector<int> &arr) {
    int i = 0;                                  // last unique element index
    for (int j = 1; j < arr.size(); j++) {
        if (arr[j] != arr[i]) {                 // new distinct value found
            i++;
            arr[i] = arr[j];
        }
    }
    return i + 1;                               // new length
}
""", caption="optimal · in place")
    P.code("py", """
def removeDuplicates(arr):
    i = 0
    for j in range(1, len(arr)):
        if arr[j] != arr[i]:
            i += 1
            arr[i] = arr[j]
    return i + 1
""", caption="python twin")
    P.chips(["TC  O(n)", "SC  O(1)", "in place", "needs SORTED input"])
    P.dryrun("Dry run on {1, 1, 2, 2, 2, 3, 3}",
             ["j", "arr[j]", "arr[i]", "action", "clean part"],
             [["1", "1", "1", "equal -> skip", "[1]"],
              ["2", "2", "1", "diff -> i=1, arr[1]=2", "[1,2]"],
              ["3", "2", "2", "equal -> skip", "[1,2]"],
              ["4", "2", "2", "equal -> skip", "[1,2]"],
              ["5", "3", "2", "diff -> i=2, arr[2]=3", "[1,2,3]"],
              ["6", "3", "3", "equal -> skip", "[1,2,3]"]],
             "return i + 1 = 3 -> {1, 2, 3, ...}")
    P.arr([1, 1, 2, 2, 2, 3, 3], marks={0: GREEN, 2: RED, 5: TEAL},
          captions={0: "i=0", 2: "i=1", 5: "i=2"}, label="arr[] (sorted)")
    P.callout("interview", "what they will ask next",
              "Unsorted array -> hash set (`O(n)` space) or sort first.  "
              "Remove duplicates so each element appears **at most twice** -> keep `i` two steps behind "
              "and compare `arr[j]` with `arr[i-2]` (LeetCode 80).")

    P.divider()
    P.h2("Cheat sheet — video 1", color=PURPLE)
    P.table(["Problem", "Brute", "Optimal", "TC / SC"],
            [["Largest element", "sort -> arr[n-1]", "carry max in 1 pass", "O(n) / O(1)"],
             ["Second largest", "sort + skip dups", "largest + slargest, 1 pass", "O(n) / O(1)"],
             ["Remove dups (sorted)", "set + copy back", "two pointers i, j", "O(n) / O(1)"]],
            fracs=[0.28, 0.24, 0.30, 0.18])
    P.quote("Never sort when a single pass can do it. Sorting is O(n log n); the answer is usually O(n).")
