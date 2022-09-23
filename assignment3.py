import datetime
import argparse
import urllib.request
import csv
import io
import re

def downloadData(url):
    
    with urllib.request.urlopen(url) as response:
        response = response.read().decode('utf-8')

    return response


def process_url(data):

    image_hits = 0
    browser_dict = {
        'IE': 0,
        'Safari': 0,
        'Chrome': 0,
        'Firefox': 0
    }
   
    csv_data = csv.reader(io.StringIO(data))
    for i, row in enumerate(csv_data):
        path_to_file = row[0]
        datetime_accessed_str = row[1]
        date_accessed = datetime.datetime.strptime(datetime_accessed_str, "%Y-%m-%d %H:%M:%S")
        
        browser = row[2]
        
        
        if re.search("gif$|jpg$|png$", path_to_file.lower()):
            image_hits += 1
        
        if re.search("IE", browser.upper()):
            browser_dict["IE"] += 1
        if re.search("safari", browser.lower()):
            browser_dict["Safari"] += 1
        if re.search("chrome", browser.lower()):
            browser_dict["Chrome"] += 1
        if re.search("firefox", browser.lower()):
            browser_dict["Firefox"] += 1
    
        max = 0
        max_hits= ""
        for k, v in browser_dict.items():
            if v > max:
                max_hits = k
                max = v
        hours = {i:0 for i in range(24)}
        hours[date_accessed.hour] += 1
    
    for hour, count in hours.items():
        print(f"Hits in hour {hour} = {count}")
    
    print (f"The most popular browser is {max_hits}")

    avg_hits = image_hits / (i + 1) * 100
    print(f"Image requests account for {avg_hits}% of all requests")

    
def main(url):
    data = downloadData(url)
    process_url(data)


if __name__ == "__main__":
    url = 'http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv'
    
    my_parser = argparse.ArgumentParser(description='Assignment3 Parser')
    
    my_parser.add_argument('--url', type=str, required=True, help='The URL we want to download')
    
    args = my_parser.parse_args()

    url = args.url
    main(url)