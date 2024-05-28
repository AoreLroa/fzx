class ElementNode:
    """
    元素节点类
    """

    def __init__(self, left_node=None, right_node=None, element=None):
        """
        构造函数
        :param left_node: 左节点
        :param right_node: 右节点
        :param element: 节点需要存储的东西
        """
        self.left_node = left_node
        self.right_node = right_node
        self.element = element

    def set_left_node(self, left_node):
        self.left_node = left_node

    def get_left_node(self):
        return self.left_node

    def set_right_node(self, right_node):
        self.right_node = right_node

    def get_right_node(self):
        return self.right_node

    def set_element(self, element):
        self.element = element

    def get_element(self):
        return self.element


class LinkQueue:
    """
    链表队列
        1、如果只需要单向链表，以左节点为主，左节点永远指向下一个节点
        2、如果需要双向链表，新增方向以右节点为主，右节点永远指向上一个节点
        3、如果需要构造树，只能构造单向树，即有向无环图

        队头（左节点）是入参，队尾（右节点）是出参
    """

    # 链表类型：单向链表、双向链表
    _LINK_TYPE = "singly_link"  # double_link
    # 记录队列的长度
    _LENGTH = None
    # 链表头
    _H_LINK: ElementNode = None
    # 链表尾
    _E_LINK: ElementNode = None

    def __init__(self, link_type=None):
        """
        构造函数
        :param link_type: 链表类型。默认为单向链表，double_link 表示双向链表
        """
        self._LENGTH = 0
        self._H_LINK = self._E_LINK = ElementNode()
        self._LINK_TYPE = link_type if (link_type == "double_link") else None

    def __str__(self):
        tmp_obj = self._H_LINK
        link_queue_str = "queue string:"
        while tmp_obj.element:
            link_queue_str += f" {tmp_obj.element}"
            tmp_obj = tmp_obj.left_node
        return link_queue_str

    @property
    def length(self):
        return self._LENGTH

    def add(self, value):
        """
        新节点加入队头
        :param value: 新节点存储的值
        :return:
        """
        tmp_obj = ElementNode(left_node=self._H_LINK, element=value)
        if self._LINK_TYPE:
            self._H_LINK.right_node = tmp_obj

        self._H_LINK = tmp_obj
        self._LENGTH += 1

    def pop(self) -> ElementNode:
        """
        弹出队尾节点
        :return tmp_obj: 队尾节点对象，返回节点中存储的值
        """
        if not self.judge_empty:
            raise IndexError("队列为空，索引越界")
        tmp_obj = self._E_LINK
        self._E_LINK = tmp_obj.right_node
        self._E_LINK.left_node = None
        if self._LINK_TYPE:
            tmp_obj.right_node = None
        self._LENGTH -= 1
        return tmp_obj.element

    def extend_link(self, front_link, back_link):
        """
        合并两个队列，并返回新的队列对象
            合并规则：以 front_link 在前，back_link 接在 front_link 的后面
        :param front_link: 前一个队列
        :param back_link: 后一个队列
        :return:
        """
        pass

    @property
    def judge_empty(self):
        """
        队列判空
        :return:
        """
        if id(self._H_LINK) == id(self._E_LINK):
            return True
        else:
            return False
