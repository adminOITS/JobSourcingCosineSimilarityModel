import re
from typing import List, Dict
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from dto import (
    JobOfferSkillResponseDto,
    CandidateSkillResponseDto,
    JobOfferExperienceResponseDto,
    CandidateExperienceResponseDto,
    JobOfferEducationResponseDto,
    CandidateEducationResponseDto,
    JobOfferLanguageResponseDto,
    CandidateLanguageResponseDto,
    AddressResponseDto,
    JobOfferResponseDto,
    ProfileResponseDto,
    RequirementLevel
)

# Optional: you can load from a file if your stopword list is large
stopWordsFrensh = ["quelqu","a","abord","absolument","afin","ah","ai","aie","aient","aies","ailleurs","ainsi","ait","allaient","allo","allons","allô","alors","anterieur","anterieure","anterieures","apres","après","as","assez","attendu","au","aucun","aucune","aucuns","aujourd","aujourd'hui","aupres","auquel","aura","aurai","auraient","aurais","aurait","auras","aurez","auriez","aurions","aurons","auront","aussi","autant","autre","autrefois","autrement","autres","autrui","aux","auxquelles","auxquels","avaient","avais","avait","avant","avec","avez","aviez","avions","avoir","avons","ayant","ayez","ayons","b","bah","bas","basee","bat","beau","beaucoup","bien","bigre","bon","boum","bravo","brrr","c","car","ce","ceci","cela","celle","celle-ci","celle-là","celles","celles-ci","celles-là","celui","celui-ci","celui-là","celà","cent","cependant","certain","certaine","certaines","certains","certes","ces","cet","cette","ceux","ceux-ci","ceux-là","chacun","chacune","chaque","cher","chers","chez","chiche","chut","chère","chères","ci","cinq","cinquantaine","cinquante","cinquantième","cinquième","clac","clic","combien","comme","comment","comparable","comparables","compris","concernant","contre","couic","crac","d","da","dans","de","debout","dedans","dehors","deja","delà","depuis","dernier","derniere","derriere","derrière","des","desormais","desquelles","desquels","dessous","dessus","deux","deuxième","deuxièmement","devant","devers","devra","devrait","different","differentes","differents","différent","différente","différentes","différents","dire","directe","directement","dit","dite","dits","divers","diverse","diverses","dix","dix-huit","dix-neuf","dix-sept","dixième","doit","doivent","donc","dont","dos","douze","douzième","dring","droite","du","duquel","durant","dès","début","désormais","e","effet","egale","egalement","egales","eh","elle","elle-même","elles","elles-mêmes","en","encore","enfin","entre","envers","environ","es","essai","est","et","etant","etc","etre","eu","eue","eues","euh","eurent","eus","eusse","eussent","eusses","eussiez","eussions","eut","eux","eux-mêmes","exactement","excepté","extenso","exterieur","eûmes","eût","eûtes","f","fais","faisaient","faisant","fait","faites","façon","feront","fi","flac","floc","fois","font","force","furent","fus","fusse","fussent","fusses","fussiez","fussions","fut","fûmes","fût","fûtes","g","gens","h","ha","haut","hein","hem","hep","hi","ho","holà","hop","hormis","hors","hou","houp","hue","hui","huit","huitième","hum","hurrah","hé","hélas","i","ici","il","ils","importe","j","je","jusqu","jusque","juste","k","l","la","laisser","laquelle","las","le","lequel","les","lesquelles","lesquels","leur","leurs","longtemps","lors","lorsque","lui","lui-meme","lui-même","là","lès","m","ma","maint","maintenant","mais","malgre","malgré","maximale","me","meme","memes","merci","mes","mien","mienne","miennes","miens","mille","mince","mine","minimale","moi","moi-meme","moi-même","moindres","moins","mon","mot","moyennant","multiple","multiples","même","mêmes","n","na","naturel","naturelle","naturelles","ne","neanmoins","necessaire","necessairement","neuf","neuvième","ni","nombreuses","nombreux","nommés","non","nos","notamment","notre","nous","nous-mêmes","nouveau","nouveaux","nul","néanmoins","nôtre","nôtres","o","oh","ohé","ollé","olé","on","ont","onze","onzième","ore","ou","ouf","ouias","oust","ouste","outre","ouvert","ouverte","ouverts","o|","où","p","paf","pan","par","parce","parfois","parle","parlent","parler","parmi","parole","parseme","partant","particulier","particulière","particulièrement","pas","passé","pendant","pense","permet","personne","personnes","peu","peut","peuvent","peux","pff","pfft","pfut","pif","pire","pièce","plein","plouf","plupart","plus","plusieurs","plutôt","possessif","possessifs","possible","possibles","pouah","pour","pourquoi","pourrais","pourrait","pouvait","prealable","precisement","premier","première","premièrement","pres","probable","probante","procedant","proche","près","psitt","pu","puis","puisque","pur","pure","q","qu","quand","quant","quant-à-soi","quanta","quarante","quatorze","quatre","quatre-vingt","quatrième","quatrièmement","que","quel","quelconque","quelle","quelles","quelqu'un","quelque","quelques","quels","qui","quiconque","quinze","quoi","quoique","r","rare","rarement","rares","relative","relativement","remarquable","rend","rendre","restant","reste","restent","restrictif","retour","revoici","revoilà","rien","s","sa","sacrebleu","sait","sans","sapristi","sauf","se","sein","seize","selon","semblable","semblaient","semble","semblent","sent","sept","septième","sera","serai","seraient","serais","serait","seras","serez","seriez","serions","serons","seront","ses","seul","seule","seulement","si","sien","sienne","siennes","siens","sinon","six","sixième","soi","soi-même","soient","sois","soit","soixante","sommes","son","sont","sous","souvent","soyez","soyons","specifique","specifiques","speculatif","stop","strictement","subtiles","suffisant","suffisante","suffit","suis","suit","suivant","suivante","suivantes","suivants","suivre","sujet","superpose","sur","surtout","t","ta","tac","tandis","tant","tardive","te","tel","telle","tellement","telles","tels","tenant","tend","tenir","tente","tes","tic","tien","tienne","tiennes","tiens","toc","toi","toi-même","ton","touchant","toujours","tous","tout","toute","toutefois","toutes","treize","trente","tres","trois","troisième","troisièmement","trop","très","tsoin","tsouin","tu","té","u","un","une","unes","uniformement","unique","uniques","uns","v","va","vais","valeur","vas","vers","via","vif","vifs","vingt","vivat","vive","vives","vlan","voici","voie","voient","voilà","voire","vont","vos","votre","vous","vous-mêmes","vu","vé","vôtre","vôtres","w","x","y","z","zut","à","â","ça","ès","étaient","étais","était","étant","état","étiez","étions","été","étée","étées","étés","êtes","être","ô"]
# Combine with English stopwords from scikit-learn
stopWords = list(set(stopWordsFrensh).union(ENGLISH_STOP_WORDS))

