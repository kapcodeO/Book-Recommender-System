import sys

class AppException(Exception):
    """
    AppException is customized exception class is designed to capture refined details about exceptions
    such as python script file line number along with the error message
    with custom exceptions one can easily spot source of error and provide quick fixes.
    """
    def __init__(self, error_message=Exception, error_detail=sys):
        """
        :param error_message: error message in string format
        """
        super().__init__(error_message)
        self.error_message = AppException.error_message_detail(error_message, error_detail=error_detail)

    @staticmethod
    def error_message_detail(error: Exception, error_detail=sys):
        """
        error: Exception object raised from module
        error_detail: is sys module contains detail information about system execution info
        """
        _, _, exc_tb = error_detail.exc_info()
        # extracting filename from exception traceback
        file_name = exc_tb.tb_frame.f_code.co_filename

        # preparing error message
        error_message = f"Error occured python script name [{file_name}]" \
                        f"line number: [{exc_tb.tb_lineno}] error message: [{error}]."
        
        return error_message

    def __repr__(self):
        """
        Formatting object of AppException
        """
        return AppException.__name__.__str__()

    def __str__(self):
        """
        Formatting how a object should be visible if used in print statement.
        """
        return self.error_message
