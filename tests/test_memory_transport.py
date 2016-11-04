from unittest import TestCase

from thriftpy.transport.memory import TMemoryBuffer
from thriftpy._compat import CYTHON


class MemoryTransport(TestCase):
    @staticmethod
    def trans(data=b'', *args, **kwargs):
        return TMemoryBuffer(data)

    def test_write(self):
        m = self.trans()
        m.write(b"hello world")

        assert b"hello world" == m.getvalue()

    def test_read(self):
        m = self.trans(b"hello world")

        assert b"hello" == m.read(5)
        m.write(b"hello")
        assert b" world" == m.read(6)
        assert b"hello" == m.getvalue()

    def test_clean(self):
        m = self.trans(b'hello world')

        assert b"hello world" == m.getvalue()
        m.clean()
        assert b"" == m.getvalue()
        m.write(b"hello")
        assert b"hello" == m.getvalue()


if CYTHON:
    from thriftpy.transport.memory import TCyMemoryBuffer

    class CyMemoryTransport(MemoryTransport):
        @staticmethod
        def trans(*args, **kwargs):
            return TCyMemoryBuffer(*args, **kwargs)

        def test_write_move(self):
            m = self.trans(buf_size=10)
            m.write(b"helloworld")

            m.read(6)
            assert b"orld" == m.getvalue()

            m.write(b"he")
            assert b"orldhe" == m.getvalue()

        def test_write_grow(self):
            m = self.trans(buf_size=10)
            m.write(b"hello world")
            assert b"hello world" == m.getvalue()

            m.read(5)
            m.write(b"hello ")
            assert b" worldhello " == m.getvalue()

        def test_write_move_grow(self):
            m = self.trans(buf_size=10)
            m.write(b"helloworld")

            m.read(6)
            m.write(b"hellowaaa")
            assert b"orldhellowaaa" == m.getvalue()

        def test_read(self):
            m = self.trans(b"hello world")
            b = m.read(5)

            assert b"hello" == b
            assert b" world" == m.getvalue()
