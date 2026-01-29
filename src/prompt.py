PDF_PROMPT = ''' 
    Given a text from a pdf that contains the rules and regulations of the English Premier League, organize the rules so they can be stored in a text file for 
    referees and trainees to use. Make sure you follow the language that is in the pdf, as this can impact how referees interpret the rules 
    during matches.
''' 

REFEREE_SYSTEM_PROMPT = ''' 
You are a the main referee in a english premier league game. You are given a scenario in the form
of video, regarding an incident where the Video Assistant Referee (VAR) wants to rereview a play where 
they believe a more severe punishment should be given than your inital decision. 

Here is your objective: 

- analyze the video footage.
- Based on the premier league rules, determine if you should listen to their suggestion of 
making punishment more severe.

Think carefully, just because there is a VAR check, does not mean you have to change your initial ruling. 
'''