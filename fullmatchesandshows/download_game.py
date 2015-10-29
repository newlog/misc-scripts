#!/usr/bin/env python
import requests
import argparse
import re
import subprocess
import os
import json

visited_links = []
correct_pattern_links = []

def get_links(urls, ignore):
    links = []
    ignore_list = ignore.split(',')
    for link in urls:
        valid_link = True
        for ext in ignore_list:
            if ext and link.endswith(ext):
                valid_link = False
                break
        if valid_link:
            links.append(link)
    return links

def clean_url(url):
    if url.endswith('</a>'):
        url = url.replace('</a>', '')
    if url.startswith('//'):
        url = 'http:' + url
    return url

def get_all_website_links(url, ignore):
    links = []
    urls = []
    try:
        if url in visited_links:
            # print('[*] Ignoring {0}'.format(url))
            return []
        resp = requests.get(clean_url(url))
        urls = re.findall('[http|https]?//(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', resp.content)
        visited_links.append(url)
        links = get_links(urls, ignore)
        #print('[+] Analyzed {0}'.format(url))
    except Exception as e:
        print('[-] Could not connect to {0}. Error: {1}'.format(url, e))
    return links

def find_pattern_links(pattern, links):
    pattern_links = []
    for link in links:
        if pattern in link:
            print('[+] Correct pattern link found: {0}'.format(link))
            pattern_links.append(link)
            correct_pattern_links.append(link)
    return pattern_links

def is_valid_domain(url, domains):
    valid_domain = False
    domains_list = domains.split(',')
    for domain in domains_list:
        if domain in url:
            valid_domain = True
            break
    return valid_domain

def handle_recursion(website_links, correct_links, depth, ignore, pattern, domains):
    if depth == 0:
        return correct_links
    else:
        for link in website_links:
            if is_valid_domain(link, domains):
                correct_links = parse_web(link, pattern, depth-1, ignore, domains)
    return correct_links

def parse_web(url, pattern, depth=2, ignore='', domains=''):
    if is_valid_domain(url, domains):
        links = get_all_website_links(url, ignore)
        found_correct_links = find_pattern_links(pattern, links)
        return handle_recursion(links, found_correct_links, depth, ignore, pattern, domains)
    return []

def build_final_urls(links):
    final_urls = []
    for link in links:
        json_objects = parse_remote_json(link)
        print_json_object(json_objects)
    return final_urls

def print_json_object(json_object):
    if type(json_object) == list:
        for j_object in json_object:
            print_json_object(j_object)
    elif json_object.get('settings'):
        print_filtered_title(json_object['settings']['title'])
    elif json_object.get('title'):
        print_filtered_title(json_object['title'])
    else:
        print_filtered_title(json_object)

def print_filtered_title(title):
    title_lower = title.lower()
    if 'bar-' in title_lower or '-bar' in title_lower or 'barcelona' in title_lower:
        print title

def parse_remote_json(url):
    json_content = {}
    try:
        res = requests.get('http:' + url)
        #print res.content
        json_content = json.loads(res.content)
    except:
        pass
    return json_content

def build_final_urls2(links):
    final_urls = []
    for link in links:
        try:
            if link.startswith('//'):
                link = link[2:]
            data = link.split('/')
            final_url = 'http://cdn.phoenix.intergi.com/' + data[1] + '/videos/' + data[4] + '/video-sd.mp4'
            final_urls.append(final_url)
        except:
            print('Manifest url malformed: {0}'.format(link))
    return final_urls

def download_files(links):
    success = True
    path = os.path.join(os.path.expanduser('~'), 'Desktop')
    for link in links:
        print('[+] Downloading {0}'.format(link))
        ret = subprocess.call(['wget','-P', path, link])
        if ret != 0:
            print('[+] An error occurred downloading file from {0}'.format(link))
            success = False
    if success:
        print('[+] Files correctly downloaded')

def run(url, pattern, depth=2, ignore='', domains='', auto=1):
    print('[+] Scraping website...')
    links = parse_web(url, pattern, depth, ignore, domains)
    video_urls = build_final_urls(correct_pattern_links)
    if auto == 1:
        download_files(video_urls)
    else:
        i = raw_input('Do you want to download files? (y/n) ')
        if i == 'y':
            download_files(video_urls)
        else:
            print('Files can be downloaded from: {0}'.format(video_urls))
    return links

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('-p', '--pattern', default='manifest.f4m')
    parser.add_argument('-d', '--depth', type=int, default=1)
    parser.add_argument('-i', '--ignore', default='js,woff,tiff,css,jpg,png,swf,mp3')
    parser.add_argument('-vd', '--domains', default='playwire,fullmatchesandshows')
    parser.add_argument('-a', '--auto', type=int, default=1)
    return parser.parse_args()

if __name__ == '__main__':
    parser = parse_args()
    links = run(parser.url, parser.pattern, parser.depth, parser.ignore, parser.domains, parser.auto)
