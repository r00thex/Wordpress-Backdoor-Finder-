#!/usr/bin/env python3
# _*_ codings: utf-8 _*_

import sys
import requests
import re
import os
from multiprocessing.dummy import Pool
from colorama import Fore, init
import threading
import requests.adapters
from datetime import datetime

init(autoreset=True)

fr = Fore.RED
fc = Fore.CYAN
fw = Fore.WHITE
fg = Fore.GREEN
fm = Fore.MAGENTA
fy = Fore.YELLOW

requests.urllib3.disable_warnings()
headers = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'}

results_lock = threading.Lock()
found_results = {
    'shells': set(),
    'uploaders': set(),
    'scanned_paths': set()
}

try:
    target = [i.strip() for i in open(sys.argv[1], mode='r', encoding='utf-8').readlines()]
except IndexError:
    exit('\n Enter <script.py> <sites.txt>')

banner = '''()


▗▖ ▗▖▗▄▄▖      ▗▄▄▖▗▞▀▘▗▞▀▜▌▄▄▄▄  ▄▄▄▄  ▗▞▀▚▖ ▄▄▄ 
▐▌ ▐▌▐▌ ▐▌    ▐▌   ▝▚▄▖▝▚▄▟▌█   █ █   █ ▐▛▀▀▘█    
▐▌ ▐▌▐▛▀▘      ▝▀▚▖         █   █ █   █ ▝▚▄▄▖█    
▐▙█▟▌▐▌       ▗▄▄▞▘                               
                                                  
Wordpress Exploiter Scanner v2.0 - Intelligent WP Paths + General
developer by @roothexh

\n'''.format(fr)
print(banner)

current_year = datetime.now().year
years = [str(year) for year in range(current_year, current_year-10, -1)]

TOP_PLUGINS = [
    'contact-form-7', 'woocommerce', 'akismet', 'jetpack', 'elementor', 'wordpress-seo', 'classic-editor', 'wpforms-lite', 'updraftplus', 'wordfence', 'all-in-one-wp-migration', 'really-simple-ssl', 'wp-super-cache', 'google-analytics-for-wordpress', 'duplicate-post', 'w3-total-cache', 'wp-mail-smtp', 'all-in-one-seo-pack', 'tablepress', 'redirection', 'broken-link-checker', 'wp-optimize', 'litespeed-cache', 'wp-rocket', 'imagify', 'smush', 'shortpixel', 'regenerate-thumbnails', 'custom-post-type-ui', 'advanced-custom-fields', 'ninja-forms', 'gravity-forms', 'wpml', 'polylang', 'translatepress', 'buddypress',' bbpress', 'ultimate-member', 'memberpress', 'learnpress', 'tutor', 'sensei', 'wp-courseware', 'lifter-lms', 'easy-digital-downloads', 'wp-e-commerce', 'ecwid-shopping-cart', 'mailchimp', 'constant-contact', 'convertkit', 'mailpoet', 'newsletter'
]

TOP_THEMES = [
    'twentytwentythree', 'twentytwentytwo', 'twentytwentyone', 'twentytwenty', 'twentynineteen', 'astra', 'hello-elementor', 'generatepress', 'oceanwp', 'neve', 'kadence', 'blocksy', 'divi', 'avada', 'enfold', 'betheme', 'flatsome', 'the7', 'x', 'salient', 'bridge', 'jupiter', 'uncode', 'woodmart', 'porto', 'newspaper', 'sahifa', 'jnews', 'soledad', 'publisher'
]

