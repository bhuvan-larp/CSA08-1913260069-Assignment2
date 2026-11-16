"""Draws the flowchart of the redesigned (bottom-up) solution -> q7_flowchart.png (needs matplotlib)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

fig, ax = plt.subplots(figsize=(6.5, 8))
ax.set_xlim(0, 10); ax.set_ylim(-0.6, 14); ax.axis("off")


def box(x, y, w, h, text, kind="proc"):
    if kind == "term":
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.45", fc="#d6eaf8", ec="black"))
    elif kind == "dec":
        ax.add_patch(Polygon([(x, y + h / 2), (x + w / 2, y), (x, y - h / 2), (x - w / 2, y)], fc="#fdebd0", ec="black"))
    else:
        ax.add_patch(plt.Rectangle((x - w / 2, y - h / 2), w, h, fc="#e8f8f5", ec="black"))
    ax.text(x, y, text, ha="center", va="center", fontsize=9)


def arrow(x1, y1, x2, y2, label=None):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="->"))
    if label:
        ax.text((x1 + x2) / 2 + 0.15, (y1 + y2) / 2, label, fontsize=8)


box(5, 13, 4, 0.9, "START: read n", "term")
arrow(5, 12.55, 5, 11.75)
box(5, 11.3, 5.6, 0.9, "a = 1 (ways(0)),  b = 1 (ways(1))")
arrow(5, 10.85, 5, 10.1)
box(5, 9.5, 5.2, 1.2, "n <= 1 ?", "dec")
arrow(5, 8.9, 5, 8.1, "no")
arrow(7.6, 9.5, 9.2, 9.5, "yes")
box(5, 7.6, 5.6, 0.9, "i = 2")
arrow(5, 7.15, 5, 6.4)
box(5, 5.8, 5.2, 1.2, "i <= n ?", "dec")
arrow(5, 5.2, 5, 4.4, "yes")
box(5, 3.9, 5.6, 0.9, "a, b = b, a + b      (new total = sum of last two)")
ax.annotate("", xy=(1.0, 5.8), xytext=(1.0, 3.9), arrowprops=dict(arrowstyle="-"))
ax.annotate("", xy=(2.4, 5.8), xytext=(1.0, 5.8), arrowprops=dict(arrowstyle="->"))
ax.plot([2.2, 1.0], [3.9, 3.9], color="black", lw=1)
ax.text(0.15, 4.9, "i = i + 1", fontsize=8, rotation=90)
arrow(7.6, 5.8, 9.0, 5.8, "no")
ax.plot([9.0, 9.0], [5.8, 2.3], color="black", lw=1)
ax.plot([9.2, 9.2], [9.5, 2.3], color="black", lw=1)
ax.annotate("", xy=(5.9, 2.0), xytext=(9.0, 2.3), arrowprops=dict(arrowstyle="->"))
box(5, 1.5, 5.4, 0.9, "print b  (= ways(n));  n <= 1 prints 1", "proc")
arrow(5, 1.05, 5, 0.55)
box(5, 0.2, 3.0, 0.6, "END", "term")
ax.set_title("Q7 redesign: bottom-up loop (two variables)", fontsize=10)
fig.savefig("q7_flowchart.png", dpi=130, bbox_inches="tight")
print("saved q7_flowchart.png")
