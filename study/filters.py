from .models import VerseStudyEntry 
import django_filters

BOOK = [
    ("Genesis", "Genesis"),
    ("Exodus", "Exodus"),
    ("Leviticus", "Leviticus"),
    ("Numbers", "Numbers"),
    ("Deuteronomy", "Deuteronomy"),
    ("Joshua", "Joshua"),
    ("Judges", "Judges"),
    ("Ruth", "Ruth"),
    ("1 Samuel", "1 Samuel"),
    ("2 Samuel", "2 Samuel"),
    ("1 Kings", "1 Kings"),
    ("2 Kings", "2 Kings"),
    ("1 Chronicles", "1 Chronicles"),
    ("2 Chronicles", "2 Chronicles"),
    ("Ezra", "Ezra"),
    ("Nehemiah", "Nehemiah"),
    ("Esther", "Esther"),
    ("Job", "Job"),
    ("Psalms", "Psalms"),
    ("Proverbs", "Proverbs"),
    ("Ecclesiastes", "Ecclesiastes"),
    ("Solomon", "Solomon"),
    ("Isaiah", "Isaiah"),
    ("Jeremiah", "Jeremiah"),
    ("Lamentations", "Lamentations"),
    ("Ezekial", "Ezekial"),
    ("Daniel", "Daniel"),
    ("Hosea", "Hosea"),
    ("Joel", "Joel"),
    ("Amos", "Amos"),
    ("Obadiah", "Obadiah"),
    ("Jonah", "Jonah"),
    ("Micah", "Micah"),
    ("Nahum", "Nahum"),
    ("Habakkuk", "Habakkuk"),
    ("Zephaniah", "Zephaniah"),
    ("Haggai", "Haggai"),
    ("Zechariah", "Zechariah"),
    ("Malachi", "Malachi"),
    ("Matthew", "Matthew"),
    ("Mark", "Mark"),
    ("Luke", "Luke"),
    ("John", "John"),
    ("Acts", "Acts"),
    ("Romans", "Romans"),
    ("1 Corinthians", "1 Corinthians"),
    ("2 Corinthians", "2 Corinthians"),
    ("Galations", "Galations"),
    ("Ephesians", "Ephesians"),
    ("Phillippians", "Phillippians"),
    ("Colossians", "Colossians"),
    ("1 Thessalonians", "1 Thessalonians"),
    ("2 Thessalonians", "2 Thessalonians"),
    ("1 Timothy", "1 Timothy"),
    ("2 Timothy", "2 Timothy"),
    ("Titus", "Titus"),
    ("Philemon", "Philemon"),
    ("Hebrews", "Hebrews"),
    ("James", "James"),
    ("1 Peter", "1 Peter"),
    ("2 Peter", "2 Peter"),
    ("1 John", "1 John"),
    ("2 John", "2 John"),
    ("3 John", "3 John"),
    ("Jude", "Jude"),
    ("Revelation", "Revelation"),
]

class VSFilter(django_filters.FilterSet):
    book_title = django_filters.ChoiceFilter(
        choices=BOOK, label="Book"
    )

    chapter = django_filters.NumberFilter(
        label="Chapter"
    )
    verse_number = django_filters.NumberFilter(
        label="Verse Number"
    )
    class Meta:
        model = VerseStudyEntry 
        fields = {}

