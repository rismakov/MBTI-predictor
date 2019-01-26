from __future__ import division

import unittest

from stylometry_analysis import StyleFeatures
from utils.utils import get_freq_of_characters_in_text_in_list, get_freq_of_items_in_list, get_count_of_characters_in_text

text = (
    "http://www.youtube.com/watch?v=qsXHcwe3krw|||http://41.media.tumblr.com/tumblr_lfouy03PMA1qa1rooo1_500.jpg|||enfp"
    " and intj moments  https://www.youtube.com/watch?v=iz7lE1g4XM4  sportscenter not top ten plays  https://www.youtub"
    "e.com/watch?v=uCdfze1etec  pranks|||What has been the most life-changing experience in your life?|||http://www.you"
    "tube.com/watch?v=vXZeYwwRDw8   http://www.youtube.com/watch?v=u8ejam5DP3E  On repeat for most of today.|||May the "
    "PerC Experience immerse you.|||The last thing my INFJ friend posted on his facebook before committing suicide the "
    "next day. Rest in peace~   http://vimeo.com/22842206|||Hello ENFJ7. Sorry to hear of your distress. It's only natu"
    "ral for a relationship to not be perfection all the time in every moment of existence. Try to figure the hard time"
    "s as times of growth, as...|||84389  84390  http://wallpaperpassion.com/upload/23700/friendship-boy-and-girl-wallp"
    "aper.jpg  http://assets.dornob.com/wp-content/uploads/2010/04/round-home-design.jpg ...|||Welcome and stuff.|||htt"
    "p://playeressence.com/wp-content/uploads/2013/08/RED-red-the-pokemon-master-32560474-450-338.jpg  Game. Set. Match"
    ".|||Prozac, wellbrutin, at least thirty minutes of moving your legs (and I don't mean moving them while sitting in"
    " your same desk chair), weed in moderation (maybe try edibles as a healthier alternative...|||Basically come up wi"
    "th three items you've determined that each type (or whichever types you want to do) would more than likely use, gi"
    "ven each types' cognitive functions and whatnot, when left by...|||All things in moderation.  Sims is indeed a vid"
    "eo game, and a good one at that. Note: a good one at that is somewhat subjective in that I am not completely promo"
    "ting the death of any given Sim...|||Dear ENFP:  What were your favorite video games growing up and what are your "
    "now, current favorite video games? :cool:|||https://www.youtube.com/watch?v=QyPqT8umzmY|||It appears to be too lat"
    "e. :sad:|||There's someone out there for everyone.|||Wait... I thought confidence was a good thing.|||I just cheri"
    "sh the time of solitude b/c i revel within my inner world more whereas most other time i'd be workin... just enjoy"
    " the me time while you can. Don't worry, people will always be around to...|||Yo entp ladies... if you're into a c"
    "omplimentary personality,well, hey.|||... when your main social outlet is xbox live conversations and even then yo"
    "u verbally fatigue quickly.|||http://www.youtube.com/watch?v=gDhy7rdfm14  I really dig the part from 1:46 to 2:50|"
    "||http://www.youtube.com/watch?v=msqXffgh7b8|||Banned because this thread requires it of me.|||Get high in backyar"
    "d, roast and eat marshmellows in backyard while conversing over something intellectual, followed by massages and k"
    "isses.|||http://www.youtube.com/watch?v=Mw7eoU3BMbE|||http://www.youtube.com/watch?v=4V2uYORhQOk|||http://www.yout"
    "ube.com/watch?v=SlVmgFQQ0TI|||Banned for too many b's in that sentence. How could you! Think of the B!|||Banned fo"
    "r watching movies in the corner with the dunces.|||Banned because Health class clearly taught you nothing about pe"
    "er pressure.|||Banned for a whole host of reasons!|||http://www.youtube.com/watch?v=IRcrv41hgz4|||1) Two baby deer"
    " on left and right munching on a beetle in the middle.  2) Using their own blood, two cavemen diary today's latest"
    " happenings on their designated cave diary wall.  3) I see it as...|||a pokemon world  an infj society  everyone b"
    "ecomes an optimist|||49142|||http://www.youtube.com/watch?v=ZRCEq_JFeFM|||http://discovermagazine.com/2012/jul-aug"
    "/20-things-you-didnt-know-about-deserts/desert.jpg|||http://oyster.ignimgs.com/mediawiki/apis.ign.com/pokemon-silv"
    "er-version/d/dd/Ditto.gif|||http://www.serebii.net/potw-dp/Scizor.jpg|||Not all artists are artists because they d"
    "raw. It's the idea that counts in forming something of your own... like a signature.|||Welcome to the robot ranks,"
    " person who downed my self-esteem cuz I'm not an avid signature artist like herself. :proud:|||Banned for taking a"
    "ll the room under my bed. Ya gotta learn to share with the roaches."
)

