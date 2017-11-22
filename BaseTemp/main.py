# -*- coding:utf-8 -*-

import os
import sys

from scrapy.cmdline import execute

sys.path.append(os.path.dirname(__file__))
# print(os.path.dirname(__file__))

# execute(['scrapy','crawl','weibo'])
# execute(['scrapy','crawl','imdbcrawl'])
# execute(['scrapy','crawl','imdb'])
# execute(['scrapy','crawl','imdbcrawl'])
execute(['scrapy','crawl','phonenum'])