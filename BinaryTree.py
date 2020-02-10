class BinaryTree:
    def __init__(self):
        self.root = None
        self.size = 0

    ################################ Page Class ##############################
    class Page:
        def __init__(self, val):

            # val represents the name of the page
            self.val = val

            self.leftChild = None
            self.rightChild = None

        def get_name(self):
            return self.val

        def set_name(self, val):
            self.val = val

        def getChildren(self):
            children = []
            if (self.leftChild != None):
                children.append(self.leftChild)
            if (self.rightChild != None):
                children.append(self.rightChild)
            return children

    #############################################################################

    def setRoot(self, page):
        self.root = page

    def insert(self, page):
        if (self.root is None):
            self.setRoot(page)
            self.size = self.size + 1
        else:
            self.insertNode(self.root, page)

    def insertNode(self, currentNode, page):
        if (page.val <= currentNode.val):
            if (currentNode.leftChild):
                self.insertNode(currentNode.leftChild, page)
            else:
                currentNode.leftChild = page
                self.size = self.size + 1
        elif (page.val > currentNode.val):
            if (currentNode.rightChild):
                self.insertNode(currentNode.rightChild, page)
            else:
                currentNode.rightChild = page
                self.size = self.size + 1

    def find(self, val):
        return self.findNode(self.root, val)

    def findNode(self, currentNode, val):
        if (currentNode is None):
            return False
        elif (val == currentNode.val):
            return True
        elif (val < currentNode.val):
            return self.findNode(currentNode.leftChild, val)
        else:
            return self.findNode(currentNode.rightChild, val)

    def is_empty(self):
        if (self.root is None):
            return True

        else:
            return False

    def size(self):
        return self.size

    def print_pages(self):
        if (self.is_empty()):
            return "[]"

        pages = []
        iterator = BinaryTree.Iterator(self, self.tree)

        for i in range(self.size):
            pages.append(iterator.next())

        for i in range(len(pages)):
            print(pages[i])

    def remove(self, val):
        current = root
        parent = None

        while (current != None):

            # matching data is found
            if (current.val == val):

                # if its a leaf page
                if (current.leftChild == None and current.rightChild == None):
                    self.size = self.size - 1
                    self.removeLeaf(parent, current)
                    return

                # if page has left child only
                elif (current.leftChild != None and current.rightChild == None):
                    self.size = self.size - 1
                    self.removeLeft(parent, current)
                    return

                    # if page has right child only
                elif (current.leftChild == None and current.rightChild != None):
                    self.size = self.size - 1
                    self.removeRight(parent, current)
                    return

                    # page has two childs
                else:
                    successor = current.rightChild

                    # checks to see whether successor moved
                    check = False

                    # checks to see whether successor has to traverse to the left
                    leftC = False

                    # find leftmost page
                    while (successor.leftChild != None):
                        successor = successor.leftChild
                        check = True
                        leftC = True

                    if (not check):
                        current.val = successor.val
                        current.rightChild = successor.rightChild
                        self.size = self.size - 1
                        return

                    # find rightmost page
                    while (successor.rightChild != None):
                        leftC = False
                        successor = successor.rightChild

                    current.val = successor.val

                    # handles deletion of reference
                    if (leftC):
                        successor.parent.leftChild = None

                    else:
                        successor.parent.rightChild = None

                    self.size = self.size - 1
                    return

            # traverse if data doesnt match
            elif (current.val <= val):
                parent = current
                current = current.rightChild

            else:
                parent = current
                current = current.rightChild

    def removeLeaf(parent_node, current_node):

        if (parent_node == None):
            self.root = None

        elif (parent_node.leftChild == current):
            parent_node.leftChild = None

        else:
            parent_node.rightChild = None

    def removeLeft(parent_node, current_node):

        if (parent_node == None):
            self.root = current_node.leftChild

        elif (parent_node.leftChild == current_node):
            parent_node.leftChild = current_node.leftChild

        else:
            parent_node.rightChild = current_node.leftChild

    def removeRight(parent_node, current_node):

        if (parent_node == None):
            self.root = current_node.leftChild

        elif (parent_node.leftChild == current):
            parent_node.leftChild = current.leftChild

        else:
            parent_node.rightChild = current.leftChild

    ########################## iterator class ######################################
    class Iterator:
        def __init__(self, tree):
            self.page_list = []
            self.cursor = tree.root
            self.top = tree.root

            self.page_list.append(tree.root)
            while (self.cursor.leftChild != None):
                self.cursor = self.cursor.leftChild
                self.page_list.append(self.cursor)

        def has_next(self):
            if (len(self.page_list) == 0):
                return False
            else:
                return True

        def next(self):
            if (not self.has_next()):
                raise IndexError()

            self.cursor = self.page_list.pop()
            self.data = self.cursor.val

            if (self.cursor.rightChild != None):
                self.cursor = self.cursor.rightChild
                self.page_list.append(self.cursor)

                while (self.cursor.leftChild != None):
                    self.cursor = self.cursor.leftChild
                    self.page_list.append(self.cursor)

            return self.data
