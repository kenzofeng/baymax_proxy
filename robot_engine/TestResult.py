import sys
from robot.api import ExecutionResult, ResultWriter

result = ExecutionResult(r'C:\Users\DT161\Desktop\1\output.xml',r'C:\Users\DT161\Desktop\2\output.xml',merge=True)
# result.save(r'C:\Users\DT161\Desktop\newoutput.xml')


writer = ResultWriter(result)
writer.write_results(log=r'C:\Users\DT161\Desktop\new\log',output=r'C:\Users\DT161\Desktop\new\output',report=r'C:\Users\DT161\Desktop\new\report')
