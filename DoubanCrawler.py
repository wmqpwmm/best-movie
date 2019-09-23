import sys,io,expanddouban,csv,os,bs4
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8-sig')

# 任务1:获取每个地区、每个类型页面的URL
def getMovieUrl(category,location):
    url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,{},{}"\
    .format(category,location)
    return url
# 任务2:获取电影页面 HTML


# 任务3:定义电影类
class Movie:
    def __init__(self,name,rate,location,category,info_link,cover_link):
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link
    def print_data(self):
        return [self.name,self.rate,self.location,self.category,self.info_link,\
        self.cover_link]


# 任务4:获得豆瓣电影的信息
def getMovies(category,location):
    movies = []
    for cat in category:
        for loc in location:
            html = expanddouban.getHtml(getMovieUrl(cat,loc),True)
            soup = bs4.BeautifulSoup(html,'html.parser')
            content_a = soup.find(id='content').find(class_='list-wp')\
            .find_all('a',recursive=False)
            for element in content_a:
                M_name = element.find(class_='title').string
                M_rate = element.find(class_='rate').string
                M_location = loc
                M_category = cat
                M_info_link = element.get('href')
                M_cover_link = element.find('img').get('src')
                movies.append(Movie(M_name,M_rate,M_location,M_category,\
                M_info_link,M_cover_link).print_data())
    return movies
# 任务3、4参考http://discussions.youdaxue.com/t/topic/50499/8


# 任务5:构造电影信息数据表
path = os.path.abspath(os.path.dirname(__file__))#当前目录
category_list = ["喜剧","爱情","科幻"]
location_list = ["中国大陆","美国","中国香港","中国台湾","日本","韩国","英国","法国",\
"德国","意大利","西班牙","印度","泰国","俄罗斯","伊朗","加拿大","澳大利亚","爱尔兰",\
"瑞典","巴西","丹麦"]
movie_list = list(getMovies(category_list, location_list))
#输出csv文件
with open(str(path)+'/movie.csv','w+',encoding='utf-8-sig') as f:
    csv_write = csv.writer(f)
    for movie in movie_list:
        csv_write.writerow(movie)#添加[]解决元素被分割问题


# 任务6:统计电影数据
#按种类统计函数
def count_cat(list_x,x):
    count = 0
    for i in range(len(list_x)):
        if x == list_x[i][3]:
            count += 1
    return count

#按地区统计函数
def count_loc(list_x,category,location):
    count = 0
    for i in range(len(list_x)):
        if category == list_x[i][3] and location == list_x[i][2]:
            count += 1
    return count

#统计每个类型电影数量
count_list_cat = []
for i in range(len(category_list)):
    count_list_cat.append([category_list[i],count_cat(movie_list,category_list[i])])

#统计所选取的每个电影类别中，数量排名前三的地区有哪些，分别占此类别电影总数的百分比为多少
with open(str(path)+'/output.txt','w+',encoding='utf-8-sig') as f:
    for i in range(len(count_list_cat)):
        cat = count_list_cat[i][0]
        count_list_loc = []
        for loc in location_list:
            count_list_loc.append([loc,count_loc(movie_list, cat, loc)])
        count_list_loc.sort(key=lambda x:x[1],reverse=True)
        f.write("{}电影中，数量排名前三的地区为{}、{}、{}，分别占此类别电影总数的百分比为{:.2f}%、{:.2f}%、{:.2f}%。"\
        .format(cat,count_list_loc[0][0],count_list_loc[1][0],count_list_loc[2][0],\
        count_list_loc[0][1]/count_list_cat[i][1]*100,\
        count_list_loc[1][1]/count_list_cat[i][1]*100,\
        count_list_loc[2][1]/count_list_cat[i][1]*100))
        f.write('\r\n')
