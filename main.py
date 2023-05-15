import requests
from bs4 import BeautifulSoup
import os
import json
import pandas as pd


#url = "https://www.myer.com.au/c/men/mens-clothing/casual-shirts"
url = ""
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/112.0.0.0 Safari/537.36'
}

params = {

}

result = []
result_paging = []
result_detail = []
jumlahdata: int


def get_data(url: str):
    print("Start ....")
    lastpage: int= 1
    page: int= 1
    url = f"https://www.myer.com.au/c/men/mens-clothing/casual-shirts?pageNumber={page}"
    res = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    pagings = soup.find('ol', attrs={'data-automation': 'paginateContainer'})
    pagings = pagings.findChildren('li')

    j = 0
    for paging in pagings:
        if j == 7:
            lastpage = int(paging.text)
        j = j + 1

    # get meta data
    # url_meta = f"https://www.myer.com.au/c/men/mens-clothing/casual-shirts?pageNumber={page}"
    # res_meta = requests.get(url_meta, params=params, headers=headers)
    # soup_meta = BeautifulSoup(res_meta.text, 'html.parser')
    # metas = soup_meta.find('meta', attrs={'name': 'google-site-verification'})


    # k = 0
    #for meta in metas:
    #    pass
    #     meta_tag = meta.text
    #     print(f"meta_tag{meta_tag}")
    #     # type(lastpage)
    #     k = k + 1

    color: str
    jumlahdata: int

    # item per page 48
    # lastpage 51

    while page < int(lastpage)+1:
        url=f"https://www.myer.com.au/c/men/mens-clothing/casual-shirts?pageNumber={page}"
        res = requests.get(url, params=params, headers=headers)
        if res.status_code == 200:
            #contents = soup.find_all('html', {'lang': 'en'})
            contents = soup.find_all('li', {'data-automation': 'product-grid-item'})
            #contents = soup.find_all('div', {'data-automation': 'product'})
            #print(contents)
            try:
                os.mkdir('file_result')
            except FileExistsError:
                pass


            for content in contents:
                #  a.Necessary data: product’s name, id, brand, seoToken, variantData’s ids, stockIndicator, url
                #  b.Nice to have dataSize guide id, size guide value
                semua = content
                id = content['id']
                productName = content.find('span', attrs={'data-automation': 'product-name'}).text
                brand = content.find('span', attrs={'data-automation': 'product-brand'}).text
                price = content.find('span', attrs={'data-automation': 'product-price-was'}).text
                linkUrl = url + content.find('a')['href']

                try:
                    variantDatasids = content.find('div', attrs={'class': 'bv-off-screen'}).text
                except:
                    variantDatasids = ''
                try:
                    stockIndicator = content.find('div', attrs={'data-bv-show': 'inline_rating'})['data-bv-ready']
                except:
                    stockIndicator = ' '


                #linkUrl = 'https://www.myer.com.au/p/maddox-sorrento-long-sleeve-sherpa-lined-check-overshirt-in-navy'
                res_detail = requests.get(linkUrl, params=params, headers=headers)

                #cek connection
                #print(f"status: res_detail.status_code{res_detail.status_code}")

                soup_detail = BeautifulSoup(res_detail.text, 'html.parser')
                content_details = soup_detail.findAll('div', attrs={'class': 'container css-1n7ul0p'})
                #print(f"content_details{content_details}")

                for content_detail in content_details:
                    color = content_detail.find('span', attrs={'data-automation': 'pdp-colour-display-value'}).text
                    SizeGuideId = content_detail.find('h3', attrs={'class': 'sgTitle'}).text
                    sizeGuideValue = content_detail.find('table', attrs={'class': 'sizeGuideTable'}).text
                    #print(f"color:{color}")
                    #print(f"SizeGuideId:{SizeGuideId}")
                    #print(f"sizeGuideValue:{sizeGuideValue}")

                # print(f"id: {id}")
                # print(f"productName: {productName}")
                # print(f"brand: {brand}")
                # print(f"price: {price}")
                # print(f"variantDatasids: {variantDatasids}")
                # print(f"linkUrl: {linkUrl}")
                # #print(f"color: {color}")
                # print(f"semua: {semua}")

                data_dict = {
                    'id': id,
                    'name': productName,
                    'brand': brand,
                    'salesprices': price,
                    #'variantDatasids': variantDatasids,
                    'stockIndicator': stockIndicator,
                    'linkUrl': linkUrl,
                    #'SeoToken': meta_tag
                    #'color': color,
                    #'SizeGuideId':SizeGuideId
                    #'sizeGuideValue':sizeGuideValue
                }

                result.append(data_dict)
            # print(f"result : {result}")


                try:
                    os.mkdir('file_result')
                except FileExistsError:
                    pass
                with open('file_result/final_data.json', 'w+') as json_data:
                    json.dump(result, json_data)
                #print(f'Json Created page !!')
                jumlahdata = len(result)
                #print(f"Total Item procesed : {jumlahdata}")

                # create csv file
                df = pd.DataFrame(result)
                df.to_csv('file_result/data.csv', index=False)
                df.to_excel('file_result/data.xlsx', index=False)
                # data created
            print(f"page {page} from {lastpage} Total Item procesed : {jumlahdata}")
            page = page + 1

        else:
            print(f"Not Ok , status code is : {res.status_code}")
    print("File json csv and xlsx created success")


if __name__ == '__main__':
    get_data(url)
    print("Scraping process is complete")