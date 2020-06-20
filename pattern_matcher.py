import spacy
nlp = spacy.load("en_core_web_sm")
from spacy.matcher import Matcher


# Patterns Starts --------------------
two_element_patterns = [[{'TAG':'JJ'}, {'TAG':'NN'}],
                            [{'TAG':'JJ'}, {'TAG':'NNS'}],
                            
                            [{'TAG':'RB'}, {'TAG':'JJ'}],
                            [{'TAG':'RBR'}, {'TAG':'JJ'}],
                            [{'TAG':'RBS'}, {'TAG':'JJ'}],
                            
                            [{'TAG':'VBN'}, {'TAG':'NN'}],
                            [{'TAG':'VBN'}, {'TAG':'NNS'}],
                            
                            [{'TAG':'VBD'}, {'TAG':'NN'}],
                            [{'TAG':'VBD'}, {'TAG':'NNS'}],
                            
                            [{'TAG':'RB'}, {'TAG':'VBN'}],
                            [{'TAG':'RBR'}, {'TAG':'VBN'}],
                            [{'TAG':'RBS'}, {'TAG':'VBN'}],
                            
                            [{'TAG':'RB'}, {'TAG':'VBD'}],
                            [{'TAG':'RBR'}, {'TAG':'VBD'}],
                            [{'TAG':'RBS'}, {'TAG':'VBD'}],
                            
                            [{'TAG':'VBN'}, {'TAG':'RB'}],
                            [{'TAG':'VBN'}, {'TAG':'RBR'}],
                            [{'TAG':'VBN'}, {'TAG':'RBS'}],
                            
                            [{'TAG':'VBD'}, {'TAG':'RB'}],
                            [{'TAG':'VBD'}, {'TAG':'RBR'}],
                            [{'TAG':'VBD'}, {'TAG':'RBS'}]]
    
three_element_patterns = [[{'TAG':'JJ'}, {'TAG':'NN'}, {'TAG':'NN'}],
                              [{'TAG':'JJ'}, {'TAG':'NN'}, {'TAG':'NNS'}],
                              [{'TAG':'JJ'}, {'TAG':'NNS'}, {'TAG':'NN'}],
                              [{'TAG':'JJ'}, {'TAG':'NNS'}, {'TAG':'NNS'}],
                              
                              [{'TAG':'NN'}, {'TAG':'VBZ'}, {'TAG':'JJ'}],
                              
                              [{'TAG':'RB'}, {'TAG':'JJ'}, {'TAG':'JJ'}],
                              [{'TAG':'RB'}, {'TAG':'RB'}, {'TAG':'JJ'}],
                              [{'TAG':'RB'}, {'TAG':'RBR'}, {'TAG':'JJ'}],
                              [{'TAG':'RB'}, {'TAG':'RBS'}, {'TAG':'JJ'}],
                              [{'TAG':'RBR'}, {'TAG':'JJ'}, {'TAG':'JJ'}],
                              [{'TAG':'RBR'}, {'TAG':'RB'}, {'TAG':'JJ'}],
                              [{'TAG':'RBR'}, {'TAG':'RBR'}, {'TAG':'JJ'}],
                              [{'TAG':'RBR'}, {'TAG':'RBS'}, {'TAG':'JJ'}],
                              [{'TAG':'RBS'}, {'TAG':'JJ'}, {'TAG':'JJ'}],
                              [{'TAG':'RBS'}, {'TAG':'RB'}, {'TAG':'JJ'}],
                              [{'TAG':'RBS'}, {'TAG':'RBR'}, {'TAG':'JJ'}],
                              [{'TAG':'RBS'}, {'TAG':'RBS'}, {'TAG':'JJ'}],
                              
                              [{'TAG':'RB'}, {'TAG':'JJ'}, {'TAG':'NN'}],
                              [{'TAG':'RB'}, {'TAG':'RB'}, {'TAG':'NN'}],
                              [{'TAG':'RB'}, {'TAG':'RBR'}, {'TAG':'NN'}],
                              [{'TAG':'RB'}, {'TAG':'RBS'}, {'TAG':'NN'}],
                              [{'TAG':'RBR'}, {'TAG':'JJ'}, {'TAG':'NN'}],
                              [{'TAG':'RBR'}, {'TAG':'RB'}, {'TAG':'NN'}],
                              [{'TAG':'RBR'}, {'TAG':'RBR'}, {'TAG':'NN'}],
                              [{'TAG':'RBR'}, {'TAG':'RBS'}, {'TAG':'NN'}],
                              [{'TAG':'RBS'}, {'TAG':'JJ'}, {'TAG':'NN'}],
                              [{'TAG':'RBS'}, {'TAG':'RB'}, {'TAG':'NN'}],
                              [{'TAG':'RBS'}, {'TAG':'RBR'}, {'TAG':'NN'}],
                              [{'TAG':'RBS'}, {'TAG':'RBS'}, {'TAG':'NN'}],
                              
                              [{'TAG':'RB'}, {'TAG':'JJ'}, {'TAG':'NNS'}],
                              [{'TAG':'RB'}, {'TAG':'RB'}, {'TAG':'NNS'}],
                              [{'TAG':'RB'}, {'TAG':'RBR'}, {'TAG':'NNS'}],
                              [{'TAG':'RB'}, {'TAG':'RBS'}, {'TAG':'NNS'}],
                              [{'TAG':'RBR'}, {'TAG':'JJ'}, {'TAG':'NNS'}],
                              [{'TAG':'RBR'}, {'TAG':'RB'}, {'TAG':'NNS'}],
                              [{'TAG':'RBR'}, {'TAG':'RBR'}, {'TAG':'NNS'}],
                              [{'TAG':'RBR'}, {'TAG':'RBS'}, {'TAG':'NNS'}],
                              [{'TAG':'RBS'}, {'TAG':'JJ'}, {'TAG':'NNS'}],
                              [{'TAG':'RBS'}, {'TAG':'RB'}, {'TAG':'NNS'}],
                              [{'TAG':'RBS'}, {'TAG':'RBR'}, {'TAG':'NNS'}],
                              [{'TAG':'RBS'}, {'TAG':'RBS'}, {'TAG':'NNS'}]
                              ]

