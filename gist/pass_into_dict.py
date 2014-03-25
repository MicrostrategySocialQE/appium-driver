__author__ = 'Zhenyu'


def test(t):
    t['a'] = 123


if __name__ == "__main__":
    t = {}
    test(t)
    print t  # t = {a:123}