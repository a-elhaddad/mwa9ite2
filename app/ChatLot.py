from datetime import datetime
from StorageManger import StorageManger
from Bot import Bot
class ChatLot(object):
    def __init__(self):
        self.name = "me"
        self.sm = StorageManger()
        self.sm.iniStatements()
        self.statments = self.sm.getStatements()
    def addUser(self,user):
        StorageManger().addUser(user)
    def getAllUser(self):
        self.sm.getAllUser()
    def get_respond(self,q):
        q = q.replace("é", "e")
        q = q.replace("è", "e")
        q = q.replace("à", "a")
        q = q.replace("â", "a")
        q = q.replace("ç", "c")
        q = q.replace("ù", "u")
        q = q.replace("ï", "i")
        q = q.replace("î", "i")

        from timeit import default_timer as timer
        start = timer()
        best_lv_distance = 0
        rep = ''
        temp =[]
        for statment in self.statments:
            lv_distance=self.levenshtein_distance(q,statment.Qt)
            temp.append("{0} , {1}, {2}".format(q,statment.Qt,str(lv_distance)))
            if lv_distance > best_lv_distance :
                rep = statment.Rep
                best_lv_distance = lv_distance
        if best_lv_distance < 0.65 :
            rep = 'Je vous demande pardon, Mais je suis stupide 🤡 ne l\'oubliez pas, Vous pouvez m\'envoyer votre commune suivie du numéro de la wilaya exemple:\n\n Alger Centre 16 .\n\nou\n\n Boumerdes 35 .\n\nNb:\n\n fonctionne que pour les villes Algériennes.'

        end = timer()
        print(end - start)
        return rep

    def levenshtein_distance(self,statement, other_statement):

        import sys

        # Use python-Levenshtein if available
        try:
            from Levenshtein.StringMatcher import StringMatcher as SequenceMatcher
        except ImportError:
            from difflib import SequenceMatcher

        PYTHON = sys.version_info[0]

        # Return 0 if either statement has a falsy text value
        if not statement or not other_statement:
            return 0

        # Get the lowercase version of both strings
        if PYTHON < 3:
            statement_text = unicode(statement.lower()) # NOQA
            other_statement_text = unicode(other_statement.lower()) # NOQA
        else:
            statement_text = str(statement.lower())
            other_statement_text = str(other_statement.lower())

        similarity = SequenceMatcher(
            None,
            statement_text,
            other_statement_text
        )

        # Calculate a decimal percent of the similarity
        percent = round(similarity.ratio(), 2)

        return percent
cht = ChatLot()