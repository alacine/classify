import pysnooper
from classify import Classify


@pysnooper.snoop()
def test():
    """单元测试"""
    test_target_dir = './test'
    test_cls = Classify(test_target_dir)
    test_cls.sort_by_extension()
    test_content = ['111', '222', '33']
    test_cls.sort_by_name(test_content)
    data_a = test_cls.extension_sorted
    data_b = test_cls.name_sorted
    test_cls.do_extension_sort()
    test_cls.export_dir(0, 'test0.json')
    # test_cls.do_name_sort()
    # test_cls.export_dir(1, 'test1.json')


if __name__ == '__main__':
    test()
