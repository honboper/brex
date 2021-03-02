from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from ast import literal_eval
from pprint import pprint
from urllib.parse import urldefrag

def get_benz(vin, wheels:list=[[0,0],[0,0]]):

    item_data = []
    base_url = f'https://mercedes.catalogs-parts.com/cat_scripts/get_vin.php?lang=en&catalog=eu&maybach=0&wheel_class=1&set_aggtyp=fg&set_vin={vin}&selectedclass=0&selectedagg=0&client=1&_=1614491468164'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    model_tag = soup.select_one('.panel.panel-default[onclick]')
    model_params = model_tag.attrs.get('onclick')
    m_list = literal_eval(model_params.replace('group_get', ''))
    
    # model_url = f'https://mercedes.catalogs-parts.com/cat_scripts/get_group.php?catalog={m_list[2]}&lang={m_list[1]}&maybach={m_list[3]}&wheel_class={m_list[4]}&classname={m_list[5]}&modelname={m_list[6]}&set_aggtyp={m_list[7]}&catalogcode={m_list[8]}&modelcode={m_list[9]}&set_spmno={m_list[10]}&set_spmaggtyp={m_list[11]}&set_spmaggmdl={m_list[12]}&set_spmaggcat={m_list[13]}&param=vin:{vin}&client=1&_=1614491468167'
    subgroup_url = f'https://mercedes.catalogs-parts.com/cat_scripts/get_subgroup.php?catalog={m_list[2]}&lang={m_list[1]}&maybach={m_list[3]}&wheel_class={m_list[4]}&classname={m_list[5]}&modelname={m_list[6]}&set_aggtyp={m_list[7]}&catalogcode={m_list[8]}&modelcode={m_list[9]}&set_spmno={m_list[10]}&set_spmaggtyp={m_list[11]}&set_spmaggmdl={m_list[12]}&set_spmaggcat={m_list[13]}&set_group=42&set_sanum=0&param=vin:{vin}&client=1&_=1614491468170'
    response = requests.get(subgroup_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    part_tags = soup.select('.panel.panel-default[onclick]')

    def get_parts(part_tags, part_code):
        for part_tag in part_tags:
            p_list = literal_eval(part_tag.attrs.get('onclick').replace('part_get',''))
            if part_code == p_list[16]:
                part_url = f'https://mercedes.catalogs-parts.com/cat_scripts/get_part.php?catalog={p_list[2]}&lang={p_list[1]}&maybach={p_list[3]}&wheel_class={p_list[4]}&classname={p_list[5]}&modelname={p_list[6]}&set_aggtyp={p_list[7]}&catalogcode={p_list[8]}&modelcode={p_list[9]}&set_spmno={p_list[10]}&set_spmaggtyp={p_list[11]}&set_spmaggmdl={p_list[12]}&set_spmaggcat={p_list[13]}&set_group={p_list[14]}&set_sanum={p_list[15]}&set_subgrp={p_list[16]}&set_stroke={p_list[17]}&set_sasubgrp={p_list[18]}&param=vin:{vin}&client=1&_=1614491468179'
        return part_url

    def get_part(url, lr, fr):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        parts = soup.select(".one_part[data-part='part_10']")
        for part in parts:
            part_text = part.text.lower()
            if lr[0] == 1:
                if 'left' in part_text:
                    item_data.append({'vin': vin, 'oem': part.a.text, 'url': url.replace(' ',"%20"), 'fr': fr, 'lr': 'l'})
            if lr[1] == 1:
                if 'right' in part_text:
                    item_data.append({'vin': vin, 'oem': part.a.text, 'url': url.replace(' ',"%20"), 'fr': fr, 'lr': 'r'})

    front, rear = wheels[0], wheels[1]
    if 1 in front:
        part_code = '030'
        part_url = get_parts(part_tags, part_code)
        get_part(part_url, front, 'f')
    if 1 in rear:
        part_code = '045'
        part_url = get_parts(part_tags, part_code)
        get_part(part_url, rear, 'r')

    return item_data

result = get_benz('WDDNG56X57A092249', [[0,1],[1,0]])
pprint(result)
print(len(result))