WP_CORE_PATHS = [
    '/images/',
    '/assets/',
    '/.well-known/',

    *[f'/wp-content/uploads/{year}/' for year in years],
    *[f'/wp-content/uploads/{year}/01/' for year in years[:3]],
    *[f'/wp-content/uploads/{year}/12/' for year in years[:3]],

    '/wp-content/uploads/',
    '/wp-includes/',
    '/wp-admin/',
    '/wp-content/',

    '/wp-content/themes/',
    *[f'/wp-content/themes/{theme}/' for theme in TOP_THEMES[:10]],
    *[f'/wp-content/themes/{theme}/images/' for theme in TOP_THEMES[:5]],
    *[f'/wp-content/themes/{theme}/js/' for theme in TOP_THEMES[:5]],
    *[f'/wp-content/themes/{theme}/assets/' for theme in TOP_THEMES[:5]],

    '/wp-content/plugins/',
    *[f'/wp-content/plugins/{plugin}/' for plugin in TOP_PLUGINS[:15]],
    *[f'/wp-content/plugins/{plugin}/assets/' for plugin in TOP_PLUGINS[:5]],
    *[f'/wp-content/plugins/{plugin}/images/' for plugin in TOP_PLUGINS[:5]],
    *[f'/wp-content/plugins/{plugin}/uploads/' for plugin in TOP_PLUGINS[:5]],

    '/wp-content/cache/',
    '/wp-content/w3tc/',
    '/wp-content/et-cache/',
    '/wp-content/cache/supercache/',
    '/wp-content/wflogs/',
    '/wp-content/upgrade/',
    '/wp-content/updraft/',
    '/wp-content/ai1wm-backups/',
    '/wp-content/backups-dup-lite/',
    '/wp-content/backup-db/',

    '/wp-content/languages/',

    '/wp-content/mu-plugins/',

    '/wp-content/uploads/woocommerce_uploads/',
    '/wp-content/uploads/woocommerce/',
    '/wp-content/uploads/wc-logs/',

    '/wp-content/uploads/elementor/',

    '/wp-admin/includes/',
    '/wp-admin/images/',
    '/wp-admin/js/',
    '/wp-admin/css/',

    '/wp-includes/images/',
    '/wp-includes/js/',
    '/wp-includes/css/',
    '/wp-includes/fonts/',
    '/wp-includes/certificates/',
    '/wp-includes/ID3/',
    '/wp-includes/IXR/',
    '/wp-includes/PHPMailer/',
    '/wp-includes/Requests/',
    '/wp-includes/SimplePie/',
    '/wp-includes/Text/',

    '/wp-content/logs/',
    '/wp-content/database-backup/',
    '/wp-content/.tmb'
]

PHP_EXTENTIONS = ['.php', '.phtml']

Strings_Shells = [
    'Yanz Webshell!', '-rw-r--r--', 'rwxrwxrwx', 'drwxr-xr-x', 'drwxrwxrwx', 'L I E R SHELL', 'Gel4y Mini Shell', '{Ninja-Shell}', 'x3x3x3x_Sh3ll', 'LIT COURSE TEAM', '403WebShell', 'Indonesian Darknet', 'AnonSec Shell', '<title>MARIJUANA</title>', 'File manager -', 'bondowoso black hat shell', 'BlackDragon', 'xXx Kelelawar Cyber Team xXx', 'UnkownSec', 'NineSec Team Shell', 'UnkownSec Shell', '[ HOME SHELL ]', 'RC-SHELL', '<title>Mini Shell</title>', 'Mini Shell', 'Negative Shell', '[+[MAD TIGER]+]', 'Franz Private Shell', 'Webshell V1.0', '>Cassano Bypass <', 'TEAM-0ROOT', 'Fighter Kamrul Plugin', '- FierzaXploit -', '<title>FierzaXploit</title>', 'Current dir:', 'Minishell', 'Current directory:', '[ ! ] Cilent Shell Backdor [ ! ]', 'Mini Shell By Black_Shadow', 'FileManager Version', 'aDriv4-Priv8 TOOL', 'B Ge Team File Manager', 'MARIJuANA', 'ineSec Team Shell', 'CHips L Pro sangad', 'Doc Root:', '[+] MINI SH3LL BYPASS [+]', 'No_Identity', '[ Mini Shell ]', 'PHU Mini Shell', 'MSQ_403', '#wp_config_error#', 'Graybyt3 Was Here', 'One Hat Cyber Team', 'Mr.Combet WebShell', 'C0d3d By Dr.D3m0', 'Zerion Mini Shell'
]

