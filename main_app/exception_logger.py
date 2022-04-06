class ConsoleExceptionLoggerMiddleware(object):
    def process_exception(self, request, exception):
        import traceback
        import sys
        exc_info = sys.exc_info()
        print("-" * 30 + "Exception" + "-" * 50)
        print('\n'.join(traceback.format_exception(*(exc_info or sys.exc_info()))))
        print("-" * 88)