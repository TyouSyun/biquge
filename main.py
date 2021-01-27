import sys
from book.spider_biquge import SpiderBiquge


if __name__ == '__main__':
    a = """                                             
功能列表：                                                                                
 1.获取小说列表
 2.保存小说
    """
    print(a)

    spider_biquge = SpiderBiquge()
    choice_function = input('请选择:')
    if choice_function == '1':
        spider_biquge.saveBookListsToMysql()
    elif choice_function == '2':
        spider_biquge.getBiqugeUrl()
    else:
        print('没有此功能')
        sys.exit(1)

