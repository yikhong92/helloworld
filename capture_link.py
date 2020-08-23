import requests
import m3u8
import re
import os
tv_channel = [
    "https://www.dailymotion.com/embed/video/kxm1wihUkjNiINrAqlg",  # NTV7
    "https://www.dailymotion.com/embed/video/kdFzSYy1bHxrForBrar",  # TV8
]
ch_addr = {}
for index, channel in enumerate(tv_channel):
    html = requests.get(channel)
    match_obj = re.search(r'\"url\":\"(https:\\/\\/www\.dailymotion\.com\\/cdn.*/(.*)\.m3u8\?sec=.*\"\}\]\},)', html.text)
    m3u8_link = match_obj.group(1).rstrip("\"}]},")
    m3u8_link = re.sub(r'\\/', '/', m3u8_link)
    print(m3u8_link)
    html = requests.get(m3u8_link)
    m3u8_obj = m3u8.loads(html.text)
    print(m3u8_obj.data)
    for url in m3u8_obj.data['playlists']:
        if url['stream_info']['name'] == '"720"':
            # print(url['uri'])
            if match_obj.group(2) in url['uri']:
                print(url['uri'].split('#cell')[0])
                if index == 0:
                    ch_addr['NTV7'] = url['uri'].split('#cell')[0]
                else:
                    ch_addr['TV8'] = url['uri'].split('#cell')[0]

# os.chdir("helloworld")
# os.system("git pull")
git_change = False
with open("testing_1.m3u", 'w', encoding="utf-8") as output_testing:
    with open("testing.m3u", encoding="utf-8") as git_file:
        for line in git_file:

            if re.match(r'.*(sec\(.*\))/dm.*kxm1wihUkjNiINrAqlg$', line):
                match_obj = re.match(r'.*(sec\(.*\))/dm.*kxm1wihUkjNiINrAqlg$', line)
                print(line)
                print(match_obj.group(1))
                ch_sec_group = re.match(r'.*(sec\(.*\)).*', ch_addr['NTV7']).group(1)
                if match_obj.group(1) != ch_sec_group:
                    print("update new link for NTV7")
                    line = re.sub(r'.*\.m3u8', ch_addr['NTV7'], line)
                    git_change = True
            if re.match(r'.*(sec\(.*\))/dm.*kdFzSYy1bHxrForBrar$', line):
                match_obj = re.match(r'.*(sec\(.*\))/dm.*kdFzSYy1bHxrForBrar$', line)
                print(line)
                print(match_obj.group(1))
                ch_sec_group = re.match(r'.*(sec\(.*\)).*', ch_addr['TV8']).group(1)
                if match_obj.group(1) != ch_sec_group:
                    print("update new link for TV8")
                    line = re.sub(r'.*\.m3u8', ch_addr['TV8'], line)
                    git_change = True

            output_testing.write(line)

os.remove("testing.m3u")
os.rename("testing_1.m3u", "testing.m3u")

if git_change:
    os.makedirs("git_hub_commit")
    os.chdir("git_hub_commit")
    os.system("git clone https://github.com/yikhong92/helloworld.git .")

