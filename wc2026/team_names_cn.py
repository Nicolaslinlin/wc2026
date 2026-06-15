"""English → 中文 country/team name mapping for display."""

CHINESE_NAMES = {
    "Germany": "德国", "Curaçao": "库拉索", "Brazil": "巴西", "Argentina": "阿根廷",
    "France": "法国", "Spain": "西班牙", "England": "英格兰", "Portugal": "葡萄牙",
    "Netherlands": "荷兰", "Italy": "意大利", "Belgium": "比利时", "Croatia": "克罗地亚",
    "Mexico": "墨西哥", "United States": "美国", "Canada": "加拿大", "Japan": "日本",
    "South Korea": "韩国", "Australia": "澳大利亚", "Morocco": "摩洛哥", "Senegal": "塞内加尔",
    "Côte d'Ivoire": "科特迪瓦", "Ecuador": "厄瓜多尔", "Uruguay": "乌拉圭", "Colombia": "哥伦比亚",
    "Switzerland": "瑞士", "Denmark": "丹麦", "Poland": "波兰", "Iran": "伊朗",
    "Saudi Arabia": "沙特", "Qatar": "卡塔尔", "Tunisia": "突尼斯", "Ghana": "加纳",
    "Cameroon": "喀麦隆", "Egypt": "埃及", "Nigeria": "尼日利亚", "Algeria": "阿尔及利亚",
    "Wales": "威尔士", "Scotland": "苏格兰", "Serbia": "塞尔维亚",
    "Cape Verde": "佛得角", "Norway": "挪威", "Austria": "奥地利",
    "Czech Republic": "捷克", "Sweden": "瑞典", "Romania": "罗马尼亚",
    "Turkey": "土耳其", "Greece": "希腊", "Ukraine": "乌克兰", "Russia": "俄罗斯",
    "New Zealand": "新西兰", "Costa Rica": "哥斯达黎加", "Panama": "巴拿马",
    "Honduras": "洪都拉斯", "Jamaica": "牙买加", "Paraguay": "巴拉圭", "Peru": "秘鲁",
    "Chile": "智利", "Venezuela": "委内瑞拉", "Bolivia": "玻利维亚",
    "South Africa": "南非", "Mali": "马里", "Burkina Faso": "布基纳法索",
    "DR Congo": "刚果（金）", "Zambia": "赞比亚", "Uzbekistan": "乌兹别克斯坦",
    "Jordan": "约旦", "Iraq": "伊拉克",
}


def to_chinese(name: str) -> str:
    return CHINESE_NAMES.get(name, name)
