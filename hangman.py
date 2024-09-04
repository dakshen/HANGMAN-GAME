import random
import hangman_stages
import datetime
import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",password='1234',database='hangman')
if mydb.is_connected:
    print("\nWELCOME TO HANGMAN GAME\n")
mycursor=mydb.cursor()

def DataInsertion(player_name,player_age,score):
    formatted_date=current_date.strftime('%Y-%m-%d %H:%M:%S')
    query="insert into logintable values(%s,%s,%s,%s)"
    val=(player_name,player_age,score,formatted_date)
    mycursor.execute(query,val)
    mydb.commit()

def DisplayActivity():
    mycursor.execute("select * from logintable")
    myresult=mycursor.fetchall()
    print("\n-----------------------------------------------------------------")
    print("Player Name\tPlayer Age\tScore\t\tLogin Date&Time")
    print("-----------------------------------------------------------------")
    for row in myresult:
        print(f"{row[0]:<14}{row[1]:^12}{row[2]:>9}{row[3].strftime('%Y-%m-%d %H:%M:%S'):>30}")
    print('\n')

def HighestScore():
    mycursor.execute("select playername,max(score) as Score from logintable group by playername order by max(Score) desc;")
    myresult=mycursor.fetchall()
    print("\n-----------------------------")
    print("Player Name\tHighest Score")
    print("-----------------------------")
    for row in myresult:
        print(f"{row[0]:<14}{row[1]:^12}")
    print('\n')

    
def game():
    lives=6

    def printlist():
        for i in display:
            print(i,end=' ') 
        print('\n')
        
    mycursor.execute("Select * from words")
    word=mycursor.fetchall()
    guess = random.choice(word)
    word=guess[0].upper()
    print("\nClue:",guess[1])
    print("\nGuess the word!\n")
        
    display=[]

    for i in range(len(word)):
        display+='_'
        
    printlist() 

    game_over=False
    while not game_over:  
        guessed_letter=input("\nGuess a letter: ").upper()
        if len(guessed_letter) != 1 or not guessed_letter.isalpha():
            print("Invalid input,Please enter a single letter.")
            continue
        
        for position in range(len(word)):
            letter=word[position]
            if letter==guessed_letter:
                display[position]=guessed_letter
        printlist() 
        
        if guessed_letter not in word:
            lives-=1
            print(hangman_stages.stages[lives])
            if lives==0:
                game_over=True
                print("Game Over,You lose!!")
                print("The word is",word)
                
        if '_' not in display:
            game_over=True
            print("You win!!")
            
    return lives*5


  
ch=10
current_date=datetime.datetime.now()
while ch>0:
    ch=int(input("-----Game Menu-----\n\n1.Play Game\n2.See Leaderboard\n3.Game History\n4.Exit\n\nSelect an option:"))
    if ch<1 and ch>3:
        print("Invalid option")
        continue
    elif ch==1:
        while True:
            player_name=input('Enter your name: ')
            if player_name.isalpha()!=True:
                print("Invalid name!")
                continue
            else:
                break
        player_age=int(input("Enter your age: "))
        score=game()
        DataInsertion(player_name,player_age,score)
        print("Score={}/30\n".format(score))
        continue
    elif ch==2:
        HighestScore()
        continue
    elif ch==3:
        DisplayActivity()
        continue
    elif ch==4:
        print('\nTHANK YOU')
        exit()
     
    
