# Comparision of CSS selectors and Xpaths:
# https://devhints.io/xpath

# Execute in the command line in the 'scrapy-projects':
# $ scrapy startproject scrapy-projects/nobel_winners

# New Scrapy project 'nobel_winners', using template directory '/home/delorian/PycharmProjects/Python-Topics/venv/lib/python3.11/site-packages/scrapy/templates/project', created in:
#     /home/delorian/PycharmProjects/Python-Topics/topics/scrapy-projects/nobel_winners
#
# You can start your first spider with:
#     cd nobel_winners
#     scrapy genspider example example.com

# - scrapy-projects
# |- nobel_winners
#  |- spiders
#   |- __init__.py
#  |- __init__.py
#  |- items.py
#  |- middlewares.py
#  |- pipelines.py
#  |-settings.py
# |- scrapy.cfg

# Countries with the Nobel Prize winners:
# https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country

# Xpath example for Argentina:
# //*[@id='Argentina']/../following-sibling::ol[1]

# Use Scrapy Shell:
# $ scrapy shell https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country

# In [1]: h3_list = response.xpath('//h3')

# In [2]: len(h3_list)
# Out[2]: 83

# In [3]: h3_0 = h3_list[0]

# In [4]: h3_0.extract()
# '<h3><span class="mw-headline" id="Algeria">Algeria</span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="/w/index.php?title=List_of_Nobel_laureates_by_country&amp;action=edit&amp;section=3" title="Edit section: Algeria"><span>edit</span></a><span class="mw-editsection-bracket">]</span></span></h3>'

# In [5]: algeria = h3_0.xpath('span[@class="mw-headline"]/text()').extract()

# In [6]: algeria
# Out[6]: ['Algeria']

# In [7]: ol_algeria_list = h3_0.xpath('following-sibling::ol[1]')

# In [8]: ol_algeria_list
# Out[8]: [<Selector query='following-sibling::ol[1]' data='<ol><li><a href="/wiki/Claude_Cohen-T...'>]

# In [9]: ol_algeria_0 = h3_0.xpath('following-sibling::ol[1]')[0]

# In [10]: ol_algeria_0
# Out[10]: <Selector query='following-sibling::ol[1]' data='<ol><li><a href="/wiki/Claude_Cohen-T...'>

# In [11]: li_algeria_list = ol_algeria_0.xpath('li')

# In [12]: li_algeria_list
# Out[12]:
# [<Selector query='li' data='<li><a href="/wiki/Claude_Cohen-Tanno...'>,
#  <Selector query='li' data='<li><a href="/wiki/Albert_Camus" titl...'>]

# In [13]: len(li_algeria_list)
# Out[13]: 2

# In [14]: li_algeria_0 = li_algeria_list[0]

# In [15]: li_algeria_0
# Out[15]: <Selector query='li' data='<li><a href="/wiki/Claude_Cohen-Tanno...'>

# In [16]: li_algeria_0.extract()
# Out[16]: '<li><a href="/wiki/Claude_Cohen-Tannoudji" title="Claude Cohen-Tannoudji">Claude Cohen-Tannoudji</a>*, Physics, 1997</li>'

# In [17]: name = li_algeria_0.xpath('a//text()')[0].extract()

# In [18]: name
# Out[18]: 'Claude Cohen-Tannoudji'

# In [19]: text_list = li_algeria_0.xpath('descendant-or-self::text()').extract()

# In [20]: text_list
# Out[20]: ['Claude Cohen-Tannoudji', '*, Physics, 1997']

# In [21]: ' '.join(text_list)
# Out[21]: 'Claude Cohen-Tannoudji *, Physics, 1997'

# In [22]: table = response.xpath("//table[contains(@class, 'wikitable sortable')]")

# In [23]: table
# Out[23]: [<Selector query="//table[contains(@class, 'wikitable sortable')]" data='<table class="wikitable sortable" sty...'>]

# In [24]: table.xpath("tbody/tr/td")[0]
# Out[24]: <Selector query='tbody/tr/td' data='<td style="text-align:left;"><span cl...'>

# In [25]: len(table.xpath("tbody/tr/td"))
# Out[25]: 160

# In [26]: table.xpath("./tbody/tr/td")[0]
# Out[26]: <Selector query='./tbody/tr/td' data='<td style="text-align:left;"><span cl...'>

# In [27]: len(table.xpath("./tbody/tr/td"))
# Out[27]: 160

# # # common mistake

# In [28]: len(table.xpath("//tbody/tr/td"))  # equivalent to response.xpath("//tbody/tr/td")
# Out[28]: 183

# # # Using a Scrapy's spider, in the 'scrapy-projects/nobel_winners' folder:

# # # List spiders

# $ scrapy list
# Nobel_winners

# $ scrapy crawl Nobel_winners -o Nobel_winners.json
# ...
#  'item_scraped_count': 1215,
# ...
# 2023-10-30 13:51:33 [scrapy.core.engine] INFO: Spider closed (finished)

# $ head Nobel_winners.json
# [
# {"country": "Algeria", "name": "Claude Cohen-Tannoudji", "link_text": "Claude Cohen-Tannoudji *, Physics, 1997"},
# {"country": "Algeria", "name": "Albert Camus", "link_text": "Albert Camus *, Literature, 1957"},
# {"country": "Argentina", "name": "César Milstein", "link_text": "César Milstein *, Physiology or Medicine, 1984"},
# {"country": "Argentina", "name": "Adolfo Pérez Esquivel", "link_text": "Adolfo Pérez Esquivel , Peace, 1980"},
# {"country": "Argentina", "name": "Luis Federico Leloir", "link_text": "Luis Federico Leloir ,  born in France , Chemistry, 1970"},
# {"country": "Argentina", "name": "Bernardo Houssay", "link_text": "Bernardo Houssay , Physiology or Medicine, 1947"},
# {"country": "Argentina", "name": "Carlos Saavedra Lamas", "link_text": "Carlos Saavedra Lamas , Peace, 1936"},
# {"country": "Armenia", "name": "Ardem Patapoutian", "link_text": "Ardem Patapoutian ,  born in Lebanon , Physiology or Medicine, 2021"},
# {"country": "Australia", "name": "Brian Schmidt", "link_text": "Brian Schmidt ,  born in the United States , Physics, 2011"},

