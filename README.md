# AutoReport
Automated reporting scripts for SHU students
  
This repo uses Github Actions to avoid deploying a self-host server.  
  
Check branch ___selenium_for_once___ for scripts.  

## How to use  
1. __To successfully run this script, you must manually submit your report once as this script utilizes your historical fill-ins.__  
2. Fork this repo.  
3. Go to the tab named _Actions_ in your forked repo and enable the workflow.  
4. Set your secrets in repo _Settings_ with variable name `student_id`, `student_id_pwd`, `in_Shanghai`, `on_Campus`, `is_Home_Address` and their corresponding values so that the scripts can access to your student account. Value of `in_Shanghai`, `on_Campus`, `is_Home_Address` should be `True` or `False`.
5. Automated reporting will execute everyday at about 08:01, 08:51 (UTC+8).  
6. If the workflow fails, a notification email will be sent to your Github account's email address.  
7. If there's need for multiple user, add different secrets and corresponding commands in `RUN` section of `master/.github/workflow/action.yml`. (Avoid unnecessary resources use in Github, thanks.)  

## Update Log
Several month ago: scripts generated  
23/11/2020: add support for the 23/11/2020 version of selfreport  
24/11/2020: add Github Actions support for the scripts so that it can run without a self-deployed server  
25/11/2020: fix an error  
28/11/2020: solve the problem of wrong input on address textbox  
23/12/2020: add support for the 22/12/2020 version of selfreport(selenium)  
17/01/2021: add support for the 17/01/2020 version of selfreport(selenium)  
20/01/2021: scripts will execute twice both in the morning and in the evening  
30/01/2021: add support for new daily report, use branch `selenium_for_once`(disable previous `action.yml`s before enable the new ones)  
01/02/2021: add support for "is home address" selection, add a new param to script execution command
14/03/2021: submit button id changed
25/04/2021(latest): submit message changed
