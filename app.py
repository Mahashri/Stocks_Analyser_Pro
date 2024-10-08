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
    # Full list of stocks
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
         'J&KBANK.NS','IREDA.NS', 'IRCTC.NS','INDHOTEL.NS','IDFCFIRSTB.NS', 'HINDZINC.NS',  'GMDCLTD.NS', 'GESHIP.NS',  
        'ESCORTS.NS', 'EICHERMOT.NS','COCHINSHIP.NS', 'COALINDIA.NS', 
        'CUB.NS', 'CHOLAFIN.NS', 'CDSL.NS',  'CEATLTD.NS', 
        'CANBK.NS','BSE.NS', 'BHARTIARTL.NS', 'BPCL.NS', 'BALKRISIND.NS', 
         'APLAPOLLO.NS','ADANIENT.NS','ADANIPORTS.NS',

		'VBL.NS', 'UBL.NS', 'UNITDSPR.NS', 
        'ULTRACEMCO.NS', 'TRENT.NS', 'TITAN.NS', 'THANGAMAYL.NS','TMB.NS', 'TECHM.NS', 
        'TATAELXSI.NS','TATACOMM.NS','TATACONSUM.NS','TATASTEEL.NS', 'TATAPOWER.NS', 'TATAINVEST.NS', 
         'TATACHEM.NS', 'TATAMOTORS.NS', 'TCS.NS',
        'SUNPHARMA.NS', 'RELIANCE.NS', 'PGHH.NS', 'PIDILITIND.NS', 
        'NESTLEIND.NS', 'MARICO.NS','MUTHOOTFIN.NS', 'MANAPPURAM.NS','LT.NS','RVNL.NS','IRCON.NS', 'IRFC.NS', 
        'INFY.NS', 'ITC.NS', 'ICICIBANK.NS', 'KALYANKJIL.NS',
        'HINDALCO.NS', 'HINDUNILVR.NS', 'HAL.NS', 'HDFCBANK.NS', 'HCLTECH.NS', 'EXIDEIND.NS', 
        'DRREDDY.NS', 'DIVISLAB.NS','DEEPAKFERT.NS', 'DEEPAKNTR.NS', 'COLPAL.NS', 'BRITANNIA.NS',
		'BAJAJHLDNG.NS', 'BAJAJHFL.NS', 'BAJAJFINSV.NS', 'BAJFINANCE.NS', 'BAJAJ-AUTO.NS',
		'ASIANPAINT.NS','APOLLOHOSP.NS', 'APOLLOTYRE.NS','ARE&M.NS', 'ACC.NS','AMBUJACEM.NS','ITC.NS'
    ]

    # Sector-wise stocks
    railway_stocks = ['RAILTEL.NS','RITES.NS','JWL.NS','TITAGARH.NS','IRCTC.NS', 'RVNL.NS', 'IRCON.NS','IRFC.NS']
    
    bank_stocks = ['YESBANK.NS','CSBBANK.NS','UTKARSHBNK.NS','JSFB.NS','DCBBANK.NS','ESAFSFB.NS','FINOPB.NS','SURYODAY.NS','CAPITALSFB.NS','DHANBANK.NS','UCOBANK.NS',
    'BANDHANBNK.NS', 'PSB.NS','RBLBANK.NS','J&KBANK.NS', 'MAHABANK.NS', 'UJJIVANSFB.NS','EQUITASBNK.NS',
    'BANKINDIA.NS', 'CENTRALBK.NS', 'AUBANK.NS',  'FEDERALBNK.NS', 'INDIANB.NS', 'IDBI.NS', 'IOB.NS', 'INDUSINDBK.NS',
    'KARURVYSYA.NS', 'PNB.NS','SOUTHBANK.NS', 'BANKBARODA.NS', 'UNIONBANK.NS','CUB.NS', 'CANBK.NS', 'IDFC.NS', 'IDFCFIRSTB.NS', 
    'KOTAKBANK.NS', 'AXISBANK.NS', 'SBIN.NS', 'TMB.NS', 'ICICIBANK.NS', 'HDFCBANK.NS']

    defence_stocks = ['BEML.NS','CYIENTDLM.NS','SOLARINDS.NS','BDL.NS','MAZDOCK.NS','DATAPATTNS.NS','COCHINSHIP.NS','BEL.NS','HAL.NS']
     
    gold_finance_stocks = ['PNGJL.NS', 'THANGAMAYL.NS','KALYANKJIL.NS','TITAN.NS','JIOFIN.NS','MUTHOOTFIN.NS','MANAPPURAM.NS','BAJAJHFL.NS', 'BAJAJFINSV.NS', 'BAJFINANCE.NS']

    power_cement_stocks =[ 'INDIACEM.NS', 'ACL.NS','RAMCOCEM.NS','DALBHARAT.NS','JKLAKSHMI.NS', 'JKCEMENT.NS', 'SHREECEM.NS','ACC.NS', 'AMBUJACEM.NS', 'ULTRACEMCO.NS',
    'SJVN.NS','EXIDEIND.NS','ARE&M.NS','TORNTPOWER.NS','NHPC.NS', 'CESC.NS','ADANIENSOL.NS','ADANIGREEN.NS', 
    'HINDZINC.NS', 'ADANIPOWER.NS', 'TATAPOWER.NS', 'TATAPOWER.NS', 'JSWENERGY.NS', 'RECLTD.NS', 'PFC.NS','NTPC.NS', 'POWERGRID.NS']


    
    
    nifty_stocks =['APOLLOHOSP.NS', 'INDUSINDBK.NS', 'HEROMOTOCO.NS', 'DRREDDY.NS', 'TATACONSUM.NS', 'SHRIRAMFIN.NS', 'EICHERMOT.NS', 'CIPLA.NS', 'BPCL.NS', 'BRITANNIA.NS', 'HDFCLIFE.NS', 'TECHM.NS', 'HINDALCO.NS', 'SBILIFE.NS', 'GRASIM.NS', 'BEL.NS', 'TATASTEEL.NS', 'NESTLEIND.NS', 'JSWSTEEL.NS', 'TRENT.NS', 'WIPRO.NS', 'ASIANPAINT.NS', 'BAJAJFINSV.NS', 'ADANIPORTS.NS', 'COALINDIA.NS', 'POWERGRID.NS', 'TITAN.NS', 'BAJAJ-AUTO.NS', 'ULTRACEMCO.NS', 'TATAMOTORS.NS', 'ADANIENT.NS', 'KOTAKBANK.NS', 'AXISBANK.NS', 'ONGC.NS', 'M&M.NS', 'MARUTI.NS', 'NTPC.NS', 'BAJFINANCE.NS', 'SUNPHARMA.NS', 'LT.NS', 'HCLTECH.NS', 'ITC.NS', 'HINDUNILVR.NS', 'SBIN.NS', 'INFY.NS', 'ICICIBANK.NS', 'BHARTIARTL.NS', 'HDFCBANK.NS', 'TCS.NS', 'RELIANCE.NS'
]
    
    
    
    
    # Helper function to fetch stock data
    def fetch_stock_data(stocks_list):
        stock_data = {}
        company_names = []

        for stock in stocks_list:
            ticker = yf.Ticker(stock)
            try:
                stock_info = ticker.info
            except Exception as e:
                print(f"Error fetching data for {stock}: {e}")
                continue

            company_name = stock_info.get('shortName') or stock_info.get('longName') or stock.replace('.NS', '')
            suffixes = ['Limited', 'Ltd.', 'Ltd', 'LTD', 'LTD.', 'LIMITED', '.', ' L', ' (I)', ' (L)']
            for suffix in suffixes:
                if company_name.endswith(suffix):
                    company_name = company_name.replace(suffix, '').strip()
                    break

            company_names.append(company_name)

            try:
                stock_data[stock] = {
                    'Name': company_name,
                    'Current Price': stock_info['currentPrice'],
                    '52 Week Low': stock_info['fiftyTwoWeekLow'],
                    '52 Week High': stock_info['fiftyTwoWeekHigh']
                }
            except KeyError:
                print(f"Data not available for {stock}")
                continue

        return company_names, stock_data

    # Function to create a plot
    def create_plot(company_names, stock_data, valid_stocks, bar_width=90, bar_start=2500, plot_height=None):
        current_price = [stock_data[stock]['Current Price'] for stock in valid_stocks]
        low_52w = [stock_data[stock]['52 Week Low'] for stock in valid_stocks]
        high_52w = [stock_data[stock]['52 Week High'] for stock in valid_stocks]

        if plot_height is None:
            plot_height = len(valid_stocks) * 1 if valid_stocks else 1

        fig, ax = plt.subplots(figsize=(6, plot_height))

        y = np.arange(len(company_names))

        for i in range(len(company_names)):
            bar_end = bar_start + bar_width
            ax.plot([bar_start, bar_end], [i, i], color='lightblue', lw=5, zorder=1)

            if high_52w[i] > low_52w[i]:
                price_position = bar_start + (current_price[i] - low_52w[i]) / (high_52w[i] - low_52w[i]) * bar_width
            else:
                price_position = bar_start

            ax.annotate('▲', xy=(price_position, i), fontsize=15, color='green', ha='center', va='center', fontweight='bold')
            ax.text(price_position, i + 0.20, f'₹{current_price[i]:.2f}', va='center', ha='center', color='black', fontweight='bold')
            ax.text(bar_start + 5, i - 0.30, f'L ₹{low_52w[i]:.2f}', va='center', ha='right', fontsize=10, color='black')
            ax.text(bar_end, i - 0.30, f'H ₹{high_52w[i]:.2f}', va='center', ha='left', fontsize=10, color='black')

        ax.set_yticks(y)
        ax.set_yticklabels(company_names, fontweight='bold')
        ax.xaxis.set_visible(False)
        ax.yaxis.set_ticks_position('none')
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        buf.seek(0)
        plot_url = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

        return plot_url

    # Fetch stock data for all stocks
    company_names, stock_data = fetch_stock_data(stocks)
    valid_stocks = [stock for stock in stocks if stock in stock_data]
    valid_company_names = [stock_data[stock]['Name'] for stock in valid_stocks]
    
    # Check if valid_stocks is empty
    if not valid_stocks:
        main_plot_url = None
    else:
        main_plot_url = create_plot(valid_company_names, stock_data, valid_stocks)
