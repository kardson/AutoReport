# AutoReport
Automated report scripts for SHU students based on Selenium  

## ~~1. Some question~~

~~Q: Why there's not a simple solution?~~  
~~A: Cuz the Cookies can not be handled properly.~~  

~~Any idea for Cookies handling so that F_ vars on the reporting page can be obtained successfully?~~

## 2. How to use
1. Set your environment timezone to Shanghai, China
2. Install Chrome
3. Download webdriver and add it to `$PATH`
4. Ensure your Python version >= 3.7
5. Deploy Venv for the script according to the requirements.txt
6. Execute ``` crontab -e```
7. Add a line `SHELL=/bin/bash` 
8. Add a new line and input the instruction below, with `[]` replaced with your info, then save and quit.
``` 
* 7,20 * * * cd [path to your script folder] && source [path to your venv]/bin/activate && python [path to the script folder]/main.py [Your student ID] [Your password] [in Shanghai or not, True or False] [on campus or not, True or False] [is home address, True or False] && deactivate
```  
__*Fill `True` or `False` in location, campus and home address status__  
__*To successfully run this script, you must manually submit your report for once as this script utilize your historical fill-ins.__  