# coding:utf-8

import Levenshtein
class TextAnalyse:
    def LevenshiteinSimilarity(self,string1,string2):
        return Levenshtein.ratio(string1,string2)
    def similay(self,string1,string2):
        similar = self.LevenshiteinSimilarity(string1,string2)
        return similar
if __name__ == '__main__':
    t = TextAnalyse()
    print t.similay('【我们的“祖宗海”岂容他人仲裁？】菲律宾南海仲裁案仲裁庭１２日做出一份无效的、没有拘束力的所谓裁决，给菲律宾单方面提起的仲裁案画上一个丑陋的句号。世人已经看清，南海仲裁案从头到尾就是一场披着法律外衣的政治闹剧。对于程序和法律适用牵强附会、证据和事实认定漏洞百出的仲裁案，中国人民绝 ',
                    '【我们的“祖宗海”岂容他人仲裁？】菲律宾南海仲裁案仲裁庭１２日做出一份无效的、没有拘束力的所谓裁决，给菲律宾单方面提起的仲裁案画上一个丑陋的句号。世人已经看清，南')