#Railway
    # Fetch stock data for Railway stocks
    railway_company_names, railway_stock_data = fetch_stock_data(railway_stocks)
    valid_railway_stocks = [stock for stock in railway_stocks if stock in railway_stock_data]
    
    # Check if valid_railway_stocks is empty
    if not valid_railway_stocks:
        railway_plot_url = None
    else:
        railway_plot_url = create_plot(railway_company_names, railway_stock_data, valid_railway_stocks)
        
#bank
    # Fetch stock data for bank stocks
    bank_company_names, bank_stock_data = fetch_stock_data(bank_stocks)
    valid_bank_stocks = [stock for stock in bank_stocks if stock in bank_stock_data]
    
    # Check if valid_bank_stocks is empty
    if not valid_bank_stocks:
        bank_plot_url = None
    else:
        bank_plot_url = create_plot(bank_company_names, bank_stock_data, valid_bank_stocks)

#defence
     # Fetch stock data for defence stocks
    defence_company_names, defence_stock_data = fetch_stock_data(defence_stocks)
    valid_defence_stocks = [stock for stock in defence_stocks if stock in defence_stock_data]
    
    # Check if valid_defence_stocks is empty
    if not valid_defence_stocks:
        defence_plot_url = None
    else:
        defence_plot_url = create_plot(defence_company_names, defence_stock_data, valid_defence_stocks)
        
