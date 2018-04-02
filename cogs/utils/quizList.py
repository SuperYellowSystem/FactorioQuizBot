# ======================================================================
# imports
# ======================================================================
from openpyxl import load_workbook

import datetime
from tzlocal import get_localzone

import discord

import random
import os

import config
from language.i18n import I18N

import logging
logger = logging.getLogger(__name__)

# ======================================================================
solution_index = {
    1: '\U0001F1E6',
    2: '\U0001F1E7',
    3: '\U0001F1E8',
    4: '\U0001F1E9'
}


class QuizItem:
    """
    This class represent an item(question) of the quiz.
    """
    def __init__(self, qid, question, answers, solution, difficulty):
        """
        Create a simple item with question/answer information

        :param qid: the question id
        :param question: the question itself
        :param answers: an array with multiple answers
        :param solution: the index of the correct answer
        :param difficulty: the difficulty of the question
        """
        self.i18n = I18N(config.LANGUAGE)
        self.__qid = qid
        self.__question = question
        self.__answers = answers
        self.__solution = solution
        self.__difficulty = difficulty

    def create_item_embed(self):
        time = datetime.datetime.now(get_localzone())
        embed = discord.Embed(colour=3447003, timestamp=time)
        answer_code = ord('A')
        output_answers = ""
        for answer in self.__answers:
            output_answers += f'{chr(answer_code)}: {answer}     '
            answer_code += 1
        embed.add_field(name=f'{self.__qid}/ {self.__question}', value=output_answers)
        embed.set_footer(text=f'{self.i18n.cmdQuizList_difficulty}: {self.__difficulty}')
        return embed

    def get_solution(self):
        return solution_index.get(self.__solution)

    def get_nb_answers(self):
        return len(self.__answers)


# ======================================================================
class QuizList:
    """
    This class generate and store all the items(questions) for the quiz
    """
    def __init__(self):
        """
        Generate a list of item from a xlsx file and store it in a list
        """
        self.__item_list = []
        self.__index = -1

        path = os.path.dirname(os.path.abspath(__file__))
        if os.name == 'nt':
            index = path.find("\\cogs")
        else:
            index = path.find("/cogs")
        file = f'{path[:index]}/questions/QCM_Factorio_{config.LANGUAGE}.xlsx'
        wb = load_workbook(filename=file, read_only=True)
        ws = wb['quiz']
        for row in range(1, ws.max_row):
            qid = ws.cell(row=row + 1, column=1).value
            question = ws.cell(row=row + 1, column=2).value
            answer1 = ws.cell(row=row + 1, column=3).value
            answer2 = ws.cell(row=row + 1, column=4).value
            answer3 = ws.cell(row=row + 1, column=5).value
            answer4 = ws.cell(row=row + 1, column=6).value
            solution = ws.cell(row=row + 1, column=7).value
            answer_total = ws.cell(row=row + 1, column=8).value
            difficulty = ws.cell(row=row + 1, column=9).value
            if answer_total < 4:
                answers = [answer1, answer2]
            else:
                answers = [answer1, answer2, answer3, answer4]
            self.__item_list.append(QuizItem(qid, question, answers, solution, difficulty))

        random.shuffle(self.__item_list)

    def select_next_item(self):
        self.__index += 1
        if self.__index == len(self.__item_list):
            self.__index = 0
        return self.__item_list[self.__index]

    def shuffle_list(self):
        random.shuffle(self.__item_list)
        self.__index = -1

# ======================================================================
# Test
# ======================================================================
# if __name__ == '__main__':
