# kb_manager.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Example Knowledge Base (you can expand this)
KB_DICT = {
    "COURSE_DETAILS": {
        "I_BTECH_I_SEM": [
            {"code": "23BS1101", "name": "Linear Algebra & Calculus", "credits": 3, "marks": 100},
            {"code": "23BS1103", "name": "Engineering Physics", "credits": 3, "marks": 100},
            {"code": "23ES1103", "name": "Introduction to Programming", "credits": 3, "marks": 100},
            {"code": "23ES1103", "name": "Basic Electrical & Electronics Engineering", "credits": 3, "marks": 100},
            {"code": "23ES1104", "name": "Engineering Graphics", "credits": 3, "marks": 100},
            {"code": "23ES1152", "name": "Engineering Physics Lab", "credits": 1, "marks": 100},
            {"code": "23ES1152", "name": "Computer Programming Lab", "credits": 1.5, "marks": 100},
            {"code": "23ES1153", "name": "IT Workshop", "credits": 1, "marks": 100},
            {"code": "23ES1154", "name": "Electrical & Electronics Engineering Workshop", "credits": 1.5, "marks": 100},
            {"code": "23MC1141", "name": "NSS/NCC/Scouts & Guides/Comm.scdy Service", "credits": 1.5, "marks": 100}
        ],
        "I_BTECH_II_SEM": [
            {"code": "23HS1201", "name": "Communicative English", "credits": 2, "marks": 100},
            {"code": "23BS1201", "name": "Differential Equations & Vector Calculus", "credits": 3, "marks": 100},
            {"code": "23BS1202", "name": "Chemistry", "credits": 3, "marks": 100},
            {"code": "23ES1201", "name": "Basic Civil & Mechanical Engineering", "credits": 3, "marks": 100},
            {"code": "23AM3201", "name": "Data Structures", "credits": 3, "marks": 100},
            {"code": "23HS1251", "name": "Communicative English Lab", "credits": 1, "marks": 100},
            {"code": "23BS1251", "name": "Chemistry Lab", "credits": 1, "marks": 100},
            {"code": "23ES1251", "name": "Engineering Workshop", "credits": 1.5, "marks": 100},
            {"code": "23AM3251", "name": "Data Structures Lab", "credits": 1.5, "marks": 100},
            {"code": "23MC1242", "name": "Health and Wellness Yoga and Sports", "credits": 0.5, "marks": 100}
        ],
        "II_BTECH_I_SEM": [
            {"code": "23BS1305", "name": "Discrete Mathematics & Graph Theory (DMGT)", "credits": 3, "marks": 100},
            {"code": "23HS1301", "name": "Universal Human Values (UHV)", "credits": 3, "marks": 100},
            {"code": "23ES1305", "name": "Artificial Intelligence (AI)", "credits": 3, "marks": 100},
            {"code": "23AM3301", "name": "Advanced Data Structures & Algorithms Analysis (ADSA)", "credits": 3, "marks": 100},
            {"code": "23AM3302", "name": "Object Oriented Programming Through Java (JAVA)", "credits": 3, "marks": 100},
            {"code": "23AM3351", "name": "ADSA Lab", "credits": 1.5, "marks": 100},
            {"code": "23AM3352", "name": "JAVA Lab", "credits": 1.5, "marks": 100},
            {"code": "23CS08355", "name": "Python Programming", "credits": 2, "marks": 100},
            {"code": "23AC1301", "name": "Environmental Science (ES)", "credits": 0, "marks": 100}
        ],
        "II_BTECH_II_SEM": [
            {"code": "23HS1403", "name": "Optimization Techniques (OT)", "credits": 2, "marks": 100},
            {"code": "23BS1402", "name": "Probability & Statistics (P&S)", "credits": 3, "marks": 100},
            {"code": "23AM3401", "name": "Machine Learning (ML)", "credits": 3, "marks": 100},
            {"code": "23AM3402", "name": "Database Management Systems (DBMS)", "credits": 3, "marks": 100},
            {"code": "23AM3403", "name": "Digital Logic & Computer Organization (DL&CO)", "credits": 3, "marks": 100},
            {"code": "23AM3451", "name": "ML Lab", "credits": 1.5, "marks": 100},
            {"code": "23AM3452", "name": "DBMS Lab", "credits": 1.5, "marks": 100},
            {"code": "23CS48453", "name": "Full Stack Development - I (FSD-I)", "credits": 2, "marks": 100},
            {"code": "23ES1451", "name": "Design Thinking & Innovation (DT&I)", "credits": 2, "marks": 100}
        ]
        # Continue same for III B.Tech etc.
    },

    "ACADEMIC_CALENDAR": {
        "II_III_BTECH": {
            "Classwork_Start": "30-06-2025",
            "Mid1": "25-08-2025 to 30-08-2025",
            "Dasara_Vacation": "29-09-2025 to 04-10-2025",
            "Mid2": "03-11-2025 to 08-11-2025",
            "End_Exams": "17-11-2025 to 29-11-2025",
            "SecondSem_Classwork": "01-12-2025",
            "Pongal_Vacation": "12-01-2026 to 17-01-2026",
            "SecondSem_Mid1": "02-02-2026 to 07-02-2026",
            "SecondSem_Mid2": "06-04-2026 to 11-04-2026",
            "SecondSem_EndExams": "20-04-2026 to 02-05-2026",
            "Internship": "04-05-2026 to 27-06-2026"
        }
    },

    "FEE_STRUCTURE": {
        "Management_Quota": 200000,
        "Counseling_Quota": 77000,
        "Exam_Fee_Sem": 1200
    },

    "STAFF_DETAILS": {
        "Teaching": [
            {"name": "Dr.B.Janakiramaiah", "role": "Professor & Head", "exp": "22 Years", "phone": "+91 9440586340", "email": "Janakiramaiah@pvpsiddhartha.ac.in"},
            {"name": "Mrs.P.Hema Venkata Ramana", "role": "Assistant Professor", "exp": "11 Years", "phone": "+91 9491853599", "email": "pandirhema90@pvpsiddhartha.ac.in"},
            {"name": "Mrs.P.Naga Mani", "role": "Assistant Professor", "exp": "13 Years", "phone": "+91 9177801240", "email": "pnagamani@pvpsiddhartha.ac.in"}
            # continue same for others
        ],
        "Non_Teaching": [
            {"name": "Ms.K.SARANYA Kumari", "role": "Office Assistant", "phone": "+91 9948699589", "email": "cmsoffice@pvpsiddhartha.ac.in"},
            {"name": "Mr.T.Anil Kumar", "role": "Junior Programmer", "phone": "+91 9866414164", "email": "tanilkumar@pvpsit.ac.in"}
            # continue same for others
        ]
    },

    "EVENTS": {
        "Hackathon": {
            "name": "IDEA Hackathon (Full Stack Hackathon)",
            "round": "Final",
            "date": "27-09-2025",
            "duration": "8 Hours",
            "mode": "Offline",
            "team_size": "3-4",
            "eligibility": "2nd/3rd/4th Year CSE/CSM/CSD/IT/ECE/EEE/MEC/Civil"
        },
        "CreativeClub": [
            {"name": "Story Fragmentation Challenge", "date": "27-09-2025", "time": "10:30 AM – 12:30 PM", "venue": "TBD", "eligibility": "Open to all", "fee": "Free"},
            {"name": "Expressive on Spot", "date": "27-09-2025", "time": "2:00 PM – 3:00 PM", "venue": "247 Lab, First Floor", "eligibility": "All Departments", "fee": "Free"}
        ]
    }


}

def load_knowledge_base():
    """
    Returns the KB dictionary and prepares text corpus for search.
    """
    corpus = []
    mapping = []

    def flatten(d, prefix=""):
        for k, v in d.items():
            if isinstance(v, dict):
                flatten(v, f"{prefix}{k}.")
            else:
                corpus.append(f"{prefix}{k}: {v}")
                mapping.append(v)

    flatten(KB_DICT)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    return {
        "kb_dict": KB_DICT,
        "corpus": corpus,
        "mapping": mapping,
        "vectorizer": vectorizer,
        "tfidf_matrix": tfidf_matrix
    }

def search_knowledge_base(query, kb_data):
    """
    Search KB using TF-IDF similarity.
    """
    vectorizer = kb_data["vectorizer"]
    tfidf_matrix = kb_data["tfidf_matrix"]
    mapping = kb_data["mapping"]

    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    best_idx = similarities.argmax()

    if similarities[best_idx] > 0.3:
        return mapping[best_idx]
    return "I'm still learning about the college."
