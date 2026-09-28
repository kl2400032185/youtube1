from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=5,
    slug="two-sum",
    title="2 Sum — pair with given target (both interview flavours)",
    meta="Striver A2Z · Arrays Playlist #5 · 18:20 · youtube.com/watch?v=UXDSeD9mN-k",
    tag="ARRAYS · PART 5",
    topic="two sum: YES/NO flavour and indices flavour",
)


def build(P):
    P.h2("The two flavours of the same question", color=TEAL)
    P.bullets([
        "**Flavour 1 (return YES/NO):** 'does a pair with sum = target exist?'",
        "**Flavour 2 (return INDICES):** LeetCode 1 — return the two positions, 1-indexed or 0-indexed.",
        "Flavour 2 forbids sorting away the original order; that decides the method you pick.",
    ])

    P.h2("1 · Brute — check every pair", color=RED)
    P.code("cpp", """
for (int i = 0; i < n; i++)
    for (int j = i + 1; j < n; j++)
        if (arr[i] + arr[j] == target) return {i, j};   // or return true
""", caption="O(n^2) time · O(1) space · the honest baseline")

    P.h2("2 · Better — sort + two pointers (flavour 1 only)", color=ORANGE)
    P.code("cpp", """
sort(arr.begin(), arr.end());
int l = 0, r = n - 1;
while (l < r) {
    int s = arr[l] + arr[r];
    if (s == target)      return true;     // "YES"
    else if (s < target)  l++;             // need bigger -> go right
    else                  r--;             // need smaller -> go left
}
return false;
""", caption="O(n log n) time · O(1) space · DESTROYS original indices")
    P.callout("gotcha", "why sorting cannot return indices",
              "Sorting rearranges the array, so the positions you found are no longer the original ones. "
              "You could keep `(value, index)` pairs, but then space is O(n) anyway — just use hashing.")

    P.h2("3 · Optimal — hash map 'look for the partner'", color=GREEN)
    P.p("While scanning `arr[i]`, the partner you need is `target - arr[i]`. Have we seen it? "
        "If yes -> done. If no -> remember `arr[i]` (store its index for flavour 2) and move on.")
    P.code("cpp", """
unordered_map<int, int> seen;              // value -> index
for (int i = 0; i < n; i++) {
    int need = target - arr[i];
    if (seen.count(need)) return {seen[need], i};   // flavour 2
    seen[arr[i]] = i;
}
return {-1, -1};
""", caption="one pass · O(n) average · keeps indices")
    P.code("py", """
def twoSum(arr, target):
    seen = {}
    for i, x in enumerate(arr):
        if target - x in seen: return [seen[target - x], i]
        seen[x] = i
    return [-1, -1]
""", caption="python twin")
    P.dryrun("Dry run on {2,6,5,8,11}, target = 14",
             ["i", "arr[i]", "need", "seen?", "action"],
             [["0", "2", "12", "no", "store 2"],
              ["1", "6", "8", "no", "store 6"],
              ["2", "5", "9", "no", "store 5"],
              ["3", "8", "6", "YES at idx 1", "return {1,3}"]],
             "The map answers 'have I met your partner?' in O(1).")
    P.arr([2, 6, 5, 8, 11], marks={1: GREEN, 3: RED}, captions={1: "6", 3: "8"},
          label="target 14 = 6 + 8")
    P.chips(["brute O(n^2)/O(1)", "sort+2ptr O(n log n)/O(1)", "hashmap O(n)/O(n)"])
    P.callout("interview", "duplicates & negative numbers",
              "Hashing handles both for free. With sorting they need care (skip equal pointers, window still "
              "works). Also: this is the template for 3-sum and 4-sum later in the playlist.")
