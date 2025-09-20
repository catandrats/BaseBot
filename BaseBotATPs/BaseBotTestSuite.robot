*** Settings ***
Test Setup        					Add Needed Image Path
Library           					SikuliLibrary
Library           					OperatingSystem
Library           					Keywords/BaseBotATPkeywords.py

*** Variables ***
${IMAGE_DIR}						${CURDIR}\\Images
${predic_image}						1
${predic_no}						1
${predic_yes}						1

*** Test Cases ***
Open Bot
	Open Basebot
Verify BaseBot is open
	Check For Process				BaseBot.exe
	${Processfound} 				Fetch Process Status
	Should Be Equal					${Processfound}			1
	Wait For 						5
Test Basebot Pattern Recognition
	Input text 						TextBox.png				ab
	Click							YesButton.png		 		
	Input text						TextBox.png				ba
	Click							NoButton.png
	${predic_image}					Exists					a_b_verification.png
	Should Be True					${predic_image}
Test Prediction Capacity
	Input text						TextBox.png				abby
	${is_exist_yes}					Exists					PredictionYesImage.png
	Should Be True					${is_exist_yes}
	Double Click					TextBox.png
	Press Special Key 				DELETE
	Input text						TextBox.png				back
	Wait For						1
	${is_exist_no}					Exists					PredictionNoImage.png
	Should Be True					${is_exist_no}
Test Save Question Functionality
	Click							SaveQuestion.png
	Input text						NameQuestion.png		ab test
	Wait For						1
	Click							Save.png
	Click In 						SaveNotification.png	YesButton.png
	Wait for						7
	Click							LoadExistingQuestion.png
	Click							SelectQuestion.png
	${options_available}			Exists					LoadOptions.png
	Delete Question					ab test
Test Load Question Functionality
	Mouse Move						cat.png
	Click							CatHighlight.png
	Click							Load.png
	Click 							NoButton.png
	Input text						TextBox.png				cat
	Wait for 						1
	${cat_yes}						Exists					PredictionYesImage.png
	Should Be True					${cat_yes}
Shutdown Processes
	Stop Remote Server
	Kill Process					BaseBot.exe				

*** Keywords ***
Add Needed Image Path
    Add Image Path    				${IMAGE_DIR}