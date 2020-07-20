# AutoReport
Automated report scripts for SHU students on campus based on Selenium  

## 1. Some question

Q: Why there's not a simple solution?  
A: Cuz the Cookies can not be handled properly.  

Any idea for Cookies handling so that F_ vars on the reporting page can be obtained successfully?

## 2. How to use
1. Set your environment timezone to Shanghai, China
1. Install Chrome
2. Dowload webdriver and place it with the script
3. Deploy Venv for the script according to the requirments.txt
4. Excute ``` crontab -e```
5. Input the instruction below, then save and quit
``` 
* 7,20 * * * source [path to your venv]/bin/activate && python [path to the script]/main.py [Your student ID] [Your password] [Temperature] && deactivate
```