text_with_punctuation_where_missing = (
    "http://www.youtube.com/watch?v=qsXHcwe3krw. http://41.media.tumblr.com/tumblr_lfouy03PMA1qa1rooo1_500.jpg. enfp"
    " and intj moments  https://www.youtube.com/watch?v=iz7lE1g4XM4  sportscenter not top ten plays  https://www.youtub"
    "e.com/watch?v=uCdfze1etec  pranks. What has been the most life-changing experience in your life? http://www.you"
    "tube.com/watch?v=vXZeYwwRDw8   http://www.youtube.com/watch?v=u8ejam5DP3E  On repeat for most of today. May the "
    "PerC Experience immerse you. The last thing my INFJ friend posted on his facebook before committing suicide the "
    "next day. Rest in peace~   http://vimeo.com/22842206. Hello ENFJ7. Sorry to hear of your distress. It's only natu"
    "ral for a relationship to not be perfection all the time in every moment of existence. Try to figure the hard time"
    "s as times of growth, as... 84389  84390  http://wallpaperpassion.com/upload/23700/friendship-boy-and-girl-wallp"
    "aper.jpg  http://assets.dornob.com/wp-content/uploads/2010/04/round-home-design.jpg ... Welcome and stuff. htt"
    "p://playeressence.com/wp-content/uploads/2013/08/RED-red-the-pokemon-master-32560474-450-338.jpg  Game. Set. Match"
    ". Prozac, wellbrutin, at least thirty minutes of moving your legs (and I don't mean moving them while sitting in"
    " your same desk chair), weed in moderation (maybe try edibles as a healthier alternative... Basically come up wi"
    "th three items you've determined that each type (or whichever types you want to do) would more than likely use, gi"
    "ven each types' cognitive functions and whatnot, when left by... All things in moderation.  Sims is indeed a vid"
    "eo game, and a good one at that. Note: a good one at that is somewhat subjective in that I am not completely promo"
    "ting the death of any given Sim... Dear ENFP:  What were your favorite video games growing up and what are your "
    "now, current favorite video games? :cool:. https://www.youtube.com/watch?v=QyPqT8umzmY. It appears to be too lat"
    "e. :sad:. There's someone out there for everyone. Wait... I thought confidence was a good thing. I just cheri"
    "sh the time of solitude b/c i revel within my inner world more whereas most other time i'd be workin... just enjoy"
    " the me time while you can. Don't worry, people will always be around to... Yo entp ladies... if you're into a c"
    "omplimentary personality,well, hey. ... when your main social outlet is xbox live conversations and even then yo"
    "u verbally fatigue quickly. http://www.youtube.com/watch?v=gDhy7rdfm14  I really dig the part from 1:46 to 2:50. "
    "http://www.youtube.com/watch?v=msqXffgh7b8. Banned because this thread requires it of me. Get high in backyar"
    "d, roast and eat marshmellows in backyard while conversing over something intellectual, followed by massages and k"
    "isses. http://www.youtube.com/watch?v=Mw7eoU3BMbE. http://www.youtube.com/watch?v=4V2uYORhQOk. http://www.yout"
    "ube.com/watch?v=SlVmgFQQ0TI. Banned for too many b's in that sentence. How could you! Think of the B! Banned fo"
    "r watching movies in the corner with the dunces. Banned because Health class clearly taught you nothing about pe"
    "er pressure. Banned for a whole host of reasons! http://www.youtube.com/watch?v=IRcrv41hgz4. 1) Two baby deer"
    " on left and right munching on a beetle in the middle.  2) Using their own blood, two cavemen diary today's latest"
    " happenings on their designated cave diary wall.  3) I see it as... a pokemon world  an infj society  everyone b"
    "ecomes an optimist. 49142. http://www.youtube.com/watch?v=ZRCEq_JFeFM. http://discovermagazine.com/2012/jul-aug"
    "/20-things-you-didnt-know-about-deserts/desert.jpg. http://oyster.ignimgs.com/mediawiki/apis.ign.com/pokemon-silv"
    "er-version/d/dd/Ditto.gif. http://www.serebii.net/potw-dp/Scizor.jpg. Not all artists are artists because they d"
    "raw. It's the idea that counts in forming something of your own... like a signature. Welcome to the robot ranks,"
    " person who downed my self-esteem cuz I'm not an avid signature artist like herself. :proud:. Banned for taking a"
    "ll the room under my bed. Ya gotta learn to share with the roaches."
)

