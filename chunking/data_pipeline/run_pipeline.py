# extract
# we will be taking a list of websites and injecting all the text into site specific files
# transform
# # clean the text so only relevant information is preserved
# # break them up into JSONs
# # embed the JSONs using OpenAI

# load
# add them to the supabase

# this should be run from chunking dir
from webscraping import scrape_site, websites
from text_processing import remove_irrelevant_info


raw_text_dir='raw_text_from_websites'
clean_text_dir='clean_text'

# scrape_site.write_text_to_directory(websites.websites, raw_text_dir)
remove_irrelevant_info.clean_raw_text(raw_text_dir, clean_text_dir)

