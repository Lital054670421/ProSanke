
SnakeAI הוא פרויקט מתקדם המאגד משחק "נחש" קלאסי עם סוכן בינה מלאכותית המשתמש בלמידת חיזוק עמוקה. הפרויקט מדגים גישות מתקדמות לאימון סוכנים, כאשר נבדקות שתי שיטות עיקריות:

- **MLP (Multi-Layer Perceptron):** רשת נוירונים עם ייצוג מופשט של מצב הלוח.
- **CNN (Convolutional Neural Network):** רשת קונבולוציונית המשתמשת בנתונים חזותיים (84×84×3) של מצב הלוח, ומביאה לביצועים מיטביים – ניקוד ממוצע גבוה יותר והחלטות איכותיות יותר במשחק.

---

## מבנה הפרויקט

```bash
├── main
│   ├── logs                      # קבצי לוג וגרפים (ניתנים להצגה באמצעות Tensorboard)
│   ├── trained_models_cnn        # מודלים מאומנים בגישת CNN (כולל את הקובץ הסופי ppo_snake_final.zip)
│   ├── trained_models_mlp        # מודלים מאומנים בגישת MLP (כולל את הקובץ הסופי ppo_snake_final.zip)
│   ├── snake_game.py             # מימוש משחק "נחש" קלאסי (כולל ממשק גרפי, קול ואינטראקציה)
│   ├── hamiltonian_agent.py      # דוגמה לסוכן אסטרטגי המשתמש במעגל מילטוני (Hamiltonian Cycle)
│   ├── snake_game_custom_wrapper_cnn.py   # מעטפת סביבתית – תצפיות ויזואליות עבור מודל CNN
│   ├── snake_game_custom_wrapper_mlp.py   # מעטפת סביבתית – תצפיות מופשטות עבור מודל MLP
│   ├── test_cnn.py              # סקריפט להערכה והרצת מבחני ביצועים של הסוכן המאומן בגישת CNN
│   ├── test_mlp.py              # סקריפט להערכה והרצת מבחני ביצועים של הסוכן המאומן בגישת MLP
│   ├── train_cnn.py             # סקריפט לאימון מודל CNN באמצעות MaskablePPO (מבוסס Stable-Baselines3)
│   └── train_mlp.py             # סקריפט לאימון מודל MLP באמצעות MaskablePPO (מבוסס Stable-Baselines3)
└── utils
    └── scripts                  # כלים עזר – לדוגמה, בדיקת סטטוס GPU ודחיסת קוד
```

---

## תיאור טכני

### עקרונות הפעולה:
- **סוכני בינה מלאכותית:**  
  שני הסוכנים מאומנים באמצעות אלגוריתם MaskablePPO, מה שמאפשר להגביל את הפעולות בהתאם לחוקי המשחק – למשל, מניעת שינוי כיוון מנוגד שעשוי להוביל להתנגשות.
  
- **ייצוג התצפיות (Observations):**  
  - בגישת **CNN** – המצב מיוצג כתמונה בגודל 84×84 עם 3 ערוצים, כאשר צבעים מייצגים את ראש הנחש, גופו והאוכל.
  - בגישת **MLP** – המצב מיוצג כמטריצה דו־ממדית עם ערכים נורמליים: 1 עבור ראש הנחש, 0.5 עבור הגוף, ו- -1 עבור האוכל.

### טכניקות מתקדמות:
- **MaskablePPO:**  
  שימוש באלגוריתם זה מאפשר לחסום פעולות לא חוקיות, ובכך לייעל את תהליך הלמידה ולהביא לביצועים אמינים יותר.
  
- **Schedulers ליניאריים:**  
  הגדרות דינמיות לשיעור הלמידה וטווח הקילוף (clip range) יורדים באופן הדרגתי לאורך האימון, מה שמסייע ביציבות תהליך הלמידה.
  
- **סביבות מרובות (SubprocVecEnv):**  
  שימוש במספר סביבות בו-זמנית מאפשר איסוף נתונים רחב ומהיר יותר, מה שמאיץ את תהליך האימון באופן משמעותי.

---

## התקנה והגדרת הסביבה

### דרישות:
- **Python:** 3.8.16
- **ספריות:**  
  Pygame, OpenAI Gym, Stable-Baselines3, sb3_contrib, Numpy, Torch (עם CUDA או MPS בהתאם למערכת)

