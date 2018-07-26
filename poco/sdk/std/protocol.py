# coding=utf-8

import struct
import six

HEADER_SIZE = 4


class SimpleProtocolFilter(object):
    """ 简单协议过滤器
        协议按照 [有效数据字节数][有效数据] 这种协议包的格式进行打包和解包
        [有效数据字节数]长度HEADER_SIZE字节
        [有效数据]长度有效数据字节数字节
        本类按照这种方式，顺序从数据流中取出数据进行拼接，一旦接收完一个完整的协议包，就会将协议包返回
        [有效数据]字段接收到后会按照utf-8进行解码，因为在传输过程中是用utf-8进行编码的
        所有编解码的操作在该类中完成
    """

    def __init__(self):
        super(SimpleProtocolFilter, self).__init__()
        self.buf = b''

    def input(self, data):
        """ 小数据片段拼接成完整数据包
            如果内容足够则yield数据包
        """
        self.buf += data
        while len(self.buf) > HEADER_SIZE:
            data_len = struct.unpack('i', self.buf[0:HEADER_SIZE])[0]
            if len(self.buf) >= data_len + HEADER_SIZE:
                content = self.buf[HEADER_SIZE:data_len + HEADER_SIZE]
                self.buf = self.buf[data_len + HEADER_SIZE:]
                yield content
            else:
                break

    @staticmethod
    def pack(content):
        """ content should be str
        """
        if isinstance(content, six.text_type):
            content = content.encode("utf-8")
        return struct.pack('i', len(content)) + content

    @staticmethod
    def unpack(data):
        """ return length, content
        """
        length = struct.unpack('i', data[0:HEADER_SIZE])
        return length[0], data[HEADER_SIZE:]
