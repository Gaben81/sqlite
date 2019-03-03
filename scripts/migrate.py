import sqlite3

connection = sqlite3.connect('questions.db')
cursor = connection.cursor()

create_questions = '''
CREATE TABLE questions (
  id INTEGER PRIMARY KEY,
  question TEXT NOT NULL
);
'''

create_answers = '''
CREATE TABLE answers (
  id INTEGER PRIMARY KEY,
  answer TEXT NOT NULL,       # nem lehet üres a mező
  position INTEGER,
  is_correct INTEGER,
  question INTEGER,

  FOREIGN KEY (question) REFERENCES questions (id) 
    ON DELETE CASCADE ON UPDATE NO ACTION
);
'''

cursor.execute('DROP TABLE IF EXISTS questions;')
cursor.execute('DROP TABLE IF EXISTS answers;')

cursor.execute(create_questions)
cursor.execute(create_answers)

connection.commit()

src_questions = [
  'Egy futóversenyen megelőzöd a második helyezettet, hányadik leszel?',
  'Milyen színű a süket botja?',
  'Hány évig tartott a 100 éves háború?',
  'Hány állatot vitt fel Mózes a bárkára?',
  'Ha megolölsz egy zombit a Fortnite-ban akkor hány killed lesz?',
]

src_answers = [
  ['Első', 'Második', 'Harmadik'],
  ['Fehér', 'Fekete', 'Nincs neki'],
  ['116', '100', '99'],
  ['Mindenből kettőt', 'Egyet sem', '100at'],
  ['0','1','nincs zombi fortnite-ban'],
]

src_corrects = [
  'b',
  'c',
  'a',
  'b',
  'c',
]

src_letters = { 'a': 0, 'b': 1, 'c' : 2, }

def insert_question(question):
  cursor.execute(
    '''INSERT INTO questions
        (question)
      VALUES
        (?)
    ''',
    (question,)
  )
  return cursor.lastrowid

def insert_answer(question_id, position, is_correct, answer):
  cursor.execute(
    '''INSERT INTO answers
          (answer, position, is_correct, question)
        VALUES
          (?, ?, ?, ?)
    ''',
    (answer, position, is_correct, question_id)
  )

for question_index, question in enumerate(src_questions):
  question_answers = src_answers[question_index]
  correct_answer_index = src_letters[src_corrects[question_index]]

  question_id = insert_question(question)
  
  for answer_index, answer in enumerate(question_answers):
    is_correct = correct_answer_index == answer_index
    insert_answer(question_id, answer_index, is_correct, answer)


connection.commit()
connection.close()
