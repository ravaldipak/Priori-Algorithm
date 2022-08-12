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
            st.dataframe(dataframe)


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

apriori = AprioriAlgo()
option = st.selectbox('select CSV',('Select','GroceryStoreDataSet'))
if(option != "Select"):
    apriori.load_data_set(datasetName=option)
    apriori.working_data()
