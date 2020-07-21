# AutoReport
Automated report scripts for SHU students on campus in a traditional way 

## 1. How to use
1. Set your environment timezone to Shanghai, China
2. Deploy Venv for the script according to the requirments.txt
4. Excute ``` crontab -e```
5. Add a line `SHELL=/bin/bash` 
6. Add a new line and input the instruction below, with `[]` replaced with your info, then save and quit.
``` 
* 7,20 * * * cd [path to your script folder] && source [path to your venv]/bin/activate && python [path to the script folder]/main.py [Your student ID] [Your password] [Temperature] && deactivate
```