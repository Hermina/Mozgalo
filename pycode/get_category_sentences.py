import load
import pickle

#get comments and grades per category
def get_category_comments(comments, file_name):
    letters = ['L','T','S','F','O']
    category = prepare_dictionary(letters)
    for comment in comments:
        category = analize_using_letter(comment, category)
    f = open('files/'+file_name, 'wb')
    pickle.dump(category, f)
    return

#prepare dictionary
def prepare_dictionary(keys):
    c = {}
    for key in keys:
        c[key] = []
    return c
      
#parse comment using key letters and punctioations expected after letter
def analize_using_letter(comment, category):
    #L-look, T-taste, S-smell, F-feel, O-overall
    letters = ['L','T','S','F','O']
    pun = [':','.','-',';']
    indexi = []
    sent = comment.comment
    for letter in letters:
        try:
            ind = sent.index(letter)
        except:
            ind = -1
        if ind >= 0  and len(sent) > (ind + 1) and sent[ind + 1] in pun:
            if letter == 'M':
                letter = 'F'
            elif letter == 'A':
                letter = 'L'
            indexi.append((ind,letter))
        elif letter == 'F':
            letters.append('M')
        elif letter == 'L':
            letters.append('A')
    if(len(indexi) == 5):
        indexi = sorted(indexi,key=lambda x: x[0])
        grades = [comment.look, comment.taste, comment.smell, comment.feel, comment.overall]
        for i in range(len(indexi) - 1):
            sentence = sent[indexi[i][0] + 2:indexi[i+1][0]]
            category[indexi[i][1]].append([sentence, grades[letters.index(indexi[i][1])]])
        sentence = sent[indexi[-1][0] + 2:]
        category[indexi[-1][1]].append([sentence, grades[letters.index(indexi[i][1])]])
    return category

