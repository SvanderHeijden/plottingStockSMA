import urllib.parse
import json
import requests
import matplotlib.pyplot as plt

"""
This application serves as a simple plotting tool for the US stock market. For closing 
data the financial moddeling pred API is used. 

@author: Sjoerd van der Heijden
"""

"""
When this definition is called the program runs.

"""
def main():
    
    ticker = input("Please input ticker: ")
    
    plot(ticker)

"""
When this definition is called the API is requested.

@return: myData is a dictionary containing the close and dates of the requested ticker.

"""
def request(ticker):
    
    myUrl  = 'https://financialmodelingprep.com/api/v3/historical-price-full/'
    
    totalUrl = urllib.parse.urljoin(myUrl, ticker)
    
    request = requests.get(totalUrl)
    
    myData = json.loads(request.text.replace("<pre>","").replace("</pre>",""))
    
    return(myData)
    
"""
When this definition is called the close is plotted and the SMA 20, 50 and 200
are plotted.
"""
def plot(ticker):
    
    plt.close("all")
    
    myData = request(ticker)
    
    myPrice = []

    myDate = []
    
    for i in range(0, len(myData["historical"])):
    
        myPrice.append(float(myData["historical"][i]["close"]))
    
        myDate.append(myData["historical"][i]["date"])
    
    moving = [20, 50, 200]
    
    for h in range(0, len(moving)):
        
        mySMA = []
        
        for i in range(moving[h]-1, len(myData["historical"])):
        
            mySum = 0
        
            for j in range(0, moving[h]-1):
            
                mySum += float(myData["historical"][i-j]["close"])
            
            mySMA.append(mySum/(moving[h]-1))    
        
        plt.plot_date(myDate[moving[h]-1:len(myDate)], mySMA, '-',  label= "SMA " + str(moving[h]) + " days")
        
        
    plt.plot_date(myDate, myPrice, 'k-' , label = 'close ' + ticker, alpha=0.2)
    
    plt.title("Daily close " + ticker + " including SMA " +  str(moving[0]) + ", "+  str(moving[1]) + ", " +  str(moving[2]) + " days.")
    
    plt.grid(True)
    
    plt.legend()
    
    plt.ylabel("Price [$]")
    
    plt.xlabel("Year")
    
    plt.show()
     
    return()
    
"""
Runs the main definition.
"""

if __name__ == '__main__':
    
    main()

