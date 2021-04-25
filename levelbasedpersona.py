#############################################
# LEVEL BASED PERSONA, SIMPLE SEGMENTATION AND RULE BASED CLASSIFICATION
#############################################

# Project Purpose & Steps
# - Thinking about the concept of persona.
# - To be able to define new customers according to the levels.
# - Simply segment new customer definitions using the qcut function.
# - When a new customer arrives, classify them according to segments.

# Our goal is to make groupings for customers that exist individually.
# Then it is to segment these groups.
# Finally, it is trying to determine which of these segments a new customer belongs to.

################# Before #####################
#
# country device gender age  price
# USA     and    M      15   61550
# BRA     and    M      19   45392
# DEU     iOS    F      16   41602
# USA     and    F      17   40004
#                M      23   39802

################# After #####################
#
#   customers_level_based      price groups
# 0        USA_AND_M_0_18 157120.000      A
# 1        USA_AND_F_0_18 151121.000      A
# 2        BRA_AND_M_0_18 149544.000      A
# 3        USA_IOS_F_0_18 133773.000      A
# 4       USA_AND_F_19_23 133645.000      A

import pandas as pd

# 1. Read the users and purchases data sets and merge the data sets according to the "uid" variable with inner join.
users = pd.read_csv("datasets/users.csv")
purchases = pd.read_csv("datasets/purchases.csv")
df = purchases.merge(users, how="inner", on="uid")
df.head()

# 2. What are the total earnings in country, device, gender, age breakdown?
df.groupby(["country", "device", "gender", "age"]).agg({"price": "sum"}).head()

# 3. To see the output better, apply the sort_values method to the code in descending order, according to price.
# Save the output as agg_df.
agg_df = df.groupby(["country", "device", "gender", "age"]).agg({"price": "sum"}).sort_values("price", ascending=False)
agg_df.head()

# 4. Convert agg_df's indexes to variable name.
agg_df.reset_index(inplace=True)
agg_df.head()

# 5. Convert age variable to categorical variable and add it to agg_df with the name "age_cat".
bins = [0, 18, 25, 35, 50, agg_df["age"].max()]
labels = ["0_18", "19_23", "24_30", "31_40", "41_" + str(agg_df["age"].max())]

agg_df["agg_cat"] = pd.cut(agg_df["age"], bins, labels=labels)
agg_df.head()

# 6. Define new level based customers and add them to the data set as variables.
agg_df["customers_level_based"] = [row[0] + "_" + row[1].upper() + "_" + row[2] + "_" + row[5] for row in agg_df.values]
agg_df.head()

agg_df = agg_df[["customers_level_based", "price"]]
agg_df.head()

# 7. Segment new customers according to price, add them to agg_df with the "segment" naming.
agg_df["segment"] = pd.qcut(agg_df["price"], 4, labels=["D", "C", "B", "A"])
agg_df.head()

# 8. Describe the segments.
agg_df.groupby("segment").agg({"price": "mean"})

# 9. In what segment is a 42-year-old Turkish woman using IOS?
agg_df[agg_df["customers_level_based"] == "TUR_IOS_F_41_75"]