### התקנה:
1. **יצירת סביבה וירטואלית עם Anaconda:**
   ```bash
   conda create -n SnakeAI python=3.8.16
   conda activate SnakeAI
   ```
2. **[אופציונלי] התקנת PyTorch עם תמיכת GPU:**
   ```bash
   conda install pytorch=2.0.0 torchvision pytorch-cuda=11.8 -c pytorch -c nvidia
   ```
3. **בדיקת זמינות GPU (אם רלוונטי):**
   ```bash
   python .\utils\check_gpu_status.py
   ```
4. **התקנת תלות הספריות:**
   ```bash
   pip install -r requirements.txt
   ```

---

## הרצת פרויקטי בינה מלאכותית

### 1. הערכת ביצועי הסוכן המאומן בגישת CNN:
להרצת מבחני ביצועים עבור המודל המאומן בגישת CNN:
```bash
cd [נתיב_לתיקיית_הפרויקט]/snake-ai/main
python test_cnn.py
```
סקריפט זה טוען את המודל המאומן (`ppo_snake_final.zip`) מתוך התיקייה המתאימה ומריץ מספר אפיזודות. במהלך ההרצה, מודפסים נתונים סטטיסטיים כגון ניקוד, מספר צעדים וגודל הנחש, ומוצגת תצוגה גרפית (אם מופעל מצב רינדור).

### 2. הערכת ביצועי הסוכן המאומן בגישת MLP:
להרצת מבחני ביצועים עבור המודל המאומן בגישת MLP:
```bash
cd [נתיב_לתיקיית_הפרויקט]/snake-ai/main
python test_mlp.py
```
תהליך זה דומה לזה של מודל ה-CNN, כאשר המודל נטען מהתיקייה המיועדת ל-MLP.

### 3. אימון מחדש של המודלים

#### אימון מודל CNN:
להפעלת תהליך האימון עבור מודל CNN:
```bash
cd [נתיב_לתיקיית_הפרויקט]/snake-ai/main
python train_cnn.py
```
תהליך האימון מנצל סביבות מרובות, לוח זמנים ליניארי, ושמירת נקודות בקרה (Checkpoints) לצורך מעקב ואופטימיזציה של תהליך הלמידה.

#### אימון מודל MLP:
להפעלת תהליך האימון עבור מודל MLP:
```bash
cd [נתיב_לתיקיית_הפרויקט]/snake-ai/main
python train_mlp.py
```

### 4. צפייה בגרפים (Logs) באמצעות Tensorboard:
ניתן לעקוב אחרי תהליך האימון והגרפים הסטטיסטיים:
```bash
cd [נתיב_לתיקיית_הפרויקט]/snake-ai/main
tensorboard --logdir=logs/
```
לאחר מכן, גשו לכתובת:
```
http://localhost:6006/
```
להצגה אינטראקטיבית של המדדים והגרפים.

---

## תובנות ופיתוח עתידי

- **ביצועים:**  
  ניסיונות מעשיים מצביעים על כך שמודל ה-CNN מספק ביצועים מיטביים, עם ניקוד גבוה יותר ויציבות גבוהה יותר בבחירת הפעולות.
  
- **גמישות:**  
  השימוש במעטפות (wrappers) שונים מאפשר התאמה מיטבית של סביבת האימון לכל מודל, מה שמאפשר חקירה והשוואה בין גישות שונות לאימון הסוכן.
  
- **פיתוח עתידי:**  
  - שיפור מתודולוגיות ה-reward והתאמתן לבעיות מורכבות יותר.
  - הרחבת הפרויקט לסביבות משחק נוספות.
  - שילוב טכניקות מתקדמות לאופטימיזציה של תהליך האימון.

---

## סיכום

SnakeAI מציג פתרון מקצועי וחדשני לשילוב משחק קלאסי עם בינה מלאכותית, תוך שימוש בטכניקות למידת חיזוק מתקדמות. הפרויקט משלב בין גישות מודרניות (CNN ו-MLP) ומספק בסיס חזק לפיתוח עתידי והרחבת השימוש בסביבות למידת חיזוק.

*לשאלות, הערות או דיווחי באגים, אנא פנו למפתחי הפרויקט.*
```