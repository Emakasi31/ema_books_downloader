#!/usr/bin/bash
echo 'From where do you wanna get book?
      1)ranobelib.me
      2)lightnovels.me'
read VAR
echo "Open 1st chapter and"
if [[ $VAR -eq 1 ]]
then
  python3 ./ranobelib_me.py
elif [[ $VAR -eq 2 ]]
then
  python3 ./lightnovels_me.py
else
  exit
fi
