from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=10,
    slug="buy-sell-stock",
    title="Best Time to Buy and Sell Stock",
    meta="Striver A2Z · Arrays Playlist #10 · 9:11 · youtube.com/watch?v=excAOvwF_Wk",
    tag="ARRAYS · PART 10",
    topic="one transaction max profit",
)


def build(P):
    P.h2("Problem", color=TEAL)
    P.p("`prices[i]` = price on day i. Buy once, sell once **later**. Max profit. "
        "`{7,1,5,3,6,4}` -> `5` (buy at 1, sell at 6). `{7,6,4,3,1}` -> `0`.")

    P.h2("1 · Brute — try every (buy, sell) pair", color=RED)
    P.code("cpp", """
int best = 0;
for (int i = 0; i < n; i++)
    for (int j = i + 1; j < n; j++)
        best = max(best, prices[j] - prices[i]);
""", caption="O(n^2) · what you must beat")

    P.h2("2 · Optimal — carry the cheapest day", color=GREEN)
    P.p("Selling today is best against the **cheapest day so far**. So keep `minPrice` updated as you "
        "walk, and ask every day: 'profit if I sold today?'")
    P.code("cpp", """
int minPrice = prices[0], best = 0;
for (int i = 1; i < n; i++) {
    best = max(best, prices[i] - minPrice);   // sell today?
    minPrice = min(minPrice, prices[i]);      // or a new record low
}
return best;
""", caption="O(n) · O(1) space")
    P.dryrun("Dry run on {7,1,5,3,6,4}",
             ["day", "price", "minPrice", "profit if sold", "best"],
             [["0", "7", "7", "-", "0"],
              ["1", "1", "1", "0", "0"],
              ["2", "5", "1", "4", "4"],
              ["3", "3", "1", "2", "4"],
              ["4", "6", "1", "5", "5"],
              ["5", "4", "1", "3", "5"]],
             "best = 5, from buying at the running minimum.")
    P.arr([7, 1, 5, 3, 6, 4], marks={1: GREEN, 4: RED}, captions={1: "buy", 4: "sell"}, label="prices[]")
    P.callout("trick", "the invariant in words",
              "'The best sell day pairs with the minimum price strictly before it.' You never need the "
              "future — only the cheapest past. That is why one forward pass is enough.")
    P.callout("interview", "follow-ups to expect",
              "k transactions / cooldown / fee are DP (the video is DP 35 in the full course), but for ONE "
              "transaction this O(n) scan is optimal — prove it: any answer is some (i,j) pair you examined.")
    P.chips(["brute O(n^2)/O(1)", "optimal O(n)/O(1)"])
    P.divider()
    P.h2("Cheat sheet — video 10", color=PURPLE)
    P.table(["Approach", "Idea", "TC/SC"],
            [["Every pair", "nested loops", "O(n^2)/O(1)"],
             ["Running minimum", "profit = price - minSoFar", "O(n)/O(1)"]],
            fracs=[0.3, 0.44, 0.26])