Strings_Uploads = [
    '<input type="file"', 'type="file"',

    '<input type="file" name="file"',
    '<input type="file" name="upload"',
    '<input type="file" name="userfile"',
    '<input type="file" name="uploadfile"',
    '<input type="file" name="file_upload"',
    '<input type="file" name="uploaded_file"',
    '<input type="file" name="upload_file"',
    '<input type="file" name="fileToUpload"',
    '<input type="file" name="attachment"',
    '<input type="file" name="Filedata"',
    '<input type="file" name="files[]"', 
    '<input type="file" name="uploadedfile"', 
    '<input type="file" name="file_to_upload"', 
    '<input type="file" name="async-upload"', 
    '<input type="file" name="qqfile"', 
    '<input type="file" name="document"', 
    '<input type="file" name="image"', 
    '<input type="file" name="photo"', 
    '<input type="file" name="filUpload"',
    '<input type="file" name="_upl"',
    '<input type="file" name="upfile"',
    '<input type="file" name="tod_upl"',

    '<input type="file" name="archivo"', 
    '<input type="file" name="fichier"', 
    '<input type="file" name="datei"', 
    '<input type="file" name="文件"', 
    '<input type="file" name="ファイル"',
    '<input type="file" name="파일"',
    '<input type="file" name="dosya"',
    '<input type="file" name="bestand"',
    '<input type="file" name="ملف"', 
    # Submit buttons
    '<input type="submit" value="Upload"', 
    '<input type="submit" value="upload"',
    '<input type="submit" name="upload" value="Upload"',
    '<input type="submit" name="submit" value="Upload"',
    '<input type="submit" name="upload" value="Upload"',
    '<input type="submit" name="upload_file" value="Upload"',
    '<input type="submit" name="upload_btn" value="Upload"',
    '<input type="submit" name="uploadbtn" value="Upload"',
    '<input type="submit" name="upload_button" value="Upload"',
    '<input type="submit" name="btn_upload" value="Upload"',
    '<input type="submit" name="submit_upload" value="Upload"',
    '<input type="submit" name="doUpload" value="Upload"', 
    '<input type="submit" name="do_upload" value="Upload"',
    '<input type="submit" name="uploadfile" value="Upload"',
    '<input type="submit" name="submitbtn" value="Upload"', 
    '<input type="submit" name="sendit" value="Upload"',
    '<input type="submit" name="send" value="Upload"', 
    '<input type="submit" name="go" value="Upload"',
    '<input type="submit" name="Submit" value="Upload"', 

    '<input type="submit" name="enviar" value="Subir"', 
    '<input type="submit" name="envoyer" value="Envoyer"', 
    '<input type="submit" name="hochladen" value="Hochladen"', 
    '<input type="submit" name="sarypsat" value="Sarypsat"', 
    '<input type="submit" name="上传" value="上传"', 
    '<input type="submit" name="アップロード" value="アップロード"',
    '<input type="submit" name="업로드" value="업로드"',
    '<input type="submit" name="yukle" value="Yükle"',
    '<input type="submit" name="uploaden" value="Uploaden"', 
    '<input type="submit" name="अपलोड करें" value="अपलोड करें"', 

    '<input type="hidden" name="action" value="upload"',
    '<input type="hidden" name="task" value="upload"',
    '<input type="hidden" name="do" value="upload"',
    '<input type="hidden" name="act" value="upload"',
    '<input type="hidden" name="mode" value="upload"',
    '<input type="hidden" name="cmd" value="upload"',
    '<input type="hidden" name="op" value="upload"',
    '<input type="hidden" name="upwkwk" value="upload"',
    '<input type="hidden" name="MAX_FILE_SIZE"',

    'type="submit" name="upload">Upload',
    'type="submit" name="submit">Upload',
    'type="submit" name="upl">Upload',
    'type="submit">Upload File',
    'value="Upload" name="upload"',
    'value="Upload" name="submit"',

    '<form enctype="multipart/form-data"',
    'multipart/form-data',

    'Upload File :',
    'Select file to upload',
    'Choose file',
    'Browse...',
    'Upload Shell',
    'Upload Files',
    'File Upload',
    'Uploader',

    'onclick="upload()',
    'doUpload()',
    'uploadFile()',
    'fileupload',
    'file_upload',

    'name="fileToUpload" id="fileToUpload"',
    'submit" value="Upload"',
    'submit" name="upload"',
    'submit">Upload File<',
    'type="button">Upload File<'
]

