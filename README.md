# backlink
Script for finding some new domain for backlink building for your website

# You should have SERP data for you target keyword from some SERP scraper tool e.g. scrapebox

after you got SERP data, next file you need to preapre is exisitng domain, skipped domain or any domain that you would not to consider to build backlink (you can start with linked domain in GSC, ahrefs, Moz)

I have some example file in this repo "serp.xlsx" for SERP and "existing domain.xlsx" for exisiting domain list. Please make sure you have a domain column on each excel file

We will use pandas to find unique domain for each file, and add column source, should be "serp" and "existing".

Convert to pandas dataframe. Then append these data together and remove duplicate.

Then we filtered only SERP data for next step.

The next one should be domain extension e.g. .ac.th, .go.th, .org, .blogspot that you want to filter out from your SERP list. Put it in excel file "domain extension.xlsx"

The we use pandas again to remove domain that contain these text.

Because we got only domain column. We need title description data for filter only language that we want.

We join data buy left join last data frame and SERP dataframe (this dataframe we have title data) by pandas and remove duplicated domain.

Then we use langdetect library to identify language of title and description for each domain. I already checked it 90% corrected for TH language.

Then we use ahrefs API to pull traffic data forr each domain. As through interface we can pull only 200 url per time. For APi, abit slow (around 2 URL per sec) but we can pull ulimited URLs until reach limit of package.

Next step we can use Ahrefs API to pull DR for each domain. And use moz api to pull DA for each domain. Then we can identify guest post price that we can negotiate base on our data for guest posting.


