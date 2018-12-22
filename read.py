#encoding:utf-8
import numpy as np
import xml.etree.ElementTree as ET

def get_questions(filename):
    questions = []
    root = ET.parse(filename).getroot()
    for child in root:
        correct_answer = child.attrib['correct'] if 'correct' in child.attrib else ''
        keep_order = child.attrib['keep_order'] if 'keep_order' in child.attrib else ''
        no_lines = child.attrib['no_lines'] if 'no_lines' in child.attrib else ''
        q = { 'text':child.attrib['txt'], 'correct':correct_answer, 'ans':[], 'keep_order':keep_order, 'no_lines':no_lines }
        for child2 in child: q['ans'].append( child2.attrib['txt'] )
        questions.append( q )
    return questions

def get_question( questions, nb ):
    q = questions[nb]
    ret_str = q['text']
    ret_str += "\n\n\\bigskip\n\n"
    if len( q['ans'] ) == 0 and q['no_lines'] != 'True': ret_str += '\\HRule\n\n' * 2
    else:
        ret_str += '\\setlength{\\leftskip}{2cm}'
        if q['keep_order'] == 'True': q_order = range(0,len(q['ans']))
        else: q_order = np.random.permutation( range(0,len(q['ans'])) )
        for a in q_order: ret_str += '\n\n' + "\\framebox(10,10){}\\hspace{.5cm}" + q['ans'][a]
        ret_str += '\n\n\\setlength{\\leftskip}{0cm}\n'
    return ret_str

all_question_lists = []
all_question_lists.append( get_questions( 'test_cad.xml' ))
all_question_lists.append( get_questions( 'test_cad_labs.xml' ))
all_question_lists.append( get_questions( 'test_intel.xml' ))
#all_question_lists.append( get_questions( 'test_intel_labs.xml' ))

with open( 'questions_content.tex', 'w' ) as f:
    np.random.seed( 207 )
    for i in range(1,25):
        f.write( "\DrawNameStamp" )
        f.write( "\DrawHeader{%d}" % i )
        for x, q_list in enumerate( all_question_lists ):
            nb = int( np.random.rand()*float( len( q_list )))
            if x < 2:
                f.write( '\paragraph{Вопрос %d}' % (x+1) + get_question(q_list, nb).encode('utf-8') )
            else:
                nb2 = int( np.random.rand()*float( len( q_list )))
                if len( q_list ) > 1:
                    while nb2 == nb: nb2 = int( np.random.rand()*float( len( q_list )))
                f.write( '\paragraph{Вопрос %d}' % (x+1) + get_question(q_list, nb).encode('utf-8') )
                f.write( '\paragraph{Вопрос %d}' % (x+1) + get_question(q_list, nb2).encode('utf-8') )
        f.write( '\\clearpage\n\n' )

import os
os.system( 'pdflatex -interaction=batchmode questions.tex' ) # -synctex=1








