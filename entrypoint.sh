#!/bin/bash

printbanner() {

    # RED='\033[31m'
    # GREEN='\033[32m'
    # YELLOW='\033[33m'
    # BLUE='\033[34m'
    # CYAN='\033[36m'
    COLORS=('\033[31m' '\033[32m' '\033[33m' '\033[34m' '\033[36m')
    NC='\033[0m' # Colore predefinito (reset)

    random_index=$(( RANDOM % ${#COLORS[@]} ))
    echo -e "${COLORS[$random_index]}"
    #cowsay -f dragon "Online Agent | Sapienza | Dipartimento di Informatica | Intelligenza Artificiale 2024"
    echo ' ________________________________________'
    echo '/ Online Agent | Sapienza | \'
    echo '\ Intelligenza Artificiale 2024         /'
    echo ' ----------------------------------------'
    echo '      \                    / \  //\'
    echo '       \    |\___/|      /   \//  \\'
    echo '            /0  0  \__  /    //  | \ \'
    echo '           /     /  \/_/    //   |  \  \'
    echo '           @_^_@'/   \/_   //    |   \   \'
    echo '           //_^_/     \/_ //     |    \    \'
    echo '        ( //) |        \///      |     \     \'
    echo '      ( / /) _|_ /   )  //       |      \     _\'
    echo '    ( // /) \'/,_ _ _/    ; \-.    |    _ _\.-~        .-~~~^-.\'
    echo '  (( / / )) ,-{        _      `-.|.-~-.           .~         `.'
    echo ' (( // / ))  '/\      /                 ~-. _ .-~      .-~^-.  \'
    echo ' (( /// ))      `.   {            }                   /      \  \'
    echo '  (( / ))     .----~-.\        \-\'                 .~         \  \`. \^-.'
    echo '             ///.----..>        \             _ -~             \`.  ^-  ^-_'
    echo '               ///-._ _ _ _ _ _ _}^ - - - - ~                     ~-- ,.-~''
    echo -e "${NC}"
}

echo "Starting the OnlineAgent"

echo "here the files in home:"
echo "#########################"
ls -laR
echo "#########################"

COMMAND="python code/main.py $1"
printbanner
echo "Executing command: $COMMAND"
eval "${COMMAND}"