SKIP_FILES = ['index', 'wp-config', 'wp-load', 'wp-settings', 'wp-blog-header']

#Real Wordpress core files to ignore
ReallyFiles = [
    'admin-filters', 'admin', 'ajax-actions', 'PHPMailer', 'SMTP', 'translations', 'mo', 'bookmark', 'getid3.lib', 'getid3', 'module.audio-video.asf', 'module.audio-video.flv', 'module.audio-video.matroska', 'class-wp', 'functions', 'plugin', 'theme', 'widgets', 'media', 'post',  'comment', 'user', 'link', 'taxonomy', 'update', 'option', 'meta', 'formatting', 'capabilities', 'query', 'rewrite', 'shortcodes', 'embed', 'http', 'filesystem', 'kses', 'pomo', 'sodium_compat', 'random_compat', 'requests', 'simplepie', 'IXR', 'Text', 'locale', 'l10n', 'i18n', 'sitemaps', 'block-patterns', 'block-template', 'rest-api', 'atomlib', 'registration', 'cron', 'feed', 'script-loader', 'taxonomy', 'nav-menu', 'deprecated', 'ms-functions', 'ms-default-filters', 'ms-deprecated', 'password', 'pluggable', 'default-filters', 'default-widgets', 'version', 'wp-db', 'wp-error', 'wp-hook', 'wp-json', 'wp-object-cache', 'wp-pep', 'wp-roles', 'wp-user', 'wp-xmlrpc'
]

def URLdomain(site):
    site = site.replace("http://", "").replace("https://", "")
    while '/' in site:
        site = site.split('/')[0]
    return site

def IndexOF(Contents):
    patterns = [
        '<title>Index of', '<h1>Index of', 'Index of /', 'Parent Directory',
        '<pre><a href=', '<table><tr><th>', '<td><td data-sort=', 'class="indexcolname"',
        '[DIR]', '[PARENTDIR]', 'alt="[DIR]"', '<td class="n"><a href=',
        'nginx autoindex', 'apache server at'
    ]
    return any(pattern in Contents for pattern in patterns)

def Send_Request(url, Path):
    try:
        return opt_session.get(url + Path, timeout=15, verify=False, allow_redirects=False)
    except:
        return None
    
def Extract_Files(FileName):
    if '.' in FileName:
        return os.path.splitext(FileName)[1].lower() in PHP_EXTENTIONS
    return False

def Extract_Folders(FoldersName):
    return '.' not in FoldersName

def Extract(Contents, Type):
    items = []
    patterns = [
        r'</td><td><a href="(.*?)">',
        r']"> <a href="(.*?)">',
        r'><a href="(.*?)"><img',
        r'<pre><a href="(.*?)">',
        r'<td class="n"><a href="(.*?)">',
        r'href="([^"]+)"'
    ]

    for pattern in patterns:
        items.extend(re.findall(pattern, Contents))

    items = list(set(items))
    cleaned = []

    for item in items:
        if item and item not in ['../', '/', '?', '../'] and not item.startswith('?'):
            if Type == 'Files' and Extract_Files(item):
                cleaned.append(item)
            elif Type == 'Folders' and Extract_Folders(item):
                cleaned.append(item if item.endswith('/') else item + '/')

    return cleaned