patterns = two_element_patterns + three_element_patterns
# Pattern Ends --------------------

 
class PatternMatcher:
    def __init__(self):
        self.patterns = patterns
        
    def find_matches(self, sentence):
        sentence = nlp(sentence)
        matcher = Matcher(nlp.vocab)
        
        i = 0
        for pattern in self.patterns:
            matcher.add(i, None, pattern)
            i += 1
            
        matches = matcher(sentence)
        for match_id, start, end in matches:
            span = sentence[start:end]
            print(matcher.get(match_id)[1], start, end, span.text)
            
        return matches
        
    def __search_opinion_word(self, match_id, match):
        from extracter_analyzer import get_polarity
        
        print("polarity: ", get_polarity(match.text))
        print("match: ", match)
        
        if match_id <= 1:
            opinion_word = match.text.split()[0]
        elif 4 < match_id < 9:
            opinion_word = match.text.split()[0]
        elif 20 < match_id < 25:
            opinion_word = match.text.split()[0]
        elif match_id == 25:  
             opinion_word = match.text.split()[2]     
        elif 37 < match_id < len(self.patterns):
            adv = match.text.split()[0]
            adj = match.text.split()[1]
            opinion_word = adv + " " + adj
        else:
            return
            
        print("Opinion word: ", opinion_word)
        return opinion_word
    
    def extract_objects(self, clusters):
        from extracter_analyzer import get_common_words
    
        cluster_objects_and_opinions = [None] * len(clusters)    
        
        for i, val in clusters.items():
            print("Cluster ", i, ": ")
            
            most_occur = get_common_words(val)
            
            cluster_objects_and_opinions[i] = {}
            objects = cluster_objects_and_opinions[i]
            print(objects)
            
            for most_oc in most_occur:
                most_oc = most_oc[0]
                objects[most_oc] = []
    
            print("Most occuring: ", most_occur)
            
            for item in val:
                cleaned, sentence, matches = item
                sentence = nlp(sentence)
                
                if len(matches) < 1:
                    continue
                
                for match_id, start, end in matches:
                    span = sentence[start:end]
    
                    for most_oc in most_occur:
                        most_oc = most_oc[0]
                        print("*", most_oc)
                        if most_oc in span.text:
                            print("FOUND -> ", span, self.patterns[match_id])
                            objects[most_oc].append(self.__search_opinion_word(match_id, span))
                            
            print(objects)
            print("\n")
            
        #print(cluster_objects_and_opinions)
            
        for i, cluster in enumerate(cluster_objects_and_opinions):
            print("\n>>> Cluster ", i, "<<<")
            
            for obj, opinion in cluster.items():
                print("-- ", obj, ": ", set(opinion))
            
            
            
        return cluster_objects_and_opinions
    
    
    
    
    
    
    
    