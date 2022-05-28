import telebot
import logging

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)


bot = telebot.TeleBot("TOKEN")