def clean_text(text):
    clean_text = str(text).lower()
    clean_text = re.sub(r'[^\w\s]', '', clean_text)
    clean_text = re.sub(r'[\[\]{}]', '', clean_text)
    clean_text = re.sub('[0-9]+', '', clean_text)
    words = clean_text.strip().split()
    clean_text = ' '.join(w for w in words if w not in stopWords)
    return clean_text

def get_match_score(texts: List[str]) -> float:
    cv = CountVectorizer(stop_words=stopWords)
    count_matrix = cv.fit_transform(texts)
    cosine_sim = cosine_similarity(count_matrix)
    return round(cosine_sim[0][1] * 100, 2)

def calculate_skill_match_score_v2(offer_skills: List[JobOfferSkillResponseDto],
                                   profile_skills: List[CandidateSkillResponseDto]) -> float:
    if not offer_skills or not profile_skills:
        return 0.0

    profile_skill_map = {
        skill.name.strip().lower(): skill.proficiencyLevel.value.upper()
        for skill in profile_skills
    }

    proficiency_scale = {
        "BEGINNER": 1,
        "BASIC": 1,
        "INTERMEDIATE": 2,
        "ADVANCED": 3,
        "FLUENT": 4,
        "EXPERT": 4,
        "MASTER": 5,
        "NATIVE": 5
    }

    total_score = 0.0
    total_weight = 0.0

    for offer_skill in offer_skills:
        skill_name = offer_skill.skillName.strip().lower()
        offer_level = proficiency_scale.get(offer_skill.proficiency.value.upper(), 0)
        profile_level = proficiency_scale.get(profile_skill_map.get(skill_name, ""), 0)

        score = 0.0
        if profile_level >= offer_level:
            score = 1.0
        elif profile_level > 0:
            score = profile_level / offer_level

        weight = 2.0 if offer_skill.requirementLevel == RequirementLevel.REQUIRED else \
                 1.0 if offer_skill.requirementLevel == RequirementLevel.PREFERRED else 0.5

        total_score += score * weight
        total_weight += weight

    return round((total_score / total_weight) * 100, 2) if total_weight else 0.0

