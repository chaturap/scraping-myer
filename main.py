import requests
from bs4 import BeautifulSoup
import os
import json
import pandas as pd


url = "https://www.myer.com.au/c/men/mens-clothing/casual-shirts"
headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/112.0.0.0 Safari/537.36'
}

params = {

}

result = []
result_paging = []


def get_data(url: str):
    lastpage=0
    page=1
    while page < lastpage+1:
        url=f"https://www.myer.com.au/c/men/mens-clothing/casual-shirts?pageNumber={page}"
        res = requests.get(url, params=params, headers=headers)
        if res.status_code == 200:
            print(f"Ok , status code is : {res.status_code}")
            soup = BeautifulSoup(res.text, 'html.parser')
            pagings = soup.find('ol', attrs={'data-automation': 'paginateContainer'})
            pagings = pagings.findChildren('li')
            j = 0
            for paging in pagings:
                #print("j,paging",j,paging)
                if j == 7 :
                    lastpage = paging.text

                    print("lastpage",lastpage)
                j= j + 1
            #lastpage = 2
            contents = soup.find_all('li', {'data-automation': 'product-grid-item'})

            try:
                os.mkdir('json_result')
            except FileExistsError:
                pass

            # item per page 48
            # lastpage 51
            for content in contents:
                #  id,  seoToken, variantData’s ids, stockIndicator
                # Size guide id, size guide value
                #id = content.find('id')
                productName = content.find('span', attrs={'data-automation': 'product-name'}).text
                brand = content.find('span', attrs={'data-automation': 'product-brand'}).text
                price = content.find('span', attrs={'data-automation': 'product-price-was'}).text
                variantDatasids = content.findChildren('div', attrs={'class', 'inlineRating'})
                linkUrl = url + content.find('a')['href']
                #print(f"id: {id}")
                print(f"productName: {productName}")
                print(f"brand: {brand}")
                print(f"price: {price}")
                print(f"variantDatasids: {variantDatasids}")
                print(f"linkUrl: {linkUrl}")

                data_dict = {
                    'name': productName,
                    'brand': brand,
                    'salesprices': price,
                    'variantDatasids': variantDatasids,
                    'linkUrl': linkUrl,
                }
                # jumlahdata = len(result)
                # print(f"jumlahdata{jumlahdata}")
                result.append(data_dict)

                try:
                    os.mkdir('file_result')
                except FileExistsError:
                    pass
                with open('file_result/final_data.json', 'w+') as json_data:
                    json.dump(result, json_data)
                print(f'Json Created page !!')
            jumlahdata = len(result)
            print(f"Item per page : {jumlahdata}")

            # create csv file
            df = pd.DataFrame(result)
            df.to_csv('file_result/data.csv', index=False)
            df.to_excel('file_result/data.xlsx', index=False)
            # data created
            print("data csv and xlsx created success")

        else:
            print(f"Not Ok , status code is : {res.status_code}")
        page = page + 1

if __name__ == '__main__':
    get_data(url)