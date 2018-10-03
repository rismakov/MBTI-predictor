mbti_types = [
    'ENTP', 'INTP', 'ENTJ', 'INTJ', 'ENFP', 'INFP', 'ENFJ', 'INFJ',
    'ESTP', 'ISTP', 'ESTJ', 'ISTJ', 'ESFP', 'ISFP', 'ESFJ', 'ISFJ'
]

formality_markers = ['thus', 'ergo', 'henceforth', 'hence']
image_markers = ['img', 'photobucket', 'png', 'jpg', 'imgur', 'jpeg', 'JPG', '.php', 'image']
swear_words = ['fuck', 'fucking', 'fucked']
insulting_words = ['dumb', 'stupid', 'idiot', 'dipshit', 'retard', 'retarded', 'idiotic', 'dumbass']
scientific_terms = ['science', 'scientific', 'evidence']

invalid_urls = [
    'URL=http', 'krhttp', 'accidenthttp', "'15758http", 
    'href=http', 'bro.http', 'url=http', '68611http', 'u=http',
    'http', "'http", 'ame=http', 'school.http'
]

freq_items = {
      'freq_question_marks': [punct, ['?'], sentences],
      'freq_exclamation_marks': [punct, ['!'], sentences],
      'freq_quotation_marks': [punct, ["'"], sentences]
}

freq_items_per_thousand = {
      'freq_commas': [punct, [','], words],
      'freq_semi_colons': [punct, [';'], words],
      'freq_ands': [non_link_words, ['and'], non_link_words],
      'freq_exclusive_words': [non_link_words, ['but', 'except'], non_link_words],
      'freq_howevers': [non_link_words, ['however'], non_link_words],
      'freq_ifs': [non_link_words, ['if'], non_link_words],
      'freq_thats': [non_link_words, ['that'], non_link_words],
      'freq_mores': [non_link_words, ['more'], non_link_words],
      'freq_verys': [non_link_words, ['very'], non_link_words],
      'freq_facts': [non_link_words, ['fact'], non_link_words],
      'freq_you': [non_link_words, ['you'], non_link_words],
      'freq_me': [non_link_words, ['I', 'me', 'mine'], non_link_words],
      'freq_we': [non_link_words, ['us', 'we', 'our'], non_link_words],
      'formality_level': [non_link_words, formality_markers, non_link_words],
      'freq_swear_words': [non_link_words, swear_words, non_link_words],
      'freq_insults': [non_link_words, insulting_words, non_link_words],
      'freq_think': [non_link_words, ['think'], non_link_words],
      'freq_feel': [non_link_words, ['feel'], non_link_words],
      'freq_believe': [non_link_words, ['believe'], non_link_words],
      'freq_know': [non_link_words, ['know'], non_link_words],
      'freq_science': [non_link_words, scientific_terms, non_link_words],
      'freq_kindness': [non_link_words, ['kindness', 'kind'], non_link_words],
      'freq_party': [non_link_words, ['party'], non_link_words],
      'freq_logic': [non_link_words, ['logic'], non_link_words],
      'freq_spiritual': [non_link_words, ['spiritual', 'spirituality'], non_link_words],
      'freq_left_terms': [
            non_link_words, 
            ['democrat', 'democrats', 'liberal', 'liberals', 'leftist', 'lefties'], 
            non_link_words
      ],
      'freq_right_terms': [
            non_link_words, 
            ['republican', 'republicans', 'conservative', 'conservatives', 'rightist'], 
            non_link_words
      ]
}