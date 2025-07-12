from bs4 import BeautifulSoup

def extract_meta_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    meta_doc_section = soup.select_one("div.meta-doc div.flex.flex-col")
    data = {}

    if meta_doc_section:
        for block in meta_doc_section.find_all("div", class_="flex", recursive=False):
            label_div = block.find("div", class_="w-2/5")
            value_div = block.find("div", class_="w-3/5")
            
            if label_div and value_div:
                label = label_div.get_text(strip=True)
                tag_block = value_div.find("div", class_="taging")
                value = tag_block.get_text(" ", strip=True) if tag_block else value_div.get_text(strip=True)
                data[label] = value
    return data
