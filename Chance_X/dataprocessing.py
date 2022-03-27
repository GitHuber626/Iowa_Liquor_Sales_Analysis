def preprocessing(df):
    '''
    Data preprocessing process, every step below has already been used in the Working Notebook with comments, so we ignore comments in this       file
    '''
    import re
    import pandas as pd
    import numpy as np
    try:
        df.drop(['invoice_and_item_number','item_number','county_number','category','volume_sold_liters'],axis=1,inplace=True)
    except:
        pass
    df['profit_per_bottle']=df['state_bottle_retail']-df['state_bottle_cost']
    df['profit_per_sale']=df['profit_per_bottle']*df['bottles_sold']
    df.drop(['store_location'],axis= 1,inplace= True)
    df['store_location_formatted']=df['store_location_formatted'].apply(lambda x: x[1:])
    df['store_location_formatted']=df['store_location_formatted'].apply(lambda x: x.strip())
    df['store_location_formatted']=df['store_location_formatted'].apply(lambda x: re.sub("\s+",",",x))
    df['coordinates']=df['store_location_formatted'].apply(lambda x: list(x.split(',')))
    for i in range(df.shape[0]):
        df['coordinates'][i].reverse()
    df.drop(['store_location_formatted'],axis= 1,inplace= True)
    df['date']=pd.to_datetime(df['date'])
    df=df.dropna(subset=['category_name'])
    df['category_name']=df['category_name'].str.lower()                                                                     
    df['liquor_type'] = np.where(df['category_name'].str.contains('rum'),'rum',
                        np.where(df['category_name'].str.contains('gin'),'gin', 
                        np.where(df['category_name'].str.contains('brandy|brandies'), 'brandy',
                        np.where(df['category_name'].str.contains('whisk|bourbon|scotch'), 'whisky',
                        np.where(df['category_name'].str.contains('tequila|mezcal'), 'tequila',
                        np.where(df['category_name'].str.contains('schnapps'), 'schnapps',
                        np.where(df['category_name'].str.contains('vodka'), 'vodka',
                        np.where(df['category_name'].str.contains('liqueur'), 'liqueur','other'))))))))
    df.drop(['category_name'],axis= 1,inplace= True)
    #add month, year and day columns
    df['month']=df['date'].dt.month
    df['year']=df['date'].dt.year
    df['day_of_year']=df['date'].dt.dayofyear
    df['day_of_week']=df['date'].dt.dayofweek
    #create a column of the different store types for hy-vee
    df['store_name']=df['store_name'].str.lower()
    def store(b):
        if ('quick' in b) or ('kwik' in b) or ('conven' in b) or ('fresh' in b):
            return 'Convenience'
        elif ('gas' in b) or ('petro' in b) or ('fuel' in b):
            return 'Gas'
        elif ('liquor' in b) or ('spirits' in b) or ('beverage' in b) or ('bottle' in b) or ('distil' in b) or ('wine' in b):
            return 'Liquor Store'
        elif ('drug' in b) or ('pharmacy' in b):
            return 'Drug Store'
        else:
            return 'Supermarket'
    df['store_type'] = df['store_name'].apply(lambda y: store(y))
    df.drop(['store_name'],axis= 1,inplace= True)
    return(df)







