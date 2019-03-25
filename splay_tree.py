class Node:
    #initializes tree node
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def print_node(self, level=0):
        tree = "\t"*level+str(self.value)+"\n"
        if self.right!=None:
            tree = self.right.print_node(level=level+1) + tree
        if self.left!=None:
            tree += self.left.print_node(level=level+1)
        return tree

    def __str__(self):
        return self.print_node()

class Splay:
    #initializes tree
    def __init__(self):
        self.root = None

    #helps visualize tree
    def __str__(self):
        return str(self.root)

    def rotate_right(self, pivot):
        #          pivot
        #        /      \
        #      left    right
        #     /    \
        # left2   right2

        n = pivot.left
        #       n
        #     /  \
        # left2  right2

        pivot.left = n.right
        #          pivot
        #        /      \
        #     right2    right

        n.right = pivot
        #         left
        #        /    \
        #     left2   pivot
        #            /    \
        #         right2   right

        return n

    def rotate_left(self, pivot):
        #          pivot
        #        /      \
        #      left    right
        #             /     \
        #          left2   right2

        n = pivot.right
        pivot.right = n.left
        n.left = pivot
        #         right
        #        /    \
        #     pivot   right2
        #    /     \
        # left    left2

        return n

    #splays value in tree rooted at Node pivot.
    #if value in tree, it's splayed to root.
    #if value isn't in pivot's tree, the
    #last node searched becomes root
    def splay(self, pivot, value):
        #there's no tree at pivot
        if pivot==None:
            return None

        #value is smaller than root
        if value < pivot.value:
            #value is not in tree.
            #since value was smaller than root,
            #and root has no left branch
            #theres nothing to splay
            if pivot.left==None:
                return pivot

            #splaying deals with both children
            #and grandchildren so we have to
            #check children of left node

            #left grandchild
            if value < pivot.left.value:
                #         pivot
                #        /    \
                #     left   right
                #    /    \
                # left2  right2

                #splay value up to the left left grandchild
                pivot.left.left = self.splay(pivot.left.left, value)
                #         pivot
                #        /    \
                #     left   right
                #    /    \
                # value  right2

                #rotate right around pivot once to bring value higher
                pivot = self.rotate_right(pivot)
                #         pivot
                #        /     \
                #     value   old_pivot
                #            /       \
                #         right2    right

            #right grandchild
            elif value > pivot.left.value:
                #         pivot
                #        /    \
                #     left   right
                #    /    \
                # left2  right2

                #splay value up to the left right grandchild
                pivot.left.right = self.splay(pivot.left.right, value)
                #         pivot
                #        /    \
                #     left   right
                #    /    \
                # left2  value

                #since rotate_left deals with the right's children,
                #we have to check
                if pivot.left.right!=None:
                    pivot.left = self.rotate_left(pivot.left)
                    #         pivot
                    #        /    \
                    #     value   right
                    #    /     \
                    # left    right3

                #else, pivot.left.right is None:
                #         pivot
                #        /    \
                #     left   right
                #    /
                # left2

            #in the case that value < pivot.left,
            #and left became the new pivot,
            #we check if pivot.left (aka value)
            #is None
            if pivot.left == None:
                return pivot

            #otherwise, we have to bring value
            #up one move level
            else:
                return self.rotate_right(pivot)

        #value is greater than root
        elif value > pivot.value:
            if pivot.right == None:
                return pivot

            if value < pivot.right.value:
                pivot.right.left = self.splay(pivot.right.left, value)
                if pivot.right.left != None:
                    pivot.right = self.rotate_right(pivot.right)
            elif value > pivot.right.value:
                pivot.right.right = self.splay(pivot.right.right, value)
                pivot = self.rotate_left(pivot)

            if pivot.right == None:
                return pivot
            else:
                return self.rotate_left(pivot)

        #if value was equal to pivot's value
        #there's nothing to splay
        else:
            return pivot

    #inserts value into tree
    def insert(self, value):
        #if tree is empty
        if self.root==None:
            self.root = Node(value)
            return

        #splay the value node to the root.
        #if value is not in tree, the
        #last node searched becomes root
        self.root = self.splay(self.root, value)

        #if the value wasn't in the tree,
        #the root is now either < or > than value.
        #we insert the value accordingly
        if value < self.root.value:
            #     root
            #   /     \
            # left    right

            n = Node(value)
            n.left = self.root.left
            #     n
            #   /
            # left

            n.right = self.root
            #     n
            #   /   \
            # left  root
            #      /    \
            #    left   right

            self.root.left = None
            #     n
            #   /   \
            # left  root
            #           \
            #           right

            #sets self.root to the new root, n
            self.root = n

        elif value > self.root.value:
            n = Node(value)
            n.right = self.root.right
            n.left = self.root
            self.root.right = None
            self.root = n
            #         n
            #       /   \
            #    root  right
            #    /
            # left

        else:
            print("value already in tree")

        #print(str(self))
        #print("-------------------------------------------------------------")

    def remove(self, value):
        #tree empty, cant remove anything
        if self.root == None:
            return

        #value node splayed to root
        #if value is not in tree, the
        #last node searched becomes root
        self.root = self.splay(self.root, value)

        #if value was in tree, remove it
        if self.root.value == value:
            if self.root.left == None:
                #     value
                #          \
                #          right
                #        /      \
                #     left2    right2

                self.root = self.root.right
                #      right
                #    /      \
                # left2    right2

            else:
                #           value
                #         /      \
                #      left     right
                #    /     \
                # left2   right2

                n = self.root.right
                self.root = self.root.left
                #      root
                #    /     \
                # left2   right2

                #since value was already splayed,
                #and root is now root.left,
                #value does not exist in the current tree
                #and all nodes in are less than value
                self.root = self.splay(self.root, value)
                #          last_searched
                #         /
                #    new_left

                self.root.right = n
                #           last_searched
                #         /              \
                #    new_left            right

        #value was not in tree
        else:
            print("value not in tree")

    def get(self, value):
        self.root = self.splay(self.root, value)
        if value == self.root.value:
            return self.root.value
        else:
            return None

def main():
    splay_tree = Splay()
    splay_tree.insert(3)
    splay_tree.insert(7)
    splay_tree.insert(2)
    splay_tree.insert(6)
    splay_tree.insert(8)
    splay_tree.insert(4)
    splay_tree.insert(9)
    splay_tree.insert(1)
    splay_tree.insert(5)
    splay_tree.insert(0)

    print(str(splay_tree))
    #print("-------------------------------------------------------------")
    #print("Got: " + str(splay_tree.get(2)))
    #print(str(splay_tree))
    #print("-------------------------------------------------------------")
    #print("Got: " + str(splay_tree.get(4)))
    #print(str(splay_tree))
    #print("-------------------------------------------------------------")
    #print("Got: " + str(splay_tree.get(2)))
    #print(str(splay_tree))
    #print("-------------------------------------------------------------")
    #splay_tree.remove(9)
    #print(str(splay_tree))
    #print("-------------------------------------------------------------")
    #print("Got: " + str(splay_tree.get(2)))
    #print(str(splay_tree))

main()
