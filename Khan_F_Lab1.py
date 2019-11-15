#Author: Fuaad Khan
#Date: October 6, 2019
#
#Purpose: This script takes in a user's numeric inputs to check whether or not they are prime.
#
#OS Version ----> Windows (PC)

#reads welcoming statement(first line) from the .txt file provided in the folder
f=open(r"..\script\read_write_file.txt",'r+')
if f.mode == 'r+' :
    contents = f.readlines()
    print(contents[0])
f.close()

#Asks the user how many times they would like to conduct the PRIME test
num_of_tests = input("how many times would you like to run this program? -> ")
i = 1

#initial input list that will eventually output the users input calculations to a .txt file
input_list = []

#runs the operation as many times as the user decided in the previous prompt
while i <= num_of_tests:

    #takes in user input
    test_num = input("Enter a number you would like to test: ")

    #checks if the number is greater than 1, if not then it is not prime
    if test_num > 1:

        #loops between 2 and the input number
        for  j in range(2,test_num):

            #if any of the numbers between two and the input divide evenly into the input, i.e. no remainder, output not prime
            if (test_num%j) ==0:
                input_list.append(str(test_num) + " is not prime")
                break

        #If there is a remainder after division, output prime    
        else:
            input_list.append(str(test_num) + " is prime")
    else:
        input_list.append(str(test_num) + " is not prime")
        
    i = i+1

#Writes the test outputs into the .txt file provided in the folder
f=open(r"..\script\read_write_file.txt",'a')
if f.mode =='a':
    f.write("\n"+"These are the outputs from your tests:"+"\n"+str(input_list))
    f.close()
    
#prints to the console and informs the user about archived tests 
print(input_list)
print("\n"+"These will be added to your text file")


