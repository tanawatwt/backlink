import pandas as pd
from langdetect import detect
import requests, json

#read and prepare scrpaed domain
serp_df = pd.read_excel("serp.xlsx")
unique_domain_serp = serp_df.drop_duplicates(subset=['domain'])
unique_domain_serp = unique_domain_serp["domain"]
unique_domain_serp = unique_domain_serp.to_frame()
unique_domain_serp["source"] = "serp"
print(unique_domain_serp)

#prepare exisitng domain
existing_domain_df = pd.read_excel("existing domain.xlsx")
existing_domain_df = existing_domain_df["domain"]
existing_domain_df = existing_domain_df.to_frame()
existing_domain_df["source"] = "existing"
print(existing_domain_df)

#append existing domain with serp domain
appended_domain = existing_domain_df.append(unique_domain_serp)
print(appended_domain)
#remove duplicated domain from exisitng
appended_domain_unique =  appended_domain.drop_duplicates(subset=['domain'])
print(appended_domain_unique)

#select on only new serp data
domain_after_remove_dup = appended_domain_unique[appended_domain_unique["source"]=="serp"]
print(domain_after_remove_dup)

#read domain extension
domain_extension_df = pd.read_excel("domain extension.xlsx", header=None)
print(domain_extension_df)


#remove each domain extension
for extension in domain_extension_df.index :
    print(domain_extension_df[0][extension])
    domain_after_remove_dup = domain_after_remove_dup[~domain_after_remove_dup["domain"].str.contains(domain_extension_df[0][extension],na = False)]
print(domain_after_remove_dup)

#merge domain after remove everything with title dataframe
domain_after_remove_dup_with_title = pd.merge(domain_after_remove_dup, serp_df, on='domain', how="left")
domain_after_remove_dup_with_title = domain_after_remove_dup_with_title.drop_duplicates(subset="domain")
domain_after_remove_dup_with_title = domain_after_remove_dup_with_title.set_index("domain")
domain_after_remove_dup_with_title["TH title"] = ""
domain_after_remove_dup_with_title["traffic"] = ""
print(domain_after_remove_dup_with_title)

#check if title is in Thai and filte on TH description
for domain in domain_after_remove_dup_with_title.index :
    text = domain_after_remove_dup_with_title.text.loc[domain]
    # if domain == "playpark.com" :
    #     break
    try :
        lang = detect(str(text))
        domain_after_remove_dup_with_title.at[domain, "TH title"] = str(lang)
    except :
        domain_after_remove_dup_with_title.at[domain, "TH title"] = "error"

domain_after_remove_dup_with_title.to_excel("result-lang-no-traffic.xlsx")

domain_after_remove_dup_with_title_only_th = domain_after_remove_dup_with_title[domain_after_remove_dup_with_title["TH title"]=="th"]

#export traffic from ahrefs
for domain in domain_after_remove_dup_with_title_only_th.index :
    text = domain_after_remove_dup_with_title_only_th.text.loc[domain]
    # if domain == "playpark.com" :
    #     break
    try :
        request = requests.post('https://apiv2.ahrefs.com/?token=09399bb9c2eda7e2da9c9e61001138d1e9259550&target=' + domain +'&limit=1000&output=json&from=positions_metrics&mode=subdomains')
        request_json = request.json()
        domain_after_remove_dup_with_title_only_th.at[domain, "traffic"] = request_json["metrics"]["traffic"]
        print(domain, ", traffic: ", request_json["metrics"]["traffic"])
    except :
        domain_after_remove_dup_with_title_only_th.at[domain, "TH title"] = "error"

domain_after_remove_dup_with_title_only_th.to_excel("result_with_traffic.xlsx")

# domain_after_remove_dup_with_title.to_excel("result.xlsx")

# appended_domain_unique = appended_domain_unique[~appended_domain_unique["domain"].str.contains(".blogspot.com",na = False)]
# print(appended_domain_unique)




