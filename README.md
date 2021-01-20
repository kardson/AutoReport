# AutoReport
Automated reporting scripts for SHU students on campus  
  
This repo uses Github Actions to avoid deploying a self-host server.  
  
Check branch ___requests___ or ___selenium___ for scripts.  

## Branchs
### 1. ___requests___  
A light way utilizes `requests` to directly post data and finish the reporting.  
This branch does not support the feature of filling in historical reports.  

### 2. ___selenium___  
The tool `selenium` is used to invoke Chrome to simulate the action of filling in elements on website.  
This branch supports the feature of filling in historical reports.

## How to use  
1. Fork this repo.  
2. Go to the tab named _Actions_ in your forked repo and enable the workflow.  
3. Set your secrets in repo _Settings_ with variable name `student_id`, `student_id_pwd` and their corresponding values so that the scripts can access to your student account.  
4. (Optional) In `master/.github/workflow/action.yml`, choose one branch configuration, uncomment it and comment the other, then commit. Default configuration uses branch ___Selenium___.  
5. Automated reporting will execute everyday at about 08:01, 08:51, 21:01, 21:51 (UTC+8).  
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
__20/01/2021(latest): scripts will execute twice both in the morning and in the evening__  