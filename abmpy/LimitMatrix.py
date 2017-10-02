import pandas as pd


class LimitMatrix:
      def __init__(self, csv_path):
          df = pd.read_csv(csv_path, encoding="utf-8")
          firstCriteriaRow = [i for i, x in enumerate(df.ix[:,0]) if "nan" not in str(x)][1]  #the index of the second non null cell in first column

          self.alternative_names = df.ix[1:firstCriteriaRow-1,1]
          self.criteria_names = df.ix[firstCriteriaRow:,1]
          criteria_sum = sum(pd.to_numeric(df.ix[firstCriteriaRow:,2]))
          alternatives_sum = sum(pd.to_numeric(df.ix[2:firstCriteriaRow-1,2]))
          self.weighted_criteria = pd.to_numeric(df.ix[firstCriteriaRow:,2]).apply(lambda x:x/criteria_sum)
          self.weighted_alternatives = []
          for i in range(1,firstCriteriaRow):
              self.weighted_alternatives.append( pd.to_numeric(df.ix[i,2]) / alternatives_sum )

          self.alternatives = {}
          for i in range(1,len(self.alternative_names)+1):
              self.alternatives[self.alternative_names.get_value(i,1)] = self.weighted_alternatives[i-1]
          self.criteria = {}  
          for i in range(len(self.alternative_names)+1,len(self.alternative_names)+len(self.criteria_names)+1):
              self.criteria[self.criteria_names.get_value(i,1)] = self.weighted_criteria.get_value(i,1)


