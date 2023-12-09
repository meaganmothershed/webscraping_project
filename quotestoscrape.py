from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from plotly.graph_objs import Bar
from plotly import offline

url = 'http://quotes.toscrape.com/page/'

def quotestoscrape(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    req = Request(url, headers=headers)
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')

    scrapedquotes = soup.select('.quote')

    scraped = {'quotes': [], 'authors': {}, 'tags': {}}

    for quote in scrapedquotes:
        author = quote.select_one('.author').get_text()
        scraped['authors'][author] = scraped['authors'].get(author, 0) + 1
        scrapedtext = quote.select_one('.text').get_text()
        scrapedtags = [tag.get_text() for tag in quote.select('.tag')]
        scraped['quotes'].append({'author': author,
                                  'text': scrapedtext,
                                  'length': len(scrapedtext.split()),
                                  'tags': scrapedtags})

        for tag in scrapedtags:
            scraped['tags'][tag] = scraped['tags'].get(tag, 0) + 1

    return scraped

alltags = {}
quote_count = {}
length = 0
quotes = 0

for webpage in range(1, 11):
    web_url = url + str(webpage)
    scrapedwebpage = quotestoscrape(web_url)

    for author, count in scrapedwebpage['authors'].items():
        quote_count[author] = quote_count.get(author, 0) + count

    length += sum(q['length'] for q in scrapedwebpage['quotes'])
    quotes += len(scrapedwebpage['quotes'])

    for scrapedtags, count in scrapedwebpage['tags'].items():
        alltags[scrapedtags] = alltags.get(scrapedtags, 0) + count

lquotes = min(quote_count, key=quote_count.get)
mquotes = max(quote_count, key=quote_count.get)
short_quote = min(scrapedwebpage['quotes'], key=lambda i: i['length'])
long_quote = max(scrapedwebpage['quotes'], key=lambda i: i['length'])
avg_quote_length = length / quotes
total_tags = sum(alltags.values())
popular_tag = max(alltags, key=alltags.get)

print(f'Author with Most Quotes: {mquotes} - {quote_count[mquotes]}')
print(f'Author with Least Quotes: {lquotes} - {quote_count[lquotes]}')
print(f'Number of Tags: {total_tags}')
print(f'Average Length: {avg_quote_length:.2f}')
print(f'Longest Quote: {long_quote["length"]}')
print(f'Shortest Quote: {short_quote["length"]}')
print(f'Most Used Tag: {popular_tag} - {alltags[popular_tag]}')


top_author_data = sorted(quote_count.items(), key = lambda i: i[1], reverse = True)[:10]
top_authors, top_quotes = zip(*top_author_data)

auth_plot = [{'type': 'bar',
              'x': top_authors,
              'y': top_quotes}]

auth_graph = {'title': 'Top 10 Authors with Their Quotes',
              'xaxis': {'title': 'Authors'},
              'yaxis': {'title': '# of Quotes'}}

top_authors_figs = {'data': auth_plot,
                    'layout': auth_graph}

offline.plot(top_authors_figs, filename = 'authors_and_quotes.html')

tag_data = sorted(alltags.items(), key = lambda i: i[1], reverse = True)[:10]
tag_names, tag_count = zip(*tag_data)

tag_plot = [{'type': 'bar',
              'x': tag_names,
              'y': tag_count}]

tag_graph = {'title': 'Top 10 Tags',
              'xaxis': {'title': 'Tags'},
              'yaxis': {'title': '# of Tags'}}

top_tags_figs = {'data': tag_plot,
                    'layout': tag_graph}

offline.plot(top_tags_figs, filename = 'tags.html')