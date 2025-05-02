import pandas as pd

pd.set_option('display.max_columns', None)

def quarter_hourly(input_path:str,with_date:bool):
    df = pd.read_csv(input_path,delimiter='\t')
    columns_to_remove = [col for col in df.columns if len(col.split('_')) == 2 and col.split('_')[1] == 'cd' or len(col.split('_')) == 3]
    df = df.drop(['site_no','15737_72137','15763_63680','248725_32295','15731_00010']+columns_to_remove,axis=1)
    columns_original_name = {
        '15732_72255':'Mean water velocity',
        '15735_00400':'pH',
        '15738_00065':'Gage height',
        '15757_00300':'Dissolved oxygen',
        '15760_00010':'Temperature',
        '236032_00060':'Discharge',
        '236033_63680':'Turbidity',
        '236034_00095':'Specific conductance',
        '257748_00480':'Salinity',
        '259962_00301':'Dissolved oxygen saturation percent',
        '284385_99133':'Nitrate plus nitrite',
        '340268_32316':'Chlorophyll fluorescence'
    }
    df = df.rename(columns=columns_original_name)
    df = df.drop(index=0,axis=0)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.set_index('datetime')
    df = df.astype('float')
    #Some of the data were negative which are not supposed to be negative
    df.loc[:, df.columns!='Temperature'] = df.loc[:, df.columns!='Temperature'].abs()
    quarterhourly_data = df.resample('15T').mean()
    quarterhourly_data = quarterhourly_data.reset_index()
    quarterhourly_data.set_index('datetime',inplace=True)
    if with_date:
        quarterhourly_data.to_csv("././preprocessed_data/USGSSacramento_with_date.csv",index=True,header=False)
    else:
        quarterhourly_data.to_csv("././preprocessed_data/USGSSacramento.csv",index=False,header=False)
    print('Saved Successfully')


if __name__=="__main__":
    quarter_hourly('data.txt',with_date=False)