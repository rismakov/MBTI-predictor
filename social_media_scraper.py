import requests
from bs4 import BeautifulSoup

from stylometry_analysis import StyleFeatures

def get_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, 'html.parser')

def get_posts(code_section, klass):
    return code_section.find_all(class_=klass)

def get_featurized_posts(url, klass):
	soup = get_soup(url)

	print(soup)

	posts = '|||'.join([post.text for post in get_posts(soup, klass)])

	print(get_posts(soup, klass))

	print(posts)
	return StyleFeatures(posts)


if __name__ == '__main__':

	url = 'https://twitter.com/elonmusk'
	tweet_html_class = "js-tweet-text-container"
	features = get_featurized_posts(url, tweet_html_class)

	filename = 'Fitted_Model_XGBC_Style'
	loaded_model = pickle.load(open(filename, 'rb'))

	data = pd.DataFrame()
	data['stylometry'] = stylometry

    features = data['stylometry'][0]
    for feature in features:
        print(feature)
        data[feature] = [d[feature] for d in data['stylometry']]

    data.drop('stylometry', axis=1, inplace=True)
    print(data.columns)

	loaded_model.predict(features)

	
	# url = 'https://www.facebook.com/...'	
	# fb_html_class = "_5pbx userContent _3ds9 _3576" 
	# fb_html_class = "_5pcr userContentWrapper"

	# featurized_posts = get_featurized_posts(url, fb_html_class)

	
