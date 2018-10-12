mbti_types = [
    'ENTP', 'INTP', 'ENTJ', 'INTJ', 'ENFP', 'INFP', 'ENFJ', 'INFJ',
    'ESTP', 'ISTP', 'ESTJ', 'ISTJ', 'ESFP', 'ISFP', 'ESFJ', 'ISFJ'
]

formality_markers = {'thus', 'ergo', 'henceforth', 'hence'}
image_markers = {'img', 'photobucket', 'png', 'jpg', 'imgur', 'jpeg', 'JPG', '.php', 'image'}
swear_words = {'fuck', 'fucking', 'fucked'}
insulting_words = {'dumb', 'stupid', 'idiot', 'dipshit', 'retard', 'retarded', 'idiotic', 'dumbass'}
scientific_terms = {'science', 'scientific', 'evidence'}

invalid_urls = [
    'URL=http', 'krhttp', 'accidenthttp', "'15758http", 
    'href=http', 'bro.http', 'url=http', '68611http', 'u=http',
    'http', "'http", 'ame=http', 'school.http'
]

freq_punctuation_per_sentence = ['?', '!', "'"]
freq_punctuation_per_word = [',', ';']
freq_tokens_per_word = {
    'ands_per_word': ['and'],
    'exclusive_words_per_word': ['but', 'except'],
    'howevers_per_word': ['however'],
    'ifs_per_word': ['if'],
    'thats_per_word': ['that'],
    'mores_per_word': ['more'], 
    'verys_per_word': ['very'],
    'facts_per_word': ['fact'],
    'you_per_word': ['you'],
    'me_per_word': ['I', 'me', 'mine'],
    'we_per_word': ['us', 'we', 'our'],
    'formality_level': formality_markers,
    'swear_words_per_word': swear_words,
    'insults_per_word': insulting_words,
    'think_per_word': ['think'],
    'feel_per_word': ['feel'],
    'believe_per_word': ['believe'],
    'know_per_word': ['know'],
    'science_per_word': scientific_terms,
    'kindness_per_word': ['kindness', 'kind'],
    'party_per_word': ['party'],
    'logic_per_word': ['logic'],
    'spiritual_per_word': ['spiritual', 'spirituality'],
    'left_terms_per_word': ['democrat', 'liberal', 'leftist', 'lefties'],
    'right_terms_per_word': ['republican', 'conservative', 'rightist'], 
    'libertarian_per_word': ['libertarian'],
    'authorirarian_per_word': ['authoritarian'],
    'music_per_word': ['music'],
    'articles_per_word': ['a', 'an', 'the'] 
} 
      