#gold&finance
 # Fetch stock data for gold&finance stocks
    gold_finance_company_names, gold_finance_stock_data = fetch_stock_data(gold_finance_stocks)
    valid_gold_finance_stocks = [stock for stock in gold_finance_stocks if stock in gold_finance_stock_data]
    
    # Check if valid_gold&finance_stocks is empty
    if not valid_gold_finance_stocks:
        gold_finance_plot_url = None
    else:
        gold_finance_plot_url = create_plot(gold_finance_company_names, gold_finance_stock_data, valid_gold_finance_stocks)

#power_cement
  # Fetch stock data for power_cement stocks
    power_cement_company_names, power_cement_stock_data = fetch_stock_data(power_cement_stocks)
    valid_power_cement_stocks = [stock for stock in power_cement_stocks if stock in power_cement_stock_data]
    
    # Check if valid_power_cement_stocks is empty
    if not valid_power_cement_stocks:
        power_cement_plot_url = None
    else:
        power_cement_plot_url = create_plot(power_cement_company_names, power_cement_stock_data, valid_power_cement_stocks)


 # Fetch stock data for nifty stocks
    nifty_company_names, nifty_stock_data = fetch_stock_data(nifty_stocks)
    valid_nifty_stocks = [stock for stock in nifty_stocks if stock in nifty_stock_data]
    
    # Check if valid_nifty_stocks is empty
    if not valid_nifty_stocks:
        nifty_plot_url = None
    else:
        nifty_plot_url = create_plot(nifty_company_names, nifty_stock_data, valid_nifty_stocks)









    return render_template('index.html', 
                           main_plot_url=main_plot_url,
                           railway_plot_url=railway_plot_url,
                           bank_plot_url=bank_plot_url,
                           defence_plot_url=defence_plot_url,
                           gold_finance_plot_url=gold_finance_plot_url,
                           power_cement_plot_url=power_cement_plot_url,
                           nifty_plot_url=nifty_plot_url)














if __name__ == '__main__':
    app.run(debug=True)
