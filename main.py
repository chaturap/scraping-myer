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

resultids = []
result = []
result_paging = []
result_detail = []
resultsize = []
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

    while page +48 < int(lastpage)+1:
        url=f"https://www.myer.com.au/c/men/mens-clothing/casual-shirts?pageNumber={page}"
        res = requests.get(url, params=params, headers=headers)
        if res.status_code == 200:
            #contents = soup.find_all('html', {'lang': 'en'})
            seotoken = soup.find('meta', {'name':'google-site-verification'})['content']
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
                #semua = content
                idproduct = content['id']
                productName = content.find('span', attrs={'data-automation': 'product-name'}).text
                brand = content.find('span', attrs={'data-automation': 'product-brand'}).text
                price = content.find('span', attrs={'data-automation': 'product-price-was'}).text
                #linkUrl = url + 'c/men/mens-clothing/casual-shirts?pageNumber=1/'+content.find('a')['href']
                linkUrl = 'https://www.myer.com.au'+content.find('a')['href']

                # Size guide id, size guide value
                # https://www.myer.com.au/p/maddox-byson-long-sleeve-sherpa-lined-check-overshirt-in-black
                urlsize = linkUrl
                #urlsize = 'https://www.myer.com.au/p/levis-relaxed-fit-western-shirt-in-blue-white'


                res_size = requests.get(urlsize, params=params, headers=headers)
                soup_size = BeautifulSoup(res_size.text, 'html.parser')
                #input_tags = soup_size.find_all('div', attrs={'data-automation': 'select-size'})
                input_tags = soup_size.find_all('input', attrs={'name': 'size'})
                ukuran = [tag['value'] for tag in input_tags]
                #print(f'sizeid:{sizeId}')
                color = soup_size.find('span', attrs={'data-automation': 'pdp-colour-display-value'}).text.strip()

                size_guide = BeautifulSoup(res_size.text, 'html.parser')
                table = size_guide.find_all('div', attrs={'class': 'sizeGuide'})
                #print(f'table: {table}')


                data_dict_size = {
                    'id': idproduct,
                    'size': ukuran,
                    'color': color,
                    #'table': table,


                }

                resultsize.append(data_dict_size)
                try:
                    os.mkdir('file_result')
                except FileExistsError:
                    pass
                with open('file_result/final_datasize.json', 'w+') as json_datasize:
                    json.dump(resultsize, json_datasize)
                # print(f'Json Created page !!')
                # jumlahdata = len(resultids)
                # print(f"Total Item procesed : {jumlahdata}")

                # create csv file
                df = pd.DataFrame(resultsize)
                df.to_csv('file_result/datasize.csv', index=False)
                df.to_excel('file_result/datasize.xlsx', index=False)



                # stock indicator
                urlapi = f'https://api-online.myer.com.au/v2/product/productsupplemental?products={idproduct}'
                r = requests.get(urlapi).json()
                data = r['productList']

                for d in data:
                    id = d['id']
                    internalId = d['internalId']
                    stockIndicator = d['stockIndicator']
                    #print(f'id={id} InternalId={internalId} StockIndicator={stockIndicator}')

                # variantData’s ids
                urlapi = f'https://api-online.myer.com.au/v2/product/pricesupplemental?products={idproduct}'
                r = requests.get(urlapi).json()
                data = r['productList']

                for d in data:
                    variants = d['variants']
                    #print("variants : ", variants)

                    for variant in variants:
                        internalIds = variant['internalId']
                        #print("internalIDS : ",internalIds)
                        data_dict_ids = {
                            'id': id,
                            'internalIds': internalIds,
                        }

                        resultids.append(data_dict_ids)
                        try:
                            os.mkdir('file_result')
                        except FileExistsError:
                            pass
                        with open('file_result/final_dataids.json', 'w+') as json_dataids:
                            json.dump(resultids, json_dataids)
                        # print(f'Json Created page !!')
                        #jumlahdata = len(resultids)
                        # print(f"Total Item procesed : {jumlahdata}")

                        # create csv file
                        df = pd.DataFrame(resultids)
                        df.to_csv('file_result/dataids.csv', index=False)
                        df.to_excel('file_result/dataids.xlsx', index=False)


                    ###################################

                data_dict = {
                    'idproduct': idproduct,
                    'name': productName,
                    'brand': brand,
                    'salesprices': price,
                    'stockIndicator': stockIndicator,
                    'linkUrl': linkUrl,
                    'SeoToken': seotoken,
                    #'SizeGuideId':size
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
    #get_api(id)
    print("Scraping process is complete")
