import requests
import sys

def search_keyword(keyword,context=False):
    keyword_variation = []
    VOCAB_IP = "23.239.3.60"
    VOCAB_USER = "28"
    VOCAB_TOKEN = "46s-78f3d93ad062b2390a69"
    vocab_url = "http://{}/concepts?term={}&partial=0&user={}&token={}".format(VOCAB_IP,keyword,VOCAB_USER,VOCAB_TOKEN)
    requested_data = requests.get(vocab_url)
    # cuid_list.add()
    cuid_list = set()
    for dic in requested_data.json():
        cui = dic.get("cui")
        if cui:
            cuid_list.add(cui)
            # get sysnonyms 
            synonym_url = "http://{}/concepts/{}/synonyms?user={}&token={}".format(VOCAB_IP,cui,VOCAB_USER,VOCAB_TOKEN)

            synonyms = requests.get(synonym_url).json()
            if synonyms:
                keyword_variation.extend(synonyms)
                synonyms = requests.get(synonym_url).json()[0]
                vocab_url_sy = "http://{}/concepts?term={}&partial=0&user={}&token={}".format(VOCAB_IP,synonyms,VOCAB_USER,VOCAB_TOKEN)
                cuid_list.add(requests.get(vocab_url_sy).json()[0].get("cui"))

            #get children
            children_url = "http://{}/concepts/{}/children?user={}&token={}".format(VOCAB_IP,cui,VOCAB_USER,VOCAB_TOKEN)
            
            children_data = requests.get(children_url).json()
            if children_data:
                for children in children_data:
                    cuid_list.add(children.get("cui"))
                    keyword_variation.extend(children.get("terms"))

    return {
            "keyword": keyword,
            "cuid_list": list(cuid_list),
            "keyword_variation": list(set(k.lower() for k in keyword_variation))
    }

if __name__ == '__main__':
    keyword = sys.argv[1]
    print search_keyword(keyword)