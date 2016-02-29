"""Class represnting Order """

from ..models import Order, Payment


class OrderClass:
    def __init__(self, userid, bookid):
        self.userid = userid
        self.bookid = bookid

    """status ="""


    def updateStatus(self,orderid):
        t_order=Order.objects.filter(orderid=orderid)
		