expected_sentences = [
    "http://www.youtube.com/watch?v=qsXHcwe3krw.",
    "http://41.media.tumblr.com/tumblr_lfouy03PMA1qa1rooo1_500.jpg.",
    "enfp and intj moments  https://www.youtube.com/watch?v=iz7lE1g4XM4  sportscenter not top ten plays  https://www.yo"
        "utube.com/watch?v=uCdfze1etec  pranks.",
    "What has been the most life-changing experience in your life?",
    "http://www.youtube.com/watch?v=vXZeYwwRDw8   http://www.youtube.com/watch?v=u8ejam5DP3E  On repeat for most of tod"
        "ay.",
    "May the PerC Experience immerse you.",
    "The last thing my INFJ friend posted on his facebook before committing suicide the next day.",
    "Rest in peace~   http://vimeo.com/22842206.",
    "Hello ENFJ7.",
    "Sorry to hear of your distress.",
    "It's only natural for a relationship to not be perfection all the time in every moment of existence.",
    "Try to figure the hard times as times of growth, as... 84389  84390  http://wallpaperpassion.com/upload/23700/frie"
        "ndship-boy-and-girl-wallpaper.jpg  http://assets.dornob.com/wp-content/uploads/2010/04/round-home-design"
        ".jpg ...",
    "Welcome and stuff.",
    "http://playeressence.com/wp-content/uploads/2013/08/RED-red-the-pokemon-master-32560474-450-338.jpg  Game.",
    "Set.",
    "Match.",
    "Prozac, wellbrutin, at least thirty minutes of moving your legs (and I don't mean moving them while sitting in"
        " your same desk chair), weed in moderation (maybe try edibles as a healthier alternative... Basically come up "
        "with three items you've determined that each type (or whichever types you want to do) would more than likely u"
        "se, given each types' cognitive functions and whatnot, when left by... All things in moderation.",
    "Sims is indeed a video game, and a good one at that.",
    "Note: a good one at that is somewhat subjective in that I am not completely promoting the death of any given Sim.."
        ". Dear ENFP:  What were your favorite video games growing up and what are your "
    "now, current favorite video games?",
    ":cool:.",
    "https://www.youtube.com/watch?v=QyPqT8umzmY.",
    "It appears to be too late.",
    ":sad:.",
    "There's someone out there for everyone.",
    "Wait...",
    "I thought confidence was a good thing.",
    "I just cherish the time of solitude b/c i revel within my inner world more whereas most other time i'd be workin.."
        ". just enjoy the me time while you can.",
    "Don't worry, people will always be around to... Yo entp ladies... if you're into a complimentary personality,well,"
        " hey.",
    "... when your main social outlet is xbox live conversations and even then you verbally fatigue quickly.",
    "http://www.youtube.com/watch?v=gDhy7rdfm14  I really dig the part from 1:46 to 2:50. http://www.youtube.com/watch?"
        "v=msqXffgh7b8.",
    "Banned because this thread requires it of me.",
    "Get high in backyard, roast and eat marshmellows in backyard while conversing over something intellectual, followe"
        "d by massages and kisses.",
    "http://www.youtube.com/watch?v=Mw7eoU3BMbE.",
    "http://www.youtube.com/watch?v=4V2uYORhQOk.",
    "http://www.youtube.com/watch?v=SlVmgFQQ0TI.",
    "Banned for too many b's in that sentence.",
    "How could you!",
    "Think of the B!",
    "Banned for watching movies in the corner with the dunces.",
    "Banned because Health class clearly taught you nothing about peer pressure.",
    "Banned for a whole host of reasons!",
    "http://www.youtube.com/watch?v=IRcrv41hgz4.",
    "1) Two baby deer on left and right munching on a beetle in the middle.",
    "2) Using their own blood, two cavemen diary today's latest happenings on their designated cave diary wall.",
    "3) I see it as... a pokemon world  an infj society  everyone becomes an optimist.",
    "49142. http://www.youtube.com/watch?v=ZRCEq_JFeFM.",
    "http://discovermagazine.com/2012/jul-aug/20-things-you-didnt-know-about-deserts/desert.jpg.",
    "http://oyster.ignimgs.com/mediawiki/apis.ign.com/pokemon-silver-version/d/dd/Ditto.gif.",
    "http://www.serebii.net/potw-dp/Scizor.jpg.",
    "Not all artists are artists because they draw.",
    "It's the idea that counts in forming something of your own... like a signature.",
    "Welcome to the robot ranks, person who downed my self-esteem cuz I'm not an avid signature artist like herself.",
    ":proud:.",
    "Banned for taking all the room under my bed.",
    "Ya gotta learn to share with the roaches."
]

