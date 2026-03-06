from collections import deque
from typing import Optional, List
class TreeNode:
    def __init__(self, val: int = 0, left: "TreeNode" = None, right: "TreeNode" = None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.max_sum = float("-inf")
        def dfs(node: Optional[TreeNode]) -> int:
            if not node:
                return 0
            left_gain = max(dfs(node.left), 0)
            right_gain = max(dfs(node.right), 0)

            current_sum = node.val + left_gain + right_gain
            self.max_sum = max(self.max_sum, current_sum)

            return node.val + max(left_gain, right_gain)
        dfs(root)
        return self.max_sum
def build_tree(level_order: List[Optional[int]]) -> Optional[TreeNode]:
    """
    Build a binary tree from a level-order list representation.
    Example: [1, 2, 3, None, None, 4, 5]
    """
    if not level_order or level_order[0] is None:
        return None
    root = TreeNode(level_order[0])
    q = deque([root])
    i = 1
    while q and i < len(level_order):
        node = q.popleft()
        if i < len(level_order) and level_order[i] is not None:
            node.left = TreeNode(level_order[i])
            q.append(node.left)
        i += 1
        if i < len(level_order) and level_order[i] is not None:
            node.right = TreeNode(level_order[i])
            q.append(node.right)
        i += 1
    return root
if __name__ == "__main__":
    sol = Solution()
    root1 = build_tree([1, 2, 3])
    print("Example 1 Output:", sol.maxPathSum(root1)) 
    root2 = build_tree([-10, 9, 20, None, None, 15, 7])
    print("Example 2 Output:", sol.maxPathSum(root2))  