def Check_Patterns(content, pattern):
    return pattern.lower() in content.lower()

def Save_Results(result_type, url):
    with results_lock:
        if url not in found_results[result_type]:
            found_results[result_type].add(url)

            file_map = {
                'shells': 'Shells.txt',
                'uploaders': 'Uploaders.txt'
            }

            if result_type in file_map:
                with open(file_map[result_type], 'a') as f:
                    f.write(url + "\n")
                return True
    return False

def Process_File(url, path, level):
    full_url = url + path

    with results_lock:
        if full_url in found_results['scanned_paths']:
            return
        found_results['scanned_paths'].add(full_url)

    response = Send_Request(url, path)
    if not response or response.status_code != 200:
        print("Target:{} {}[{}]:{} <=== Not Vuln".format(url, fr, level, path))
        return
    
    content = response.text

    for shell_sig in Strings_Shells:
        if Check_Patterns(content, shell_sig):
            if Save_Results('shells', full_url):
                print("{}Target: {} {} <==== $${}$$ ====> Success Shell".format(fy,full_url,fg,level))
            return
        
def Scan_Deep(url, path, level, max_level=7, visited=None):
    if visited is None:
        visited = set()
    if level > max_level or path in visited:
        return
    visited.add(path)

    response = Send_Request(url, path)
    if not response:
        return
    
    if IndexOF(response.text):
        print("{}[+] Index Of - Level {} => {}{}".format(fc, level, path, fw))
        files = Extract(response.text, 'Files')
        folders = Extract(response.text, 'Folders')

        for elements in ReallyFiles:
            element = elements + ".php"
            if element in files:
                files.remove(element)

        for file in files:
            if not any(skip in file for skip in SKIP_FILES):
                Process_File(url, path + file, level)

        for folder in folders:
            if folder not in ['../', './', '/']:
                print("{}[*] Level {} => {}{}".format(fm, level + 1, path + folder, fw))
                Scan_Deep(url, path + folder, level + 1, max_level, visited.copy())

def CmsChecker(site):
    url = "http://" + URLdomain(site)
    print("\n{}[+] WordPress Site: {}{}".format(fc, url, fw))

    for path in WP_CORE_PATHS:
        print("\n{}[*] Checking: {}{}".format(fm, path, fw))
        Scan_Deep(url, path, 1)

class OptimizedSession:
    def __init__(self):
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=100,
            pool_maxsize=100,
            max_retries=0
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.session.headers.update({'User-Agent': headers['User-Agent']})
        self.session.max_redirects = 1

    def get(self, url, **kwargs):
        return self.session.get(url, **kwargs)
opt_session = OptimizedSession()

if __name__ == "__main__":
    print("{}[!] WordPress Enchanced Settings:{}".format(fy, fw))
    print("     - Max Depth: 7 levels")
    print("     - WordPress + General Paths: {} total paths".format(len(WP_CORE_PATHS)))
    print("     - General Paths: /images/, /assets/, /.well-known/")
    print("     - Top Plugins: {} plugins included".format(len(TOP_PLUGINS)))
    print("     - Top Themes: {} themes included".format(len(TOP_THEMES)))
    print("     - Years Range: {} years ({}-{})".format(len(years), years[-1], years[0]))
    print("     - Threading: 150 threads\n")

    mp = Pool(150)
    mp.map(CmsChecker, target)
    mp.close()
    mp.join()

    print("\n{}[+] Completed!{}".format(fg, fw))
    print("{}[+] Results:{}".format(fg, fw))
    print("     - Shells.txt: {}".format(len(found_results['shells'])))
    print("     - Uploaders.txt: {}".format(len(found_results['uploaders'])))
    print("     - Total Scanned: {}".format(len(found_results['scanned_paths'])))
