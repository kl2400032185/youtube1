from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=2,
    slug="rotate-k-union-intersection-move-zeros",
    title="Rotate by K · Move Zeros to End · Union & Intersection",
    meta="Striver A2Z · Arrays Playlist #2 · 1:13:17 · youtube.com/watch?v=wvcQg43_V8U",
    tag="ARRAYS · PART 2",
    topic="rotation tricks, zeros, two-pointer union/intersection",
)


def build(P):
    P.h2("1 · Left rotate by ONE place", color=RED)
    P.bullets([
        "`{1,2,3,4,5}` -> `{2,3,4,5,1}`. Save `arr[0]` in `temp`, shift everyone left, put `temp` at the end.",
    ])
    P.code("cpp", """
int temp = arr[0];
for (int i = 1; i < n; i++) arr[i - 1] = arr[i];
arr[n - 1] = temp;                       // O(n) time, O(1) space
""")

    P.h2("2 · Left rotate by K places", color=RED)
    P.p("Example `k = 2`: `{1,2,3,4,5,6,7}` -> `{3,4,5,6,7,1,2}`. First, always do `k = k % n` "
        "(rotating n times changes nothing; k can be bigger than n).")
    P.h3("Brute — temp array for the first k")
    P.bullets([
        "Copy `arr[0..k-1]` to temp, shift `arr[k..n-1]` left by k, copy temp to the tail.",
        "`O(n)` time but **O(k) space** — the space is what we want to kill.",
    ])
    P.h3("Optimal — the REVERSAL trick (in place)", color=GREEN)
    P.flow(["reverse 0 .. k-1", "reverse k .. n-1", "reverse the WHOLE array"])
    P.code("cpp", """
void reverse(vector<int> &a, int lo, int hi) {
    while (lo < hi) swap(a[lo++], a[hi--]);
}
k = k % n;
reverse(arr, 0, k - 1);
reverse(arr, k, n - 1);
reverse(arr, 0, n - 1);
""", caption="3 reversals · O(n) time · O(1) space")
    P.dryrun("Dry run on {1,2,3,4,5,6,7}, k = 2",
             ["step", "result", "idea"],
             [["rev(0,1)", "{2,1,3,4,5,6,7}", "flip the part that leaves"],
              ["rev(2,6)", "{2,1,7,6,5,4,3}", "flip the part that stays"],
              ["rev(0,6)", "{3,4,5,6,7,1,2}", "one more flip un-does both"]],
             "Two flips + one global flip = a clean rotation. Right rotate = same steps in reverse order.")
    P.arr([1, 2, 3, 4, 5, 6, 7], marks={0: RED, 1: RED, 2: GREEN, 6: GREEN},
          captions={0: "leaves", 2: "stays"}, label="arr[], k = 2")
    P.callout("interview", "right rotate instead?",
              "Right rotate by k == left rotate by `n - k`. Or reverse the WHOLE array first, "
              "then reverse `0..k-1`, then `k..n-1`. Say which one you are doing out loud.")

    P.divider()
    P.h2("3 · Move all zeros to the END", color=RED)
    P.h3("Brute — collect then overwrite")
    P.bullets([
        "Put non-zeros into a temp list, copy back, fill the rest with 0. `O(n)` time, O(n) space.",
    ])
    P.h3("Optimal — two pointers with a SWAP", color=GREEN)
    P.bullets([
        "Step 1: find the position `i` of the **first 0** (if none, done).",
        "Step 2: `j = i+1 .. n-1` — whenever `arr[j] != 0`, `swap(arr[i], arr[j])`, then `i++`.",
        "`i` always points at the next zero waiting to be exchanged; order of non-zeros is preserved.",
    ])
    P.code("cpp", """
int i = 0;
while (i < n && arr[i] != 0) i++;        // first zero
for (int j = i + 1; j < n; j++) {
    if (arr[j] != 0) swap(arr[i++], arr[j]);
}
""", caption="one pass after finding the first zero · O(1) space")
    P.chips(["TC  O(n)", "SC  O(1)", "stable order", "in place"])

    P.divider()
    P.h2("4 · UNION of two sorted arrays", color=TEAL)
    P.p("Union = all distinct elements from both, each once, sorted. `{2,2,3}` + `{1,2,3}` -> `{1,2,2,3}`? "
        "NO -> `{1,2,3}`.  Striver's definition: every element appearing in either, printed once.")
    P.h3("Brute — a set")
    P.bullets(["Insert everything into an ordered `set`; print it. `O((m+n) log(m+n))` time, O(m+n) space."])
    P.h3("Optimal — merge-style two pointers", color=GREEN)
    P.code("cpp", """
int i = 0, j = 0;
while (i < m || j < n) {
    if (j == n || (i < m && a[i] <= b[j])) {
        if (uni.empty() || uni.back() != a[i]) uni.push_back(a[i]);
        i++;
    } else {
        if (uni.empty() || uni.back() != b[j]) uni.push_back(b[j]);
        j++;
    }
}
""", caption="take the smaller side, skip if same as last taken")
    P.chips(["TC  O(m+n)", "SC  O(1) extra (answer aside)"])

    P.h2("5 · INTERSECTION of two sorted arrays", color=TEAL)
    P.h3("Brute — nested loops")
    P.bullets([
        "For each `a[i]`, scan all of `b`; mark used positions to avoid double counting. `O(m*n)` time.",
    ])
    P.h3("Optimal — two pointers walking together", color=GREEN)
    P.code("cpp", """
while (i < m && j < n) {
    if (a[i] < b[j])      i++;             // a[i] too small, it can never match
    else if (a[i] > b[j]) j++;
    else { ans.push_back(a[i]); i++; j++; } // equal -> common element
}
""", caption="sorted input is what makes this possible")
    P.callout("note", "pattern to remember",
              "Union = take the SMALLER pointer every time; Intersection = advance the smaller pointer "
              "until the two become equal. Both are one pass because both arrays are sorted.")
    P.divider()
    P.h2("Cheat sheet — video 2", color=PURPLE)
    P.table(["Problem", "Optimal idea", "TC / SC"],
            [["Rotate by 1", "temp + shift", "O(n) / O(1)"],
             ["Rotate by k", "3 reversals (k%n first!)", "O(n) / O(1)"],
             ["Zeros to end", "swap at first-zero pointer", "O(n) / O(1)"],
             ["Union", "merge pointers + skip dup of last", "O(m+n) / O(1)"],
             ["Intersection", "move smaller ptr until equal", "O(m+n) / O(1)"]],
            fracs=[0.26, 0.46, 0.28])
