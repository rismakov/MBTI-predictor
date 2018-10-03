from __future__ import division

import numpy as np

from collections import Counter
from string import punctuation
from textblob import TextBlob

from stylometry_constants import (
    formality_markers, freq_items, freq_items_per_thousand, 
    image_markers, insulting_words, invalid_urls, mbti_types, scientific_terms, swear_words
)


class StyleFeatures(dict):
    '''
    Retrieves features of writing style
    '''

    def __init__(self, posts):
        # sentences works by finding punctuation at the ends of sentences. 
        # all posts combined with periods added to the end of each post - to be able to detect sentences
        all_comments = posts.replace('|||', ' ')  # combination of all posts
        all_comments_w_added_periods = posts.replace('|||', '. ') 
        
        textblob_comments = TextBlob(all_comments)  # this is a string
        textblob_comments_w_periods = TextBlob(all_comments_w_added_periods)

        words = [word.singularize() for word in textblob_comments.words]
        sentences = textblob_comments_w_periods.sentences

        links = set([word for word in words if ('www.' in word) or ('http' in word) or 
                     ('.com' in word) or ('v=' in word)])

        # remove links from list of words
        non_link_words = [word for word in words if word not in links]

        # remove links from sentences of words
        comments_wo_links = textblob_comments
        comments_wo_links_w_periods = textblob_comments_w_periods
        if len(links) > 0:
            for link in links:
                comments_wo_links = comments_wo_links.replace(link, '')
                comments_wo_links_w_periods = comments_wo_links_w_periods.replace(link, '')  

        non_link_sentences = comments_wo_links_w_periods.sentences
        
        num_of_comments = len(posts.split('|||'))
        num_of_words = len(words)
        self['avg_post_len'] = num_of_words / num_of_comments

        num_of_non_link_words = len(non_link_words)
        num_of_sentences = len(sentences)
        num_of_non_link_sentences = len(non_link_sentences)

        sentence_lens = [len(sentence.split()) for sentence in sentences]
        punct = [char for char in comments_wo_links if char in punctuation]

        pos_tags = textblob_comments_w_periods.pos_tags

        keys = [
            'freq_adjs', 'freq_interjections', 'freq_proper_nouns', 'freq_nouns', 
            'freq_personal_pronouns', 'freq_prepositions', 'freq_determiners', 'freq_adverbs', 'freq_verbs'
        ]
        pos_abvs = [
            'JJ', 'UH', 'NNP', 'NN', 
            'PRP', 'IN', 'DT', 'RB', 'VB'
        ]

        for key, pos_abv in zip(keys, pos_abvs):
            self[key] = len([tag for word, tag in pos_tags if tag == pos_abv]) / num_of_non_link_words

        # corrected_words = posts_w_no_links.correct().words
        # self['freq_spelling_mistakes'] = len([word for (word, correct_word) in zip(non_link_words, corrected_words) 
        #                                     if word != correct_word]) / self['non_link_words_len']        
        # self['freq_noun_phrases'] = len(posts_w_no_links_w_periods.noun_phrases) / self['non_link_words_len']

        

        # TO DO: separate images from links
        # imgur, png, jpg, photobucket
        legit_links = []
        facepalms = []
        trolls = []
        youtube_links = []
        images = []
        gifs = []
        tumblr_links = []
        vimeo_links = []
        for link in links:
            if all(link != invalid_link for invalid_link in invalid_urls) and ('v=' not in link):
                legit_links.append(link)
                if 'facepalm' in link:
                    facepalms.append(link) 
                elif 'troll' in link:
                    trolls.append(link)
                elif 'youtube' in link:
                    youtube_links.append(link)
                elif 'tumblr.com' in link:
                    tumblr_links.append(link)
                elif 'vimeo' in link:
                    vimeo_links.append(link)
                elif '.gif' in link:
                    gifs.append(link)
                elif any([image_marker in link for image_marker in image_markers]):
                    images.append(link)

        # vimeo, tumblr.com, image, blogspot.com, thoughtcatalog, buzzfeed, JPG, php, businessinsider

        self['freq_ellipses'] = sum([len(sentence.split('...')) - 1 for sentence in sentences]) / num_of_sentences
        self['freq_emojis'] = sum([(sentence[0] == ':') and (sentence[-2] == ':') 
            for sentence in non_link_sentences]) / num_of_sentences
        self['freq_smilies'] = sum([(':)' in sentence) or (':D' in sentence) or (': )' in sentence) 
            for sentence in non_link_sentences]) / num_of_sentences
        self['freq_all_caps'] = sum([(word.upper() == word) and (word not in mbti_types) 
            for word in non_link_words]) / num_of_non_link_words

        self['freq_links'] = (len(legit_links) / num_of_comments) * 1000
        self['freq_vimeo'] = (len(vimeo_links) / num_of_comments) * 1000
        self['freq_tumblr'] = (len(tumblr_links) / num_of_comments) * 1000
        self['freq_gifs'] = (len(gifs) / num_of_comments) * 1000
        self['freq_facepalms'] = (len(facepalms) / num_of_comments) * 1000 
        self['freq_trolls'] = (len(trolls) / num_of_comments) * 1000 
        self['freq_youtube_links'] = (len(youtube_links) / num_of_comments) * 1000 
        self['freq_images'] = (len(images) / num_of_comments) * 1000 
        self['freq_sentence_capitalization'] = sum([sentence[0].upper() == sentence[0] for sentence in non_link_sentences])
        self['polarity'] = textblob_comments.sentiment.polarity
        self['subjectivity'] = textblob_comments.sentiment.subjectivity
        self['word_diversity'] = len(set(non_link_words)) / num_of_non_link_words
        self['mean_word_len'] = np.mean([len(word) for word in non_link_words])
        self['mean_sentence_len'] = np.mean(sentence_lens)
        self['std_sentence_len'] = np.std(sentence_lens)

    def get_freq_using_list_len(list_of_items, normalizer):
        return (len(legit_links) / normalizer) * 1000

    def get_freq_of_items_in_list(self, lst, search_items, normalizer):
        '''
        Finds normalized frequencies of tokens.
        Input: lst is a list of the item you are counting through,
        search_item (list or array-like object) is the item you are counting,
        normalizer (also list, or array-like) is the object you are normalizing it by
        (words,sentences, or punctuation usually).
        '''
        cnt = 0
        for item in search_items:
            cnt += lst.count(item) / len(normalizer)
        return cnt

    def get_all_freq_tokens(self, punct, sentences, words, non_link_words):
        for item, params in freq_items.items():
            self[item] = self.get_freq_of_items_in_list(params[0], params[1], params[2])

        for item, params in freq_items_per_thousand.items():
            self[item] = self.get_freq_of_items_in_list(params[0], params[1], params[2]) * 1000
