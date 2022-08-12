import streamlit as st
import pandas as pd
import numpy as np

class AprioriAlgo:

    # init method or constructor
    def __init__(self):
        self.set_title()

    # Set Titles
    def set_title(self):
        st.set_page_config(
            page_title="Apriori",
            page_icon="👋",
        )
        st.write("# Apriori Algorithm!")

    # show data 
    def data_show(self,title,dataframe):
        # Show dataFrame
        agree = st.checkbox(title)
        if agree:
            st.table(dataframe)


    # Load Dataset 
    def load_data_set(self,datasetName):
        self.df = pd.read_csv("./DB/"+datasetName+".csv", names=['Products'])
        

    # working on dataset
    def working_data(self):
        self.grocery_df = pd.DataFrame(list(self.df["Products"].apply(lambda x:x.split(",") )))
        self.grocery_df.fillna('Null',inplace=True)
        self.data_show(title="Show Data",dataframe=self.grocery_df)
        self.TransactionEncoder(self.grocery_df)

    # Transaction Enconder
    def TransactionEncoder(self,dataframe):
        # Get Unique Columns 
        self.columns = self.get_unique_values(dataframe)
        self.data_show(title="Show Unique Columns",dataframe=self.columns)

        # Create Tidy Data's
        self.tidy_data = self.tidy_data()
        self.data_show(title="Show Tidy Data",dataframe=self.tidy_data)
        
        # Sum Of Data
        self.data_show(title="Show Sum Of Tidy Data",dataframe=self.tidy_data.sum())

        # Calculating Support Value
        self.supportVal = self.calc_support_val(self.tidy_data)
        self.data_show(title="Show All Support Value ( in % )",dataframe=self.supportVal)
        self.data_show(title="Show >=15% Support Value ( in % )",dataframe=self.supportVal[self.supportVal.Support >= 15])
        pass

    # unique values
    def get_unique_values(self,dataframe):
        unique_list = []
        for i in range(0,dataframe.shape[0]):
            for j in range(0,dataframe.shape[1]):
                if(dataframe[j][i] != "Null"):
                    if dataframe[j][i] not in unique_list:
                        unique_list.append(dataframe[j][i])
        unique_list.sort()
        return unique_list

    # Create Tidly Data
    def tidy_data(self):
        new_rows = []
        for i in range(len(self.grocery_df)):
            new_data = []
            demoLst = list(self.grocery_df.iloc[i])
            for unq in self.columns:
                if unq in demoLst: 
                    new_data.append(1)
                else: 
                    new_data.append(0)
            new_rows.append(new_data)   
        tidy_data = pd.DataFrame(new_rows,columns=self.columns) 
        return tidy_data

    # Calculating Support Value
    def calc_support_val(self,dataframe):
        sup = pd.DataFrame(((dataframe.sum() / dataframe.shape[0]) * 100), columns = ["Support"]).sort_values("Support", ascending = False)
        return sup


    # ---------------------------------------------------------Code from Here--------------------------------------------------------

    def aprioriFun(self,trans_data,supp=3, con=0.5):
        freq = pd.DataFrame()
        df = self.count_item(trans_data)
        self.data_show(title="Show Count Item",dataframe=df)
        i = 1;
        while(len(df) != 0):
            df = self.prune(df, supp)
    
            if len(df) > 1 or (len(df) == 1 and int(df.supp_count >= supp)):
                freq = df
            
            itemsets = self.join(df.item_sets)
        
            if(itemsets is None):
                return freq
        
            df = self.count_itemset(trans_data, itemsets)
            self.data_show(title="Show ItemSet {0}".format(i),dataframe=df)
            i = i + 1
        return df

    def prune(self,data,supp):    
        df = data[data.supp_count >= supp] 
        return df

    def count_itemset(self,transaction_df, itemsets):    
        count_item = {}
        for item_set in itemsets:
            set_A = set(item_set)
            for row in trans_df:
                set_B = set(row)
            
                if set_B.intersection(set_A) == set_A: 
                    if item_set in count_item.keys():
                        count_item[item_set] += 1
                    
                    else:
                        count_item[item_set] = 1
                    
        data = pd.DataFrame()
        data['item_sets'] = count_item.keys()
        data['supp_count'] = count_item.values()
    
        return data

    def count_item(self,trans_items):    
        count_ind_item = {}
        for row in trans_items:
            for i in range(len(row)):
                if row[i] in count_ind_item.keys():
                    count_ind_item[row[i]] += 1
                else:
                    count_ind_item[row[i]] = 1
        
        data = pd.DataFrame()
        data['item_sets'] = count_ind_item.keys()
        data['supp_count'] = count_ind_item.values()
        data = data.sort_values('item_sets')
        return data

    def join(self,list_of_items):
        itemsets = []
        i = 1
        for entry in list_of_items:
            proceding_items = list_of_items[i:]
            for item in proceding_items:
                if(type(item) is str):
                    if entry != item:
                        tuples = (entry, item)
                        itemsets.append(tuples)
                else:
                    if entry[0:-1] == item[0:-1]:
                        tuples = entry+item[1:]
                        itemsets.append(tuples)
            i = i+1
        if(len(itemsets) == 0):
            return None
        return itemsets

apriori = AprioriAlgo()
option = st.selectbox('select CSV V1',('Select','GroceryStoreDataSet'))
if(option != "Select"):
    df = pd.read_csv("./DB/"+option+".csv", names=['Products'])
    trans_df = df.Products.str.split(',')
    freq_item_sets = apriori.aprioriFun(trans_df, 4)
    apriori.data_show(title="Show Final Output",dataframe=freq_item_sets)

st.markdown("""---""")

option = st.selectbox('select CSV V2',('Select','GroceryStoreDataSet'))
if(option != "Select"):
    apriori.load_data_set(datasetName=option)
    apriori.working_data()
