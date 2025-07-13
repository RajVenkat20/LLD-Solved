from enum import Enum
import time
from abc import ABC, abstractmethod

class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    ERROR = 3

class LogMessage:
    def __init__(self, level, message):
        self.level = level
        self.message = message
        self.timestamp = time.time()

    def getLevel(self):
        return self.level
    
    def getMessage(self):
        return self.message
    
    def getTimestamp(self):
        return self.timestamp
    
    def __str__(self):
        return f"[{self.level}] {self.timestamp} - {self.message}"
    
class LogAppender(ABC):
    @abstractmethod
    def append(self, logMessage):
        pass

class ConsoleAppender(LogAppender):
    def append(self, logMessage):
        print(logMessage)

class FileAppender(LogAppender):
    def __init__(self, filePath):
        self.filePath = filePath

    def append(self, logMessage):
        with open(self.filePath, "a") as file:
            file.write(str(logMessage) + "\n")

class LoggerConfiguration:
    def __init__(self, logLevel, logAppender):
        self.logLevel = logLevel
        self.logAppender = logAppender

    def getLogLevel(self):
        return self.logLevel
    
    def setLogLevel(self, logLevel):
        self.logLevel = logLevel
    
    def getLogAppender(self):
        return self.logAppender
    
    def setLogAppender(self, logAppender):
        self.logAppender = logAppender

class Logger:
    def __init__(self, config = None):
        if(not config):
            self.config = LoggerConfiguration(LogLevel.INFO, ConsoleAppender())
        else:
            self.config = config

    def setConfig(self, config):
        self.config = config

    def log(self, level, message):
        if(level.value >= self.config.getLogLevel().value):
            logMessage = LogMessage(level, message)
            self.config.getLogAppender().append(logMessage)

    def debug(self, message):
        self.log(LogLevel.DEBUG, message)
    
    def info(self, message):
        self.log(LogLevel.INFO, message)

    def error(self, message):
        self.log(LogLevel.ERROR, message)

logger = Logger()
config = LoggerConfiguration(LogLevel.ERROR, ConsoleAppender())
logger.setConfig(config)
# Logging with default configuration
logger.info("This is an information message")
logger.debug("This is a debug message")
logger.error("This is an error message")
        
 # Changing log level and appender
config = LoggerConfiguration(LogLevel.DEBUG, FileAppender("log.txt"))
logger.setConfig(config)
logger.debug("This is a debug message")
logger.info("This is an information message")