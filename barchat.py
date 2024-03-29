import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Data



def drawBarChart():

    values = []

    sales_quater = []
    expenses_qauter = []
    margin_quater = []
    netprofit_quater = []

    data  = {"quarters": {"": {"1": "Sales +", "2": "Expenses +", "3": "Operating Profit", "4": "OPM %", "5": "Other Income +", "6": "Interest", "7": "Depreciation", "8": "Profit before tax", "9": "Tax %", "10": "Net Profit +", "11": "EPS in Rs", "12": "Raw PDF"}, "Dec 2020": {"1": "494", "2": "168", "3": "326", "4": "66%", "5": "-19", "6": "-15", "7": "105", "8": "217", "9": "9%", "10": "198", "11": "0.50", "12": ""}, "Mar 2021": {"1": "464", "2": "222", "3": "241", "4": "52%", "5": "751", "6": "30", "7": "97", "8": "866", "9": "28%", "10": "620", "11": "1.58", "12": ""}, "Jun 2021": {"1": "662", "2": "154", "3": "508", "4": "77%", "5": "59", "6": "26", "7": "96", "8": "445", "9": "23%", "10": "342", "11": "0.87", "12": ""}, "Sep 2021": {"1": "882", "2": "271", "3": "611", "4": "69%", "5": "44", "6": "15", "7": "102", "8": "538", "9": "25%", "10": "405", "11": "1.03", "12": ""}, "Dec 2021": {"1": "549", "2": "171", "3": "379", "4": "69%", "5": "63", "6": "38", "7": "102", "8": "301", "9": "22%", "10": "235", "11": "0.60", "12": ""}, "Mar 2022": {"1": "323", "2": "181", "3": "143", "4": "44%", "5": "75", "6": "82", "7": "103", "8": "32", "9": "77%", "10": "7", "11": "0.02", "12": ""}, "Jun 2022": {"1": "1,004", "2": "176", "3": "828", "4": "82%", "5": "108", "6": "144", "7": "100", "8": "691", "9": "12%", "10": "609", "11": "1.55", "12": ""}, "Sep 2022": {"1": "878", "2": "166", "3": "713", "4": "81%", "5": "86", "6": "117", "7": "105", "8": "577", "9": "23%", "10": "445", "11": "1.13", "12": ""}, "Dec 2022": {"1": "552", "2": "171", "3": "381", "4": "69%", "5": "177", "6": "105", "7": "105", "8": "347", "9": "17%", "10": "287", "11": "0.73", "12": ""}, "Mar 2023": {"1": "504", "2": "326", "3": "178", "4": "35%", "5": "68", "6": "49", "7": "86", "8": "112", "9": "85%", "10": "17", "11": "0.04", "12": ""}, "Jun 2023": {"1": "675", "2": "192", "3": "483", "4": "72%", "5": "71", "6": "90", "7": "101", "8": "363", "9": "25%", "10": "272", "11": "0.69", "12": ""}, "Sep 2023": {"1": "878", "2": "172", "3": "706", "4": "80%", "5": "89", "6": "124", "7": "102", "8": "569", "9": "23%", "10": "440", "11": "1.12", "12": ""}, "Dec 2023": {"1": "543", "2": "175", "3": "368", "4": "68%", "5": "49", "6": "122", "7": "112", "8": "183", "9": "24%", "10": "139", "11": "0.35", "12": ""}}, "profit-loss": {"": {"1": "Sales +", "2": "Expenses +", "3": "Operating Profit", "4": "OPM %", "5": "Other Income +", "6": "Interest", "7": "Depreciation", "8": "Profit before tax", "9": "Tax %", "10": "Net Profit +", "11": "EPS in Rs", "12": "Dividend Payout %"}, "Mar 2013": {"1": "1,682", "2": "242", "3": "1,440", "4": "86%", "5": "245", "6": "54", "7": "447", "8": "1,185", "9": "11%", "10": "1,052", "11": "2.54", "12": "38%"}, "Mar 2014": {"1": "1,872", "2": "268", "3": "1,604", "4": "86%", "5": "237", "6": "29", "7": "475", "8": "1,338", "9": "17%", "10": "1,114", "11": "2.69", "12": "36%"}, "Mar 2015": {"1": "2,816", "2": "372", "3": "2,443", "4": "87%", "5": "309", "6": "65", "7": "641", "8": "2,047", "9": "18%", "10": "1,677", "11": "4.05", "12": "26%"}, "Mar 2016": {"1": "2,494", "2": "431", "3": "2,063", "4": "83%", "5": "541", "6": "218", "7": "677", "8": "1,709", "9": "17%", "10": "1,411", "11": "3.41", "12": "32%"}, "Mar 2017": {"1": "2,679", "2": "480", "3": "2,199", "4": "82%", "5": "411", "6": "55", "7": "680", "8": "1,875", "9": "18%", "10": "1,545", "11": "3.73", "12": "74%"}, "Mar 2018": {"1": "2,228", "2": "524", "3": "1,705", "4": "76%", "5": "409", "6": "101", "7": "365", "8": "1,648", "9": "26%", "10": "1,225", "11": "3.12", "12": "122%"}, "Mar 2019": {"1": "2,645", "2": "606", "3": "2,039", "4": "77%", "5": "397", "6": "251", "7": "390", "8": "1,795", "9": "24%", "10": "1,367", "11": "3.47", "12": "62%"}, "Mar 2020": {"1": "2,703", "2": "590", "3": "2,112", "4": "78%", "5": "587", "6": "344", "7": "384", "8": "1,972", "9": "21%", "10": "1,567", "11": "3.99", "12": "55%"}, "Mar 2021": {"1": "2,485", "2": "619", "3": "1,867", "4": "75%", "5": "425", "6": "42", "7": "393", "8": "1,856", "9": "11%", "10": "1,646", "11": "4.19", "12": "53%"}, "Mar 2022": {"1": "2,417", "2": "623", "3": "1,794", "4": "74%", "5": "195", "6": "226", "7": "404", "8": "1,360", "9": "27%", "10": "990", "11": "2.52", "12": "68%"}, "Mar 2023": {"1": "2,938", "2": "665", "3": "2,273", "4": "77%", "5": "310", "6": "449", "7": "396", "8": "1,738", "9": "22%", "10": "1,359", "11": "3.46", "12": "51%"}, "TTM": {"1": "2,600", "2": "864", "3": "1,736", "4": "67%", "5": "277", "6": "385", "7": "400", "8": "1,227", "9": "", "10": "868", "11": "2.20", "12": ""}}, "shareholding": {"": {"1": "Promoters +", "2": "FIIs +", "3": "DIIs +", "4": "Public +", "5": "No. of Shareholders"}, "Mar 2021": {"1": "86.77%", "2": "2.33%", "3": "5.41%", "4": "5.49%", "5": "1,43,481"}, "Jun 2021": {"1": "86.77%", "2": "2.40%", "3": "5.29%", "4": "5.54%", "5": "1,67,301"}, "Sep 2021": {"1": "86.77%", "2": "2.53%", "3": "4.93%", "4": "5.77%", "5": "1,92,116"}, "Dec 2021": {"1": "86.77%", "2": "2.51%", "3": "4.63%", "4": "6.09%", "5": "2,56,012"}, "Mar 2022": {"1": "86.77%", "2": "2.65%", "3": "4.00%", "4": "6.59%", "5": "3,09,180"}, "Jun 2022": {"1": "86.77%", "2": "2.93%", "3": "3.42%", "4": "6.88%", "5": "3,11,302"}, "Sep 2022": {"1": "86.77%", "2": "2.96%", "3": "3.83%", "4": "6.42%", "5": "2,88,279"}, "Dec 2022": {"1": "86.77%", "2": "2.31%", "3": "3.81%", "4": "7.11%", "5": "3,12,024"}, "Mar 2023": {"1": "86.77%", "2": "1.75%", "3": "4.06%", "4": "7.41%", "5": "3,16,055"}, "Jun 2023": {"1": "86.77%", "2": "1.40%", "3": "4.32%", "4": "7.50%", "5": "3,19,143"}, "Sep 2023": {"1": "81.85%", "2": "0.91%", "3": "5.74%", "4": "11.51%", "5": "6,20,023"}, "Dec 2023": {"1": "81.85%", "2": "1.68%", "3": "5.97%", "4": "10.51%", "5": "6,55,627"}}}
     

    header_q = []
    header_p = []
    header_s = []
    iter = 0

    for key, value in data.items():
        iter = iter + 1
        for k, v in value.items():
            if iter==1 and k!='':
                header_p.append(k)
            elif iter==2 and k!='':
                header_q.append(k)
            elif iter==3 and k!='':
                header_s.append(k)
    
    print(header_p)
    print(header_q)
    print(header_s)


    index = 1
    for key, value in data.items():
        sales_quater = []
        expenses_qauter = []
        margin_quater = []
        netprofit_quater = []
        
        for i, (k, v) in enumerate(value.items()):
            
            # print(k.keys())
            if i!=0:
                print(k,i, '????????????????????')
                # print(k,"okeyyyyyyyyyyyyyyyy")
                # print(v,"vvvvvvvvvvvvvvvvvvvvvv")
                # print(v[str(index)],"valueeeeeeeeeeeeee")

                sales_quater.append(v[str(index)])
                expenses_qauter.append(v[str(index+1)])
                margin_quater.append(v[str(index+3)])
                netprofit_quater.append(v[str(index+4)])

        print(sales_quater)
        print(expenses_qauter)
        print(margin_quater)
        print(netprofit_quater)

        sales_quater = [int(x.replace(',', '')) for x in sales_quater]
        expenses_qauter = [int(x.replace(',', '')) for x in expenses_qauter]
        # margin_quater = [int(x).replace(',', '') for x in margin_quater]
        netprofit_quater = [int(x.replace(',', '')) for x in netprofit_quater]

        categories = ['1','2','3','4','5','6','7','8','9','10','11','12','13']


        # Create bar chart
        # plt.bar(categories, expenses_qauter, color=['skyblue' if int(s) >= 0 else 'lightcoral' for s in expenses_qauter
        #                                              ])
        
        fig, axs = plt.subplots(1, 3, figsize=(15, 5))

        # Create the first bar chart
        axs[0].bar(categories, sales_quater, color='skyblue')
        axs[0].set_title('Sales Data Quaterly')

        # Create the second bar chart
        axs[1].bar(categories, expenses_qauter, color='salmon')
        axs[1].set_title('Exepenses')

        # Create the third bar chart
        axs[2].bar(categories, netprofit_quater, color='lightgreen')
        axs[2].set_title('Net Profit')


        # Add labels and title
        plt.xlabel('Categories')
        plt.ylabel('Sales')
        plt.title('Bar Chart Example')

        # Show the plot
        plt.show()
                    

drawBarChart()
