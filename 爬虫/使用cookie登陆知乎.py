import urllib.request

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'cookie': '_zap=ad3a2cda-1362-46bf-b772-edf15ad22dd1; d_c0=AFDTfSw27RWPTg60Uw42ejwX14TXA_2sCVc=|1669476254; __snaker__id=4LB2wgmQrYQJKIJa; YD00517437729195%3AWM_NI=f4MnF8wX6MvQ5puLdcFntnqg22ZqkheHVya3ixuppxM7neuDREQPOaAxmE1h44p5f58u%2BgCaCK3RVTDq65EFeTvTJ0CZuhAYZyE6nZLgqOK0Ygu%2BvPtLzvZP49f%2BGwa%2FbXM%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eed2d25c89e89996c661e99a8bb3c14a878e8bacc1709aebf9a8b26df798c0b4e92af0fea7c3b92aa6ec838fc534b588faaef55bf7b0bbade76986b2bc8ff46df2ee9692ea64a7989a9ae439aba8bb91f3748fe9a286f850929b9fb1ce6b83a8a3a6b464f8ecc0d6e53ffcabe588c26b8195fdb3d56088affad6c84ea78cbab5c93c8186bb89c4539aa78bd7ed5290b9bfb0ca3c9bb9bbccf55cb894b697d95cf8e7aaccc67da3f1aeb9d037e2a3; YD00517437729195%3AWM_TID=e5hklYUHrD9ABVBFUUeQIdtqHikoCtWy; q_c1=c866a33fd70c4279a30b09347441566a|1669521119000|1669521119000; z_c0=2|1:0|10:1675078015|4:z_c0|80:MS4xMzNXckdnQUFBQUFtQUFBQVlBSlZUWF8zeEdRWHBLRUFnX1NYUkpqSUg2dlhteWpVRjlTSE1nPT0=|e423d3d4fdff8b3040f417de8544441522e544a8f75cf89acff8c45262808c57; _xsrf=2f154a7c-3e05-4ea1-adde-362fad31e689; arialoadData=false; tst=r; SUBMIT_0=08f8a8fe-b95b-4199-b065-6326179f6b40; KLBRSID=031b5396d5ab406499e2ac6fe1bb1a43|1675487366|1675487239; SESSIONID=iqKeuxHosW5CyxPqDGzgHlL88a7xMsYfqAGQ8OOABg8',
    'referer': 'https://www.zhihu.com/people/ijiayezi'}

url = 'https://www.zhihu.com/creator'
request = urllib.request.Request(url=url, headers=headers)
response = urllib.request.urlopen(request)
content = response.read().decode('utf-8')

with open('E:/库/桌面/0.html', 'wt', encoding='utf-8') as f:
    f.write(content)
