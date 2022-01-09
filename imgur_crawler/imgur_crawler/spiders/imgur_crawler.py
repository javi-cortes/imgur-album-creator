import scrapy

from imgur_crawler.settings import WEB_TO_CRAWL

from scrapy.linkextractors import LinkExtractor

from imgur_crawler.imgur_handler import ImgurClientWrapper


class ImgurCrawlerSpider(scrapy.Spider):
    name = 'imgur_crawler'
    start_urls = [
        WEB_TO_CRAWL,
    ]
    # from LinkExtractor class but removing images
    IGNORED_EXTENSIONS = [
        # archives
        '7z', '7zip', 'bz2', 'rar', 'tar', 'tar.gz', 'xz', 'zip',
    
        # images
        # 'mng', 'pct', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'pst', 'psp', 'tif',
        # 'tiff', 'ai', 'drw', 'dxf', 'eps', 'ps', 'svg', 'cdr', 'ico',
    
        # audio
        'mp3', 'wma', 'ogg', 'wav', 'ra', 'aac', 'mid', 'au', 'aiff',
    
        # video
        '3gp', 'asf', 'asx', 'avi', 'mov', 'mp4', 'mpg', 'qt', 'rm', 'swf', 'wmv',
        'm4a', 'm4v', 'flv', 'webm',
    
        # office suites
        'xls', 'xlsx', 'ppt', 'pptx', 'pps', 'doc', 'docx', 'odt', 'ods', 'odg',
        'odp',
    
        # other
        'css', 'pdf', 'exe', 'bin', 'rss', 'dmg', 'iso', 'apk'
    ]

    def parse(self, response, **kwargs):
        print("\n\n\n\nSTARTING TO PARSE\n\n")
        link_extractor = LinkExtractor(
            deny_extensions=self.IGNORED_EXTENSIONS,
            tags=("img",),
            attrs=("src",),
            canonicalize=True,
            unique=True,
            deny_domains=("mediavida.com", "b.scorecardresearch.com"),
        )
        imgur_client_wrapper = ImgurClientWrapper()
        # you can set your own album ID
        album_id = input("provide an imgur album ID")

        for link in link_extractor.extract_links(response):
            print(f"{link.url} found")
            imgur_img_id = imgur_client_wrapper.upload_image_to_imgur(link.url)
            if imgur_img_id:
                imgur_client_wrapper.add_image_to_album(album_id, imgur_img_id)

        follow_link = response.xpath("//a[contains(., 'Siguiente')]//@href").get()
        if follow_link:
            print(f"\n\nNext link found! legoo {follow_link}")
            next_page = response.urljoin(follow_link)
            yield scrapy.Request(next_page, callback=self.parse)

        print(f"scrappy ended at {response.url}")