def calculate_experience_match_score_v2(offer_experiences: List[JobOfferExperienceResponseDto],
                                        candidate_experiences: List[CandidateExperienceResponseDto]) -> float:
    if not offer_experiences or not candidate_experiences:
        return 0.0

    def years_of_exp(exp):
        try:
            start = datetime.strptime(exp.startDate, "%Y-%m-%d")
            end = datetime.strptime(exp.endDate, "%Y-%m-%d") if not exp.isCurrent else datetime.today()
            return (end - start).days / 365
        except:
            return 0

    total_score = 0.0
    total_weight = 0.0

    for offer_exp in offer_experiences:
        best_score = 0.0
        offer_title = offer_exp.title.strip().lower()
        weight = 2.0 if offer_exp.requirementLevel == RequirementLevel.REQUIRED else \
                 1.0 if offer_exp.requirementLevel == RequirementLevel.PREFERRED else 0.5
        required_years = offer_exp.yearsRequired or 0

        for candidate_exp in candidate_experiences:
            candidate_title = candidate_exp.jobTitle.strip().lower()
            title_score = get_match_score([offer_title, candidate_title]) / 100.0
            year_score = min(years_of_exp(candidate_exp) / required_years, 1.0) if required_years else 1.0
            combined_score = 0.3 * title_score + 0.7 * year_score
            best_score = max(best_score, combined_score)

        total_score += best_score * weight
        total_weight += weight

    return round((total_score / total_weight) * 100, 2) if total_weight else 0.0

def calculate_education_match_score_v2(offer_educations: List[JobOfferEducationResponseDto],
                                       candidate_educations: List[CandidateEducationResponseDto]) -> float:
    if not offer_educations or not candidate_educations:
        return 0.0

    total_score = 0.0
    total_weight = 0.0

    for offer_edu in offer_educations:
        best_score = 0.0

        for candidate_edu in candidate_educations:
            score = 0.0

            if offer_edu.degree and candidate_edu.degree:
                degree_sim = get_match_score([offer_edu.degree.lower(), candidate_edu.degree.lower()])
                score += 0.5 if degree_sim > 75 else 0.3 if degree_sim > 40 else 0.0

            if offer_edu.field and candidate_edu.field:
                field_sim = get_match_score([offer_edu.field.lower(), candidate_edu.field.lower()])
                score += 0.3 if field_sim > 75 else 0.2 if field_sim > 40 else 0.0

            if offer_edu.institution and candidate_edu.institution:
                inst_sim = get_match_score([offer_edu.institution.lower(), candidate_edu.institution.lower()])
                score += 0.2 if inst_sim > 75 else 0.0

            best_score = max(best_score, score)

        weight = 2.0 if offer_edu.requirementLevel == RequirementLevel.REQUIRED else \
                 1.0 if offer_edu.requirementLevel == RequirementLevel.PREFERRED else 0.5
        total_score += best_score * weight
        total_weight += weight

    return round((total_score / total_weight) * 100, 2) if total_weight else 0.0

def calculate_language_match_score_v2(offer_languages: List[JobOfferLanguageResponseDto],
                                      candidate_languages: List[CandidateLanguageResponseDto]) -> float:
    if not offer_languages or not candidate_languages:
        return 0.0

    candidate_map = {
        lang.language.strip().lower(): lang.proficiencyLevel.name.upper()
        for lang in candidate_languages
    }

    proficiency_scale = {
        "BEGINNER": 1,
        "INTERMEDIATE": 2,
        "ADVANCED": 3,
        "FLUENT": 4,
        "NATIVE": 5
    }

    total_score = 0.0
    total_weight = 0.0

    for offer_lang in offer_languages:
        lang = offer_lang.language.strip().lower()
        offer_score = proficiency_scale.get(offer_lang.proficiency.name.upper(), 0)
        candidate_score = proficiency_scale.get(candidate_map.get(lang, ""), 0)

        score = 1.0 if candidate_score >= offer_score else candidate_score / offer_score if candidate_score > 0 else 0.0

        weight = 2.0 if offer_lang.requirementLevel == RequirementLevel.REQUIRED else \
                 1.0 if offer_lang.requirementLevel == RequirementLevel.PREFERRED else 0.5
        total_score += score * weight
        total_weight += weight

    return round((total_score / total_weight) * 100, 2) if total_weight else 0.0

