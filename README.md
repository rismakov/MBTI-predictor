<h2>About Myer-Briggs Type Indicator</h2>

<br> 

The Myers Briggs Type Indicator is a personality test that looks at an individual's pyschological preferences to place them into one of 16 distinct personality types, defined by preferences spanning along four dimensions:

<ul>
  <li> <b>Extroversion-Introversion (E-I)</b>: How you intertact with the world and gain energy from interactions -- by being inwardly focused (Introversion) or outwardly turned (Extroversion)?</li> <br>
  <li><b>Intutition-Sensing (N-S)</b>: How you process information -- based on the information itself (Sensing) or your own thoughts and interpretations about the information (Intuition)? </li><br>
  <li><b> Feeling-Thinking (F-T)</b>: How you make decisions -- based on logic and hard facts in search of the objective truth (Thinking) or on personal values and an inner sense of morality in search for harmony (Feeling)? </li><br>
  <li><b> Judging-Perceiving (J-P):</b> How you organize your time and incoming information -- in a structured, organized way seeing the world as more black and white (Judging) or in a flexible, adaptable way prefering to keep options open (Perceiving)? </li>
</ul>

Although the MBTI has been critized for poor reliability (i.e. producing different results when taken on different occasions by the same person) and not being entirely comprehension (due to neuroticism not being taken into account), it still remains one of the most popular online personality tests to date and is especially popular within the business sector.
<br><br>
The purpose of this project is to investigate whether patterns and predictive features can be extracted from the text to pinpoint an individual's personality type. The ability to use writing style and word usage to detect a person's personality might be a more precise and more reliable method of detecting pyscological preferences than self-reported tests.

<h2>Limitations with MBTI Testing</h2>
<br>
				
There are a few issues with the current method of extracting a person's personality type. Self-reports tend to be unreliable for several reasons:

<ol>
	<li> Most people can guess what personality function a question relates too (ie. We tend to be aware that the question "Do you prefer to stay in and read a book instead of going out to a party" refers to Extroversion/Introversion), and may choose to answer based on how they prefer to identify themselves as opposed to directly answering the question. This injects bias into how we choose to respond to the questions. </li>
	<li> In many cases we don't have a strong preference for one way or the other, or we may vary depending on our mood or other contextual information that is not present in the question. This injects unreliability in how we choose to answer and may shift results when we retake the test.</li>
	<li> The tests improve with the addition of extra questions. However, answering so many questions may be tiring for users.</li>
					</ol><br>

Given these limitations, using social media text might provide a more seamless and reliable method of extracting personality type. Below I will explain how I set out to acheive this.

<h2>About MBTI data set</h2>
<br>
The data consisted of around ~8600 datapoints, gathered from personalitycafe.com, a forum used for discussing various topics pertaining to personality. Each row consisted of the users self-reported MBTI type and approximately 50 posts for each user in the set.
<br><br>
Since the data was collected from a site tailored towards a specific topic, certain words were removed that might introduce leakage into the model (i.e. if a person might be more likely to reference their own type within their posts, we don't want the model to 'cheat' by learning that 'ISFJ' is mostly linked to ISFJs).
<br><br>
Some words removed included Myer-Briggs types, Enneagram types, personality functions (ie Fi, Fe, Ni, Ne, etc,), and any term that may be specifically related to personality types that are not likely to be representative of the type of posts the algorithm will be used to predict off.
<br><br>
After doing some basic, standard cleaning of the text, the first step was looking at the distribution of the types among the data.

The data set was mostly skewed towards 'IN's and 'EN's, with very few 'ES's in the set, pretty much the reverse of what the real distribution in the global population is.
<br><br>
Plotted below is the distribution of the types with the data set (first plot) compared to the global population distribution (second plot). The third plot shows the difference between the real percent the types appear in the world and the percent they appear in our data set. As you can see, 'IN's are vastly overrepresented in the data. 'ES's and 'IS's, by contrast, while the most common types, are underrepresented within the data.
<br><br>

<img src="static\images\mbti\type_distributions.png" width="40%" height="40%"/>
<br>

I considered whether to perform oversampling on the classes to get a more representative blend. In the end I decided to keep the training data as is, with the assumption that the people who will be interacting with a MBTI personality predicter app will most likely resemble the data set distribution as opposed to the real world distribution. <br><br>

In order to compare properly, I created two Baseline Models: one that randomly predicted with the same probabilities as the distribution of the types in the set, and the second which always chose the majority class (INFP in this case). This allowed me to compare the model predictions to baseline models that similarily took the unbalanced labels into account.

<br>
          
<h2>Feature engineering</h2>
<br>
Particular writing styles have been found to be assocaited with certain personality traits. Moreso, aside from looking purely at word usage, it has been shown that the way the author expresses his or her thoughts is able to reveal character to an even greater degree.
<br><br>One example of this is how introverts have been found to use 'I', 'me', 'myself' terms more so than extroverts, who prefer 'they', 'them', 'us', 'we'. This relates to introverts' tendencies to be more inside their heads and more prone to perceiving a situation from their own viewpoint.
<br><br>
Other studies have found that words that are used to express balance or nuance (“except,” “but,” etc.) are correlated with higher cognitive complexity, better grades, and even truthfulness.
<br><br>
In addition to both of the above features being included in the featurized data set, some other features used for this task, include:
<ul>
	<li> average word length</p></li>
	<li> average length of post</p></li>
	<li> average sentence length</p></li>
						<li> sentence length variability</p></li>
						<li> polarity </p></li>
						<li> subjectivity </p></li>
						<li> level of formatlity </p></li>
						<li> word diversity</p></li>
						<li> different parts of speech usage</p></li>
						<li> frequency of using curse words</p></li>
						<li> frequency of certain types of words (sad words, happy words, etc)</p></li>
						<li> sentence capitalization</p></li>
						<li> use of ALL CAPS </p></li>
						<li> etc. ...</p></li>
					</ul>

For full list, view code at: github.com/rismakov/MBTI_predictor.
<br><br>
In addition to extracting stylistic features, I performed TFIDF on the data. (TFIDF is a measure for scoring words: in short, words that words that appear often in a single document, but very rarely in other documents are scored higher).

<h2>Type Word Usage Differences</h2>
				
<br>
The types tend to use different types of words with more frequency. Doing a TFIDF analysis, which observes how often a word is used in a specific text normalized to the times it's used in general among all the texts available, I investigated which words were used most often by which type.

<br><br> Plotted below are the top TFIDF words used by each type as compared to all the rest of the types. As you can see, 'INF' types tend to use words like 'dreams', 'heart', 'soul', 'sad', while 'INT' and 'ENT' types tend to use 'argument', 'debate', 'science', 'intelligence', as well as higher levels of swear words. 'ES' and 'IS' types tend to use words more often pertaining to physical objects and people: 'husband', 'sister', 'coffee', 'phone', etc.
<br><br>
<img src="static\images\mbti\top_words_for_each_type.png" width="80%" height="80%"/>
						<br>
