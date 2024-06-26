"""
Define common constants.
"""
TRAIN_JSON = 'train.json'
DEV_JSON = 'dev.json'
TEST_JSON = 'test.json'

GLOVE_DIR = 'dataset/glove'

EMB_INIT_RANGE = 1.0
MAX_LEN = 100

# vocab
PAD_TOKEN = '<PAD>'
PAD_ID = 0
UNK_TOKEN = '<UNK>'
UNK_ID = 1

VOCAB_PREFIX = [PAD_TOKEN, UNK_TOKEN]

# hard-coded mappings from fields to ids
SUBJ_NER_TO_ID = {PAD_TOKEN: 0, UNK_TOKEN: 1, 'ORGANIZATION': 2, 'PERSON': 3}

OBJ_NER_TO_ID = {PAD_TOKEN: 0, UNK_TOKEN: 1, 'PERSON': 2, 'ORGANIZATION': 3, 'DATE': 4, 'NUMBER': 5, 'TITLE': 6, 'COUNTRY': 7, 'LOCATION': 8, 'CITY': 9, 'MISC': 10, 'STATE_OR_PROVINCE': 11, 'DURATION': 12, 'NATIONALITY': 13, 'CAUSE_OF_DEATH': 14, 'CRIMINAL_CHARGE': 15, 'RELIGION': 16, 'URL': 17, 'IDEOLOGY': 18}

NER_TO_ID = {PAD_TOKEN: 0, UNK_TOKEN: 1, 'O': 2, 'PERSON': 3, 'ORGANIZATION': 4, 'LOCATION': 5, 'DATE': 6, 'NUMBER': 7, 'MISC': 8, 'DURATION': 9, 'MONEY': 10, 'PERCENT': 11, 'ORDINAL': 12, 'TIME': 13, 'SET': 14}

POS_TO_ID = {PAD_TOKEN: 0, UNK_TOKEN: 1, 'NNP': 2, 'NN': 3, 'IN': 4, 'DT': 5, ',': 6, 'JJ': 7, 'NNS': 8, 'VBD': 9, 'CD': 10, 'CC': 11, '.': 12, 'RB': 13, 'VBN': 14, 'PRP': 15, 'TO': 16, 'VB': 17, 'VBG': 18, 'VBZ': 19, 'PRP$': 20, ':': 21, 'POS': 22, '\'\'': 23, '``': 24, '-RRB-': 25, '-LRB-': 26, 'VBP': 27, 'MD': 28, 'NNPS': 29, 'WP': 30, 'WDT': 31, 'WRB': 32, 'RP': 33, 'JJR': 34, 'JJS': 35, '$': 36, 'FW': 37, 'RBR': 38, 'SYM': 39, 'EX': 40, 'RBS': 41, 'WP$': 42, 'PDT': 43, 'LS': 44, 'UH': 45, '#': 46}

DEPREL_TO_ID = {PAD_TOKEN: 0, UNK_TOKEN: 1, 'punct': 2, 'compound': 3, 'case': 4, 'nmod': 5, 'det': 6, 'nsubj': 7, 'amod': 8, 'conj': 9, 'dobj': 10, 'ROOT': 11, 'cc': 12, 'nmod:poss': 13, 'mark': 14, 'advmod': 15, 'appos': 16, 'nummod': 17, 'dep': 18, 'ccomp': 19, 'aux': 20, 'advcl': 21, 'acl:relcl': 22, 'xcomp': 23, 'cop': 24, 'acl': 25, 'auxpass': 26, 'nsubjpass': 27, 'nmod:tmod': 28, 'neg': 29, 'compound:prt': 30, 'mwe': 31, 'parataxis': 32, 'root': 33, 'nmod:npmod': 34, 'expl': 35, 'csubj': 36, 'cc:preconj': 37, 'iobj': 38, 'det:predet': 39, 'discourse': 40, 'csubjpass': 41}

