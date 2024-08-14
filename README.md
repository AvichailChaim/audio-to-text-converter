המרת אודיו לטקסט
המרת קבצי טקסט לאודיו והמרת קבצי אודיו לטקסט.

סקירה כללית
פרויקט זה מאפשר להמיר קבצי אודיו לטקסט וקבצי טקסט לאודיו. הפרויקט נבנה על ידי אביחיל חיים דוויק באמצעות Flask ומשתמש ב-Google Text-to-Speech (gTTS) להמרת טקסט לאודיו וב-Google Speech Recognition להמרת אודיו לטקסט.

תכונות
המרת אודיו לטקסט: תמיכה בקבצי אודיו בפורמטים MP3, WAV, ו-OGG, והמרתם לטקסט באמצעות ה-API של Google Speech Recognition.
המרת טקסט לאודיו: המרת קבצי טקסט לאודיו בפורמט MP3 באמצעות Google Text-to-Speech.
ממשק פשוט: ממשק אינטרנטי קל לשימוש להעלאה ולעיבוד של קבצים.
דרישות מקדימות
Python 3.7 או גרסה גבוהה יותר
Flask
gTTS
pydub
התקנה
שכפול המאגר (Repository):

bash
Copy code
git clone https://github.com/AvichailChaim/audio-to-text-converter.git
ניווט לתיקיית הפרויקט:

bash
Copy code
cd audio-to-text-converter
התקנת התלויות הנדרשות:

מומלץ להגדיר סביבה וירטואלית (לא חובה, אך מומלץ):

bash
Copy code
python -m venv venv
source venv/bin/activate   # ב-Windows: venv\Scripts\activate
ולאחר מכן להתקין את התלויות:

bash
Copy code
pip install -r requirements.txt
הרצת האפליקציה:

bash
Copy code
python app.py
גישה לאפליקציה:

פתחו את הדפדפן והיכנסו לכתובת http://127.0.0.1:5000/ כדי להתחיל להשתמש באפליקציה.

פריסה ב-Heroku
להלן השלבים לפריסת האפליקציה ב-Heroku:

יצירת אפליקציה ב-Heroku:

bash
Copy code
heroku create your-app-name
דחיפת הקוד ל-Heroku:

bash
Copy code
git push heroku master
הגדלת ה-Dynos:

bash
Copy code
heroku ps:scale web=1
פתיחת האפליקציה:

bash
Copy code
heroku open
רישיון
הפרויקט הזה נבנה על ידי אביחיל חיים דוויק ומוגן תחת רישיון MIT.

הערות נוספות:
קובץ דרישות (requirements.txt):
יש ליצור את הקובץ requirements.txt באמצעות הפקודה:

bash
Copy code
pip freeze > requirements.txt
סביבה וירטואלית:
מומלץ להשתמש בסביבה וירטואלית כדי לנהל את התלויות של Python בפרויקט. כך תבטיחו שהפרויקט שלכם מבודד מפרויקטי Python אחרים במערכת שלכם.
