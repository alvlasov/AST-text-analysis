# -*- coding: utf-8 -*
import logging

from east import consts


class EastException(Exception):
    """Base EAST Exception.

    To correctly use this class, inherit from it and define
    a 'msg_fmt' property. That msg_fmt will get printf'd
    with the keyword arguments provided to the constructor.
    """
    msg_fmt = "An unknown exception occurred."

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if 'code' not in self.kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                pass

        if not message:
            try:
                message = self.msg_fmt % kwargs
            except KeyError as e:
                # kwargs doesn't match a variable in the message
                # log the issue and the kwargs

                # if CONF.fatal_exception_format_errors:
                #     raise e
                # else:
                #     # at least get the core message out if something happened
                message = self.msg_fmt

        super(EastException, self).__init__(message)

    def format_message(self):
        if self.__class__.__name__.endswith('_Remote'):
            return self.args[0]
        else:
            return self


class NotFoundException(EastException):
    msg_fmt = "Not found."


class NoSuchASTAlgorithm(NotFoundException):
    msg_fmt = "There is no AST construction algorithm with name `%(name)s`."


class TomitaNotInstalledException(EastException):
    msg_fmt = ("Please, add the tomita distribution corresponding to your operating system "
               "to `tools/tomita`. The tomita binary file can be downloaded from %s" %
               consts.URL.TOMITA)


class EmptyStringsCollectionException(EastException):
    msg_fmt = "The input strings collection is empty."