expected_links = [
    'www.youtube.com/watch',
    '41.media.tumblr.com/tumblr_lfouy03PMA1qa1rooo1_500.jpg',
    'www.youtube.com/watch', 'www.youtube.com/watch',
    'www.youtube.com/watch', 'www.youtube.com/watch',
    'vimeo.com/22842206',
    'wallpaperpassion.com/upload/23700/friendship-boy-and-girl-wallpaper.jpg',
    'assets.dornob.com/wp-content/uploads/2010/04/round-home-design.jpg',
    'playeressence.com/wp-content/uploads/2013/08/RED-red-the-pokemon-master-32560474-450-338.jpg',
    'www.youtube.com/watch', 'www.youtube.com/watch',
    'www.youtube.com/watch', 'www.youtube.com/watch',
    'www.youtube.com/watch', 'www.youtube.com/watch',
    'www.youtube.com/watch', 'www.youtube.com/watch',
    'discovermagazine.com/2012/jul-aug/20-things-you-didnt-know-about-deserts/desert.jpg',
    'oyster.ignimgs.com/mediawiki/apis.ign.com/pokemon-silver-version/d/dd/Ditto.gif',
    'www.serebii.net/potw-dp/Scizor.jpg'
]

class StyleFeaturesTests(unittest.TestCase):
    def test_add_periods_to_end_of_posts_if_punct_missing(self):
        style_text = StyleFeatures(text)
        result = style_text.add_periods_to_end_of_posts_if_punct_missing()

        self.assertEqual(len(result), len(text_with_punctuation_where_missing))
        self.assertEqual(result, text_with_punctuation_where_missing)

    def test_get_sentences(self):
        self.maxDiff = None

        sentence_w_ellipse_at_front = '...This is a sentence. This is another sentence.'
        expected_result = ['...This is a sentence.', 'This is another sentence.']
        style_text = StyleFeatures(sentence_w_ellipse_at_front)
        self.assertEqual(style_text.get_sentences(), expected_result)

        sentence_w_ellipse_at_end = 'This is a sentence. this is another sentence...'
        expected_result = ['This is a sentence.', 'this is another sentence...']
        style_text = StyleFeatures(sentence_w_ellipse_at_end)
        self.assertEqual(style_text.get_sentences(), expected_result)

        sentence_w_ellipse_at_end_and_front = '...This is a sentence... This is another sentence...'
        expected_result = ['...This is a sentence...', 'This is another sentence...']
        style_text = StyleFeatures(sentence_w_ellipse_at_end_and_front)
        self.assertEqual(style_text.get_sentences(), expected_result)

        sentence_w_ellipse_at_middle = 'This is a sentence.. This is another sentence...'
        expected_result = ['This is a sentence..', 'This is another sentence...']
        style_text = StyleFeatures(sentence_w_ellipse_at_middle)
        self.assertEqual(style_text.get_sentences(), expected_result)

        sentence_w_ellipse_at_middle_2 = 'This is a sentence... this is another sentence...'
        expected_result = ['This is a sentence... this is another sentence...']
        style_text = StyleFeatures(sentence_w_ellipse_at_middle_2)
        self.assertEqual(style_text.get_sentences(), expected_result)

        sentence_w_two_ellipses = '...This is a sentence.. this is another sentence...'
        expected_result = ['...This is a sentence.. this is another sentence...']
        style_text = StyleFeatures(sentence_w_two_ellipses)
        self.assertEqual(style_text.get_sentences(), expected_result)

        text_2 = '...This is a sentence||| This is another sentence...'
        expected_result = ['...This is a sentence.', 'This is another sentence...']
        style_text = StyleFeatures(text_2)
        self.assertEqual(style_text.get_sentences(), expected_result)

        text_3 = 'This is a sentence.||| This is another sentence...'
        expected_result = ['This is a sentence.', 'This is another sentence...']
        style_text = StyleFeatures(text_3)
        self.assertEqual(style_text.get_sentences(), expected_result)

        text_4 = 'This is a sentence...||| This is another sentence...'
        expected_result = ['This is a sentence...', 'This is another sentence...']
        style_text = StyleFeatures(text_4)
        self.assertEqual(style_text.get_sentences(), expected_result)

        text_5 = 'This is a sentence...||| ...This is another sentence'
        expected_result = ['This is a sentence...', '...This is another sentence.']
        style_text = StyleFeatures(text_5)
        self.assertEqual(style_text.get_sentences(), expected_result)

        text_6 = 'This is a sentence...||| ...This is another sentence...'
        expected_result = ['This is a sentence...', '...This is another sentence...']
        style_text = StyleFeatures(text_6)
        self.assertEqual(style_text.get_sentences(), expected_result)

        style_text = StyleFeatures(text)
        self.assertEqual(style_text.get_sentences(), expected_sentences)

    def test_get_words(self):
        sentence = ("Welcome to the robot ranks, person who downed my self-esteem cuz I'm not an avid signature artist "
                    "like herself. :proud:. http://www.youtube.com/watch?v=qsXHcwe3krw. ADD UPPERCASE WORDS.")

        expected_words = [
            'Welcome', 'to', 'the', 'robot', 'rank', 'person',
            'who', 'downed', 'my', 'self-esteem', 'cuz', 'I', "'m",
            'not', 'an', 'avid', 'signature', 'artist', 'like', 'herself',
            'proud', 'www.youtube.com/watch', 'ADD', 'UPPERCASE', 'WORD'
        ]

        style_text = StyleFeatures(sentence)
        result = style_text.get_words()
        self.assertEqual(len(result), len(expected_words))
        self.assertEqual(result, expected_words)

    def test_separate_links_from_words(self):
        style_text = StyleFeatures(text)
        result = style_text.separate_links_from_words()
        # self.assertEqual(len(expected_links), len(style_text.links))
        self.assertEqual(expected_links, style_text.links)

    def test_is_emoji(self):
        proud_emoji = ':proud:.'
        sad_emoji = ':sad:.'
        not_emoji = 'whatever'

        proud_emoji_result = StyleFeatures.is_emoji(proud_emoji)
        sad_emoji_result = StyleFeatures.is_emoji(sad_emoji)
        not_emoji_result = StyleFeatures.is_emoji(not_emoji)

        self.assertEqual(proud_emoji_result, True)
        self.assertEqual(sad_emoji_result, True)
        self.assertEqual(not_emoji_result, False)

    def test_add_frequencies_of_link_types_to_stylometry_markers(self):
        style_text = StyleFeatures(text)
        style_text.add_frequencies_of_link_types_to_stylometry_markers()

        expected_links = 21 / style_text.num_of_posts * 100
        expected_facepalms = 0 / style_text.num_of_posts * 100
        expected_trolls = 0 / style_text.num_of_posts * 100
        expected_youtubes = 13 / style_text.num_of_posts * 100
        expected_tumblrs = 1 / style_text.num_of_posts * 100
        expected_vimeos = 1 / style_text.num_of_posts * 100
        expected_gifs = 1 / style_text.num_of_posts * 100
        expected_images = 7 / style_text.num_of_posts * 100

        self.assertEqual(style_text.stylometry_markers['links_per_post'], expected_links)
        self.assertEqual(style_text.stylometry_markers['facepalm_per_post'], expected_facepalms)
        self.assertEqual(style_text.stylometry_markers['troll_per_post'], expected_trolls)
        self.assertEqual(style_text.stylometry_markers['youtube_per_post'], expected_youtubes)
        self.assertEqual(style_text.stylometry_markers['tumblr.com_per_post'], expected_tumblrs)
        self.assertEqual(style_text.stylometry_markers['vimeo_per_post'], expected_vimeos)
        self.assertEqual(style_text.stylometry_markers['.gif_per_post'], expected_gifs)
        self.assertEqual(style_text.stylometry_markers['images_per_post'], expected_images)

    def test_get_count_smilie_per_word(self):
        example = 'Hi :) How are you?:) I am good:) :-)'
        example2 = 'Hi :D How are you?:) I am good:D'
        example3 = 'Hi :) How are you?:-) I am good:)'

        self.assertEqual(StyleFeatures.get_count_smilie_per_word(example, ':)'), 3)
        self.assertEqual(StyleFeatures.get_count_smilie_per_word(example2, ':D'), 2)
        self.assertEqual(StyleFeatures.get_count_smilie_per_word(example3, ':-)'), 1)

class UtilitiesTests(unittest.TestCase):
    def test_get_freq_of_characters_in_text_in_list(self):
        lst = ['apple.gif', 'banana.gif', 'apple', 'gif', 'monkey', 'monkey.gif']
        search_items = ['gif', 'monkey']
        normalizer = 6

        expected_result = 5/6
        result = get_freq_of_characters_in_text_in_list(lst, search_items, normalizer)
        self.assertEqual(expected_result, result)

    def test_get_freq_of_items_in_list(self):
        lst = ['apple.gif', 'banana.gif', 'apple', 'gif', 'monkey', 'monkey.gif']
        search_items = ['gif', 'monkey']
        normalizer = 6

        expected_result = 2/6
        result = get_freq_of_items_in_list(lst, search_items, normalizer)
        self.assertEqual(expected_result, result)

    def test_get_count_of_characters_in_text(self):
        text = 'monkey eats the banana but doesnt like the apple. so it eats the banana.'
        characters = 'banana'

        expected_result = 2
        result = get_count_of_characters_in_text(text, characters)
        self.assertEqual(expected_result, result)

if __name__ == '__main__':
    unittest.main()
