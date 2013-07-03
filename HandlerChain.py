# coding: utf-8
'''
Created on 2013-7-3
handler chain
@author: xuechong
'''
from moehandlers.SellMoeHandler import SellMoeHandler
from Weixin import textReply
import logging

__default_chain__ = (SellMoeHandler,)

class HandlerChain(object):
    """
    the handler chain 
    call doChain to get a reply xml str
    """
    handlers = list()
    userMsg = None
    
    def __init__(self,userMsg):
        self.handlers=list(__default_chain__)
        logging.debug("new handlerChain" + str(self.handlers))
        self.userMsg = userMsg
        
    def doChain(self):
        """
        invoke handlers and return reply xmlstr
        """
        result =  self.invokeNext()
        return result==None and textReply(self.userMsg) or result
    
    def invokeNext(self):
        """
        invoke next handler until there is no handler left or have result
        returns None if no handler can hand the income msg
        """
        result = None
        if len(self.handlers)>0:
            handler = self.handlers.pop()()
            result = handler.handle(self)
            if result==None and len(self.handlers)>0:
                result = self.invokeNext()
        return result
    
    def getMsgType(self):
        """
        get the msgtype of the income msg
        """
        return self.userMsg.get("MsgType")
    
    def getMsgContent(self):
        """
        get the content of the income msg
        """
        return self.userMsg.get("Content")
        