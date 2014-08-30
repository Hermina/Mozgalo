import re
import pickle

class BAclass:
    # @TODO add comments
    #funkcija u file zapisuje disctionary
    #kljuc je ime pive
    #oznacimo sa V vrijednosti na pocetku svakog filea s komentarima(ono medu upitnicima)
    #vrijednost dictionaria je [V[0],V[1],V[2],V[3],V[4],V[5],beerReview]
    #gdje beerReview ima vrijenosti kao dolje(oznaceno)
    def  __init__(self, loadFile, rewiewsFile, usersFile):
        self.beerNames  = {}
        self.users = {}
        beerNames = open(loadFile+'toplist.txt', 'r')
        lines = beerNames.readlines()
        for line in lines:
            beerName = line[line.find(']')+2:line[1:].find('[')]
            beerName = beerName.replace('/','-')
            self.beerNames[beerName] = []
        count = 0
        dobre = 0
        for beer in self.beerNames.keys():
            print beer
            try:
                f = open(loadFile + beer + '.txt','r')
            except:
                print loadFile + beer + '.txt'
                continue
            lines = f.read().splitlines()
            for i in range(len(lines)):
                if i == 0:
                    words = lines[i].split('?')
                    for j in range(len(words)):
                        if j % 2 == 0 and j < 11:
                            self.beerNames[beer].append(words[j])
                    self.beerNames[beer].append([])
                    #print(self.beerNames[beer])
                elif len(lines[i]) > 0 and lines[i][0] == '[':
                    try:
                        username = lines[i].split("More by ")[-1]
                        link = lines[i][1:lines[i].find(']')]
                        rest = lines[i].split(']' + username)[1]
                        grade = re.findall(r"[-+]?\d[.]?[\d]*[ ]*[/]5", rest)[0].split(' /')[0]
                        city = rest[1:rest.find(grade)-1]
                        # rDev +171.7% look: 5 | smell: 5 | taste: 5 | feel: 5 |  overall: 5
                        rDev = re.findall(r"rDev[ ].*%", rest)[0].split()[1]
                        look = re.findall(r"look:[ ]\d[.]?[\d]*", rest)[0].split()[1]
                        smell = re.findall(r"smell:[ ]\d[.]?[\d]*", rest)[0].split()[1]
                        taste = re.findall(r"taste:[ ]\d[.]?[\d]*", rest)[0].split()[1]
                        feel = re.findall(r"feel:[ ]\d[.]?[\d]*", rest)[0].split()[1]
                        overall = re.findall(r"overall:[ ]\d[.]?[\d]*", rest)[0].split()[1]
                        textBegining = lines[i].find('overall: ' + overall) + len('overall: ' + overall)
                        date = re.findall(r'\d\d[-]\d\d[-]\d\d\d\d',lines[i])[0]
                        textEnd = lines[i].rfind("Serving type:")
                        text = lines[i][textBegining:textEnd]
                        if username not in self.users.keys():
                            self.users[username] = []
                            self.users[username].append(link)
                            self.users[username].append(city)
                        ##############
                        beerReview = []
                        beerReview.append(username)
                        beerReview.append(grade)
                        beerReview.append(rDev)
                        beerReview.append(look)
                        beerReview.append(smell)
                        beerReview.append(taste)
                        beerReview.append(feel)
                        beerReview.append(overall)
                        beerReview.append(text)
                        beerReview.append(date)
                        ##############
                        self.beerNames[beer][6].append(beerReview)
                        dobre += 1
                    except:
                        count += 1
                        continue
        f = open('files/'+rewiewsFile,'wb')
        pickle.dump(self.beerNames,f)
        f = open('files/'+usersFile,'wb')
        pickle.dump(self.users,f)
        print "ne dobre"  + str(count)
        print "dobre" + str(dobre)
        print len(self.beerNames.keys())
        print len(self.users.keys())

    def getBeerList(self):
        return self.beerNames.keys()

    def getDataByBeerName(self, name):
        return self.beerNames[name]

    def getScoreByBeerName(self, name):
        return self.beerNames[name][0]

    def getUsersByBeerName(self, name):
        pass


BA = BAclass('../datares3/','beersS.txt', 'usersS.txt' )
