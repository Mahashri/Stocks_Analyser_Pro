from flask import Flask, render_template
import yfinance as yf
import matplotlib
# Set the backend to 'Agg' before importing pyplot
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    
    stocks = [
        
        'ZOMATO.NS','VHL.NS',
        'TITAGARH.NS',
        'TIINDIA.NS','SUZLON.NS','SIEMENS.NS','SCHAEFFLER.NS','SAFARI.NS',
        'RADICO.NS','RAILTEL.NS','RAJESHEXPO.NS','RAMCOCEM.NS','PFIZER.NS','PEL.NS',
        'MARUTI.NS','MRPL.NS',
        'MGL.NS','LATENTVIEW.NS','KOTAKBANK.NS',
        'KNRCON.NS','KICL.NS',
        'KPITTECH.NS',
        'KEI.NS','KCP.NS','KAYNES.NS','JINDALSTEL.NS','JSWSTEEL.NS','JWL.NS','JSWHL.NS','JKTYRE.NS','JKPAPER.NS','JKCEMENT.NS',
        'ICICIPRULI.NS','HONDAPOWER.NS',
        'HEROMOTOCO.NS','HAVELLS.NS',
        'HDFCLIFE.NS','HDFCAMC.NS','GSPL.NS', 
        'GSFC.NS', 'GNFC.NS',
        'GAIL.NS','FSL.NS','ELGIEQUIP.NS','DIXON.NS','DATAPATTNS.NS','CUMMINSIND.NS',
        'CHOLAFIN.NS','CHENNPETRO.NS','CRISIL.NS','CCL.NS','BHARATFORG.NS','BEL.NS','BDL.NS','BERGEPAINT.NS',
        'DMART.NS','DALBHARAT.NS','BHARTIHEXA.NS','APARINDS.NS','ANDHRAPAP.NS','ACL.NS',

        'ZYDUSLIFE.NS','WIPRO.NS', 'VEDL.NS','UNIONBANK.NS',  'SULA.NS', 'SAIL.NS', 
        'SOUTHBANK.NS', 'MOTHERSON.NS','SHRIRAMFIN.NS','SHREECEM.NS', 'SRF.NS',   'RECLTD.NS',
         'PFC.NS', 'POLYCAB.NS', 'PERSISTENT.NS', 'POWERGRID.NS', 
        'OIL.NS','ONGC.NS','NMDC.NS',
        'NTPC.NS','NATCOPHARM.NS','NATIONALUM.NS',  'M&M.NS', 'MAHSEAMLES.NS','JIOFIN.NS', 'KTKBANK.NS', 
        'KALYANKJIL.NS', 'J&KBANK.NS','IREDA.NS', 'IRCTC.NS','INDHOTEL.NS','IDFCFIRSTB.NS', 'HINDZINC.NS',  'GMDCLTD.NS', 'GESHIP.NS',  
        'ESCORTS.NS', 'EICHERMOT.NS','COCHINSHIP.NS', 'COALINDIA.NS', 
        'CUB.NS', 'CHOLAFIN.NS', 'CDSL.NS',  'CEATLTD.NS', 
        'CANBK.NS','BSE.NS', 'BHARTIARTL.NS', 'BPCL.NS', 'BALKRISIND.NS', 
         'APLAPOLLO.NS','ADANIENT.NS','ADANIPORTS.NS',

		'VBL.NS', 'UBL.NS', 'UNITDSPR.NS', 
        'ULTRACEMCO.NS', 'TRENT.NS', 'TITAN.NS', 'THANGAMAYL.NS','TMB.NS', 'TECHM.NS', 
        'TATAELXSI.NS','TATACOMM.NS','TATACONSUM.NS''TATASTEEL.NS', 'TATAPOWER.NS', 'TATAINVEST.NS', 
         'TATACHEM.NS', 'TATAMOTORS.NS', 'TCS.NS',
        ,'SUNPHARMA.NS', 'RELIANCE.NS', 'PGHH.NS', 'PIDILITIND.NS', 
        'NESTLEIND.NS', 'MARICO.NS','MUTHOOTFIN.NS', 'MANAPPURAM.NS','LT.NS','RVNL.NS', 'IRFC.NS', 
        'INFY.NS', 'ITC.NS', 'ICICIBANK.NS', 
        'HINDALCO.NS', 'HINDUNILVR.NS', 'HAL.NS', 'HDFCBANK.NS', 'HCLTECH.NS', 'EXIDEIND.NS', 
        'DRREDDY.NS', 'DIVISLAB.NS','DEEPAKFERT.NS', 'DEEPAKNTR.NS', 'COLPAL.NS', 'BRITANNIA.NS',
		'BAJAJHLDNG.NS', 'BAJAJHFL.NS', 'BAJAJFINSV.NS', 'BAJFINANCE.NS', 'BAJAJ-AUTO.NS',
		 'ASIANPAINT.NS','APOLLOHOSP.NS', 'APOLLOTYRE.NS', 'ACC.NS','AMBUJACEM.NS','ITC.NS'
    ]

    
    stock_data = {}
    company_names = []  # List to hold company names

    for stock in stocks:
        ticker = yf.Ticker(stock)
        try:
            stock_info = ticker.info
        except Exception as e:
            print(f"Error fetching data for {stock}: {e}")
            continue

        # Fetch the company name and remove "Ltd", "Limited", etc.
        company_name = stock_info.get('shortName') or stock_info.get('longName') or stock.replace('.NS', '')
        suffixes = ['Limited', 'Ltd.', 'Ltd', 'LTD', 'LTD.', 'LIMITED','.',' L',' (I)',' (L)']
        for suffix in suffixes:
            if company_name.endswith(suffix):
                company_name = company_name.replace(suffix, '').strip()
                break  # Remove only one suffix

        company_names.append(company_name)
                      

        try:
            stock_data[stock] = {
                'Name': company_name,  # Store the company name                                               
                'Current Price': stock_info['currentPrice'],
                '52 Week Low': stock_info['fiftyTwoWeekLow'],
                '52 Week High': stock_info['fiftyTwoWeekHigh']
            }
        except KeyError:
            print(f"Data not available for {stock}")
            continue

    # Ensure that company_names and stock_data are aligned
    valid_stocks = [stock for stock in stocks if stock in stock_data]
    valid_company_names = [stock_data[stock]['Name'] for stock in valid_stocks]
    current_price = [stock_data[stock]['Current Price'] for stock in valid_stocks]
    low_52w = [stock_data[stock]['52 Week Low'] for stock in valid_stocks]
    high_52w = [stock_data[stock]['52 Week High'] for stock in valid_stocks]

    # Define the fixed width for the bars (all bars will be of the same width)
    bar_width = 90  # A constant width for all bars
    bar_start = 2500  # Move the bars to the center of the page

    # Create a clean horizontal bar plot with increased size
    fig, ax = plt.subplots(figsize=(8, 125))  # Increased width for better visibility

    y = np.arange(len(valid_company_names))

    # Loop through each stock to create bars and labels
    for i in range(len(valid_company_names)):
        bar_end = bar_start + bar_width  # All bars will end at the same fixed point

        # Plot a static bar of fixed length
        ax.plot([bar_start, bar_end], [i, i], color='lightblue', lw=5, zorder=1)

        # Calculate the relative position of the current price between the 52-week low and high
        if high_52w[i] > low_52w[i]:
            price_position = bar_start + (current_price[i] - low_52w[i]) / (high_52w[i] - low_52w[i]) * bar_width
        else:
            price_position = bar_start  # Edge case: if 52-week low equals high (or zero), place at start

        # Place a green arrow (↑) for the current price on the bar
        ax.annotate('▲', xy=(price_position, i), fontsize=15, color='green', ha='center', va='center', fontweight='bold')

        # Display the current price above the bar
        ax.text(price_position, i + 0.25, f'₹{current_price[i]:.2f}', va='center', ha='center', color='black', fontweight='bold')

        # Add bold low and high labels below the bar (moved closer)
        ax.text(bar_start+5, i - 0.30, f'L ₹{low_52w[i]:.2f}', va='center', ha='right', fontsize=10, color='black')
        ax.text(bar_end, i - 0.30, f'H ₹{high_52w[i]:.2f}', va='center', ha='left', fontsize=10,  color='black')

    # Remove all axis ticks, labels, and grids
    ax.set_yticks(y)
    ax.set_yticklabels(valid_company_names, fontweight='bold')
    ax.xaxis.set_visible(False)
    ax.yaxis.set_ticks_position('none')
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Increase vertical spacing between bars
    for i in range(len(valid_company_names)):
        ax.text(0, i, '', fontsize=1)  # This line adds spacing; you can adjust it

    # Save the plot to a BytesIO object and encode it as base64 for HTML rendering
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    buf.seek(0)
    plot_url = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    return render_template('index.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