def calculate_location_match_score(offer_city: str, offer_country: str, offer_zip: str,
                                   candidate_address: AddressResponseDto) -> float:
    def normalize(val): return val.strip().lower() if val else ""

    score = 0.0
    if normalize(offer_country) == normalize(candidate_address.country): score += 0.4
    if normalize(offer_city) == normalize(candidate_address.city): score += 0.4
    if normalize(offer_zip) == normalize(candidate_address.zipCode): score += 0.2

    return round(score * 100, 2)

def calculate_title_match_score(offer_title: str, profile_title: str) -> float:
    return get_match_score([offer_title.lower(), profile_title.lower()])



def transform_matching_rate(cosine_similarity_score: float) -> float:
    """
    Transforms a cosine similarity score (0–100) to a more intuitive matching rate (15–99.99).
    """

    if cosine_similarity_score < 10:
        lower_bound = 15
        upper_bound = 25
        transformed_score = lower_bound + ((cosine_similarity_score - 4) * (upper_bound - lower_bound) / 6)

    elif cosine_similarity_score < 20:
        lower_bound = 25
        upper_bound = 50
        transformed_score = lower_bound + ((cosine_similarity_score - 10) * (upper_bound - lower_bound) / 10)

    elif cosine_similarity_score < 30:
        lower_bound = 50
        upper_bound = 73
        transformed_score = lower_bound + ((cosine_similarity_score - 20) * (upper_bound - lower_bound) / 10)

    elif cosine_similarity_score < 40:
        lower_bound = 73
        upper_bound = 90
        transformed_score = lower_bound + ((cosine_similarity_score - 30) * (upper_bound - lower_bound) / 10)

    elif cosine_similarity_score < 50:
        lower_bound = 90
        upper_bound = 92
        transformed_score = lower_bound + ((cosine_similarity_score - 40) * (upper_bound - lower_bound) / 10)

    elif cosine_similarity_score < 60:
        lower_bound = 92
        upper_bound = 94
        transformed_score = lower_bound + ((cosine_similarity_score - 50) * (upper_bound - lower_bound) / 10)

    elif cosine_similarity_score < 75:
        lower_bound = 94
        upper_bound = 95
        transformed_score = lower_bound + ((cosine_similarity_score - 60) * (upper_bound - lower_bound) / 15)

    else:
        lower_bound = 95
        upper_bound = 99.99
        transformed_score = lower_bound + ((cosine_similarity_score - 75) * (upper_bound - lower_bound) / 25)

    # Ensure the final value doesn't exceed 99.99
    return min(round(transformed_score, 2), 99.99)





def calculate_all_matching_scores(offer: JobOfferResponseDto, profile: ProfileResponseDto) -> Dict[str, float]:
    candidate = profile.candidate

    return {
        "skillMatch": transform_matching_rate(float(calculate_skill_match_score_v2(offer.skills, profile.skills))),
        "experienceMatch": transform_matching_rate(float(calculate_experience_match_score_v2(offer.experiences, candidate.experiences))),
        "educationMatch": transform_matching_rate(float(calculate_education_match_score_v2(offer.educations, candidate.education))),
        "languageMatch": transform_matching_rate(float(calculate_language_match_score_v2(offer.languages, candidate.languages))),
        "locationMatch": transform_matching_rate(float(calculate_location_match_score(offer.city, offer.country, offer.zipCode, candidate.address))),
        "titleMatch": transform_matching_rate(float(calculate_title_match_score(offer.title, profile.profileTitle)))
    }


def calculate_total_match_score(scores: dict, weights: dict = None) -> float:
    """
    Calculate weighted average from individual matching scores.
    
    :param scores: Dict of match scores (e.g., skillMatch, experienceMatch, etc.)
    :param weights: Dict of weights per match type (defaults to equal weighting)
    :return: Weighted match score rounded to 2 decimal places
    """
    if not scores:
        return 0.0

    # Default to equal weights if not provided
    if weights is None:
        # Define custom weights (optional)
        weights = {
            'skillMatch': 0.4,
            'experienceMatch': 0.3,
            'educationMatch': 0.1,
            'languageMatch': 0.1,
            'locationMatch': 0.05,
            'titleMatch': 0.05
        }

    weighted_sum = 0.0
    total_weight = 0.0

    for key, value in scores.items():
        weight = weights.get(key, 1.0)
        weighted_sum += value * weight
        total_weight += weight

    if total_weight == 0:
        return 0.0

    return round(weighted_sum / total_weight, 2)