LABEL_TO_ID = {'no_relation': 0, 'org:members': 1, 'per:siblings': 2, 'per:spouse': 3, 'org:country_of_branch': 4, 'per:country_of_death': 5, 'per:parents': 6, 'per:stateorprovinces_of_residence': 7, 'org:top_members/employees': 8, 'org:dissolved': 9, 'org:number_of_employees/members': 10, 'per:stateorprovince_of_death': 11, 'per:origin': 12, 'per:children': 13, 'org:political/religious_affiliation': 14, 'per:city_of_birth': 15, 'per:title': 16, 'org:shareholders': 17, 'per:employee_of': 18, 'org:member_of': 19, 'org:founded_by': 20, 'per:countries_of_residence': 21, 'per:other_family': 22, 'per:religion': 23, 'per:identity': 24, 'per:date_of_birth': 25, 'org:city_of_branch': 26, 'org:alternate_names': 27, 'org:website': 28, 'per:cause_of_death': 29, 'org:stateorprovince_of_branch': 30, 'per:schools_attended': 31, 'per:country_of_birth': 32, 'per:date_of_death': 33, 'per:city_of_death': 34, 'org:founded': 35, 'per:cities_of_residence': 36, 'per:age': 37, 'per:charges': 38, 'per:stateorprovince_of_birth': 39}
LABEL_TO_ID_HIER = {'no_relation': 0, 'org:members': 1, 'per:siblings': 2, 'per:spouse': 3, 'org:country_of_branch': 4, 'per:country_of_death': 5, 'per:parents': 6, 'per:stateorprovinces_of_residence': 7, 'org:top_members/employees': 8, 'org:dissolved': 9, 'org:number_of_employees/members': 10, 'per:stateorprovince_of_death': 11, 'per:origin': 12, 'per:children': 13, 'org:political/religious_affiliation': 14, 'per:city_of_birth': 15, 'per:title': 16, 'org:shareholders': 17, 'per:employee_of': 18, 'org:member_of': 19, 'org:founded_by': 20, 'per:countries_of_residence': 21, 'per:other_family': 22, 'per:religion': 23, 'per:identity': 24, 'per:date_of_birth': 25, 'org:city_of_branch': 26, 'org:alternate_names': 27, 'org:website': 28, 'per:cause_of_death': 29, 'org:stateorprovince_of_branch': 30, 'per:schools_attended': 31, 'per:country_of_birth': 32, 'per:date_of_death': 33, 'per:city_of_death': 34, 'org:founded': 35, 'per:cities_of_residence': 36, 'per:age': 37, 'per:charges': 38, 'per:stateorprovince_of_birth': 39, 'org:location_of_branch':40, 'per:location_of_birth':41, 'per:location_of_death':42, 'per:locations_of_residence':43, 'per:family':44, 'per-per':45, 'per-org':46, 'per-misc':47, 'per-loc':48, 'org-per':49, 'org-org':50, 'org-misc':51, 'org-loc':52, 'per':53, 'org':54, 'relation':55, 'root':56}

PARENTS = {'org:city_of_branch': 'org:location_of_branch',
          'org:country_of_branch': 'org:location_of_branch',
          'org:stateorprovince_of_branch': 'org:location_of_branch',
          'per:city_of_birth': 'per:location_of_birth',
          'per:country_of_birth': 'per:location_of_birth',
          'per:stateorprovince_of_birth': 'per:location_of_birth',
          'per:city_of_death': 'per:location_of_death',
          'per:country_of_death': 'per:location_of_death',
          'per:stateorprovince_of_death': 'per:location_of_death',
          'per:cities_of_residence' : 'per:locations_of_residence',  
          'per:countries_of_residence' : 'per:locations_of_residence',
          'per:stateorprovinces_of_residence' : 'per:locations_of_residence',
          'per:children' : 'per:family',
          'per:other_family' : 'per:family',
          'per:parents' : 'per:family',
          'per:siblings' : 'per:family',
          'per:spouse' : 'per:family'}
RELABELED_LABEL_TO_ID = {'no_relation': 0, 'org:members': 1, 'org:location_of_branch': 2, 'per:location_of_death': 3, 'per:family': 4, 
                         'per:locations_of_residence': 5, 'org:top_members/employees': 6, 'org:dissolved': 7, 'org:number_of_employees/members': 8, 
                         'per:origin': 9, 'org:political/religious_affiliation': 10, 'per:location_of_birth': 11, 'per:title': 12, 
                         'org:shareholders': 13, 'per:employee_of': 14, 'org:member_of': 15, 'org:founded_by': 16, 'per:religion': 17, 
                         'per:identity': 18, 'per:date_of_birth': 19, 'org:city_of_branch': 20, 'org:alternate_names': 21, 'org:website': 22, 
                         'per:cause_of_death': 23, 'per:schools_attended': 24, 'per:date_of_death': 25, 'org:founded': 26, 'per:age': 27, 
                         'per:charges': 28}

INFINITY_NUMBER = 1e12
