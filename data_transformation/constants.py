from utils.constants import MBTI_TYPES_LOWER, MBTI_TYPES_PLURAL

ENNEAGRAM_TERMS = [
  '1w2', '2w1', '2w3', '3w2', '3w4', '4w3', '4w5',
  '6w5', '6w7', '7w6', '7w8', '8w7', '8w9', '9w8',
  'so', 'sp', 'sx', 'enneagram', 'ennegram', 'socionics', 'tritype',
  '7s', '8s'
]

FUNCTIONS = [
  'fe', 'fi', 'ne', 'ni', 'se', 'si', 'te', 'ti', 'sj', 
  'dom', 'sensing', 'perceiving', 'extrovert', 'introvert',
]

IMAGE_TERMS = [
  'gif', 
  'giphy', 
  'image', 
  'img', 
  'imgur', 
  'jpeg', 
  'jpg', 
  'JPG', 
  'photobucket', 
  'php',
  'player_embedded', 
  'png', 
  'staticflickr', 
  'tinypic',
]

INVALID_WORDS = [
  'im', 'mbti', 'functions', 'myers', 'briggs', 'types', 'type',
  'personality', '16personalities', '16', 'personalitycafe', 'tapatalk'
]

MBTI_PARTS = [
  'es', 'fj', 'fs', 'nt', 'nf', 'st', 'sf', 'sj',
  'nts', 'nfs', 'sts', 'sfs', 'sjs',
  'enxp', 'esxp', 'exfj', 'exfp', 'extp',
  'inxj', 
  'ixfp', 'ixtp', 'ixtj', 'ixfj',
  'xnfp', 'xntp', 'xnfj', 'xnfp', 'xstj', 'xstp',
  'nfp', 'ntp', 'ntj', 'nfp', 'sfj', 
  'sps',
]

URL_TERMS = ['http', 'https', 'www', 'com', 'youtube', 'youtu', 'watch']

# combine all invalid words to remove from TFIDF vectoried matrix
STOPWORDS = (
  ENNEAGRAM_TERMS 
  + FUNCTIONS 
  + IMAGE_TERMS 
  + INVALID_WORDS 
  + MBTI_PARTS 
  + MBTI_TYPES_LOWER 
  + MBTI_TYPES_PLURAL 
  + URL_TERMS
)
