# simpleGrades
A simple command line application to help people track their grades

------------------------------
Setup
------------------------------
1) Copy and paste the grades.py file into the folder of your choice, preferably the one that comes up when you open Command Prompt.
   This is usually C:\Users\[Insert Name here]

2) Enter "python grades.py" to open

3) Upon exit, this will creates a "grades.json" file. This is where the data is stored so be sure not to delete it!


------------------------------
Commands
------------------------------

There are 3 commands that should be used.

1) [add] or [ad]
2) [dis] or [di]
3) [rem], [re] or [rm]

commands are structured typically as such: [command],[class],[category],[item],[score]

------------------------------
The [add] command
------------------------------
(2 arguments -> Creates a class): add,math  
	- this will initialize an empty class with the name of "math"
	- be sure to not include spaces where you do not want them
	- (Info) try to keep these names short because you will have to type this often!

(3 arguments -> Creates a category): add,math,quiz=20
	- this will initialize an empty category of name "quiz" in the already-existing "math" class. "quiz" will have a weight of 20%


(5 arguments -> Creates an item): add,math,quiz,quiz 1,34/50
	- this will create an item with the name "quiz 1" in the quiz category with a score of 34/50
	- (Warn) This does not support values with a denominator of zero!



------------------------------
The [dis] command (Stands for display)
------------------------------

(2 arguments -> Displays a class): dis,math

(3 arguments -> Displays the items in a category): dis,math,quiz


------------------------------
The [dis] command (Stands for display)
------------------------------

(2 arguments -> Deletes a class): rem,math

(3 arguments -> Deletes a category): rem,math,quiz

(4 arguments -> Deletes an item): rem,math,quiz,quiz 1
